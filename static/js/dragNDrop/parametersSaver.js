function getInputs(droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];
	var propertiesPannel = document.getElementById("propertiesPannel").getElementsByTagName("form");
	var inputValues = [];

	for(var i=0; i<propertiesPannel.length; i++){
		var parameterChecked = undefined;
		var parameterValue = undefined;	

		var formNode = propertiesPannel[i];
		//There is a checkbox
		var checkboxNode = formNode[0];
		var parameterChecked = checkboxNode.checked;
		
		if(droppedElement.arguments[i].needs_value){
			var parameterValue = formNode[1].value;
		}

	    var inputValue = {
	        "checked": parameterChecked,
	        "value": parameterValue,
	    };
	    inputValues.push(inputValue);
	}
	return inputValues;
}

function getInputsExtraInput(droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];
	var propertiesPannel = document.getElementById("propertiesPannel").getElementsByTagName("form");
	var inputValues = [];

	for(var i=0; i<propertiesPannel.length; i++){

		if(i===0){
			var formNode = propertiesPannel[i];	
			droppedElements[droppedElementIndex].extraValue = formNode[0].value;
		}
		else{
			var parameterChecked = undefined;
			var parameterValue = undefined;	

			var formNode = propertiesPannel[i];
			//There is a checkbox
			var checkboxNode = formNode[0];
			var parameterChecked = checkboxNode.checked;
			
			if(droppedElement.arguments[i-1].needs_value){
				var parameterValue = formNode[1].value;
			}

		    var inputValue = {
		        "checked": parameterChecked,
		        "value": parameterValue,
		    };
		    inputValues.push(inputValue);
		}
	}
	return inputValues;
}

function getTagInputs(droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];
	var propertiesPannel = document.getElementById("propertiesPannel").getElementsByTagName("form");
	var inputValues = [];

	for(var i=0; i<propertiesPannel.length; i++){

		var parameterChecked = undefined;
		var parameterValue = undefined;

		var formNode = propertiesPannel[i];
		//There is a checkbox
		var checkboxNode = formNode[0];
		var parameterChecked = checkboxNode.checked;

		if(droppedElement.arguments[i].name === "name"){
			var parameterValue = formNode[1].value;
		}
		else if(droppedElement.arguments[i].name === "tags"){
			var chipsID = formNode.children[2].id;
			var data = document.getElementById(chipsID);

			if(data !== null){
				var parameterValue = "";				
				for(var j=0; j<data.children.length-1; j++){
		 			var chipNode = data.children[j];
		 			parameterValue += chipNode.firstChild.data;
		 			if(j+1 < data.children.length-1){
						parameterValue += "\t";
		 			}		 			
		 		}
			}
		}

	    var inputValue = {
	        "checked": parameterChecked,
	        "value": parameterValue,
	    };
	    inputValues.push(inputValue);

	}
	console.log(inputValues);
	return inputValues;
}

function saveFromInput(droppedElementIndex, elementID){
	if (elementID === undefined ){
		alert("You need to select an item to edit first");
		return;
	}
	var droppedElement = droppedElements[droppedElementIndex];
    if(droppedElement.category === 1){
    	var values = getInputs(droppedElementIndex);        
    }
	else{
        var values = getInputsExtraInput(droppedElementIndex);
    }	
	saveValuesInJSON(droppedElementIndex, values);
	drawParameterList(droppedElementIndex, elementID);	
}

function saveTagFromInput(droppedElementIndex, elementID){
	if (elementID === undefined ){
		alert("You need to select an item to edit first");
		return;
	}
	var values = getTagInputs(droppedElementIndex);
	saveValuesInJSON(droppedElementIndex, values);
	drawParameterList(droppedElementIndex, elementID);	
}

function saveValuesInJSON(droppedElementIndex, values) {
	var droppedElement = droppedElements[droppedElementIndex];
    var arguments = droppedElement.arguments;

    for (var i = 0; i < arguments.length; i++) {

        if (values[i].checked === undefined && (values[i].value === undefined || values[i].value === "")) {
            continue;
        }

        if (values[i].checked) {
            droppedElement.arguments[i].visible = true;
        }

        if (values[i].value !== undefined) {
            droppedElement.arguments[i].value = values[i].value;
        }
    }
}