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
var mask= document.getElementById("mask");
async function get_data() {
    var url = document.URL;
    var getvalue = url.split("?")[1];
    id = url.split("=")[1];
    // if(id==undefined){
    //     id="a0917f1f-b1b9-4656-a48e-851bf15fede3"
    // }
    var result1 = await getToken_fhir().then((res1) => {

        token_fhir = res1;
        console.log("token= " + token_fhir)
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
    for (var i = 0; i < data1.extension.length; i++) {
        if (data1.extension[i].url == 'Respiratory mask') {
            mask.innerText="使用呼吸器："+(data1.extension[i].valueDecimal?"是":"否")
            console.log("mask",data1.extension[i].valueDecimal)
        }
    }
    age.innerText = "年齡：" + Math.ceil((new Date - new Date(data1.birthDate)) / 31536000000);
    height.innerText = "身高：" + Math.round(data2.entry[0].resource.valueQuantity.value * 100) / 100 + " " + data2.entry[0].resource.valueQuantity.unit;
    weight.innerText = "體重：" + Math.round(data3.entry[0].resource.valueQuantity.value * 100) / 100 + " " + data3.entry[0].resource.valueQuantity.unit;
}

async function update_name() {
    await update(
        "請輸入新的姓名",
        (data, newData) => {
            data['name'][0]["given"][0] = newData
            return data
        },
        'names',
        '姓名：')
}
async function update_sex() {
    await update(
        "請輸入新的性別",
        (data, newData) => {
            data['gender'] = newData
            return data
        },
        'sex',
        '性別：')
}
async function update_birth() {
    await update(
        "請輸入新的生日",
        (data, newData) => {
            data['birthDate'] = newData
            age.innerText = "年齡：" + Math.ceil((new Date - new Date(newData)) / 31536000000);
            return data
        },
        'birth',
        '生日：').catch(error => console.log(error))

}
async function update_mask() {
    await update(
        "請輸入是否使用呼吸器(1:是 0:否)",
        (data, newData) => {
            for(var i=0;i<data.extension.length;i++){
                if(data.extension[i].url=='Respiratory mask'){
                    data.extension[i].valueDecimal=Number(newData)
                    mask.innerText="使用呼吸器："+(newData?"是":"否")
                    return data
                }
            }
            
        },
        'mask',
        '使用呼吸器：').catch(error => console.log(error))
    }
async function update_height() {
    await update_Observation("請輸入身高", "Body Height", "身高：", "height")
}
async function update_weight() {
    await update_Observation("請輸入體重", "Body Weight", "體重：", "weight")
}