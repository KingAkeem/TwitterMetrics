function saveData(data, fileName) {
	const a = document.createElement("a");
	document.body.appendChild(a);
	a.style = "display: none";
	const blob = new Blob([data], {type: "octet/stream"});
	const url = window.URL.createObjectURL(blob);
	a.href = url;
	a.download = fileName;
	a.click();
	window.URL.revokeObjectURL(url);
}

function downloadAsJson(rows) {
	const content = JSON.stringify(rows);
	var a = document.createElement("a");
	var file = new Blob([content], {type: 'text/plain'});
	a.href = URL.createObjectURL(file);
	a.download = `${getUsername()}-tweets.txt`;
	a.click();
}

function downloadAsCsv(rows) {
	const username = getUsername();
	const request = new XMLHttpRequest();
	request.open('POST', `/export/csv?username=${username}`);
	const data = new FormData();
	data.append('rows', JSON.stringify(rows));
	request.onreadystatechange = function() {
		if (request.readyState === XMLHttpRequest.DONE) {
			if (request.status === 0 || (request.status >= 200 && request.status < 400)) {
				saveData(request.response,`${username}-tweets.csv`)
			} else {
				console.error('Unable to process request.', request.responseText);
			}
		}
	}
	request.send(data);
}

function getRows() {
	const table = $('#table-container').children()[0];
	if (table) {
		/**
		currently sends data back to server once a database has been added, the ID will be sent so the server can retrieve the results
		**/
		const rows =[];
		for (let i = 0; i < table.rows.length; i++) {
		const row = table.rows[i];
		const rowData = {};
		for (let j = 0; j < row.children.length; j++) {
			const cell = row.children[j];
			if (cell.id.trim() === "") continue;
			rowData[cell.id] = cell.innerText;   
		}
		if (Object.entries(rowData).length === 0) continue;
		rows.push(rowData);
		}
		return rows;
	}
}

 function getUsername() {
    const table = $('#table-container').children()[0];
    if (table) {
      const username = table.rows[0].children[0].innerText;
      return username; 
    }
}

function insertTweets(tweets) {
	const tweetTable = $("<table class='result-table'>");
	$('#table-container').empty();
	$('#table-container').append(tweetTable);

	const userHeader = $('<tr>');
	userHeader.append(`<th colspan="2">@${$('#username').val()}</th>`);
	tweetTable.append(userHeader);

	// if tweets are found then create table 
	if (tweets.length > 0) { 
		const header = $('<tr>');
		// sort keys
		const keys = Object.keys(tweets[0]).sort();
		keys.forEach(key => header.append(`<th>${key}</th>`));
		tweetTable.append(header);

		const extractExtension = (fname) => {
			return fname.slice((fname.lastIndexOf(".") - 1 >>> 0) + 2);
		};

		tweets.forEach(tweet => {
			const bodyRow = $(`<tr id=${tweet.id}>`);
			keys.forEach(key => {
				let value = `${tweet[key]}`;
				try {
					const extension = extractExtension(tweet[key]);
					switch (extension.toLowerCase()) {
					case 'jpg': 
					value = `<img src="${tweet[key]}"/>`;
					
					}
				} catch(err) { 
					console.debug(err);
				}
				bodyRow.append(`<td id=${key}>${value}</td>`);
				tweetTable.append(bodyRow);
			});
		});
	}
}