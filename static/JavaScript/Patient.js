var patient_json = {
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
    "birthDate": "",
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
    "gender": "",
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
                ""
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
var height_obj = {
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
    "id": "",
    "issued": "2019-07-23T00:19:26.134-04:00",
    "meta": {
        "lastUpdated": "2022-11-09T14:46:42.090842+00:00",
        "versionId": "MTY2ODAwNTIwMjA5MDg0MjAwMA"
    },
    "resourceType": "Observation",
    "status": "final",
    "subject": {
        "reference": "Patient/"
    },
    "valueQuantity": {
        "code": "cm",
        "system": "http://unitsofmeasure.org",
        "unit": "cm",
        "value": 0
    }
}
var weight_obj = {
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
        "reference": "Patient/"
    },
    "valueQuantity": {
        "code": "kg",
        "system": "http://unitsofmeasure.org",
        "unit": "kg",
        "value": 0
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
    let url = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/" + (isPatient ? "Patient" : "Observation");
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

    return (patient_obj.id)
}
var patient_id

async function add_patient(name, sex, birth, weight, height) {
    var suc = false
    let objPatient = JSON.parse(JSON.stringify(patient_json));
    let objHeight = JSON.parse(JSON.stringify(height_obj));
    let objWeight = JSON.parse(JSON.stringify(weight_obj));
    objPatient['name'][0]['given'][0] = name
    objPatient['gender'] = sex
    objPatient['birthDate'] = birth
    var patient_id
    await add_data(objPatient, true).then((id) => {
        console.log("success insert basic data")
        patient_id = id
        objHeight['id'] = patient_id
        objHeight['valueQuantity']['value'] = Number(height)
        objHeight['subject']['reference'] = 'Patient/' + patient_id
        objWeight['id'] = patient_id
        objWeight['valueQuantity']['value'] = Number(weight)
        objWeight['subject']['reference'] = 'Patient/' + patient_id
         add_data(objHeight, false)
         add_data(objWeight, false)
         suc=true
    })

    if (suc) {
        console.log("success")
    }
    return suc
}
