var url = document.URL;
var getvalue = url.split("?")[1];
var id = getvalue.split("=")[1];

//確認選擇這些模型分析
function sure_click(element) {
	var result = ""
	if (document.getElementById("choice1_s").checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice2_s").checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice3_s").checked) {
		result += "T";
	}
	else {
		result += "F";
	}

	window.location.replace('http://localhost:5000/sepsis?id=' + id + "&method=" + result);
}

//返回至病人資料頁
function back_click(element) {
	window.location.replace('http://localhost:5000/patientprofile?id=' + id);
}