var usedExtras = [];
var usedKeywords = [];
var usedTestcases = [];

var variablesSection      = false;
var variablesSectionEnded = false;

var keywordSection        = false;
var keywordSectionEnded   = false;

var testcaseSection       = false;
var testcaseSectionEnded  = false;

var addedOwnDescription   = false;

function resetUsedArraysVariables(){
    usedExtras = [];
    usedKeywords = [];
    usedTestcases = [];
}

function resetSections(){
    variablesSection      = false;
    variablesSectionEnded = false;

    keywordSection        = false;
    keywordSectionEnded   = false;

    testcaseSection       = false;
    testcaseSectionEnded  = false;

    addedOwnDescription   = false;
}

function checkIfExtraElementsExist(){
    if(usedExtras.length === 0){
        usedExtras = null;
    }
    if(usedKeywords.length === 0){
        usedKeywords = null;
    }
    if(usedTestcases.length === 0){
        usedTestcases = null;
    }  
}

function addKeywordName(){
    var keywordNameTextArea = document.getElementById("keyword_name");
    var testcaseNameTextArea = document.getElementById("testcase_name");

    if(keywordNameTextArea !== null){
        translatedRow = keywordNameTextArea.value;
        return translatedRow;
    }
    else if(testcaseNameTextArea !== null){
        translatedRow = testcaseNameTextArea.value;
        return translatedRow;
    }
    else{
        return "";
    }
}

function addDocumentationSection(){
    var translatedRow = "\t[Documentation]\t";

    var keywordDescriptionTextArea = document.getElementById("keyword_description");
    var testcaseDescriptionTextArea = document.getElementById("testcase_description");
    
    if(keywordDescriptionTextArea !== null){
        translatedRow += keywordDescriptionTextArea.value;
        translatedRow += "\n";
        return translatedRow;
    }
    else if(testcaseDescriptionTextArea !== null){
        translatedRow += testcaseDescriptionTextArea.value;
        translatedRow += "\n";
        return translatedRow;
    }
    else{
        return "";
    }    
}

function isKeyword(){
    var keywordNameTextArea = document.getElementById("keyword_name");
    if(keywordNameTextArea !== null){
        return true
    }
    else{
        return false;
    }
}

function isTestcase(){
    var testcaseNameTextArea = document.getElementById("testcase_name");
    if(testcaseNameTextArea !== null){
        return true
    }
    else{
        return false;
    }
}

function isAVariable(dropppedCommandName){
    if(dropppedCommandName === "Global variable") {
        return true;
    }
    else{
        return false;
    }
}

function handleSections(startedSection){

    if(startedSection == "keywords"){

        if(variablesSection){
            variablesSection = false;
            variablesSectionEnded = true;
        }
        if(testcaseSection){
            testcaseSection = false;
            testcaseSectionEnded = true;
        }

    }
    else if(startedSection == "variables"){

        if(keywordSection){
            keywordSection = false;
            keywordSectionEnded = true;
        }
        if(testcaseSection){
            testcaseSection = false;
            testcaseSectionEnded = true;
        }

    }
    else if(startedSection == "testcases"){

        if(variablesSection){
            variablesSection = false;
            variablesSectionEnded = true;
        }
        if(keywordSection){
            keywordSection = false;
            keywordSectionEnded = true;
        }

    }
    else{
        console.log("Error handling sections");
    }    
}

function handleKeywordSection(keywordName, customKeyword){
    if(keywordSectionEnded){
        return;
    }

    var startedSection = "keywords";
    handleSections(startedSection);

    var translatedRow = "\n";

    // Version 3
    // ToDo
    // Version 3 will handle a flag if the user wants to add the section or not.
    // At this moment it will not add the section if the current object is not a keyword
    if(!isKeyword()){
        translatedRow = "\t"+keywordName+"\n";
        keywordSection = true;
        return translatedRow;
    }

    if(!keywordSection){
        translatedRow += "*** Keywords ***\n";
        keywordSection = true;
    }
    
    if(customKeyword){
        translatedRow += "\t"+keywordName+"\n";
    }
    else{
        translatedRow += keywordName+"\n";    
    }
    

    return translatedRow;
}

