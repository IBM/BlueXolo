/*
    This file contains all functions and methods related with drag an drop

    *This includes all the logic related since the drag of the element
    until is dropped and added to the variable "DropppedElements".

    *DroppedElements is initialized in each create and edit html as an 
    empty array.

    *This file contains also the logic to create empty rows between
    dropped elements.

    *Each time a element is dropped it need to be recognized where
    if it is being dropped in a empty row or inside an element.
    This is important because dropped elements needs a indentation.

    *Because of perfomance, drawing and logic is being done by
    iteration or direct changin into a variable ("DroppedElements").
    With this in mind, the only moment to see DOM's id is when an element
    changes from a place to other. And the position in the table says
    its original place.

    *Manipulation of variable DroppedElement (jsonManipulator.js) and drawing of
    elements in table (dropCreator.js) are done in differente files
*/


function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    deleteTemporaryRows();
    createEmptyRowsBetweenCommands();
    movingElement = true;
}

function moveDroppedElement(ev) {
    var elementID = ev.dataTransfer.getData("text");
    var belongsToPanel = elementID.slice(elementID.length - 9);

    if (belongsToPanel !== "drag-drop") {
        drop(ev);
        var originalNode = document.getElementById(elementID);
        if (originalNode !== null) {
            //Delete the node
            rowNode.parentNode.removeChild(rowNode);
        }
    }
}

function startDragDroppedElement(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
    deleteTemporaryRows();
    createEmptyRowsBetweenCommands();
}

function dropBeforeThisElement(ev) {
    var data = ev.dataTransfer.getData("text");

    var dragAndDropPanel = "drag-drop";
    var keywordsPanel = "keyword-drag-drop";
    var testcasePanel = "testcase-drag-drop";

    var positionOfFirstDash = data.indexOf("-");

    var belongsToPanel = data.slice(positionOfFirstDash + 1);

    if(belongsToPanel === dragAndDropPanel){    
        
        movingElement = true;

        var insertBeforeThisEmptyRow = ev.target.parentNode;
        var positionToAddElement = insertBeforeThisEmptyRow.id;
        positionToAddElement = positionToAddElement.split("-")[2];
        positionToAddElement--;

        var firstElement = data.split("-")[0];
        var elementID = firstElement.indexOf("_") ? firstElement.split("_")[0] : firstElement;
        var sourceID = firstElement.indexOf("_") ? parseInt(firstElement.split("_")[1]) : null;
        var indentation = 1;

        if(positionToAddElement === -1){
            positionToAddElement = droppedElements.length;
        }

        addElementToJSONInIndex(indentation, elementID, positionToAddElement, sourceID);
        drawElementsFromJSON();

        return true;
    }
    else if(belongsToPanel === keywordsPanel){    
        
        movingElement = true;

        var insertBeforeThisEmptyRow = ev.target.parentNode;
        var positionToAddElement = insertBeforeThisEmptyRow.id;
        positionToAddElement = positionToAddElement.split("-")[2];
        positionToAddElement--;

        var elementID = data.split("-")[0];
        var indentation = 1;

        if(positionToAddElement === -1){
            positionToAddElement = droppedElements.length;
        }

        addKeywordToJSONInIndex(indentation, elementID, positionToAddElement);
        drawElementsFromJSON();

        return true;
    }
    else if(belongsToPanel === testcasePanel){    
        
        movingElement = true;

        var insertBeforeThisEmptyRow = ev.target.parentNode;
        var positionToAddElement = insertBeforeThisEmptyRow.id;
        positionToAddElement = positionToAddElement.split("-")[2];
        positionToAddElement--;

        var elementID = data.split("-")[0];
        var indentation = 1;

        if(positionToAddElement === -1){
            positionToAddElement = droppedElements.length;
        }

        addTestcaseToJSONInIndex(indentation, elementID, positionToAddElement);
        drawElementsFromJSON();

        return true;
    }    

    // Because is moving, the drop event is going to delete the original element after drop it
    movingElement = true;
    var insertBeforeThisEmptyRow = ev.target.parentNode;

    var elementID = ev.dataTransfer.getData("text");
    var movedElement = document.getElementById(elementID).parentNode;
    var dragDropSpace = document.getElementById('dragDropSpace');

    var movedFromID = movedElement.id;
    var movedToID = insertBeforeThisEmptyRow.id;
    movedToID = movedToID.split("-")[2];

    moveElements(movedFromID, movedToID);
    drawElementsFromJSON();
}

function moveElements(movedFromID, movedToID) {
    var childrensToMove = getIdentationChilds(movedFromID - 1);

    var lastEmptyRow = 0;
    var firstEmptyRow = 1;

    if (movedFromID == firstEmptyRow && movedToID != lastEmptyRow) {
        movedToID--;
        movedFromID--;

        var lastIndexToBeMoved = movedFromID + childrensToMove.length;
        var sliced = droppedElements.slice(movedFromID, lastIndexToBeMoved);

        for (var i = 0; i < sliced.length; i++) {
            droppedElements.splice(movedToID + i, 0, sliced[i]);
        }

        droppedElements.splice(movedFromID, childrensToMove.length);

    }
    else if (movedToID == lastEmptyRow) {
        movedToID--;
        movedFromID--;

        var lastIndexToBeMoved = movedFromID + childrensToMove.length;
        var sliced = droppedElements.slice(movedFromID, lastIndexToBeMoved);
        droppedElements.splice(movedFromID, childrensToMove.length);

        for (var i = 0; i < sliced.length; i++) {
            droppedElements.push(sliced[i]);
        }
    }
    else {
        movedToID--;
        movedFromID--;
        for (var i = 0; i < childrensToMove.length; i++) {
            var tempElement = droppedElements[movedFromID + i];
            droppedElements.splice(movedFromID + i, 1);
            droppedElements.splice(movedToID + i, 0, tempElement);
        }
    }
}

