/*
https://fhir2-dm5wodoipq-de.a.run.app/
*/
function getPatient(token) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Patient";
    var xhr = new XMLHttpRequest(); // XMLHttpRequest物件(以此物件的方法進行資料請求)
    xhr.open('GET', dataUrl, true); // 以GET方法開啟一個請求 //open('Method',API的URL,預設值為true非同步進行)
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send(); // 送出請求(若為GET參數不填或填null)

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      // console.log(this.responseText);
      resolve(APIresult);
    }
  });
}

function getPatientById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Patient/" + id;
    var xhr = new XMLHttpRequest(); // XMLHttpRequest物件(以此物件的方法進行資料請求)
    xhr.open('GET', dataUrl, true); // 以GET方法開啟一個請求 //open('Method',API的URL,預設值為true非同步進行)
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send(); // 送出請求(若為GET參數不填或填null)

    xhr.onload = function () {
      APIresult = JSON.parse(this.responseText);
      // console.log(this.responseText);
      resolve(APIresult);
    }
  });
}

function getHeightById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Observation?subject=" + id + "&code=http://loinc.org|8302-2" + "&_sort=-date";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      console.log(this.responseText)
      APIresult = JSON.parse(this.responseText);
      resolve(APIresult);
    }
  });
}

function getWeightById(token, id) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Observation?subject=" + id + "&code=http://loinc.org|29463-7" + "&_sort=-date";
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
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Observation?subject=Patient/" + id+"&_count=500";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    xhr.send();

    xhr.onload = function () {
      console.log(this.responseText)
      APIresult = JSON.parse(this.responseText);
      // console.log(this.responseText);
      resolve(APIresult);
    }
  });
}

