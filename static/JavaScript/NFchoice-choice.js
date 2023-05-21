var url = document.URL;
var getvalue = url.split("?")[1];
var id = getvalue.split("=")[1];
var sea;

//確認選擇這些模型分析
function sure_click(element) {
	var result = ""
	if (document.getElementById("choice" + 1).checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice" + 2).checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice" + 3).checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice" + 4).checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("choice" + 5).checked) {
		result += "T";
	}
	else {
		result += "F";
	}
	if (document.getElementById("sea").checked) {
		sea = 1;
	}
	else {
		sea = 0;
	}
	window.location.replace('http://localhost:5001/NF?id=' + id + "&method=" + result + "&sea=" + sea);
}

//返回至病人資料頁
function back_click(element) {
	window.location.replace('http://localhost:5001/patientprofile?id=' + id);
}