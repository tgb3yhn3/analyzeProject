var url = document.URL;
var getvalue = url.split("?")[1];
var id = getvalue.split("=")[1];
//NF按鈕被按下時
function NF_click(element) {
	window.location.replace('https://fhir2-dm5wodoipq-de.a.run.app/NFchoice?id=' + id);
}

//sepsis按鈕被按下時
function sepsis_click(element) {
	window.location.replace('https://fhir2-dm5wodoipq-de.a.run.app/sepsischoice?id=' + id);
}

//back按鈕被按下時
function back_click(element) {
	window.location.replace('https://fhir2-dm5wodoipq-de.a.run.app/patientlist');
}