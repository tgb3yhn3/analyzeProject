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
function renderLinkIcon(node) {
	const iconSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
	const iconPath = document.createElementNS(
	  'http://www.w3.org/2000/svg',
	  'path'
	);
  
	iconSvg.setAttribute('fill', 'currentColor');
	iconSvg.setAttribute('viewBox', '0 0 16 16');
	iconSvg.setAttribute('width', '1em');
	iconSvg.setAttribute('height', '1em');
	iconSvg.setAttribute('stroke', 'black');
	// iconSvg.cla.add("bi bi-file-earmark-person-fil");
	iconSvg.classList.add('post-icon');
  
	iconPath.setAttribute(
	  'd',
	  'M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0zm2 5.755V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-.245S4 12 8 12s5 1.755 5 1.755z'
	);

  
	iconSvg.appendChild(iconPath);
  
	return node.appendChild(iconSvg);
  }
function list_update() {
	return new Promise((resolve) => {
		var myList = document.getElementById('listDiv');
		myList.className+=" row"
		for (var x = 0; x < arr_name.length; x++) {
			var newList = document.createElement('div');
			newList.style.marginTop = "1.5em";
			newList.style.marginBottom = "1.5em";
			var text = document.createElement('h1');
			var img=document.createElement('img')
			img.src="static/images/person.svg"
			// var hr = document.createElement('hr');
			var textNode = document.createTextNode(arr_name[x]);
			newList.id = "op" + x;
			
			newList.className = "option"
			newList.className += " col-md-4"
			// text.appendChild(img)
			renderLinkIcon(text)
			text.appendChild(textNode)
			newList.appendChild(text);
			
			myList.appendChild(newList);
			// myList.appendChild(hr);
			if(x%3==2){
				let hr = document.createElement('hr');
				myList.appendChild(hr);
			}
		}
		resolve = "list_update()"
	})
}

function create_href() {
	for (var i = 0; i < arr_id.length; i++) {
		href.push('https://fhir2-dm5wodoipq-de.a.run.app/patientprofile?id=' + arr_id[i]);
		document.getElementById('op' + i).setAttribute('value', href[i]);
		document.getElementById('op' + i).setAttribute('onclick', 'window.location.replace("' + href[i] + '")');
		// document.getElementById('op' + i).onclick = function (event) {
		// 	console.log(event.target);
		// 	//window.location.replace(event.target.getAttribute('value'));
		// }
	}
}
async function add_data(data, isPatient = true) {
	let token
	let patient_obj
	let result1 = await getToken_fhir().then((res1) => {
		token = res1;
		console.log("token = " + token)
	});

	//開始PUT
	let url = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/" + (isPatient ? "Patient" : "Observation");
	const headers = new Headers({
		"Content-Type": "application/fhir+json",
		"Authorization": "Bearer " + token,
	});

	// 設定請求主體，此處使用 JSON 格式的 FHIR 資源

	//   console.log(updateJson(patien_json,"name",))


	const body = JSON.stringify(data)
	console.log(body)
	//console.log(body)
	//patien_json['name'][0]["given"][0]=new_name

	// 設定請求選項
	const options = {
		method: "POST",
		headers: headers,
		body: body
	};

	// 發送請求
	const responses = await fetch(url, options)
		.then((response) =>
			response.json()

		)
		.then((data) => {

			//console.log(data)
			//document.getElementById(htmlId).innerHTML = htmlPrefix + new_data

			//patient_obj=
			patient_obj = data
			//console.log(patient_obj.id)
			console.log("更新成功!")


		}).then(() => {


		})
		.catch(error => console.error(error));
	console.log(patient_obj.id)
	return patient_obj.id
}

