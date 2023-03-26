var url = document.URL;
var getvalue = url.split("?")[1];
var id = getvalue.split("&")[0].split("=")[1];
var TTTTT = getvalue.split("&")[1].split("=")[1];
var token_fhir
var data1
var data2
var data3
var model_index = ["randomForest", 'logisticregression', "supportVectorMachine"];
var score_index = ["randomForest_proba", 'logisticregression_proba', "supportVectorMachine_proba"];

//Sepsis function
//需要抓的資料
//qSOFA變數
var respiratoryRate;                //呼吸(>=22/分)
var consciousness;                  //意識改變(非滿分就算<100)
var systolicPressure;               //收縮壓(<=100,(mmHg))
//SOFA變數
var PF_ratio;                        //呼吸(PaO2/FiO2 ratio,(mmHg))
var respirator = new Boolean(false);//呼吸器 
var Platelet;                       //凝血(血小板*10^3/uL)               
var Bilirubin;                      //肝臟(膽紅素,(mg/dL))                       
var MAP;                            //心血管(平均動脈壓,(mmHg))                        
var Dopamine;                       //心血管(多巴胺,(ug/kg/min))                     
var epinephrine;                    //心血管(腎上腺素)                  
var norepinephrine;                 //心血管(去甲基腎上腺素,(ug/kg/min))    
var Dobutamine = new Boolean(false);//心血管(多保他命)         
var ComaScale;                      //中樞神經(昏迷指數)                    
var Creatinine;                     //腎臟(肌酸酐,mg/dL)          
var urineVolume;                    //腎臟(尿量,mL/day)         
//上一次的SOFA值
var lastSOFA;                       //old                
//判斷是否敗血性休克
var infusion;                       //敗血性休克(判斷是否輸液)
var Lactate;                        //敗血性休克(血中乳酸,(mmole/L))

//變數接收方法回傳的值
//qSOFA值
var scoreOfqSOFA
// var scoreOfqSOFA = caculateqSOFA(33, 100, 100);

//SOFA值 -new
var SOFA;
var SOFA_wei = new Array();
var scoreOfSOFA;
// var SOFA = caculateSOFA(500, 100, 1, 50, 100, 0, 50, 50, 50, 15, 1, 50);

//sepsis_predict
var gcs
var meds_ams15b
var meds_plt150b
var bun
var FIO2_percent

//主程式判斷(最後結果)
var result;

var CirculatoryColor, RenalColor;

