function translateToRobot(callBackFunction) {
    var dragNDrop = document.getElementById("dragDropSpace");
    var rowsInTable = dragNDrop.children;

    var terminal = document.getElementById("terminal");
    terminal.value = "";

    var translation = [];

    var inForLoop = false;
    var identationForLoop = 1;

    var keywordDroppedCategory = 6;
    var testcaseDroppedCategory = 7;

    for (var i = 0; i < droppedElements.length; i++) {

        if (droppedElements[i].category === keywordDroppedCategory) {
            translateDroppedKeyword(droppedElements[i].keywordJSON);
            if ((i + 1) >= rowsInTable.length) {
                if (callBackFunction !== undefined) {
                    callBackFunction();
                }
                return true;
            } else {
                continue;
            }
        }

        if (droppedElements[i].category === testcaseDroppedCategory) {
            translateDroppedTestcase(droppedElements[i].keywordJSON);
            if ((i + 1) >= rowsInTable.length) {
                if (callBackFunction !== undefined) {
                    callBackFunction();
                }
                return true;
            } else {
                continue;
            }
        }        

        var elementType = droppedElements[i].id;
        var identationLevel = droppedElements[i].indentation;
        var parameters = droppedElements[i].arguments;

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIdentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIdentation(identationLevel);
        }
        else {
            var translatedRow = handleIdentation(identationLevel);
        }

        translatedRow += handleTranslationOf(droppedElements[i], parameters);
        terminal.value += translatedRow;

        if ((i + 1) >= rowsInTable.length) {
            if (callBackFunction !== undefined) {
                callBackFunction();
            }
            return true;
        }

        if (droppedElements[i].name === "for in" || droppedElements[i].name === "for in range") {
            inForLoop = true;
            identationForLoop = (Number(identationLevel));
        }

    }
}

function translateDroppedTestcase(testcase) {
    var dragNDrop = document.getElementById("dragDropSpace");
    var rowsInTable = dragNDrop.children;

    var terminal = document.getElementById("terminal");
    var translation = [];

    var inForLoop = false;
    var identationForLoop = 1;

	var keywordDroppedCategory = 6;

    for (var i = 0; i < testcase.length; i++) {
        if (testcase[i].category === keywordDroppedCategory) {
            translateDroppedKeyword(testcase[i].keywordJSON);
            if ((i + 1) >= rowsInTable.length) {
                return true;
            } else {
                continue;
            }
        }

        var elementType = testcase[i].id;
        var identationLevel = testcase[i].indentation;
        var parameters = testcase[i].arguments;

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIdentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIdentation(identationLevel);
        }
        else {
            var translatedRow = handleIdentation(identationLevel);
        }

        translatedRow += handleTranslationOf(testcase[i], parameters);
        terminal.value += translatedRow;

        if (testcase[i].name === "for in" || testcase[i].name === "for in range") {
            inForLoop = true;
            identationForLoop = (Number(identationLevel));
        }

    }
}

function translateDroppedKeyword(keyword) {
    var dragNDrop = document.getElementById("dragDropSpace");
    var rowsInTable = dragNDrop.children;

    var terminal = document.getElementById("terminal");
    var translation = [];

    var inForLoop = false;
    var identationForLoop = 1;

    for (var i = 0; i < keyword.length; i++) {
        var elementType = keyword[i].id;
        var identationLevel = keyword[i].indentation;
        var parameters = keyword[i].arguments;

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIdentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIdentation(identationLevel);
        }
        else {
            var translatedRow = handleIdentation(identationLevel);
        }

        translatedRow += handleTranslationOf(keyword[i], parameters);
        terminal.value += translatedRow;

        if (keyword[i].name === "for in" || keyword[i].name === "for in range") {
            inForLoop = true;
            identationForLoop = (Number(identationLevel));
        }

    }
}

function handleIdentation(identationLevel){
	var identation = '';
	for(var i=0; i<identationLevel-1; i++){
		identation += '\t';
	}
	return identation;
}

function handleTranslationOf(data, parameters){
	var translatedRow = '';
  
    var elementType = data.name;

    if(elementType === "comment"){
        translatedRow += translateComment(parameters);
    }
    else if(elementType === "for in"){
        translatedRow += translateForIn(parameters);
    }
    else if(elementType === "for in range"){
        translatedRow += translateForInRange(parameters);
    }    
    else if(elementType === "variable"){
        translatedRow += translateVariable(parameters);
    }
    else if(elementType === "command"){
        translatedRow += translateCommand(parameters);
    }
    else if(elementType === "tags"){
        translatedRow += translateTag(parameters);
    }else{
    	// Command from R-Extract or M-Extract
    	translatedRow += translateExternCommand(data);
    }

    translatedRow += "\n";
    return translatedRow;
}

function translateExternCommand(commandData){
	var scriptLine = commandData.name;
	var arguments = commandData.arguments;

	for(var i=0; i<arguments.length; i++){
		if(arguments[i].visible === true){
			scriptLine += "   " + arguments[i].name;
		}
		
		if(arguments[i].needs_value && arguments[i].value !== undefined && arguments[i].value !== ""){
			scriptLine += "   " + arguments[i].value + " ";
		}
	
	}

	if(commandData.extraValue !== undefined){
		scriptLine += "    " + commandData.extraValue;
	}		

	return scriptLine;
}

function removeAllSpacesBeforeValue(originalString){
	while(originalString.charAt(0) === " "){
		originalString = originalString.substr(1);
	}
	return originalString;
}

function translateComment(parameters){
	var comment = parameters[0].value;
	return "# " + comment;
}

function translateForIn(parameters){
	var start = parameters[0].value;
	var end = parameters[1].value;

	start = removeAllSpacesBeforeValue(start);
	end = removeAllSpacesBeforeValue(end);

	return ":FOR " + start + " IN " + end;
}

function translateForInRange(parameters){
	var start = parameters[0].value;
	var end = parameters[1].value;

	start = removeAllSpacesBeforeValue(start);
	end = removeAllSpacesBeforeValue(end);

	return ":FOR " + start + " IN RANGE " + end;
}

function translateVariable(parameters){
	var variableName = parameters[0].value;
	var variableValue = parameters[1].value;

	variableName = removeAllSpacesBeforeValue(variableName);
	variableValue = removeAllSpacesBeforeValue(variableValue);

	var scriptLine =  "    " + '${'+variableName+'}= ' + variableValue;
	return scriptLine;
}

function translateCommand(parameters){
	var commandScript = parameters[0].value;
	return commandScript;
}

function replaceAllOccurences(search, replacement, string){
    return string.replace(new RegExp(search, 'g'), replacement);
}

function translateTag(parameters){

	var tagName = parameters[0].value;
	var tagValue = parameters[1].value;

	tagName = removeAllSpacesBeforeValue(tagName);

    var translationOfTagsData = replaceAllOccurences("; ", "    ", tagValue);

	var scriptLine = '['+tagName+']    ';
	scriptLine += translationOfTagsData;

	return scriptLine;
}