async function add_patient() {
	let name_add = window.prompt("請輸入姓名")
	let gender_add = window.prompt("請輸入性別")
	let birth_add = window.prompt("請輸入生日")
	let patient_json = {
		"address": [
			{
				"city": "Franklin",
				"country": "US",
				"extension": [
					{
						"extension": [
							{
								"url": "latitude",
								"valueDecimal": 42.12256333208218
							},
							{
								"url": "longitude",
								"valueDecimal": -71.34002158683731
							}
						],
						"url": "http://hl7.org/fhir/StructureDefinition/geolocation"
					}
				],
				"line": [
					"892 Keeling Mews"
				],
				"postalCode": "02038",
				"state": "Massachusetts"
			}
		],
		"birthDate": birth_add,
		"communication": [
			{
				"language": {
					"coding": [
						{
							"code": "en-US",
							"display": "English",
							"system": "urn:ietf:bcp:47"
						}
					],
					"text": "English"
				}
			}
		],
		"deceasedDateTime": "2017-09-13T00:17:55-04:00",
		"extension": [
			{
				"extension": [
					{
						"url": "ombCategory",
						"valueCoding": {
							"code": "2106-3",
							"display": "White",
							"system": "urn:oid:2.16.840.1.113883.6.238"
						}
					},
					{
						"url": "text",
						"valueString": "White"
					}
				],
				"url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
			},
			{
				"extension": [
					{
						"url": "ombCategory",
						"valueCoding": {
							"code": "2186-5",
							"display": "Not Hispanic or Latino",
							"system": "urn:oid:2.16.840.1.113883.6.238"
						}
					},
					{
						"url": "text",
						"valueString": "Not Hispanic or Latino"
					}
				],
				"url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
			},
			{
				"url": "http://hl7.org/fhir/StructureDefinition/patient-mothersMaidenName",
				"valueString": "Wava789 White193"
			},
			{
				"url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
				"valueCode": "M"
			},
			{
				"url": "http://hl7.org/fhir/StructureDefinition/patient-birthPlace",
				"valueAddress": {
					"city": "Braintree",
					"country": "US",
					"state": "Massachusetts"
				}
			},
			{
				"url": "http://synthetichealth.github.io/synthea/disability-adjusted-life-years",
				"valueDecimal": 72.56905691990069
			},
			{
				"url": "http://synthetichealth.github.io/synthea/quality-adjusted-life-years",
				"valueDecimal": 19.43094308009931
			},
			{
				"url": "sea water",
				"valueDecimal": 0
			},
			{
				"url": "Respiratory mask",
				"valueDecimal": 0
			}
		],
		"gender": gender_add,
		"id": "3ed438bf-0c3e-4cb7-890b-35e93af280c8",
		"identifier": [
			{
				"system": "https://github.com/synthetichealth/synthea",
				"value": "6c6e933e-65c5-46d1-b4fc-eca7f44c36d1"
			},
			{
				"system": "http://hospital.smarthealthit.org",
				"type": {
					"coding": [
						{
							"code": "MR",
							"display": "Medical Record Number",
							"system": "http://terminology.hl7.org/CodeSystem/v2-0203"
						}
					],
					"text": "Medical Record Number"
				},
				"value": "6c6e933e-65c5-46d1-b4fc-eca7f44c36d1"
			},
			{
				"system": "http://hl7.org/fhir/sid/us-ssn",
				"type": {
					"coding": [
						{
							"code": "SS",
							"display": "Social Security Number",
							"system": "http://terminology.hl7.org/CodeSystem/v2-0203"
						}
					],
					"text": "Social Security Number"
				},
				"value": "999-20-5992"
			},
			{
				"system": "urn:oid:2.16.840.1.113883.4.3.25",
				"type": {
					"coding": [
						{
							"code": "DL",
							"display": "Driver's License",
							"system": "http://terminology.hl7.org/CodeSystem/v2-0203"
						}
					],
					"text": "Driver's License"
				},
				"value": "S99952703"
			},
			{
				"system": "http://standardhealthrecord.org/fhir/StructureDefinition/passportNumber",
				"type": {
					"coding": [
						{
							"code": "PPN",
							"display": "Passport Number",
							"system": "http://terminology.hl7.org/CodeSystem/v2-0203"
						}
					],
					"text": "Passport Number"
				},
				"value": "X84135900X"
			}
		],
		"maritalStatus": {
			"coding": [
				{
					"code": "M",
					"display": "M",
					"system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus"
				}
			],
			"text": "M"
		},
		"meta": {
			"lastUpdated": "2023-03-25T17:57:46.411113+00:00",
			"versionId": "MTY3OTc2NzA2NjQxMTExMzAwMA"
		},
		"multipleBirthBoolean": false,
		"name": [
			{
				"family": "Kirlin939",
				"given": [
					name_add
				],
				"prefix": [
					"Mr."
				],
				"use": "official"
			}
		],
		"resourceType": "Patient",
		"telecom": [
			{
				"system": "phone",
				"use": "home",
				"value": "555-333-1617"
			}
		],
		"text": {
			"div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">Generated by <a href=\"https://github.com/synthetichealth/synthea\">Synthea</a>.Version identifier: v2.4.0-404-ge7ce2295\n .   Person seed: -3447902653576265313  Population seed: 0</div>",
			"status": "generated"
		}
	}
	let new_id
	await add_data(patient_json, true).then((data) => {
		new_id = data
		console.log(new_id)
	})
	let height_add = window.prompt("請輸入身高")
	let weight_add = window.prompt("請輸入體重")

	let WBC_add = window.prompt("請輸入WBC")//6000
	let CRP_add = window.prompt("請輸入CRP")//25
	let Seg_add = window.prompt("請輸入Seg")//50
	let Band_add = window.prompt("請輸入Band")//4.5

	let respiratoryRate_add = window.prompt("請輸入respiratoryRate")//19
	let consciousness_add = window.prompt("請輸入consciousness")//100
	let systolicPressure_add = window.prompt("請輸入systolicPressure")//124
	let PF_ratio_add = window.prompt("請輸入PF_ratio")//360
	let Platelet_add = window.prompt("請輸入Platelet")//156
	let Bilirubin_add = window.prompt("請輸入Bilirubin")//7
	let MAP_add = window.prompt("請輸入平均動脈壓")//68
	let Dopamine_add = window.prompt("請輸入Dopamine")//13
	let epinephrine_add = window.prompt("請輸入epinephrine")//0
	let norepinephrine_add = window.prompt("請輸入norepinephrine")//0
	let dobutamine_add = window.prompt("請輸入dobutamine")//0
	let ComaScale_add = window.prompt("請輸入ComaScale")//16
	let Creatinine_add = window.prompt("請輸入Creatinine")//0.9
	let urineVolume_add = window.prompt("請輸入urineVolume")//822
	let lastSOFA_add = window.prompt("請輸入lastSOFA")//0
	let infusion_add = window.prompt("請輸入infusion")//0
	let Lactate_add = window.prompt("請輸入Lactate")//2
	let gcs_add = window.prompt("請輸入gcs")//16
	let bun_add = window.prompt("請輸入bun")//15.5
	let FIO2_percent_add = window.prompt("請輸入FIO2_percent")//0.33

	let respiratoryRate_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "9279-1",
					"display": "Respiratory rate",
					"system": "http://loinc.org"
				}
			],
			"text": "Respiratory rate"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/323528e6-1ebb-469b-8a0b-3bd4e03be6b5"
		},
		"id": "a26487f6-13e3-4ee4-91a2-a1074cb9eb52",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:19.830439+00:00",
			"versionId": "MTY3ODg3MzU3OTgzMDQzOTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "times/min",
			"system": "http://unitsofmeasure.org",
			"unit": "times/min",
			"value": Number(respiratoryRate_add)
		}
	}
	let consciousness_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "80288-4",
					"display": "Level of consciousness",
					"system": "http://loinc.org"
				}
			],
			"text": "Level of consciousness"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/1c48a667-9e77-4e02-80fb-ab4b310e046b"
		},
		"id": "4b480ace-6294-49f7-a9a3-32e557d7276e",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.175597+00:00",
			"versionId": "MTY3ODg3MzU4MDE3NTU5NzAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "{score}",
			"system": "http://unitsofmeasure.org",
			"unit": "{score}",
			"value": Number(consciousness_add)
		}
	}
	let systolicPressure_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "55284-4",
					"display": "Blood Pressure",
					"system": "http://loinc.org"
				}
			],
			"text": "Blood Pressure"
		},
		"component": [
			{
				"code": {
					"coding": [
						{
							"code": "8462-4",
							"display": "Diastolic Blood Pressure",
							"system": "http://loinc.org"
						}
					],
					"text": "Diastolic Blood Pressure"
				},
				"valueQuantity": {
					"code": "mm[Hg]",
					"system": "http://unitsofmeasure.org",
					"unit": "mm[Hg]",
					"value": 71.40576225472539
				}
			},
			{
				"code": {
					"coding": [
						{
							"code": "8480-6",
							"display": "Systolic Blood Pressure",
							"system": "http://loinc.org"
						}
					],
					"text": "Systolic Blood Pressure"
				},
				"valueQuantity": {
					"code": "mm[Hg]",
					"system": "http://unitsofmeasure.org",
					"unit": "mm[Hg]",
					"value": Number(systolicPressure_add)
				}
			}
		],
		"effectiveDateTime": "2016-11-08T18:14:24-05:00",
		"encounter": {
			"reference": "Encounter/b7f1fe7d-def2-49c1-ba65-e7b289bcb08a"
		},
		"id": "25c8a7b7-d3e2-4471-b165-f97a00be192f",
		"issued": "2016-11-08T18:14:24.746-05:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.343729+00:00",
			"versionId": "MTY3ODg3MzU4MDM0MzcyOTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		}
	}
	let height_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "8302-2",
					"display": "Body Height",
					"system": "http://loinc.org"
				}
			],
			"text": "Body Height"
		},
		"effectiveDateTime": "2019-07-23T00:19:26-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": new_id,
		"issued": "2019-07-23T00:19:26.134-04:00",
		"meta": {
			"lastUpdated": "2022-11-09T14:46:42.090842+00:00",
			"versionId": "MTY2ODAwNTIwMjA5MDg0MjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "cm",
			"system": "http://unitsofmeasure.org",
			"unit": "cm",
			"value": Number(height_add)
		}
	}
	let weight_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "29463-7",
					"display": "Body Weight",
					"system": "http://loinc.org"
				}
			],
			"text": "Body Weight"
		},
		"effectiveDateTime": "2019-08-27T00:19:26-04:00",
		"encounter": {
			"reference": "Encounter/be779465-3532-446c-9003-40a509b6a038"
		},
		"id": "63f5e6b0-e5c7-442e-aa24-8f0e3aa441ed",
		"issued": "2019-08-27T00:19:26.134-04:00",
		"meta": {
			"lastUpdated": "2022-11-09T14:46:42.116905+00:00",
			"versionId": "MTY2ODAwNTIwMjExNjkwNTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "kg",
			"system": "http://unitsofmeasure.org",
			"unit": "kg",
			"value": Number(weight_add)
		}
	}
	let WBC_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "26464-8",
					"display": "Leukocytes in Blood",
					"system": "http://loinc.org"
				}
			],
			"text": "WBC"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/1c48a667-9e77-4e02-80fb-ab4b310e046b"
		},
		"id": "8c072d3e-6b82-42d0-9b9a-c081d662c24f",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:13.666059+00:00",
			"versionId": "MTY3ODg3MzU3MzY2NjA1OTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "10*3/μL",
			"system": "http://unitsofmeasure.org",
			"unit": "10*3/μL",
			"value": Number(WBC_add)
		}
	}
	let CRP_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "1988-5",
					"display": "C reactive protein in Serum or Plasma",
					"system": "http://loinc.org"
				}
			],
			"text": "CRP"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/41837dda-0080-4664-90d8-e70a9ce512dd"
		},
		"id": "2262a284-34c5-442f-aa79-b09f2185574c",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:12.975402+00:00",
			"versionId": "MTY3ODg3MzU3Mjk3NTQwMjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mg/dL",
			"system": "http://unitsofmeasure.org",
			"unit": "mg/dL",
			"value": Number(CRP_add)
		}
	}
	let Seg_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "26505-8",
					"display": "Segmented neutrophils/100 leukocytes in Blood",
					"system": "http://loinc.org"
				}
			],
			"text": "Seg"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "10fd6d1d-37c2-4f7c-b7f0-ec278aabefb4",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:13.790456+00:00",
			"versionId": "MTY3ODg3MzU3Mzc5MDQ1NjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "%",
			"system": "http://unitsofmeasure.org",
			"unit": "%",
			"value": Number(Seg_add)
		}
	}
	let Band_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "26508-2",
					"display": "Band form neutrophils/100 leukocytes in Blood",
					"system": "http://loinc.org"
				}
			],
			"text": "Band"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/62857701-5d87-424b-b5b1-c10cf4be8ddb"
		},
		"id": "d37f224e-a511-42e6-af6e-d7b759c152f2",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:10.016993+00:00",
			"versionId": "MTY3ODg3MzU3MDAxNjk5MzAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "%",
			"system": "http://unitsofmeasure.org",
			"unit": "%",
			"value": Number(Band_add)
		}
	}
	let PF_ratio_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "50984-4",
					"display": "Horowitz index in Arterial blood",
					"system": "http://loinc.org"
				}
			],
			"text": "PFratio"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/1c48a667-9e77-4e02-80fb-ab4b310e046b"
		},
		"id": "70baa700-9b12-4d85-9b5c-d6ffb0ca68d7",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.265882+00:00",
			"versionId": "MTY3ODg3MzU4MDI2NTg4MjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mmHg",
			"system": "http://unitsofmeasure.org",
			"unit": "mmHg",
			"value": Number(PF_ratio_add)
		}
	}
	let Platelet_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "26515-7",
					"display": "Platelets in Blood",
					"system": "http://loinc.org"
				}
			],
			"text": "Platelets in Blood"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/59d20c39-3a0c-4750-ace3-8c22a0c91d0c"
		},
		"id": "42fbae86-cfd9-47b3-a35a-33aa6cdf47fb",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.370074+00:00",
			"versionId": "MTY3ODg3MzU4MDM3MDA3NDAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "10*3/μL",
			"system": "http://unitsofmeasure.org",
			"unit": "10*3/μL",
			"value": Number(Platelet_add)
		}
	}
	let Bilirubin_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "1975-2",
					"display": "Bilirubin.total in Serum or Plasma",
					"system": "http://loinc.org"
				}
			],
			"text": "Bilirubin.total in Serum or Plasma"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/cd07956e-0239-462f-9549-dda9f4335cfe"
		},
		"id": "8c13f3a4-0a39-47e7-8577-3cf7d783f42f",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:19.587379+00:00",
			"versionId": "MTY3ODg3MzU3OTU4NzM3OTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mg/dL",
			"system": "http://unitsofmeasure.org",
			"unit": "mg/dL",
			"value": Number(Bilirubin_add)
		}
	}
	let MAP_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "8478-0",
					"display": "Mean blood pressure",
					"system": "http://loinc.org"
				}
			],
			"text": "Mean blood pressure"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "dd31724b-0c7b-472c-92b9-e7e49a62fcf8",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-25T15:05:47.904361+00:00",
			"versionId": "MTY3OTc1Njc0NzkwNDM2MTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mmHg",
			"system": "http://unitsofmeasure.org",
			"unit": "mmHg",
			"value": Number(MAP_add)
		}
	}
	let Dopamine_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "14703-3",
					"display": "DOPamine in Serum or Plasma",
					"system": "http://loinc.org"
				}
			],
			"text": "DOPamine in Serum or Plasma"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "5da1c078-89da-4583-8deb-da3a5f47226c",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-25T17:23:22.406892+00:00",
			"versionId": "MTY3OTc2NTAwMjQwNjg5MjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "ug/kg/min",
			"system": "http://unitsofmeasure.org",
			"unit": "ug/kg/min",
			"value": Number(Dopamine_add)
		}
	}
	let epinephrine_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "11046-0",
					"display": "EPINEPHrine in Urine",
					"system": "http://loinc.org"
				}
			],
			"text": "EPINEPHrine in Urine"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "fa7c382d-5e07-4f04-b7f7-c10a19e14fcd",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-25T17:21:35.205745+00:00",
			"versionId": "MTY3OTc2NDg5NTIwNTc0NTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "ug/kg/min",
			"system": "http://unitsofmeasure.org",
			"unit": "ug/kg/min",
			"value": Number(epinephrine_add)
		}
	}
	let norepinephrine_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "2666-6",
					"display": "Norepinephrine in Urine",
					"system": "http://loinc.org"
				}
			],
			"text": "Norepinephrine in Urine"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "b5ad5851-f731-4fff-a84e-cf7885d9ddde",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-25T17:23:07.751826+00:00",
			"versionId": "MTY3OTc2NDk4Nzc1MTgyNjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "ug/kg/min",
			"system": "http://unitsofmeasure.org",
			"unit": "ug/kg/min",
			"value": Number(norepinephrine_add)
		}
	}
	Dobutamine_obj={
		"category": [
		  {
			"coding": [
			  {
				"code": "vital-signs",
				"display": "vital-signs",
				"system": "http://terminology.hl7.org/CodeSystem/observation-category"
			  }
			]
		  }
		],
		"code": {
		  "coding": [
			{
			  "code": "21248-0",
			  "display": "Dobutamine in Serum or Plasma",
			  "system": "http://loinc.org"
			}
		  ],
		  "text": "Dobutamine in Serum or Plasma"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
		  "reference": "Encounter/41837dda-0080-4664-90d8-e70a9ce512dd"
		},
		"id": "70c433d8-e825-4172-93e8-f9c3bebdb664",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
		  "lastUpdated": "2023-03-15T09:46:12.306039+00:00",
		  "versionId": "MTY3ODg3MzU3MjMwNjAzOTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
		  "reference": "Patient/"+new_id
		},
		"valueQuantity": {
		  "code": "mg/ml",
		  "system": "http://unitsofmeasure.org",
		  "unit": "mg/ml",
		  "value": Number(dobutamine_add)
		}
	  }
	let ComaScale_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "35088-4",
					"display": "Glasgow coma score total",
					"system": "http://loinc.org"
				}
			],
			"text": "Glasgow coma score total"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "2fde8de7-8053-4888-8141-3448bc40bfec",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-25T17:07:17.966733+00:00",
			"versionId": "MTY3OTc2NDAzNzk2NjczMzAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "{score}",
			"system": "http://unitsofmeasure.org",
			"unit": "{score}",
			"value": Number(ComaScale_add)
		}
	}
	let Creatinine_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "2160-0",
					"display": "Creatinine in Serum or Plasma",
					"system": "http://loinc.org"
				}
			],
			"text": "Creatinine in Serum or Plasma"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/323528e6-1ebb-469b-8a0b-3bd4e03be6b5"
		},
		"id": "d7a052c1-b515-4902-825d-fd32a6649f20",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:16.571641+00:00",
			"versionId": "MTY3ODg3MzU3NjU3MTY0MTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mg/dL",
			"system": "http://unitsofmeasure.org",
			"unit": "mg/dL",
			"value": Number(Creatinine_add)
		}
	}
	let urineVolume_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "9192-6",
					"display": "Urine output 24 hour",
					"system": "http://loinc.org"
				}
			],
			"text": "Urine output 24 hour"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/323528e6-1ebb-469b-8a0b-3bd4e03be6b5"
		},
		"id": "dd9ab5f2-0f85-407c-b8ae-d4abf9cb4034",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:19.409180+00:00",
			"versionId": "MTY3ODg3MzU3OTQwOTE4MDAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mL/day",
			"system": "http://unitsofmeasure.org",
			"unit": "mL/day",
			"value": Number(urineVolume_add)
		}
	}
	let lastSOFA_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "96790-1",
					"display": "SOFA Total Score",
					"system": "http://loinc.org"
				}
			],
			"text": "SOFA Total Score"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/41837dda-0080-4664-90d8-e70a9ce512dd"
		},
		"id": "943b04d5-13d2-4733-afd8-b8a2b416858a",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.008457+00:00",
			"versionId": "MTY3ODg3MzU4MDAwODQ1NzAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "{score}",
			"system": "http://unitsofmeasure.org",
			"unit": "{score}",
			"value": lastSOFA_add
		}
	}
	let infusion_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "76310-2",
					"display": "Infusion volume.programmed Procedure Infusion pump",
					"system": "http://loinc.org"
				}
			],
			"text": "Infusion"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/62857701-5d87-424b-b5b1-c10cf4be8ddb"
		},
		"id": "aa7ab4e5-2dc9-41ce-97fc-3606a432b7d0",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:16.940278+00:00",
			"versionId": "MTY3ODg3MzU3Njk0MDI3ODAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "ml",
			"system": "http://unitsofmeasure.org",
			"unit": "ml",
			"value": Number(infusion_add)
		}
	}
	let Lactate_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "2524-7",
					"display": "Lactate in Serum or Plasma",
					"system": "http://loinc.org"
				}
			],
			"text": "Lactate in Serum or Plasma"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "06a498b7-1d0b-41ff-8c51-d0befb8606af",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.020071+00:00",
			"versionId": "MTY3ODg3MzU4MDAyMDA3MTAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mmole/L",
			"system": "http://unitsofmeasure.org",
			"unit": "mmole/L",
			"value": Number(Lactate_add)
		}
	}
	let gcs_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "35088-4",
					"display": "Glasgow coma score total",
					"system": "http://loinc.org"
				}
			],
			"text": "Glasgow coma score total"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/6d6c07f8-0521-48f6-860b-953a6cd0aa2c"
		},
		"id": "fa383ced-c26d-4ac6-b690-acfa8b48e79b",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-26T02:45:16.977732+00:00",
			"versionId": "MTY3OTc5ODcxNjk3NzczMjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "{score}",
			"system": "http://unitsofmeasure.org",
			"unit": "{score}",
			"value": Number(gcs_add)
		}
	}
	let bun_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "3094-0",
					"display": "Urea nitrogen [Mass/volume] in Blood",
					"system": "http://loinc.org"
				}
			],
			"text": "bun"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/41837dda-0080-4664-90d8-e70a9ce512dd"
		},
		"id": "3320d394-4b75-4ab2-be3c-b8ea70d5e92c",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:20.311543+00:00",
			"versionId": "MTY3ODg3MzU4MDMxMTU0MzAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "mg/dL",
			"system": "http://unitsofmeasure.org",
			"unit": "mg/dL",
			"value": Number(bun_add)
		}
	}
	let FIO2_percent_add_obj = {
		"category": [
			{
				"coding": [
					{
						"code": "vital-signs",
						"display": "vital-signs",
						"system": "http://terminology.hl7.org/CodeSystem/observation-category"
					}
				]
			}
		],
		"code": {
			"coding": [
				{
					"code": "3150-0",
					"display": "Inhaled oxygen concentration",
					"system": "http://loinc.org"
				}
			],
			"text": "FIO2_percent"
		},
		"effectiveDateTime": "2011-08-08T23:24:58-04:00",
		"encounter": {
			"reference": "Encounter/41837dda-0080-4664-90d8-e70a9ce512dd"
		},
		"id": "e6533e65-97ca-4754-9a6d-64ab045d750f",
		"issued": "2011-08-08T23:24:58.908-04:00",
		"meta": {
			"lastUpdated": "2023-03-15T09:46:16.757736+00:00",
			"versionId": "MTY3ODg3MzU3Njc1NzczNjAwMA"
		},
		"resourceType": "Observation",
		"status": "final",
		"subject": {
			"reference": "Patient/" + new_id
		},
		"valueQuantity": {
			"code": "%",
			"system": "http://unitsofmeasure.org",
			"unit": "%",
			"value": Number(FIO2_percent_add)
		}
	}
	if (WBC_add && CRP_add && Seg_add && Band_add && PF_ratio_add && Platelet_add && Bilirubin_add && MAP_add && Dopamine_add && epinephrine_add && norepinephrine_add && ComaScale_add && Creatinine_add && urineVolume_add) {
		await add_data(respiratoryRate_add_obj, false).then(
			await add_data(consciousness_add_obj, false)).then(
				await add_data(systolicPressure_add_obj, false)).then(
					await add_data(height_obj, false)).then(
						await add_data(weight_obj, false)).then(
							await add_data(WBC_add_obj, false)).then(
								await add_data(CRP_add_obj, false)).then(
									await add_data(Seg_add_obj, false)).then(
										await add_data(Band_add_obj, false)).then(
											await add_data(PF_ratio_obj, false)).then(
												await add_data(Platelet_obj, false)).then(
													await add_data(Bilirubin_obj, false)).then(
														await add_data(MAP_obj, false)).then(
															await add_data(Dopamine_obj, false)).then(
																await add_data(epinephrine_obj, false)).then(
																	await add_data(norepinephrine_obj, false)).then(
																		await add_data(ComaScale_obj, false)).then(
																			await add_data(Creatinine_obj, false)).then(
																				await add_data(urineVolume_obj, false)).then(
																					await add_data(lastSOFA_add_obj, false)).then(
																						await add_data(infusion_add_obj, false)).then(
																							await add_data(Lactate_add_obj, false)).then(
																								await add_data(gcs_add_obj, false)).then(
																									await add_data(bun_add_obj, false)).then(
																										await add_data(FIO2_percent_add_obj, false)).then(
																											alert("更新成功")
																										)

	}

}
	//location.reload();