async function get_data() {
    var result1 = await getToken_fhir().then((res1) => {
        token_fhir = res1;
    });
    var result2 = await getObservationById(token_fhir, id).then((res2) => {
        data1 = res2;
    })
    var result3 = await getPatientById(token_fhir, id).then((res3) => {
        data2 = res3;
    })
    for (var i = 0; i < data1.entry.length; i++) {
        var data_text = data1.entry[i].resource.code.text;
        if (data_text == 'Respiratory rate') {
            respiratoryRate = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Level of consciousness') {
            consciousness = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Blood Pressure') {
            systolicPressure = data1.entry[i].resource.component[1].valueQuantity.value;
        }
        if (data_text == 'PFratio') {
            PF_ratio = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Platelets in Blood') {
            Platelet = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Bilirubin.total in Serum or Plasma') {
            Bilirubin = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Mean blood pressure') {
            MAP = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'DOPamine in Serum or Plasma') {
            Dopamine = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'EPINEPHrine in Urine') {
            epinephrine = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Norepinephrine in Urine') {
            norepinephrine = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Dobutamine in Serum or Plasma') {
            Dobutamine = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Glasgow coma score total') {
            ComaScale = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Creatinine in Serum or Plasma') {
            Creatinine = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Urine output 24 hour') {
            urineVolume = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'SOFA Total Score') {
            lastSOFA = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Infusion') {
            infusion = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Lactate in Serum or Plasma') {
            Lactate = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'Glasgow coma score total') {
            gcs = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'bun') {
            bun = data1.entry[i].resource.valueQuantity.value;
        }
        if (data_text == 'FIO2_percent') {
            FIO2_percent = data1.entry[i].resource.valueQuantity.value;
        }
        if (gcs < 15) {
            meds_ams15b = 2
        }
        else {
            meds_ams15b = 0
        }
        if (Platelet < 150) {
            meds_plt150b = 3
        }
        else {
            meds_plt150b = 0
        }
    }
    for (var i = 0; i < data2.extension.length; i++) {
        if (data2.extension[i].url == 'Respiratory mask') {
            respirator = data2.extension[i].valueDecimal;
        }
    }

    scoreOfqSOFA = caculateqSOFA(respiratoryRate, consciousness, systolicPressure)
    SOFA = caculateSOFA(PF_ratio, respirator, Platelet, Bilirubin, MAP, Dopamine, epinephrine, norepinephrine, Dobutamine, ComaScale, Creatinine, urineVolume);
    scoreOfSOFA = SOFA[0];

    //判斷結果
    result = getResult(scoreOfqSOFA, lastSOFA, infusion, MAP, Lactate);

    sepsisChangeColor(SOFA[1], SOFA[2], SOFA[3], SOFA[4], SOFA[5], SOFA[6]);

    var result4 = await getModelResult_sepsis(gcs, meds_ams15b, meds_plt150b, sofa_res = SOFA[1], sofa_ner = SOFA[5], sofa_liver = SOFA[3],
        sofa_coag = SOFA[2], sofa_renal = SOFA[6], bun, cre = Creatinine, plt = Platelet, FIO2_percent, PF_ratio, fio2_per = FIO2_percent * 100, fio2_cb = FIO2_percent * 100).then((res4) => {
            data3 = res4;
            //確認選擇哪些模型呈現分析
            for (var i = 0; i < TTTTT.length; i++) {
                var Yes_No
                if (data3[model_index[i]] == 1) {
                    Yes_No = true;
                }
                else {
                    Yes_No = false;
                }
                if (TTTTT[i] == "T") {
                    document.getElementById(score_index[i] + "_s").innerHTML = "信心度 " + data3[score_index[i]] + "%"
                    if (Yes_No) {
                        document.getElementById("choice" + (i + 2) + "-1_s").style.border = "medium solid red"
                        document.getElementById("choice" + (i + 2) + "-2_s").innerHTML = "判定為 Sepsis";
                    }
                    else {
                        document.getElementById("choice" + (i + 2) + "-1_s").style.border = "medium solid green"
                        document.getElementById("choice" + (i + 2) + "-2_s").innerHTML = "判定為 non-Sepsis";
                    }
                }
                else if (TTTTT[i] == "F") {
                    document.getElementById("choice" + (i + 2) + "_s").style.display = "none";
                }
            }
        })

    var RespiratoryColor = textColor('Respiratory', PF_ratio, respirator);
    document.getElementById(RespiratoryColor.id).className = RespiratoryColor.class;
    document.getElementById(RespiratoryColor.id).title = RespiratoryColor.value;

    var CoagulationColor = textColor('Coagulation', Platelet);
    document.getElementById(CoagulationColor.id).className = CoagulationColor.class;
    document.getElementById(CoagulationColor.id).title = CoagulationColor.value;

    var LiverColor = textColor('Liver', Bilirubin);
    document.getElementById(LiverColor.id).className = LiverColor.class;
    document.getElementById(LiverColor.id).title = LiverColor.value;

    CirculatoryColor = textColor('Circulatory', Dopamine, epinephrine, norepinephrine, Dobutamine, MAP);
    for (var i = 0; i < CirculatoryColor.length; i++) {
        document.getElementById(CirculatoryColor[i].id).className = CirculatoryColor[i].class;
        document.getElementById(CirculatoryColor[i].id).title = CirculatoryColor[i].value;
    }

    var CentralNervousSystemColor = textColor('CentralNervousSystem', ComaScale);
    document.getElementById(CentralNervousSystemColor.id).className = CentralNervousSystemColor.class;
    document.getElementById(CentralNervousSystemColor.id).title = CentralNervousSystemColor.value;

    RenalColor = textColor('Renal', Creatinine, urineVolume);
    for (var i = 0; i < RenalColor.length; i++) {
        document.getElementById(RenalColor[i].id).className = RenalColor[i].class;
        document.getElementById(RenalColor[i].id).title = RenalColor[i].value;
    }

    SOFA_wei.push(RespiratoryColor.id[RespiratoryColor.id.length - 1]);
    SOFA_wei.push(CoagulationColor.id[CoagulationColor.id.length - 1]);
    SOFA_wei.push(LiverColor.id[LiverColor.id.length - 1]);
    SOFA_wei.push(CirculatoryColor[0].id[CirculatoryColor[0].id.length - 1]);
    SOFA_wei.push(CentralNervousSystemColor.id[CentralNervousSystemColor.id.length - 1]);
    SOFA_wei.push(RenalColor[0].id[RenalColor[0].id.length - 1]);

    document.getElementById("sepans1").innerHTML = PF_ratio;
    document.getElementById("sepans1").className = RespiratoryColor.class;
    document.getElementById("sepans2").innerHTML = Platelet;
    document.getElementById("sepans2").className = CoagulationColor.class;
    document.getElementById("sepans3").innerHTML = Bilirubin;
    document.getElementById("sepans3").className = LiverColor.class;
    document.getElementById("sepans4_0").innerHTML = "平均動脈壓 "+MAP
    document.getElementById("sepans4_1").innerHTML ="Dopamine "+ Dopamine
    document.getElementById("sepans4_2").innerHTML ="epinephrine "+epinephrine
    document.getElementById("sepans4_3").innerHTML = "norepinephrine "+norepinephrine
    for (var i = 0; i < CirculatoryColor.length; i++) {
        try {
            document.getElementById(CirculatoryColor[i].idc).className = CirculatoryColor[i].class;
        } catch (error) {
        }
    }
    document.getElementById("sepans5").innerHTML = ComaScale;
    document.getElementById("sepans5").className = CentralNervousSystemColor.class;
    document.getElementById("sepans6").innerHTML = Creatinine;
    document.getElementById("sepans7").innerHTML = urineVolume;
    for (var i = 0; i < RenalColor.length; i++) {
        try {
            document.getElementById(RenalColor[i].idc).className = RenalColor[i].class;
        } catch (error) {
        }
    }
};

