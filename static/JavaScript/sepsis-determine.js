function getResult(scoreOfqSOFA, lastScore, infusion, MAP, Lactate) {
    if (scoreOfSOFA - lastScore >= 2 && scoreOfSOFA > lastScore) {
        if (infusion > 0 && MAP >= 65 && Lactate > 2) {
            return document.getElementById("hint").textContent = "SOFA總分為" + scoreOfSOFA + "分，因上一次SOFA值為" + lastScore + "分，診斷敗血性休克";
        }
        else {
            return document.getElementById("hint").textContent = "SOFA總分為" + scoreOfSOFA + "分，因上一次SOFA值為" + lastScore + "分，診斷為敗血症";
        }
    }
    else {
        return document.getElementById("hint").textContent = "SOFA總分為" + scoreOfSOFA + "分，因上一次SOFA值為" + lastScore + " 分，沒有大幅增加。評估臨床狀況，若臨床必要時再評估敗血症可能。";
    }
}

//計算qSOFA值
function caculateqSOFA(respiratoryRate, consciousness, systolicPressure) {
    var scoreOfqSOFA = 0;
    if (respiratoryRate > 22) {
        scoreOfqSOFA++;
    }
    if (consciousness < 100) {
        scoreOfqSOFA++;
    }
    if (systolicPressure <= 100) {
        scoreOfqSOFA++;
    }
    return scoreOfqSOFA;
}

//計算SOFA值
function caculateSOFA(PFratio, respirator, Platelet, Bilirubin, MAP, Dopamine, epinephrine, norepinephrine, Dobutamine, ComaScale, Creatinine, urineVolume) {
    var scoreRespiratory;
    var scoreCoagulation;
    var scoreLiver;
    var scoreCirculatory;
    var scoreCentralNervousSystem;
    var scoreRenal;
    var scoreOfSOFA = 0;
    //肺
    if (PFratio < 100 && respirator == 1)
        scoreRespiratory = 4;
    else if (PFratio < 200 && respirator == 1)
        scoreRespiratory = 3;
    else if (PFratio < 300)
        scoreRespiratory = 2;
    else if (PFratio < 400)
        scoreRespiratory = 1;
    else    //PFratio>=400
        scoreRespiratory = 0;
    //血
    if (Platelet < 20)
        scoreCoagulation = 4;
    else if (Platelet < 50)
        scoreCoagulation = 3;
    else if (Platelet < 100)
        scoreCoagulation = 2;
    else if (Platelet < 150)
        scoreCoagulation = 1;
    else    //Platelet>=150
        scoreCoagulation = 0;
    //肝
    if (Bilirubin > 12)
        scoreLiver = 4;
    else if (Bilirubin >= 6.0 && Bilirubin <= 11.9)
        scoreLiver = 3;
    else if (Bilirubin >= 2.0 && Bilirubin <= 5.9)
        scoreLiver = 2;
    else if (Bilirubin >= 1.2 && Bilirubin <= 1.9)
        scoreLiver = 1;
    else    //Bilirubin<1.2
        scoreLiver = 0;
    //心
    if (Dopamine > 15 || epinephrine > 0.1 || norepinephrine > 0.1)
        scoreCirculatory = 4;
    else if (Dopamine >= 5 || epinephrine > 0 || norepinephrine > 0)
        scoreCirculatory = 3;
    else if (Dopamine > 0 || Dobutamine == 1)
        scoreCirculatory = 2;
    else if (MAP < 70)
        scoreCirculatory = 1;
    else    //MAP>=70
        scoreCirculatory = 0;
    //神
    if (ComaScale < 6)
        scoreCentralNervousSystem = 4;
    else if (ComaScale >= 6 && ComaScale <= 9)
        scoreCentralNervousSystem = 3;
    else if (ComaScale >= 10 && ComaScale <= 12)
        scoreCentralNervousSystem = 2;
    else if (ComaScale >= 13 && ComaScale <= 14)
        scoreCentralNervousSystem = 1;
    else    //ComaScale=15
        scoreCentralNervousSystem = 0;
    //腎
    if (Creatinine > 5.0 || urineVolume < 200)
        scoreRenal = 4;
    else if ((Creatinine >= 3.5 && Creatinine <= 4.9) || urineVolume < 500)
        scoreRenal = 3;
    else if (Creatinine >= 2.0 && Creatinine <= 3.4)
        scoreRenal = 2;
    else if (Creatinine >= 1.2 && Creatinine <= 1.9)
        scoreRenal = 1;
    else    //Creatinine<12
        scoreRenal = 0;

    scoreOfSOFA = scoreRespiratory + scoreCoagulation + scoreLiver
        + scoreCirculatory + scoreCentralNervousSystem + scoreRenal;

    var myArray = new Array(7);
    myArray[0] = scoreOfSOFA;
    myArray[1] = scoreRespiratory;
    myArray[2] = scoreCoagulation;
    myArray[3] = scoreLiver;
    myArray[4] = scoreCirculatory;
    myArray[5] = scoreCentralNervousSystem;
    myArray[6] = scoreRenal;
    return myArray;
}