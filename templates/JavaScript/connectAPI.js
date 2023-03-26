function getPatient(token) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Patient";
    var xhr = new XMLHttpRequest(); // XMLHttpRequest物件(以此物件的方法進行資料請求)
    xhr.open('GET', dataUrl, true); // 以GET方法開啟一個請求 //open('Method',API的URL,預設值為true非同步進行)
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send(); // 送出請求(若為GET參數不填或填null)

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      // console.log(data);
      resolve(APIresult);
    }
  });
}

function getPatientById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Patient/" + id;
    var xhr = new XMLHttpRequest(); // XMLHttpRequest物件(以此物件的方法進行資料請求)
    xhr.open('GET', dataUrl, true); // 以GET方法開啟一個請求 //open('Method',API的URL,預設值為true非同步進行)
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send(); // 送出請求(若為GET參數不填或填null)

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      // console.log(data);
      resolve(APIresult);
    }
  });
}

function getHeightById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Observation?subject=" + id + "&code=http://loinc.org|8302-2" + "&_sort=-date";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getWeightById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Observation?subject=" + id + "&code=http://loinc.org|29463-7" + "&_sort=-date";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getObservationById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Observation?subject=Patient/" + id;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getObservationByCode(token, id, code) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/crack-will-380312/locations/asia-east1/datasets/patient/fhirStores/Test/fhir/Observation?subject=" + id + "&code=http://loinc.org|" + code + "&_sort=-date";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getModelResult_NF(sea, wbc, crp, seg, band) {
  return new Promise((resolve, reject) => {
    var dataUrl = "http://localhost:5000/GET/predict/NF";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', dataUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    var value = {
      "sea": sea,
      "wbc": wbc,
      "crp": crp,
      "seg": seg,
      "band": band
    }
    var value_data = JSON.stringify(value);
    xhr.send(value_data);

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getModelResult_sepsis(gcs, meds_ams15b, meds_plt150b, sofa_res, sofa_ner, sofa_liver,
  sofa_coag, sofa_renal, bun, cre, plt, FIO2_percent, PF_ratio, fio2_per, fio2_cb) {
  return new Promise((resolve, reject) => {
    var dataUrl = "http://localhost:5000/GET/predict/sepsis";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', dataUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    var value = {
      'gcs': gcs, 'meds_ams15b': meds_ams15b, 'meds_plt150b': meds_plt150b, 'sofa_res': sofa_res, 'sofa_ner': sofa_ner, 'sofa_liver': sofa_liver,
      'sofa_coag': sofa_coag, 'sofa_renal': sofa_renal, 'bun': bun, 'cre': cre, 'plt': plt, 'FIO2_percent': FIO2_percent, 'PF_ratio': PF_ratio, 'fio2_per': fio2_per, 'fio2_cb': fio2_cb
    }
    var value_data = JSON.stringify(value);
    xhr.send(value_data);

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getToken_fhir() {
  return new Promise((resolve, reject) => {
    var dataUrl = "http://localhost:5000/GET/token_fhir";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.send();

    xhr.onload = function () {
      console.log(this.responseText);
      APIresult = JSON.parse(this.responseText);
       
      resolve(APIresult);
    }
  });
}