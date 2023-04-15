var token_fhir
var data1
var data2

var url = document.URL;
var getvalue = url.split("?")[1];
var id = getvalue.split("&")[0].split("=")[1];
var TTTTT = getvalue.split("&")[1].split("=")[1];
var sea = parseInt(getvalue.split("&")[2].split("=")[1]);
var wbc;
var crp;
var seg;
var band;
var model_index = ["decisionTree", "randomForest", 'logisticregression', "neuralNetwork", "supportVectorMachine"];
var score_index = ["decisionTree_proba", "randomForest_proba", 'logisticregression_proba', "neuralNetwork_proba", "supportVectorMachine_proba"];


async function get_data() {
    var result1 = await getToken_fhir().then((res1) => {
        token_fhir = res1;
    });
    var result2 = await getObservationById(token_fhir, id).then((res2) => {
        data1 = res2;
    })
    for (var i = 0; i < data1.entry.length; i++) {
        if (data1.entry[i].resource.code.text == 'WBC') {
            wbc = data1.entry[i].resource.valueQuantity.value
        }
        if (data1.entry[i].resource.code.text == 'CRP') {
            crp = data1.entry[i].resource.valueQuantity.value
        }
        if (data1.entry[i].resource.code.text == 'Seg') {
            seg = data1.entry[i].resource.valueQuantity.value
        }
        if (data1.entry[i].resource.code.text == 'Band') {
            band = data1.entry[i].resource.valueQuantity.value
        }
    }
    sheet();
    var result3 = await getModelResult_NF(sea, wbc, crp, seg, band).then((res3) => {
        data2 = res3;
        //確認選擇哪些模型呈現分析
        for (var i = 0; i < TTTTT.length; i++) {
            var Yes_No
            if (data2[model_index[i]] == 1) {
                Yes_No = true;
            }
            else {
                Yes_No = false;
            }
            if (TTTTT[i] == "T") {
                document.getElementById(score_index[i]).innerHTML = "信心度 " + data2[score_index[i]] + "%"
                if (Yes_No) {
                    document.getElementById("choice" + (i + 1) + "-1").style.border = "medium solid red"
                    document.getElementById("choice" + (i + 1) + "-2").innerHTML = "判定為 NF";
                }
                else {
                    document.getElementById("choice" + (i + 1) + "-1").style.border = "medium solid green"
                    document.getElementById("choice" + (i + 1) + "-2").innerHTML = "判定為 non-NF";
                }
            }
            else if (TTTTT[i] == "F") {
                document.getElementById("choice" + (i + 1)).style.display = "none";
            }
        }
        display_image(calculateresult(band, sea, seg, crp), 'resultimage');
        radar_test();
    })
};

function display_image(src, alt) {     //顯示圖片
    var a = document.getElementById("choice1-0");
    a.src = src;
    a.alt = alt;
}

function calculateresult(band, sea, seg, crp) {          //計算結果
    if (band > 1)
        return "static/images/Dt1.png";
    else if (sea > 0) {
        if (seg > 83)
            return "static/images/Dt2.png";
        else
            return "static/images/Dt3.png";
    }
    else {
        if (crp > 151.84)
            return "static/images/Dt4.png";
        else
            return "static/images/Dt5.png";
    }
}
function back_click(element) {
    window.location.replace('http://localhost:5001/NFchoice?id=' + id);
}

function backlist(element) {
    window.location.replace('http://localhost:5001/patientlist');
}

function show() {
    chk = document.getElementById("DTchk")
    pic = document.getElementById("choice1-0");
    if (chk.checked) {
        pic.style.display = "none";
        chk.checked = false;
    }
    else {
        pic.style.display = "flex";
        chk.checked = true;
    }
}

function detail(element) {
    window.open('http://localhost:5001/NFbodyvalue' + '?sea=' + sea + '&wbc=' + wbc + '&crp=' + crp + '&seg=' + seg + '&band=' + band)
}

