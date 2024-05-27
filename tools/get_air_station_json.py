import requests
import json


# 空氣品質
url = "https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON"
response = requests.get(url)
result = response.json()
extracted_data = []
for record in result['records']:
    extracted_record = {
        'sitename': record['sitename'],
        'longitude': float(record['longitude']),
        'latitude': float(record['latitude'])
    }
    extracted_data.append(extracted_record)
    
# 將提取的數據轉換回 JSON 格式
new_json_data = json.dumps(extracted_data, indent=2)

# 輸出新的 JSON 數據
print(new_json_data)


# 將 JSON 數據寫入文件
file_path = 'extracted_data.json'  # 文件名稱和路徑
with open(file_path, 'w', encoding='utf-8') as file:  # 使用 UTF-8 編碼打開文件
    json.dump(json.loads(new_json_data), file, indent=2, ensure_ascii=False)


print(f"JSON 數據已成功寫入文件: {file_path}")