//表格資料
function sheet() {
    let table = document.createElement('table');
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');

    table.appendChild(thead);
    table.appendChild(tbody);

    // Adding the entire table to the body tag
    document.getElementById('sheet').appendChild(table);

    let row_1 = document.createElement('tr');
    let head_1 = document.createElement('th');
    head_1.innerHTML = "系統／分數";
    let head_0 = document.createElement('th');
    head_0.innerHTML = '<div>詳細數值</div>';
    let head_2 = document.createElement('th');
    head_2.innerHTML = '<div class ="sep_green">0</div>';
    let head_3 = document.createElement('th');
    head_3.innerHTML = '<div class ="sep_yellow">1</div>';
    let head_4 = document.createElement('th');
    head_4.innerHTML = '<div class ="sep_orange">2</div>';
    let head_5 = document.createElement('th');
    head_5.innerHTML = '<div class ="sep_red">3</div>';
    let head_6 = document.createElement('th');
    head_6.innerHTML = '<div class ="sep_purple">4</div>';


    row_1.appendChild(head_1);
    row_1.appendChild(head_0);
    row_1.appendChild(head_2);
    row_1.appendChild(head_3);
    row_1.appendChild(head_4);
    row_1.appendChild(head_5);
    row_1.appendChild(head_6);
    thead.appendChild(row_1);


    // Creating and adding data to second row of the table
    let row_2 = document.createElement('tr');
    let row_2_data_1 = document.createElement('td');
    row_2_data_1.innerHTML = "呼吸PaO<sub>2</sub>/FiO<sub>2</sub>，<br>mmHg";
    let row_2_data_0 = document.createElement('td');
    row_2_data_0.innerHTML = "<div data-resource-type='PFratio' id=sepans1></div>";
    let row_2_data_2 = document.createElement('td');
    row_2_data_2.innerHTML = "<div id=Respiratory_0>≧ 400</div>";
    let row_2_data_3 = document.createElement('td');
    row_2_data_3.innerHTML = "<div id=Respiratory_1>＜ 400</div>";
    let row_2_data_4 = document.createElement('td');
    row_2_data_4.innerHTML = "<div id=Respiratory_2>＜ 300</div>";
    let row_2_data_5 = document.createElement('td');
    row_2_data_5.innerHTML = "<div id=Respiratory_3>＜ 200<br>並使用呼吸器</div>";
    let row_2_data_6 = document.createElement('td');
    row_2_data_6.innerHTML = "<div id=Respiratory_4>＜ 100<br>並使用呼吸器</div>";


    row_2.appendChild(row_2_data_1);
    row_2.appendChild(row_2_data_0);
    row_2.appendChild(row_2_data_2);
    row_2.appendChild(row_2_data_3);
    row_2.appendChild(row_2_data_4);
    row_2.appendChild(row_2_data_5);
    row_2.appendChild(row_2_data_6);
    tbody.appendChild(row_2);


    // Creating and adding data to third row of the table
    let row_3 = document.createElement('tr');
    let row_3_data_1 = document.createElement('td');
    row_3_data_1.innerHTML = "凝血<br>血小板 ×10<sup>3</sup>3/uL";
    let row_3_data_0 = document.createElement('td');
    row_3_data_0.innerHTML = "<div data-resource-type='Platelets in Blood' id=sepans2></div>";
    let row_3_data_2 = document.createElement('td');
    row_3_data_2.innerHTML = "<div id=Coagulation_0>≧ 150</div>";
    let row_3_data_3 = document.createElement('td');
    row_3_data_3.innerHTML = "<div id=Coagulation_1>＜ 150</div>";
    let row_3_data_4 = document.createElement('td');
    row_3_data_4.innerHTML = "<div id=Coagulation_2>＜ 100</div>";
    let row_3_data_5 = document.createElement('td');
    row_3_data_5.innerHTML = "<div id=Coagulation_3>＜ 50</div>";
    let row_3_data_6 = document.createElement('td');
    row_3_data_6.innerHTML = "<div id=Coagulation_4>＜ 20</div>";


    row_3.appendChild(row_3_data_1);
    row_3.appendChild(row_3_data_0);
    row_3.appendChild(row_3_data_2);
    row_3.appendChild(row_3_data_3);
    row_3.appendChild(row_3_data_4);
    row_3.appendChild(row_3_data_5);
    row_3.appendChild(row_3_data_6);
    tbody.appendChild(row_3);

    // Creating and adding data to forth row of the table
    let row_4 = document.createElement('tr');
    let row_4_data_1 = document.createElement('td');
    row_4_data_1.innerHTML = "肝臟<br>膽紅素，mg/dL";
    let row_4_data_0 = document.createElement('td');
    row_4_data_0.innerHTML = "<div data-resource-type='Bilirubin.total in Serum or Plasma' id=sepans3></div>";
    let row_4_data_2 = document.createElement('td');
    row_4_data_2.innerHTML = "<div id=Liver_0>＜ 1.2</div>";
    let row_4_data_3 = document.createElement('td');
    row_4_data_3.innerHTML = "<div id=Liver_1>1.2-1.9</div>";
    let row_4_data_4 = document.createElement('td');
    row_4_data_4.innerHTML = "<div id=Liver_2>2.0-5.9</div>";
    let row_4_data_5 = document.createElement('td');
    row_4_data_5.innerHTML = "<div id=Liver_3>6.0-11.9</div>";
    let row_4_data_6 = document.createElement('td');
    row_4_data_6.innerHTML = "<div id=Liver_4>＞ 12</div>";


    row_4.appendChild(row_4_data_1);
    row_4.appendChild(row_4_data_0);
    row_4.appendChild(row_4_data_2);
    row_4.appendChild(row_4_data_3);
    row_4.appendChild(row_4_data_4);
    row_4.appendChild(row_4_data_5);
    row_4.appendChild(row_4_data_6);
    tbody.appendChild(row_4);

    // 第五列表格
    let row_5 = document.createElement('tr');
    let row_5_data_1 = document.createElement('td');
    row_5_data_1.innerHTML = "心血管";
    let row_5_data_0 = document.createElement('td');
    row_5_data_0.innerHTML = "<div id=sepans4></div>";
    let row_5_data_0_1 = document.createElement('div');
    row_5_data_0_1.innerHTML="    <div data-resource-type='Mean blood pressure' data-resource-prefix='平均動脈壓 ' id=sepans4_0> "  + 
    "</div><div data-resource-type='DOPamine in Serum or Plasma' data-resource-prefix='Dopamine ' id=sepans4_1> " + 
    "</div><div data-resource-type='EPINEPHrine in Urine'  data-resource-prefix='epinephrine ' id=sepans4_2> "  + 
    "</div><div data-resource-type='Norepinephrine in Urine' data-resource-prefix='norepinephrine ' id=sepans4_3> "  + "</div>";
    row_5_data_0.appendChild(row_5_data_0_1)
    let row_5_data_2 = document.createElement('td');
    row_5_data_2.innerHTML = "<div id=Map_0 style=\"white-space: pre;\">平均動脈壓<br>≧ 70mmHg</div>";
    let row_5_data_3 = document.createElement('td');
    row_5_data_3.innerHTML = "<div id=Map_1 style=\"white-space: pre;\">平均動脈壓<br>＜ 70mmHg</div>";
    let row_5_data_4 = document.createElement('td');
    row_5_data_4.innerHTML = "<div id=Dopamine_2 style=\"white-space: pre;\">Dopamine＜5</div>或<div id=Dobutamine_2 style=\"white-space: pre;\">任何dobutamine</div>";
    let row_5_data_5 = document.createElement('td');
    row_5_data_5.innerHTML = "<div id=Dopamine_3 style=\"white-space: pre;\">Dopamine 5.1-15</div>或<div id=epinephrine_3 style=\"white-space: pre;\">epinephrine ≦ 0.1</div>或<div id=norepinephrine_3 style=\"white-space: pre;\">norepinephrine ≦ 0.1</div>";
    let row_5_data_6 = document.createElement('td');
    row_5_data_6.innerHTML = "<div id=Dopamine_4 style=\"white-space: pre;\">Dopamine＞15</div>或<div id=epinephrine_4 style=\"white-space: pre;\">epinephrine＞0.1</div>或<div id=norepinephrine_4 style=\"white-space: pre;\">norepinephrine＞0.1</div>";


    row_5.appendChild(row_5_data_1);
    row_5.appendChild(row_5_data_0);
    row_5.appendChild(row_5_data_2);
    row_5.appendChild(row_5_data_3);
    row_5.appendChild(row_5_data_4);
    row_5.appendChild(row_5_data_5);
    row_5.appendChild(row_5_data_6);
    tbody.appendChild(row_5);

    let row_6 = document.createElement('tr');
    let row_6_data_1 = document.createElement('td');
    row_6_data_1.innerHTML = "中樞神經<br>昏迷指數";
    let row_6_data_0 = document.createElement('td');
    row_6_data_0.innerHTML = "<div data-resource-type='Glasgow coma score total' id=sepans5></div>";
    let row_6_data_2 = document.createElement('td');
    row_6_data_2.innerHTML = "<div id=CentralNervousSystem_0>15</div>";
    let row_6_data_3 = document.createElement('td');
    row_6_data_3.innerHTML = "<div id=CentralNervousSystem_1>13-14</div>";
    let row_6_data_4 = document.createElement('td');
    row_6_data_4.innerHTML = "<div id=CentralNervousSystem_2>10-12</div>";
    let row_6_data_5 = document.createElement('td');
    row_6_data_5.innerHTML = "<div id=CentralNervousSystem_3>6-9</div>";
    let row_6_data_6 = document.createElement('td');
    row_6_data_6.innerHTML = "<div id=CentralNervousSystem_4>＜ 6</div>";


    row_6.appendChild(row_6_data_1);
    row_6.appendChild(row_6_data_0);
    row_6.appendChild(row_6_data_2);
    row_6.appendChild(row_6_data_3);
    row_6.appendChild(row_6_data_4);
    row_6.appendChild(row_6_data_5);
    row_6.appendChild(row_6_data_6);
    tbody.appendChild(row_6);

    let row_7 = document.createElement('tr');
    let row_7_data_1 = document.createElement('td');
    row_7_data_1.innerHTML = "<div style=\"white-space: pre;\">腎臟<br>Creatinine,mg/dL</div>";
    
    let row_7_data_0 = document.createElement('td');
    row_7_data_0.innerHTML = "<div data-resource-type='Creatinine in Serum or Plasma' id=sepans6></div>";
    let row_7_data_2 = document.createElement('td');
    row_7_data_2.innerHTML = "<div id=Renal_0>＜ 1.2</div>";
    let row_7_data_3 = document.createElement('td');
    row_7_data_3.innerHTML = "<div id=Renal_1>1.2-1.9</div>";
    let row_7_data_4 = document.createElement('td');
    row_7_data_4.innerHTML = "<div id=Renal_2>2.0-3.4</div>";
    let row_7_data_5 = document.createElement('td');
    row_7_data_5.innerHTML = "<div id=Renal_3>3.5-4.9</div>";
    let row_7_data_6 = document.createElement('td');
    row_7_data_6.innerHTML = "<div id=Renal_4>＞ 5.0</div>";


    row_7.appendChild(row_7_data_1);
    row_7.appendChild(row_7_data_0);
    row_7.appendChild(row_7_data_2);
    row_7.appendChild(row_7_data_3);
    row_7.appendChild(row_7_data_4);
    row_7.appendChild(row_7_data_5);
    row_7.appendChild(row_7_data_6);
    tbody.appendChild(row_7);

    let row_8 = document.createElement('tr');
    let row_8_data_1 = document.createElement('td');
    row_8_data_1.innerHTML = "<div style=\"white-space: pre;\">腎臟<br>小便量，mL/day</div>";
    let row_8_data_0 = document.createElement('td');
    row_8_data_0.innerHTML = "<div data-resource-type='Urine output 24 hour' id=sepans7></div>";
    let row_8_data_2 = document.createElement('td');
    row_8_data_2.innerHTML = "";
    let row_8_data_3 = document.createElement('td');
    row_8_data_3.innerHTML = "";
    let row_8_data_4 = document.createElement('td');
    row_8_data_4.innerHTML = "";
    let row_8_data_5 = document.createElement('td');
    row_8_data_5.innerHTML = "<div id=urineVolume_3>200-500</div>";
    let row_8_data_6 = document.createElement('td');
    row_8_data_6.innerHTML = "<div id=urineVolume_4>＜ 200</div>";


    row_8.appendChild(row_8_data_1);
    row_8.appendChild(row_8_data_0);
    row_8.appendChild(row_8_data_2);
    row_8.appendChild(row_8_data_3);
    row_8.appendChild(row_8_data_4);
    row_8.appendChild(row_8_data_5);
    row_8.appendChild(row_8_data_6);
    tbody.appendChild(row_8);
}

//返回至病人資料頁
function back_click(element) {
    window.location.replace('http://localhost:5000/sepsischoice?id=' + id);
}

function backlist(element) {
    window.location.replace('http://localhost:5000/patientlist');
}

get_data();
sheet();
$(document).ready(()=>{
    console.log("in")
    for(let i=1;i<=7;i++){
        console.log(i)
        if(i==4){
          
            for(let j=0;j<4;j++){
                let now=String(i)+"_"+String(j)
                console.log("sepans"+now)
                document.getElementById("sepans"+now).addEventListener('click',()=>{
                    let resourceType=document.getElementById("sepans"+now).getAttribute("data-resource-type")
                     update_Observation("請輸入更新數值",resourceType,document.getElementById("sepans"+now).getAttribute("data-resource-prefix"),"sepans"+now,false)
                })
            }
            continue
        }
        let now=String(i)
        document.getElementById("sepans"+now).addEventListener('click',()=>{
            let resourceType=document.getElementById("sepans"+now).getAttribute("data-resource-type")
             update_Observation("請輸入更新數值",resourceType,"","sepans"+now)
        })
    }
})