function getObservationByCode(token, id, code) {
  return new Promise((resolve, reject) => {
    var dataUrl = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Observation?subject=" + id + "&code=http://loinc.org|" + code + "&_sort=-date";
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
    var dataUrl = "https://fhir2-dm5wodoipq-de.a.run.app/GET/predict/NF";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', dataUrl, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    // xhr.setRequestHeader('Authorization', 'Bearer ' + token)
    var value = {
      "sea": Number(sea),
      "wbc": Number(wbc),
      "crp": Number(crp),
      "seg": Number(seg),
      "band": Number(band)
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
    console.log(gcs)
  return new Promise((resolve, reject) => {
    var dataUrl = "https://fhir2-dm5wodoipq-de.a.run.app/GET/predict/sepsis";
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
    var dataUrl = "https://fhir2-dm5wodoipq-de.a.run.app/GET/token_fhir";
    var xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl, true);
    xhr.send();
    
    xhr.onload = function () {
      //console.log(this.responseText)
      APIresult = JSON.parse(this.responseText);
      console.log(this.responseText);
      //console.log(data);
      resolve(APIresult);
    }
  });
}async function update(promptStr, settingFunc, htmlId, htmlPrefix) {
  let new_data = window.prompt(promptStr)
  if (new_data == null||new_data == "") {
      alert("請輸入資料")
      return
  }
  let token
  let patien_json
  let ori_url = document.URL
  let id = ori_url.split("=")[1];
  let result1 = await getToken_fhir().then((res1) => {
      token = res1;
      console.log("token = " + token)
  });
  var result2 = await getPatientById(token, id).then((res2) => {
      patien_json = res2;
  });
  //開始PUT
  let url = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/Patient/" + id;
  const headers = new Headers({
      "Content-Type": "application/fhir+json",
      "Authorization": "Bearer " + token,
  });

  // 設定請求主體，此處使用 JSON 格式的 FHIR 資源

  //   console.log(updateJson(patien_json,"name",))


  const body = JSON.stringify(settingFunc(patien_json, new_data))

  //console.log(body)
  //patien_json['name'][0]["given"][0]=new_name

  // 設定請求選項
  const options = {
      method: "PUT",
      headers: headers,
      body: body
  };

  // 發送請求
  const response = await fetch(url, options)
      .then((response ) => {
          if (response.ok) {
            if(htmlId=='mask'){
              new_data = new_data.replace(/1/g,"有").replace(/0/g,"無")
            }
              document.getElementById(htmlId).innerHTML = htmlPrefix + new_data
              alert("更新成功!")
          } else {
              throw Error(JSON.stringify(response))
          }
      }

      )
      .then(data => () => {

          // console.log(data)

      }).then(() => {


      })
      .catch(error => console.error(error));


}
async function update_Observation(promptStr, code_text, htmlPrefix, htmlId,htmlUnit=true) {
  let new_data = window.prompt(promptStr)//要放入的資料
  if(new_data=="" || new_data== null){
    alert("請輸入資料")
    return
  }
  let token//JWT 驗證 token
  let patien_json//病人的所有有observation JSON 資料
  let ori_url = document.URL//原始URL
  let resultOfData//response中提取出的資料
  let id = ori_url.split("=")[1].split("&")[0];//從URL中提取出病人ID(由頁面傳入)
  //取得JWT 驗證token
  let result1 = await getToken_fhir().then((res1) => {
      token = res1;
      console.log("token = " + token)
  });
  //用病人ID 取得病人所有 observation JSON 資料
  let result2 = await getObservationById(token, id).then((res2) => {
      patien_json = res2;
  });
  //從response 提取出對應的資料
  
  for (var i=patien_json.entry.length-1;i>0;i--) {
    const element=patien_json.entry[i]
      if (element.resource.code.text == code_text) {
          element.resource.valueQuantity.value = Number(new_data)
          //取得該資料的ID
          let url = element.fullUrl+""
          const headers = new Headers({
              "Content-Type": "application/fhir+json",
              "Authorization": "Bearer " + token,
          });
          const body = JSON.stringify(element.resource)
          const options = {
              method: "PUT",
              headers: headers,
              body: body
          };
          
          await fetch(url, options)
          .then((response) => {
              if (response.ok) {
                  document.getElementById(htmlId).innerHTML = htmlPrefix + new_data+" "+(htmlUnit?element.resource.valueQuantity.unit:"")
                  alert("更新成功!")
              } else {
                  alert("更新失敗!")
                  throw Error(JSON.stringify(response))

              }
              
          }
  
          )
          .then(data => () => {
  
              console.log("YA"+data)
  
          })
          .catch(error => console.error(error));
          break
      }
  }



  //開始PUT


  // 設定請求主體，此處使用 JSON 格式的 FHIR 資源

  //   console.log(updateJson(patien_json,"name",))




}
function update_data(token,id,source_type,data_type,data){//no use
  console.log(token,id,source_type,data_type,data)
  const url = "https://healthcare.googleapis.com/v1beta1/projects/agile-device-389611/locations/asia-east1/datasets/fhir/fhirStores/fhir/"+source_type+"/"+data_type;

// 設定請求標頭
const headers = new Headers({
  "Content-Type": "application/fhir+json",
  "Authorization": "Bearer "+token,
});

// 設定請求主體，此處使用 JSON 格式的 FHIR 資源
const body = JSON.stringify({ 
  "resourceType": source_type,
  "id": data_type,
  "gender":"female"
});

// 設定請求選項
const options = {
  method: "PUT",
  headers: headers,
  body: body
};

// 發送請求
fetch(url, options)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
}
function updateJson(jsonString, paramName, paramValue) {
  // 将 JSON 字符串解析为 JavaScript 对象
  console.log(jsonString)
  let jsonObj = jsonString;

  // 检查对象中是否存在该参数
  if (jsonObj.hasOwnProperty(paramName)) {
    // 更新参数值
    jsonObj[paramName] = paramValue;
  }

  // 将更新后的对象转换为 JSON 字符串并返回
  return JSON.stringify(jsonObj);
}