function sheet() {
    let table = document.createElement('table');
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');

    table.appendChild(thead);
    table.appendChild(tbody);

    // Adding the entire table to the body tag
    document.getElementById('sheet').appendChild(table);

    let row_1 = document.createElement('tr');
    let heading_1 = document.createElement('th');
    heading_1.innerHTML = "col.<br>row.";
    let heading_2 = document.createElement('th');
    heading_2.innerHTML = "<nobr>目前病患</nobr>";
    let heading_3 = document.createElement('th');
    heading_3.innerHTML = "<nobr>NF</nobr><br><nobr>中位數</nobr>";
    let heading_4 = document.createElement('th');
    heading_4.innerHTML = "<nobr>non-NF</nobr><br>中位數</br>";


    row_1.appendChild(heading_1);
    row_1.appendChild(heading_2);
    row_1.appendChild(heading_3);
    row_1.appendChild(heading_4);
    thead.appendChild(row_1);


    // Creating and adding data to second row of the table
    let row_2 = document.createElement('tr');
    let row_2_data_1 = document.createElement('td');
    row_2_data_1.innerHTML = "Sea Water<br>海水";
    let row_2_data_2 = document.createElement('td');
    row_2_data_2.innerHTML = decideSeaColor(sea);
    let row_2_data_3 = document.createElement('td');
    row_2_data_3.innerHTML = '<div class ="red"> 0.385</div>';
    let row_2_data_4 = document.createElement('td');
    row_2_data_4.innerHTML = '<div class ="green"> 0.149</div>';


    row_2.appendChild(row_2_data_1);
    row_2.appendChild(row_2_data_2);
    row_2.appendChild(row_2_data_3);
    row_2.appendChild(row_2_data_4);
    tbody.appendChild(row_2);


    // Creating and adding data to second row of the table
    let row_3 = document.createElement('tr');
    let row_3_data_1 = document.createElement('td');
    row_3_data_1.innerHTML = "WBC<br>白血球";
    //WBC正常參考值為70~140mg/dL
    let row_3_data_2 = document.createElement('td');
    row_3_data_2.innerHTML = decideWBCColor(wbc);
    let row_3_data_3 = document.createElement('td');
    row_3_data_3.innerHTML = '<div class ="red"> 14000</div>';
    let row_3_data_4 = document.createElement('td');
    row_3_data_4.innerHTML = '<div class ="green"> 9700</div>';


    row_3.appendChild(row_3_data_1);
    row_3.appendChild(row_3_data_2);
    row_3.appendChild(row_3_data_3);
    row_3.appendChild(row_3_data_4);
    tbody.appendChild(row_3);

    // Creating and adding data to second row of the table
    let row_4 = document.createElement('tr');
    let row_4_data_1 = document.createElement('td');
    row_4_data_1.innerHTML = "CRP<br>C反應蛋白";
    //CRP正常參考值為70~140mg/dL
    let row_4_data_2 = document.createElement('td');
    row_4_data_2.innerHTML = decideCRPColor(crp);
    let row_4_data_3 = document.createElement('td');
    row_4_data_3.innerHTML = '<div class ="red"> 127.37</div>';
    let row_4_data_4 = document.createElement('td');
    row_4_data_4.innerHTML = '<div class ="green"> 29.65</div>';


    row_4.appendChild(row_4_data_1);
    row_4.appendChild(row_4_data_2);
    row_4.appendChild(row_4_data_3);
    row_4.appendChild(row_4_data_4);
    tbody.appendChild(row_4);

    // Creating and adding data to second row of the table
    let row_5 = document.createElement('tr');
    let row_5_data_1 = document.createElement('td');
    row_5_data_1.innerHTML = "SEG<br><nobr>多形核白血球</nobr>";
    //SEG正常參考值為40~70%
    let row_5_data_2 = document.createElement('td');
    row_5_data_2.innerHTML = decideSEGColor(seg);
    let row_5_data_3 = document.createElement('td');
    row_5_data_3.innerHTML = '<div class ="red"> 82.95</div>';
    let row_5_data_4 = document.createElement('td');
    row_5_data_4.innerHTML = '<div class ="green"> 76</div>';


    row_5.appendChild(row_5_data_1);
    row_5.appendChild(row_5_data_2);
    row_5.appendChild(row_5_data_3);
    row_5.appendChild(row_5_data_4);
    tbody.appendChild(row_5);

    // Creating and adding data to second row of the table
    let row_6 = document.createElement('tr');
    let row_6_data_1 = document.createElement('td');
    row_6_data_1.innerHTML = "Band<br>帶狀白血球";
    //Band正常參考值為0~0.5%
    let row_6_data_2 = document.createElement('td');
    row_6_data_2.innerHTML = decideBandColor(band);
    let row_6_data_3 = document.createElement('td');
    row_6_data_3.innerHTML = '<div class ="red"> 0.5</div>';
    let row_6_data_4 = document.createElement('td');
    row_6_data_4.innerHTML = '<div class ="green"> 0</div>';


    row_6.appendChild(row_6_data_1);
    row_6.appendChild(row_6_data_2);
    row_6.appendChild(row_6_data_3);
    row_6.appendChild(row_6_data_4);
    tbody.appendChild(row_6);
}



function decideSeaColor(sea) {
    //Sea Water
    //NF:0.385  non-NF:0.149
    if (sea >= 0.385) {
        //變紅色
        return '<div title ="大於NF平均數" class ="red">' + sea + '</div>';
    }
    else {
        //變綠色
        return '<div title ="小於non-NF平均數" class ="green">' + sea + '</div>';
    }
}

function decideWBCColor(wbc) {
    //WBC
    //NF:14000; non-NF:9700
    if (wbc >= 14000) {
        //變紅色
        return '<div title ="大於NF中位數" class ="red">' + wbc + '</div>';
    }
    else if (wbc <= 9700) {
        //變綠色
        return '<div title ="小於non-NF中位數" class ="green">' + wbc + '</div>';
    }
    else {
        //變黃色
        return '<div title ="介於中間" class ="yellow">' + wbc + '</div>';
    }
}

function decideCRPColor(crp) {
    //CRP
    //NF:127.37; non-NF:29.65
    if (crp >= 127.37) {
        //變紅色
        return '<div title ="大於NF中位數" class ="red">' + crp + '</div>';
    }
    else if (crp <= 29.65) {
        //變綠色
        return '<div title ="小於non-NF中位數" class ="green">' + crp + '</div>';
    }
    else {
        //變黃色
        return '<div title ="介於中間" class ="yellow">' + crp + '</div>';
    }
}

function decideSEGColor(seg) {
    //SEG
    //NF:82.95; non-NF:76
    if (seg >= 82.95) {
        //變紅色
        return '<div title ="大於NF中位數" class ="red">' + seg + '</div>';
    }
    else if (seg <= 76) {
        //變綠色
        return '<div title ="小於non-NF中位數" class ="green">' + seg + '</div>';
    }
    else {
        //變黃色
        return '<div title ="介於中間" class ="yellow">' + seg + '</div>';
    }

}

function decideBandColor(band) {
    //Band
    //NF:0.5; non-NF:0
    if (band >= 0.5) {
        //變紅色
        return '<div title ="大於NF中位數" class ="red">' + band + '</div>';
    }
    else if (band <= 0) {
        //變綠色
        return '<div title ="小於non-NF中位數" class ="green">' + band + '</div>';
    }
    else {
        //變黃色
        return '<div title ="介於中間" class ="yellow">' + band + '</div>';
    }
}

get_data();