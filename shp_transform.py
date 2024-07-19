import geopandas as gpd
from shapely.geometry import Point
from shapely.affinity import translate, rotate, scale
import math

def calculate_length_and_bearing(start_point, end_point):
    """
    주어진 시작점과 끝점으로 선분의 길이와 방위각을 계산합니다.
    
    :param start_point: shapely.geometry.Point 객체로 시작점 좌표
    :param end_point: shapely.geometry.Point 객체로 끝점 좌표
    :return: (length, bearing) 길이와 방위각 (도 단위)
    """
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

def calculate_dxdy(start_point, end_point):
    """
    주어진 시작점과 끝점으로 선분의 길이와 방위각을 계산합니다.
    
    :param start_point: shapely.geometry.Point 객체로 시작점 좌표
    :param end_point: shapely.geometry.Point 객체로 끝점 좌표
    :return: (length, bearing) 길이와 방위각 (도 단위)
    """
    dx = end_point.x - start_point.x
    dy = end_point.y - start_point.y    
    return dx, dy

def transform_geometry(geometry, translation=(0, 0), rotation_angle=0, scaling_factor=1, rotation_origin=(0, 0)):
    """
    주어진 기하학적 객체에 대해 이동, 회전, 축척 변환을 적용합니다.
    
    :param geometry: 변환할 shapely 기하학적 객체
    :param translation: (x, y) 이동 거리 (기본값: (0, 0))
    :param rotation_angle: 회전 각도 (기본값: 0도)
    :param scaling_factor: 축척 배율 (기본값: 1)
    :return: 변환된 shapely 기하학적 객체
    """
    # 이동 변환
    transformed_geometry = translate(geometry, xoff=translation[0], yoff=translation[1])
    
    # 회전 변환 (기본값: 원점 기준 회전)
    transformed_geometry = rotate(transformed_geometry, rotation_angle, origin=rotation_origin)
    
    # 축척 변환
    transformed_geometry = scale(transformed_geometry, xfact=scaling_factor, yfact=scaling_factor, origin=rotation_origin)
    
    return transformed_geometry

def adjust_shapefile_features(input_shapefile, output_shapefile, translation=(0, 0), rotation_angle=0, scaling_factor=1, rotation_origin=(0, 0)):
    """
    Shapefile의 피처 좌표에 대해 이동, 회전, 축척 변환을 적용하여 새로운 Shapefile에 저장합니다.
    
    :param input_shapefile: 입력 Shapefile 경로
    :param output_shapefile: 출력 Shapefile 경로
    :param translation: (x, y) 이동 거리 (기본값: (0, 0))
    :param rotation_angle: 회전 각도 (기본값: 0도)
    :param scaling_factor: 축척 배율 (기본값: 1)
    """
    # Shapefile 읽기
    gdf = gpd.read_file(input_shapefile)
    
    # 각 피처의 기하학적 객체에 대해 변환 적용
    gdf['geometry'] = gdf['geometry'].apply(lambda geom: transform_geometry(geom, translation, rotation_angle, scaling_factor, rotation_origin))
    
    # 변환된 Shapefile 쓰기
    gdf.to_file(output_shapefile, encoding='utf-8')


# 사용 예시
if __name__ == '__main__':
    input_shapefile = 'test.shp'
    output_shapefile = 'test_trasform.shp'
    l1_s = Point(217351.37, 505549.82)
    l1_e = Point(216828.55, 507359.74)
    l2_s = Point(219991.27, 505193.11)
    l2_e = Point(219657.02, 507186.06)

    dxdy = calculate_dxdy(l1_s, l2_s)
    r1, v1 = calculate_length_and_bearing(l1_s, l1_e)
    r2, v2 = calculate_length_and_bearing(l2_s, l2_e)

    s = r2 / r1
    dv = v2 - v1
    
    translation = dxdy  # x 방향으로 10만큼, y 방향으로 20만큼 이동
    rotation_angle = dv # 45도 회전
    scaling_factor = s # 1.5배 축척
    rotation_origin = (l2_s.x, l2_s.y)

    adjust_shapefile_features(input_shapefile, output_shapefile, translation, rotation_angle, scaling_factor, rotation_origin=rotation_origin)

    print(dxdy, dv, s)
