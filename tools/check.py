import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 將經緯度轉換為弧度
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # 地球半徑，單位: 公里
    return distance

# 你的位置
your_lat = 22.61480
your_lon = 120.31390

# 前金地點
jinkou_lat = 22.63390278
jinkou_lon = 120.28676111

# 復興地點
fuxing_lat = 22.608711
fuxing_lon = 120.312017

# 計算距離
distance_to_jinkou = haversine(your_lat, your_lon, jinkou_lat, jinkou_lon)
distance_to_fuxing = haversine(your_lat, your_lon, fuxing_lat, fuxing_lon)

# 輸出結果
if distance_to_jinkou < distance_to_fuxing:
    print("你距離前金比較近")
elif distance_to_jinkou > distance_to_fuxing:
    print("你距離復興比較近")
else:
    print("你距離前金和復興的距離相同")
