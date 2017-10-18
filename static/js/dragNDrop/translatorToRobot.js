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

/*	Elements are not translated like this
	if(commandData.extraValue !== undefined){
		scriptLine += "\n...    " + commandData.extraValue;
		scriptLine += "\n";
	}
*/	

	for(var i=0; i<arguments.length; i++){
		if(arguments[i].visible === true){
			scriptLine += " " + arguments[i].name;
		}
		
		if(arguments[i].needs_value && arguments[i].value !== undefined && arguments[i].value !== ""){
			scriptLine += "" + arguments[i].value + " ";
		}
	
	}

	if(commandData.extraValue !== undefined){
		scriptLine += " " + commandData.extraValue;
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

	var scriptLine = '${'+variableName+'}= ' + variableValue;
	return scriptLine;
}

function translateCommand(parameters){
	var commandScript = parameters[0].value;
	return commandScript;
}

function translateTag(parameters){

	var tagName = parameters[0].value;
	var tagValue = parameters[1].value;

	tagName = removeAllSpacesBeforeValue(tagName);
	tagValue = removeAllSpacesBeforeValue(tagValue);

	var scriptLine = '['+tagName+'] ';
	scriptLine += tagValue;

	return scriptLine;
}