function handleTestcaseSection(testcaseName){

    if(testcaseSectionEnded){
        return;
    }

    var startedSection = "testcases";
    handleSections(startedSection);

    var translatedRow = "\n";

    if(!testcaseSection){
        translatedRow += "*** Test Cases ***\n";

        testcaseSection = true;
    }
    
    translatedRow += testcaseName + "\n";

    return translatedRow;
}

function handleVariablesSection(){

    if(variablesSectionEnded){
        return;
    }

    var startedSection = "variables";
    handleSections(startedSection);

    var translatedRow = "";

    if(!variablesSection){
        translatedRow += "*** Variables ***";
        translatedRow += "\n";
        variablesSection = true;
    }
    
    return translatedRow;
}

function translateToRobot(callBackFunction) {

    resetUsedArraysVariables();
    resetSections();

    var dragNDrop = document.getElementById("dragDropSpace");
    var rowsInTable = dragNDrop.children;

    var terminal = document.getElementById("terminal");
    terminal.value = "";

    var translation = [];

    var inForLoop = false;
    var identationForLoop = 1;

    var commandProductCategory = 3;
    var externalLibrariesCategory = 5;

    var keywordDroppedCategory = 6;
    var testcaseDroppedCategory = 7;

    var alreadyAdded = false;

    for (var i = 0; i < droppedElements.length; i++) {

        if (droppedElements[i].category === keywordDroppedCategory) {

            var keywordName = droppedElements[i].name;
            var customKeyword = true;
            var translatedRow = handleKeywordSection(keywordName, customKeyword);

            terminal.value += translatedRow;
            
            var keywordUsedID = droppedElements[i].id;
            var newKeywordUsed = droppedElements[i].keywordJSON;
            addKeywordToUsedArray( keywordUsedID, newKeywordUsed);
            //translateDroppedKeyword(droppedElements[i].keywordJSON);
            
            if ((i + 1) >= droppedElements.length) {
                if (callBackFunction !== undefined) {
                    callBackFunction();
                }
                return true;
            } else {
                continue;
            }
        }

        if (droppedElements[i].category === testcaseDroppedCategory) {

            var testcaseName = droppedElements[i].name;
            var translatedRow = handleTestcaseSection(testcaseName);
            terminal.value += translatedRow;

            var testcaseUsedID = droppedElements[i].id;
            var newTestcaseUsed = droppedElements[i].keywordJSON;

            addTestcaseToUsedArray( testcaseUsedID, newTestcaseUsed);
            //translateDroppedTestcase(droppedElements[i].keywordJSON);

            if ((i + 1) >= droppedElements.length) {
                if (callBackFunction !== undefined) {
                    callBackFunction();
                }
                return true;
            } else {
                continue;
            }
        }

        if(droppedElements[i].category === commandProductCategory
            || droppedElements[i].category === externalLibrariesCategory){
                var commandID = droppedElements[i].source.id;
                addExtraToUsedArray(commandID);
        }

        var elementType = droppedElements[i].id;
        var identationLevel = droppedElements[i].indentation;
        var parameters = droppedElements[i].arguments;

        // Handles for
        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIndentation(identationForLoop - 1, variablesSectionEnded);
            translatedRow += "\\    ";
            translatedRow += handleIndentation(identationLevel, variablesSectionEnded);
        }
        else {
            var translatedRow = handleIndentation(identationLevel, variablesSectionEnded);
        }

        // Handles variables
        var isAVariableFlag = isAVariable(droppedElements[i].name);

        if (isAVariableFlag) {
            //translatedRow += handleVariablesSection();
            terminal.value += handleVariablesSection();

            translatedRow = handleTranslationOf(droppedElements[i], parameters);
            terminal.value += translatedRow;

            alreadyAdded = true;
        }        

        //if (variablesSection && droppedElements[i].name !== "variable") {
        if (variablesSection && !isAVariableFlag) {            
            variablesSection = false;
            variablesSectionEnded = true;
        }

        if(!addedOwnDescription && !isAVariableFlag){
            
            if(isKeyword()){
                //never was added *** Keyword ***            
                var keywordName = addKeywordName();
                var customKeyword = false;
                var keywordDescription = handleKeywordSection(keywordName, customKeyword);

                keywordDescription += addDocumentationSection();                
                terminal.value += keywordDescription;
                terminal.value += "\t";
            }
            
            if(isTestcase()){
                //never was added *** Testcase ***
                var keywordName = addKeywordName();
                var keywordDescription = handleTestcaseSection(keywordName);

                keywordDescription += addDocumentationSection();
                terminal.value += keywordDescription;
                terminal.value += "\t";
            }

            addedOwnDescription = true;
        }

        if(!alreadyAdded){
            translatedRow += handleTranslationOf(droppedElements[i], parameters);
            terminal.value += translatedRow;            
        }

        alreadyAdded = false;

        if ((i + 1) >= rowsInTable.length) {


        if(!addedOwnDescription){
            
            if(isKeyword()){
                //never was added *** Keyword ***            
                var keywordName = addKeywordName();
                var customKeyword = false;
                var keywordDescription = handleKeywordSection(keywordName, customKeyword);

                keywordDescription += addDocumentationSection();                
                terminal.value += keywordDescription;
                terminal.value += "\t";
            }
            
            if(isTestcase()){
                //never was added *** Testcase ***
                var keywordName = addKeywordName();
                var keywordDescription = handleTestcaseSection(keywordName);

                keywordDescription += addDocumentationSection();
                terminal.value += keywordDescription;
                terminal.value += "\t";
            }

            addedOwnDescription = true;
        }

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

function getTranslationOfKeyword(keyword){
    var translation = "";

    var inForLoop = false;
    var identationForLoop = 1;

    var commandProductCategory = 3;
    var externalLibrariesCategory = 5;

    for (var i = 0; i < keyword.length; i++) {
        var elementType = keyword[i].id;
        var identationLevel = keyword[i].indentation;
        var parameters = keyword[i].arguments;

        if(keyword[i].category === commandProductCategory
            || keyword[i].category === externalLibrariesCategory){
                var commandID = keyword[i].source.id;;
                addExtraToUsedArray(commandID);
        }

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIndentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIndentation(identationLevel);
        }
        else {
            var translatedRow = handleIndentation(identationLevel);
        }

        translatedRow += handleTranslationOf(keyword[i], parameters);
        translation += translatedRow;
        translation += "\n";


        if (keyword[i].name === "for in" || keyword[i].name === "for in range") {
            inForLoop = true;
            identationForLoop = (Number(identationLevel));
        }
    }

    return translation;
}

function getTranslationOfTestcase(testcase){
    var translation = "";

    var inForLoop = false;
    var identationForLoop = 1;

    var commandProductCategory = 3;
    var externalLibrariesCategory = 5;

    var keywordDroppedCategory = 6;

    for (var i = 0; i < testcase.length; i++) {

        if (testcase[i].category === keywordDroppedCategory) {

            var keywordUsedID = testcase[i].id;
            var newKeywordUsed = testcase[i].keywordJSON;
            addKeywordToUsedArray( keywordUsedID, newKeywordUsed)

            var identationLevel = testcase[i].indentation;
            var translatedRow = handleIndentation(identationLevel);

            if(identationLevel === undefined){
                identationLevel = 0;
            }

            translatedRow += testcase[i].name;
            translation += translatedRow;
            translation += "\n";
        }
        else{

            if(testcase[i].category === commandProductCategory
                || testcase[i].category === externalLibrariesCategory){
                    var commandID = testcase[i].source.id;;
                    addExtraToUsedArray(commandID);
            }

            var elementType = testcase[i].id;
            var identationLevel = testcase[i].indentation;
            var parameters = testcase[i].arguments;

            if (inForLoop && Number(identationLevel) <= identationForLoop) {
                inForLoop = false;
            }

            if (inForLoop) {
                var translatedRow = handleIndentation(identationForLoop - 1);
                translatedRow += "\\    ";
                translatedRow += handleIndentation(identationLevel);
            }
            else {
                var translatedRow = handleIndentation(identationLevel);
            }

            translatedRow += handleTranslationOf(testcase[i], parameters);
            translation += translatedRow;
            translation += "\n";

            if (testcase[i].name === "for in" || testcase[i].name === "for in range") {
                inForLoop = true;
                identationForLoop = (Number(identationLevel));
            }
        }
    }

    return translation;
}

function addKeywordToUsedArray( keywordID, keyword){
    var translation = getTranslationOfKeyword(keyword);    

    var newElement = {
        id: keywordID,
        script: translation,
    };

    usedKeywords.push(newElement);
}

function addExtraToUsedArray(sourceID){

    var newElement = {
        source: sourceID,
    };

    usedExtras.push(newElement);
}

function addTestcaseToUsedArray( testcaseID, testcase){
    var translation = getTranslationOfTestcase(testcase);

    var newElement = {
        id: testcaseID,
        script: translation,
    };

    usedTestcases.push(newElement);
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

        if(identationLevel === undefined){
            identationLevel = 0;
        }

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIndentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIndentation(identationLevel);
        }
        else {
            var translatedRow = handleIndentation(identationLevel);
        }

        translatedRow += handleTranslationOf(keyword[i], parameters);
        terminal.value += translatedRow;

        if (keyword[i].name === "for in" || keyword[i].name === "for in range") {
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

        if(identationLevel === undefined){
            identationLevel = 0;
        }

        if (inForLoop && Number(identationLevel) <= identationForLoop) {
            inForLoop = false;
        }

        if (inForLoop) {
            var translatedRow = handleIndentation(identationForLoop - 1);
            translatedRow += "\\    ";
            translatedRow += handleIndentation(identationLevel);
        }
        else {
            var translatedRow = handleIndentation(identationLevel);
        }

        translatedRow += handleTranslationOf(testcase[i], parameters);
        terminal.value += translatedRow;

        if (testcase[i].name === "for in" || testcase[i].name === "for in range") {
            inForLoop = true;
            identationForLoop = (Number(identationLevel));
        }

    }
}

