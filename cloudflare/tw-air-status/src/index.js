export default {
	async fetch(request) {

		const { searchParams } = new URL(request.url);
		let loc = searchParams.get('loc');
		let site = loc ? loc : "前金";
		let air_status = "";

		try {
			const response = await fetch("https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON");
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

		let html = {
			"air": air_status
		};

		return new Response(JSON.stringify(html), {
			headers: {
				"content-type": "text/json;charset=UTF-8",
			},
		});
	}
};
