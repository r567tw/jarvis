export default {
	async fetch(request, env, ctx) {
		// 取得經緯度，由於 cloudflare 取得的經緯度可能有點問題, 所以開放使用參數輸入
		const { searchParams } = new URL(request.url);
		let lat = searchParams.get('lat');
		let log = searchParams.get('log');

		const latitude = lat ? parseFloat(lat) : parseFloat(request.cf.latitude);
		const longitude = log ? parseFloat(log) : parseFloat(request.cf.longitude);

		// 查找最近的 sitename
		let nearestSitename = await this.findNearestSitename(latitude, longitude, env);

		let site = nearestSitename ? nearestSitename : "前金";
		let air_status = "";

		try {
			const apiKey = env.AIR_API_KEY; // 假設你的 API 金鑰儲存在環境變數中
			console.log(apiKey)

			const response = await fetch(`https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=${apiKey}&limit=1000&sort=ImportDate%20desc&format=JSON`);
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
	async findNearestSitename(latitude, longitude, env) {
		let minDistance = Number.MAX_VALUE;
		let nearestSitename = "";
		const sites = await env.twairstations.get("sites");
		const jsonData = JSON.parse(sites);

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
};
