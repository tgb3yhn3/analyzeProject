// JavaScript Document
var token_fhir
var data1
var data2
var data3
var id
get_data();

var names = document.getElementById("names");
var sex = document.getElementById("sex");
var birth = document.getElementById("birth");
var age = document.getElementById("age");
var height = document.getElementById("height");
var weight = document.getElementById("weight");

async function get_data() {
    var url = document.URL;
    var getvalue = url.split("?")[1];
    id = url.split("=")[1];
    var result1 = await getToken_fhir().then((res1) => {
        token_fhir = res1;
    });
    var result2 = await getPatientById(token_fhir, id).then((res2) => {
        data1 = res2;
    });
    var result3 = await getHeightById(token_fhir, id).then((res3) => {
        data2 = res3;
    });
    var result4 = await getWeightById(token_fhir, id).then((res4) => {
        data3 = res4;
    });
    names.innerText = "姓名：" + data1.name[0].given[0];
    sex.innerText = "性別：" + data1.gender;
    birth.innerText = "生日：" + data1.birthDate;
    age.innerText = "年齡：" + Math.ceil((new Date - new Date(data1.birthDate)) / 31536000000);
    height.innerText = "身高：" + Math.round(data2.entry[0].resource.valueQuantity.value * 100) / 100 + " " + data2.entry[0].resource.valueQuantity.unit;
    weight.innerText = "體重：" + Math.round(data3.entry[0].resource.valueQuantity.value * 100) / 100 + " " + data3.entry[0].resource.valueQuantity.unit;
}