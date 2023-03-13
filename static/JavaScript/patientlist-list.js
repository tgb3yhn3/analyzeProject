// JavaScript Document
var token_fhir
var data
var arr_name
var arr_id
var href
arr_name = new Array();
arr_id = new Array();
href = new Array();
get_data();

async function get_data() {
	var result1 = await getToken_fhir().then((res1) => {
		// console.log("res1：" + res1);
		token_fhir = res1;
		// console.log("token_fhir：" + token_fhir);
	});
	var result2 = await getPatient(token_fhir).then((res2) => {
		// console.log("res2：" + res2);
		data = res2;
		// console.log("patientlist：" + data);

		for (i = 0; i < data.entry.length; i++) {
			arr_name.push(data.entry[i].resource.name[0].given[0]);
		}
		for (i = 0; i < data.entry.length; i++) {
			arr_id.push(data.entry[i].resource.id);
		}
		// listClick(arr_name.length, arr_id);
	})
	list_update();
	create_href();
};

function list_update() {
	return new Promise((resolve) => {
		var myList = document.getElementById('listDiv');
		for (var x = 0; x < arr_name.length; x++) {
			var newList = document.createElement('div');
			var textNode = document.createTextNode(arr_name[x]);
			newList.id = "op" + x;
			newList.className = "option";
			newList.appendChild(textNode);
			myList.appendChild(newList);
		}
		resolve = "list_update()"
	})
}

function create_href() {
	for (var i = 0; i < arr_id.length; i++) {
		href.push('https://nfsepsisanalysis-xiglc7mhia-uc.a.run.app/patientprofile?id=' + arr_id[i]);
		document.getElementById('op' + i).setAttribute('value', href[i]);
		document.getElementById('op' + i).onclick = function (event) {
			window.location.replace(event.target.getAttribute('value'));
		}
	}
}