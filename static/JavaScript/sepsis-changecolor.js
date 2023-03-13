function sepsisChangeColor(Respiratory, Coagulation, Liver, Circulatory, CentralNervousSystem, Renal) {
	var color1 = 'rgb(37, 186, 82)';
	var color2 = 'rgb(252, 237, 37)';
	var color3 = 'rgb(240, 137, 48)';
	var color4 = 'rgb(187, 44, 8)';
	var color5 = 'rgb(109, 0, 136)';
	var id1 = 'lung'
	var id2 = 'blood'
	var id3 = 'liver'
	var id4 = 'heart'
	var id5 = 'brain'
	var id6 = 'kidney'
	switch (Respiratory) {
		case 0: {
			document.getElementById(id1).style.fill = color1;
			document.getElementById(id1).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id1).style.fill = color2;
			document.getElementById(id1).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id1).style.fill = color3;
			document.getElementById(id1).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id1).style.fill = color4;
			document.getElementById(id1).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id1).style.fill = color5;
			document.getElementById(id1).style.stroke = color5;
			break;
		}
	}

	switch (Coagulation) {
		case 0: {
			document.getElementById(id2).style.fill = color1;
			document.getElementById(id2).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id2).style.fill = color2;
			document.getElementById(id2).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id2).style.fill = color3;
			document.getElementById(id2).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id2).style.fill = color4;
			document.getElementById(id2).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id2).style.fill = color5;
			document.getElementById(id2).style.stroke = color5;
			break;
		}
	}

	switch (Liver) {
		case 0: {
			document.getElementById(id3).style.fill = color1;
			document.getElementById(id3).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id3).style.fill = color2;
			document.getElementById(id3).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id3).style.fill = color3;
			document.getElementById(id3).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id3).style.fill = color4;
			document.getElementById(id3).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id3).style.fill = color5;
			document.getElementById(id3).style.stroke = color5;
			break;
		}
	}

	switch (Circulatory) {
		case 0: {
			document.getElementById(id4).style.fill = color1;
			document.getElementById(id4).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id4).style.fill = color2;
			document.getElementById(id4).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id4).style.fill = color3;
			document.getElementById(id4).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id4).style.fill = color4;
			document.getElementById(id4).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id4).style.fill = color5;
			document.getElementById(id4).style.stroke = color5;
			break;
		}
	}

	switch (CentralNervousSystem) {
		case 0: {
			document.getElementById(id5).style.fill = color1;
			document.getElementById(id5).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id5).style.fill = color2;
			document.getElementById(id5).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id5).style.fill = color3;
			document.getElementById(id5).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id5).style.fill = color4;
			document.getElementById(id5).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id5).style.fill = color5;
			document.getElementById(id5).style.stroke = color5;
			break;
		}
	}

	switch (Renal) {
		case 0: {
			document.getElementById(id6).style.fill = color1;
			document.getElementById(id6).style.stroke = color1;
			break;
		}
		case 1: {
			document.getElementById(id6).style.fill = color2;
			document.getElementById(id6).style.stroke = color2;
			break;
		}
		case 2: {
			document.getElementById(id6).style.fill = color3;
			document.getElementById(id6).style.stroke = color3;
			break;
		}
		case 3: {
			document.getElementById(id6).style.fill = color4;
			document.getElementById(id6).style.stroke = color4;
			break;
		}
		case 4: {
			document.getElementById(id6).style.fill = color5;
			document.getElementById(id6).style.stroke = color5;
			break;
		}
	}
}