function createEmptyRowsBetweenCommands() {
    var dragDropSpace = document.getElementById('dragDropSpace');
    var nextRow = dragDropSpace.firstChild;

    if(nextRow === null){
        return;
    }

    var tempEmptyRows = 0;

    var td = document.createElement("tr");
    td.id = "temporary-row-" + tempEmptyRows;

    var textNode = document.createElement("div");
    textNode.className = "temporaryRow";
    td.append(textNode);

    td.setAttribute('ondrop', 'dropBeforeThisElement(event)');
    td.setAttribute('onmouseup', 'dropBeforeThisElement(event)');
    dragDropSpace.append(td);

    while (nextRow.nextSibling !== null) {
        tempEmptyRows++;
        var td = document.createElement("tr");
        td.id = "temporary-row-" + tempEmptyRows;

        var textNode = document.createElement("div");
        textNode.className = "temporaryRow";
        td.append(textNode);

        td.setAttribute('ondrop', 'dropBeforeThisElement(event)');
        td.setAttribute('onmouseup', 'dropBeforeThisElement(event)');
        dragDropSpace.append(td);

        dragDropSpace.insertBefore(td, nextRow);
        nextRow = nextRow.nextSibling;
    }
}

function getIdentationChilds(movedFromID) {
    var childrenIDs = [];
    childrenIDs.push(movedFromID);

    var parentIdentation = droppedElements[movedFromID].indentation;

    for (var i = movedFromID + 1; i < droppedElements.length; i++) {

        var identationOfNext = droppedElements[i].indentation;
        if (parentIdentation < identationOfNext) {
            childrenIDs.push(i);
        }
        else {
            return childrenIDs;
        }
    }

    return childrenIDs;
}

function getLastIdentationChild(movedFromID) {
    var parentIdentation = droppedElements[movedFromID].indentation;

    for (var i = movedFromID + 1; i < droppedElements.length; i++) {
        var identationOfNext = droppedElements[i].indentation;
        if (parentIdentation >= identationOfNext) {
            break;
        }
    }

    return i;
}

function deleteTemporaryRows() {
    var dragDropSpace = document.getElementById('dragDropSpace');
    var temporaryDivs = document.getElementsByClassName("temporaryRow");
    while (temporaryDivs.length > 0) {
        dragDropSpace.removeChild(temporaryDivs[0].parentNode);
    }
}

function drop(ev) {
    ev.preventDefault();
    deleteTemporaryRows();

    if(ev.target.parentNode.parentNode === null){
        return;
    }

    if (ev.dataTransfer === undefined) {
        return;
    }

    var data = ev.dataTransfer.getData("text");
    // You can only drag the correct elements
    if (document.getElementById(data) === null) {
        return;
    }

    var nodeCopy = document.getElementById(data).cloneNode(true);
    var elementID = ev.dataTransfer.getData("text");
    nodeCopy.id = getNewID(elementID);
    var targetID = ev.target.id;

    var newClass = getNewClass(ev.target.className);
    if (!newClass) {
        return;
    }

    nodeCopy.className = newClass;

    var firstElement = elementID.split("-")[0];
    var commandID = firstElement.indexOf("_") ? firstElement.split("_")[0] : firstElement;
    var sourceID = firstElement.indexOf("_") ? parseInt(firstElement.split("_")[1]) : null;
    var indentation = nodeCopy.className.split("-")[1];

    var belongsToPanel = elementID.slice(elementID.length - 9);
    var dragAndDropPanel = "drag-drop";
    var keywordsPanel = "keyword-drag-drop";
    var testcasePanel = "testcase-drag-drop";    

    var targetRow = ev.target.parentNode.parentNode.id;

    if (elementID.length >= 19) {
        //It could belong to the keyword panel
        var belongsToPanel = elementID.slice(elementID.length - keywordsPanel.length);
        if (belongsToPanel === keywordsPanel) {
            //It belongs to the keyword panel!
            var keywordID = commandID;
            if (targetRow !== "") {
                var addElementInThisPosition = getLastIdentationChild(targetRow - 1);
                addKeywordToJSONInIndex(indentation, keywordID, addElementInThisPosition);
            } else {
                addKeywordToJSON(indentation, keywordID);
            }
        }else{
            //Then it could belong to the testcase panel
            var belongsToPanel = elementID.slice(elementID.length - testcasePanel.length);
            if (belongsToPanel === testcasePanel) {            
                //It belongs to the testcase panel!
                var testcaseID = commandID;
                if (targetRow !== "") {
                    var addElementInThisPosition = getLastIdentationChild(targetRow - 1);
                    addTestcaseToJSONInIndex(indentation, testcaseID, addElementInThisPosition);
                } else {
                    addTestcaseToJSON(indentation, testcaseID);
                }
            }
        }
    }
    else {
        if (targetRow !== "") {
            var addElementInThisPosition = getLastIdentationChild(targetRow - 1);
            addElementToJSONInIndex(indentation, commandID, addElementInThisPosition, sourceID);
        } else {
            addElementToJSON(indentation, commandID, sourceID);
        }

        var belongsToPanel = elementID.slice(elementID.length - dragAndDropPanel.length);
        if (belongsToPanel !== dragAndDropPanel) {
            // Deletes the original node because it was moved (it is not a copy)
            var originalNode = document.getElementById(elementID);
            var rowNode = originalNode.parentNode;
            rowNode.parentNode.removeChild(rowNode);
        }
    }
}