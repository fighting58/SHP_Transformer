import geopandas as gpd
from shapely.geometry import Point, base, mapping, shape
from shapely.affinity import translate, rotate, scale
import math

def calculate_length_and_bearing(start_point: Point, end_point: Point) -> tuple: 
    """
    주어진 시작점과 끝점으로 선분의 길이와 방위각을 계산합니다.
    
    :param start_point: (shapely.geometry.Point), 객체로 시작점 좌표
    :param end_point: (shapely.geometry.Point), 객체로 끝점 좌표
    :return: (tuple), length, bearing 길이와 방위각(도 단위)    
    """
    #  tuple이면 Point객체로 변경
    if isinstance(start_point, tuple):
        start_point = Point(*start_point)
    if isinstance(end_point, tuple):
        end_point = Point(*end_point)
    
    # 좌표 추출
    x1, y1 = start_point.x, start_point.y
    x2, y2 = end_point.x, end_point.y
    
    # 선분의 길이 계산 (피타고라스 정리)
    length =math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # 방위각 계산 (atan2 사용)
    bearing = math.degrees(math.atan2(y2 - y1, x2 - x1))
    
    # 방위각을 0 ~ 360 범위로 조정
    if bearing < 0:
        bearing += 360
    
    return length, bearing

def calculate_dxdy(start_point: Point, end_point: Point) -> tuple:
    """
    주어진 시작점과 끝점으로 선분의 길이와 방위각을 계산합니다.
    
    :param start_point: (shapely.geometry.Point), 객체로 시작점 좌표
    :param end_point: (shapely.geometry.Point), 객체로 끝점 좌표
    :return: (length, bearing) 길이와 방위각 (도 단위)
    """
    if isinstance(start_point, tuple):
        start_point = Point(*start_point)
    if isinstance(end_point, tuple):
        end_point = Point(*end_point)

    dx = end_point.x - start_point.x
    dy = end_point.y - start_point.y    
    return dx, dy

def transform_geometry(geometry: base.BaseGeometry, translation: tuple=(0, 0), rotation_angle: float=0, scaling_factor: float=1.0, rotation_origin: tuple=(0, 0)) -> base.BaseGeometry:
    """
    주어진 기하학적 객체에 대해 이동, 회전, 축척 변환을 적용합니다.
    
    :param geometry: (BaseGeometry), 변환할 shapely 기하학적 객체
    :param translation: (tuple) x, y 이동 거리 (기본값: (0, 0))
    :param rotation_angle: (float), 회전 각도(단위: degree) (기본값: 0도)
    :param scaling_factor: (float), 축척 배율 (기본값: 1)
    :param rotation_origin: (tuple), 회전 기준점(기본값: (0, 0))
    :return: (BaseGeometry), 변환된 shapely 기하학적 객체
    """
    # 이동 변환
    transformed_geometry = translate(geometry, xoff=translation[0], yoff=translation[1])
    
    # 회전 변환 (기본값: 원점 기준 회전)
    transformed_geometry = rotate(transformed_geometry, rotation_angle, origin=rotation_origin)
    
    # 축척 변환
    transformed_geometry = scale(transformed_geometry, xfact=scaling_factor, yfact=scaling_factor, origin=rotation_origin)

    # 소수점 3자리로 변환
    transformed_geometry = round_coordinates(transformed_geometry, precision=3)
    
    return transformed_geometry

def round_coordinates(geom: base.BaseGeometry, precision: int = 3) -> base.BaseGeometry:
    """
    주어진 geometry 객체의 모든 좌표를 소수점 precision 자리로 반올림합니다.

    :param geom: (BaseGeometry), 변환할 shapely geometry 객체
    :param precision: (int), 반올림할 소수점 자리 수 (기본값은 3)
    
    Return: BaseGeometry, 좌표가 반올림된 새로운 geometry 객체
    """
    if geom.is_empty:
        return geom
    
    # geometry를 GeoJSON 포맷으로 변환하여 좌표 접근
    geom_mapping = mapping(geom)
    
    # 좌표 반올림 처리
    def round_elements(nested):
        rounded = []
        for item in nested:
            if isinstance(item, (list, tuple)):
                # 리스트나 튜플인 경우 재귀적으로 호출
                rounded.append(round_elements(item))
            else:
                # 소수점 3째 자리에서 반올림
                rounded.append(round(item, 3))
        return rounded

    geom_mapping['coordinates'] = round_elements(geom_mapping['coordinates'])
    return shape(geom_mapping)

def adjust_shapefile_features(input_shapefile: str, output_shapefile: str, translation: tuple=(0, 0), rotation_angle: float=0, scaling_factor: float=1.0, rotation_origin: tuple=(0, 0), encoding='cp949'):
    """
    Shapefile의 피처 좌표에 대해 이동, 회전, 축척 변환을 적용하여 새로운 Shapefile에 저장합니다.
    
    :param input_shapefile: (str), 입력 Shapefile 경로
    :param output_shapefile: (str), 출력 Shapefile 경로
    :param translation: (tuple), x, y 이동 거리 (기본값: (0, 0))
    :param rotation_angle: (float), 회전 각도 (기본값: 0도)
    :param scaling_factor: (float), 축척 배율 (기본값: 1)
    :param rotation_origin: (tuple), 회전 기준점 (기본값: (0, 0))
    :return: none, shp 파일 저장
    """
    # Shapefile 읽기
    gdf = gpd.read_file(input_shapefile, encoding=encoding)
    
    # 각 피처의 기하학적 객체에 대해 변환 적용
    gdf['geometry'] = gdf['geometry'].apply(lambda geom: transform_geometry(geom, translation, rotation_angle, scaling_factor, rotation_origin))

       # 변환된 Shapefile 쓰기
    gdf.to_file(output_shapefile, encoding=encoding)