function textColor(text = '', value1 = 0, value2 = 0, value3 = 0, value4 = 0, value5 = 0) {
	switch (text) {
		case 'Respiratory': {
			if (value1 < 100 && value2 == 1) {
				return { id: 'Respiratory_4', class: 'sep_purple', value: value1 + ', 使用呼吸器' }
			}
			else if (value1 < 200 && value2 == 1) {
				return { id: 'Respiratory_3', class: 'sep_red', value: value1 + ', 使用呼吸器' }
			}
			else if (value1 < 300) {
				return { id: 'Respiratory_2', class: 'sep_orange', value: value1 }
			}
			else if (value1 < 400) {
				return { id: 'Respiratory_1', class: 'sep_yellow', value: value1 }
			}
			else {//>=400
				return { id: 'Respiratory_0', class: 'sep_green', value: value1 }
			}
			break;
		}
		case 'Coagulation': {
			if (value1 < 20) {
				return { id: 'Coagulation_4', class: 'sep_purple', value: value1 }
			}
			else if (value1 < 50) {
				return { id: 'Coagulation_3', class: 'sep_red', value: value1 }
			}
			else if (value1 < 100) {
				return { id: 'Coagulation_2', class: 'sep_orange', value: value1 }
			}
			else if (value1 < 150) {
				return { id: 'Coagulation_1', class: 'sep_yellow', value: value1 }
			}
			else {//>=150
				return { id: 'Coagulation_0', class: 'sep_green', value: value1 }
			}
			break;
		}
		case 'Liver': {
			if (value1 > 12) {
				return { id: 'Liver_4', class: 'sep_purple', value: value1 }
			}
			else if (value1 < 1.2) {
				return { id: 'Liver_0', class: 'sep_green', value: value1 }
			}
			else if (value1 < 2) {
				return { id: 'Liver_1', class: 'sep_yellow', value: value1 }
			}
			else if (value1 < 6) {
				return { id: 'Liver_2', class: 'sep_orange', value: value1 }
			}
			else {//6<=x<=12
				return { id: 'Liver_3', class: 'sep_red', value: value1 }
			}
			break;
		}
		case 'Circulatory': {// Dopamine, epinephrine, norepinephrine, Dobutamine, Map
			var returnArray = new Array();
			if (value1 > 15 || value2 > 0.1 || value3 > 0.1) {
				if (value1 > 15) {
					returnArray.push({ id: 'Dopamine_4', class: 'sep_purple', value: value1, idc: 'sepans4_1' });
				}
				if (value2 > 0.1) {
					returnArray.push({ id: 'epinephrine_4', class: 'sep_purple', value: value2, idc: 'sepans4_2' });
				}
				if (value3 > 0.1) {
					returnArray.push({ id: 'norepinephrine_4', class: 'sep_purple', value: value3, idc: 'sepans4_3' });
				}
			}
			else if (value1 >= 5 || value2 > 0 || value3 > 0) {
				if (value1 >= 5) {
					returnArray.push({ id: 'Dopamine_3', class: 'sep_red', value: value1, idc: 'sepans4_1' });
				}
				if (value2 > 0) {
					returnArray.push({ id: 'epinephrine_3', class: 'sep_red', value: value2, idc: 'sepans4_2' });
				}
				if (value3 > 0) {
					returnArray.push({ id: 'norepinephrine_3', class: 'sep_red', value: value3, idc: 'sepans4_3' });
				}
			}
			else if (value1 > 0 || value4 == 1) {
				if (value1 > 0) {
					returnArray.push({ id: 'Dopamine_2', class: 'sep_orange', value: value1, idc: 'sepans4_1' });
				}
				if (value4 == 1) {
					returnArray.push({ id: 'Dobutamine_2', class: 'sep_orange', value: value4 });
				}
			}
			else if (value5 < 70) {
				returnArray.push({ id: 'Map_1', class: 'sep_yellow', value: value5, idc: 'sepans4_0' });
			}
			else {
				returnArray.push({ id: 'Map_0', class: 'sep_green', value: value5, idc: 'sepans4_0' });
			}
			return returnArray;
			break;
		}
		case 'CentralNervousSystem': {
			if (value1 < 6) {
				return { id: 'CentralNervousSystem_4', class: 'sep_purple', value: value1 }
			}
			else if (value1 <= 9) {
				return { id: 'CentralNervousSystem_3', class: 'sep_red', value: value1 }
			}
			else if (value1 <= 12) {
				return { id: 'CentralNervousSystem_2', class: 'sep_orange', value: value1 }
			}
			else if (value1 <= 14) {
				return { id: 'CentralNervousSystem_1', class: 'sep_yellow', value: value1 }
			}
			else {//=15
				return { id: 'CentralNervousSystem_0', class: 'sep_green', value: value1 }
			}
			break;
		}
		case 'Renal': {
			var returnArray = new Array();
			if (value1 >= 5 || value2 < 200) {
				if (value2 < 200) {
					returnArray.push({ id: 'urineVolume_4', class: 'sep_purple', value: value2, idc: 'sepans7' })
				}
				if (value1 >= 5) {
					returnArray.push({ id: 'Renal_4', class: 'sep_purple', value: value1, idc: 'sepans6' })
				}
			}
			else if (value1 >= 3.5 || value2 < 500) {
				if (value2 < 500) {
					returnArray.push({ id: 'urineVolume_3', class: 'sep_red', value: value2, idc: 'sepans7' })
				}
				if (value1 >= 3.5) {
					returnArray.push({ id: 'Renal_3', class: 'sep_red', value: value1, idc: 'sepans6' })
				}
			}
			else if (value1 >= 2) {
				returnArray.push({ id: 'Renal_2', class: 'sep_orange', value: value1, idc: 'sepans6' })
			}
			else if (value1 >= 1.2) {
				returnArray.push({ id: 'Renal_1', class: 'sep_yellow', value: value1, idc: 'sepans6' })
			}
			else {
				returnArray.push({ id: 'Renal_0', class: 'sep_green', value: value1, idc: 'sepans6' })
			}
			return returnArray;
			break;
		}
	}
}