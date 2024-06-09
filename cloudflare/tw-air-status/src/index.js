export default {
	async fetch(request) {
		// 取得經緯度，由於 cloudflare 取得的經緯度可能有點問題, 所以開放使用參數輸入
		const { searchParams } = new URL(request.url);
		let lat = searchParams.get('lat');
		let log = searchParams.get('log');

		const latitude = lat ? parseFloat(lat) : parseFloat(request.cf.latitude);
		const longitude = log ? parseFloat(log) : parseFloat(request.cf.longitude);

		// 查找最近的 sitename
		let nearestSitename = this.findNearestSitename(latitude, longitude);

		let site = nearestSitename ? nearestSitename : "前金";
		let air_status = "";

		try {
			const response = await fetch("https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=04387458-0f09-47f9-9f68-9de9c4b69fdc&limit=1000&sort=ImportDate%20desc&format=JSON");
			const content = await response.json();
			const records = content.records;

			records.forEach(record => {
				if (record.sitename == site) {
					air_status = record.status;
				}
			});

		} catch (error) {
			console.log(error)
			air_status = "狀態取得失敗";
		}

		let data = {
			"station": nearestSitename,
			"air": air_status,
			"lat": latitude,
			"log": longitude
		};

		return Response.json(data)
	},


	// 找到最近的 sitename
	findNearestSitename(latitude, longitude) {
		let minDistance = Number.MAX_VALUE;
		let nearestSitename = "";
		const jsonData = this.getSites();

		jsonData.forEach(record => {
			const sitename = record.sitename;
			const recordLatitude = record.latitude;
			const recordLongitude = record.longitude;

			// 計算距離
			const distance = this.calculateDistance(latitude, longitude, recordLatitude, recordLongitude);

			// 更新最小距離和最近的 sitename
			if (distance < minDistance) {
				minDistance = distance;
				nearestSitename = sitename;
			}
		});

		return nearestSitename;
	},

	// 計算兩點間的距離（這是一個簡化的方法，實際上可能需要更複雜的計算）
	calculateDistance(lat1, lon1, lat2, lon2) {
		const earthRadiusKm = 6371; // 地球半徑，單位為公里

		const degToRad = (deg) => deg * (Math.PI / 180);

		const dLat = degToRad(lat2 - lat1);
		const dLon = degToRad(lon2 - lon1);

		const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
			Math.cos(degToRad(lat1)) * Math.cos(degToRad(lat2)) *
			Math.sin(dLon / 2) * Math.sin(dLon / 2);
		const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
		const distance = earthRadiusKm * c;

		return distance;
	},

	getSites() {
		return [
			{
				"sitename": "基隆",
				"longitude": 121.760056,
				"latitude": 25.129167
			},
			{
				"sitename": "汐止",
				"longitude": 121.64081,
				"latitude": 25.06624
			},
			{
				"sitename": "萬里",
				"longitude": 121.689881,
				"latitude": 25.179667
			},
			{
				"sitename": "新店",
				"longitude": 121.537778,
				"latitude": 24.977222
			},
			{
				"sitename": "土城",
				"longitude": 121.451861,
				"latitude": 24.982528
			},
			{
				"sitename": "板橋",
				"longitude": 121.458667,
				"latitude": 25.012972
			},
			{
				"sitename": "新莊",
				"longitude": 121.4325,
				"latitude": 25.037972
			},
			{
				"sitename": "菜寮",
				"longitude": 121.481028,
				"latitude": 25.06895
			},
			{
				"sitename": "林口",
				"longitude": 121.36548982,
				"latitude": 25.07798949
			},
			{
				"sitename": "淡水",
				"longitude": 121.449239,
				"latitude": 25.1645
			},
			{
				"sitename": "士林",
				"longitude": 121.51666356,
				"latitude": 25.10334003
			},
			{
				"sitename": "中山",
				"longitude": 121.526528,
				"latitude": 25.062361
			},
			{
				"sitename": "萬華",
				"longitude": 121.507972,
				"latitude": 25.046503
			},
			{
				"sitename": "古亭",
				"longitude": 121.529556,
				"latitude": 25.020608
			},
			{
				"sitename": "松山",
				"longitude": 121.578611,
				"latitude": 25.05
			},
			{
				"sitename": "大同",
				"longitude": 121.51342074,
				"latitude": 25.06331455
			},
			{
				"sitename": "桃園",
				"longitude": 121.30500531,
				"latitude": 24.9947107
			},
			{
				"sitename": "大園",
				"longitude": 121.20251473,
				"latitude": 25.06100357
			},
			{
				"sitename": "觀音",
				"longitude": 121.08283092,
				"latitude": 25.03556747
			},
			{
				"sitename": "平鎮",
				"longitude": 121.203986,
				"latitude": 24.952786
			},
			{
				"sitename": "龍潭",
				"longitude": 121.21645772,
				"latitude": 24.86400048
			},
			{
				"sitename": "湖口",
				"longitude": 121.03886894,
				"latitude": 24.90009696
			},
			{
				"sitename": "竹東",
				"longitude": 121.08895493,
				"latitude": 24.74091408
			},
			{
				"sitename": "新竹",
				"longitude": 120.97236752,
				"latitude": 24.8056356
			},
			{
				"sitename": "頭份",
				"longitude": 120.89869286,
				"latitude": 24.69690679
			},
			{
				"sitename": "苗栗",
				"longitude": 120.82011468,
				"latitude": 24.56499183
			},
			{
				"sitename": "三義",
				"longitude": 120.75956754,
				"latitude": 24.38248443
			},
			{
				"sitename": "豐原",
				"longitude": 120.74252414,
				"latitude": 24.25699731
			},
			{
				"sitename": "沙鹿",
				"longitude": 120.568794,
				"latitude": 24.225628
			},
			{
				"sitename": "大里",
				"longitude": 120.67844444,
				"latitude": 24.09961111
			},
			{
				"sitename": "忠明",
				"longitude": 120.641092,
				"latitude": 24.151958
			},
			{
				"sitename": "西屯",
				"longitude": 120.616917,
				"latitude": 24.162197
			},
			{
				"sitename": "彰化",
				"longitude": 120.541519,
				"latitude": 24.066
			},
			{
				"sitename": "線西",
				"longitude": 120.469061,
				"latitude": 24.131672
			},
			{
				"sitename": "二林",
				"longitude": 120.409653,
				"latitude": 23.925175
			},
			{
				"sitename": "南投",
				"longitude": 120.685306,
				"latitude": 23.913
			},
			{
				"sitename": "斗六",
				"longitude": 120.544994,
				"latitude": 23.711853
			},
			{
				"sitename": "崙背",
				"longitude": 120.348742,
				"latitude": 23.757547
			},
			{
				"sitename": "新港",
				"longitude": 120.345531,
				"latitude": 23.554839
			},
			{
				"sitename": "朴子",
				"longitude": 120.2478,
				"latitude": 23.46538
			},
			{
				"sitename": "臺西",
				"longitude": 120.19933333,
				"latitude": 23.702175
			},
			{
				"sitename": "嘉義",
				"longitude": 120.44125148,
				"latitude": 23.46477865
			},
			{
				"sitename": "新營",
				"longitude": 120.31725,
				"latitude": 23.305633
			},
			{
				"sitename": "善化",
				"longitude": 120.29740529,
				"latitude": 23.11337642
			},
			{
				"sitename": "安南",
				"longitude": 120.2175,
				"latitude": 23.048197
			},
			{
				"sitename": "臺南",
				"longitude": 120.21947897,
				"latitude": 22.98928311
			},
			{
				"sitename": "美濃",
				"longitude": 120.530542,
				"latitude": 22.883583
			},
			{
				"sitename": "橋頭",
				"longitude": 120.305689,
				"latitude": 22.757506
			},
			{
				"sitename": "仁武",
				"longitude": 120.332631,
				"latitude": 22.689056
			},
			{
				"sitename": "鳳山",
				"longitude": 120.357422,
				"latitude": 22.628126
			},
			{
				"sitename": "大寮",
				"longitude": 120.425311,
				"latitude": 22.56413611
			},
			{
				"sitename": "林園",
				"longitude": 120.41175,
				"latitude": 22.4795
			},
			{
				"sitename": "楠梓",
				"longitude": 120.328289,
				"latitude": 22.733667
			},
			{
				"sitename": "左營",
				"longitude": 120.292917,
				"latitude": 22.674861
			},
			{
				"sitename": "前金",
				"longitude": 120.28676111,
				"latitude": 22.63390278
			},
			{
				"sitename": "前鎮",
				"longitude": 120.30833356,
				"latitude": 22.6044507
			},
			{
				"sitename": "小港",
				"longitude": 120.337736,
				"latitude": 22.565833
			},
			{
				"sitename": "屏東",
				"longitude": 120.488033,
				"latitude": 22.673081
			},
			{
				"sitename": "潮州",
				"longitude": 120.561175,
				"latitude": 22.523108
			},
			{
				"sitename": "恆春",
				"longitude": 120.788928,
				"latitude": 21.958069
			},
			{
				"sitename": "臺東",
				"longitude": 121.15045,
				"latitude": 22.755358
			},
			{
				"sitename": "花蓮",
				"longitude": 121.599769,
				"latitude": 23.971306
			},
			{
				"sitename": "陽明",
				"longitude": 121.529583,
				"latitude": 25.182722
			},
			{
				"sitename": "宜蘭",
				"longitude": 121.746394,
				"latitude": 24.747917
			},
			{
				"sitename": "冬山",
				"longitude": 121.792928,
				"latitude": 24.632203
			},
			{
				"sitename": "三重",
				"longitude": 121.493806,
				"latitude": 25.072611
			},
			{
				"sitename": "中壢",
				"longitude": 121.221667,
				"latitude": 24.953278
			},
			{
				"sitename": "竹山",
				"longitude": 120.677306,
				"latitude": 23.756389
			},
			{
				"sitename": "永和",
				"longitude": 121.516306,
				"latitude": 25.017
			},
			{
				"sitename": "復興",
				"longitude": 120.312017,
				"latitude": 22.608711
			},
			{
				"sitename": "埔里",
				"longitude": 120.967903,
				"latitude": 23.968842
			},
			{
				"sitename": "馬祖",
				"longitude": 119.93149378,
				"latitude": 26.15188416
			},
			{
				"sitename": "金門",
				"longitude": 118.312256,
				"latitude": 24.432133
			},
			{
				"sitename": "馬公",
				"longitude": 119.566158,
				"latitude": 23.569031
			},
			{
				"sitename": "關山",
				"longitude": 121.161933,
				"latitude": 23.045083
			},
			{
				"sitename": "麥寮",
				"longitude": 120.251825,
				"latitude": 23.753506
			},
			{
				"sitename": "富貴角",
				"longitude": 121.53656894,
				"latitude": 25.29681695
			},
			{
				"sitename": "大城",
				"longitude": 120.26964167,
				"latitude": 23.85493056
			},
			{
				"sitename": "彰化（員林）",
				"longitude": 120.56373,
				"latitude": 23.96117
			},
			{
				"sitename": "高雄（湖內）",
				"longitude": 120.24535,
				"latitude": 22.87985556
			},
			{
				"sitename": "臺南（麻豆）",
				"longitude": 120.24583056,
				"latitude": 23.17904722
			},
			{
				"sitename": "屏東（琉球）",
				"longitude": 120.37722,
				"latitude": 22.35222
			},
			{
				"sitename": "新北(樹林)",
				"longitude": 121.38352778,
				"latitude": 24.94902778
			},
			{
				"sitename": "大甲（日南國小）",
				"longitude": 120.65525382,
				"latitude": 24.39017512
			},
			{
				"sitename": "屏東(枋山)",
				"longitude": 120.651472,
				"latitude": 22.260899
			}
		];
	}


};