function handleIndentation(identationLevel){

    if(variablesSectionEnded || keywordSection || testcaseSection){        
        identationLevel = parseInt(identationLevel) + 1;
    }

    var identation = '';
    for(var i=0; i<identationLevel-1; i++){
        identation += '\t';
    }
    return identation;
}

function handleTranslationOf(data, parameters){
    var translatedRow = '';
  
    var elementType = data.name;
    var elementType = elementType.toLowerCase();

    if(elementType === "comment"){
        translatedRow += translateComment(parameters);
    }
    else if(elementType === "for in"){
        translatedRow += translateForIn(parameters);
    }
    else if(elementType === "for in range"){
        translatedRow += translateForInRange(parameters);
    }    
    else if(elementType === "variable" || elementType === "global variable"){
        translatedRow += translateVariable(parameters);
    }
    else if(elementType === "command"){
        translatedRow += translateCommand(parameters);
    }
    else if(elementType === "tags"){
        translatedRow += translateTag(parameters);
    }
    else if(elementType === "list"){
        translatedRow += translateList(parameters);
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

    var keywordsCategory = 6;

    if(commandData.category === keywordsCategory){
        return scriptLine;
    }

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
    if(originalString === undefined){
        return;
    }
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

function translateList(parameters){
    var tagName = parameters[0].value;
    var tagValue = parameters[1].value;

    tagName = removeAllSpacesBeforeValue(tagName);

    var translationOfTagsData = replaceAllOccurences("; ", "    ", tagValue);

    var scriptLine = '@{'+tagName+'}    ';
    scriptLine += translationOfTagsData;

    return scriptLine;
}

function translateVariable(parameters){
    var variableName = parameters[0].value;
    var variableValue = parameters[1].value;

    variableName = removeAllSpacesBeforeValue(variableName);
    variableValue = removeAllSpacesBeforeValue(variableValue);

    var scriptLine =  '${'+variableName+'}    ' + variableValue;
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