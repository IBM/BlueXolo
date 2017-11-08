function createElementInTable(nodeCopy, iDTarget) {
    nodeCopy = createEmptyParameterList(nodeCopy);

    nodeCopy.setAttribute('ondragstart', 'startDragDroppedElement(event)');
    nodeCopy.setAttribute('ondrop', 'moveDroppedElement(event)');
    nodeCopy.setAttribute('draggable', true);

    var dragNDrop = document.getElementById("dragDropSpace");
    var td = document.createElement("tr");

    elementsInTable++;
    td.id = elementsInTable;

    td.addEventListener("click", function () {
        addClickEvent(this.children[1].id);
    });

    function addClickEvent(id) {
        if (id === undefined || id === '') {
            return;
        }
        showProperties(id);
    }

    // Create button to delete the element
    var deleteButton = createButtonToDeleteRow(td.id);
    td.appendChild(deleteButton);

    td.className = nodeCopy.className;
    td.appendChild(nodeCopy);

    if (iDTarget === 'dragDropSpace') {
        dragNDrop.appendChild(td);
    }
    else if (iDTarget === '') {
        return;
    }
    else {
        var targetNode = document.getElementById(iDTarget);
        var parentIdentation = targetNode.className;

        var nextRow = targetNode.parentNode;

        while (nextRow.nextSibling !== null) {
            nextRow = nextRow.nextSibling;
            // Index of '1' because delete button comes first
            var identationOfNext = nextRow.children[1].className;

            if (identationOfNext.split("-")[1] <= parentIdentation.split("-")[1]) {
                targetNode.parentNode.parentNode.insertBefore(td, nextRow);
                return;
            }
        }

        dragNDrop.appendChild(td);
    }
}

function drawElementsFromJSON() {
    resetDropCounters();
    var dragNDrop = document.getElementById("dragDropSpace");
    dragNDrop.innerHTML = "";
    var keywordCategory = 6;

    for (var i = 0; i < droppedElements.length; i++) {
        var newID = getNewID(droppedElements[i].id);
        var newClass = "drop-" + droppedElements[i].indentation;

        var basicDnDNode = document.createElement("div");
        var textNode = document.createElement("text");

        //Gives style to the button and makes the dropped element clickable
        basicDnDNode.id = newID;
        basicDnDNode.className = newClass;

        var commandProductCategory = 3;
        var commandRobotCategory = 4;
        var commandLibrariesCategory = 5;
        if (droppedElements[i].category === commandProductCategory ||
            droppedElements[i].category === commandRobotCategory ||
            droppedElements[i].category === commandLibrariesCategory) {

            var libraryName = droppedElements[i].source.name;
            textNode.innerText += libraryName + "." + droppedElements[i].name;
        }
        else {
            textNode.innerText += droppedElements[i].name;
        }

        //Gives style to the button
        textNode.className = newClass;
        basicDnDNode.appendChild(textNode);

        //Appends an empty parameter list in order to populate it after
        basicDnDNode = createEmptyParameterList(basicDnDNode);

        basicDnDNode.setAttribute('ondragstart', 'startDragDroppedElement(event)');
        basicDnDNode.setAttribute('ondrop', 'moveDroppedElement(event)');
        basicDnDNode.setAttribute('draggable', true);

        var td = document.createElement("tr");

        elementsInTable++;
        td.id = elementsInTable;

        td.addEventListener("click", function () {
            var rowNodeIndex = this.id;
            addClickEvent(this.children[1].id, rowNodeIndex);
        });

        function addClickEvent(htmlID, rowNodeIndex) {
            var DOMnode = document.getElementById(htmlID);
            if (DOMnode === null) {
                //The element was deleted. The trigger was the delete button
                return;
            }
            var indexToModify = rowNodeIndex - 1;
            showProperties(htmlID, indexToModify);
        }

        // Create button to delete the element
        var deleteButton = createButtonToDeleteRow(td.id);
        td.appendChild(deleteButton);

        td.className = basicDnDNode.className;
        td.appendChild(basicDnDNode);

        dragNDrop.appendChild(td);

        if (droppedElements[i].category === keywordCategory) {

        } else {
            drawParameterList(i, newID);
        }
    }
}

function createEmptyParameterList(node) {
    var attributeList = document.createElement("ul");
    attributeList.id = node.id + "-" + "parameters";

    attributeList.className = "parameter";
    attributeList.style.fontWeight = "normal";

    var li = document.createElement('li');
    attributeList.appendChild(li);

    node.appendChild(attributeList);
    return node;
}

function createEmptyParameterListForKeywords(node) {
    var attributeList = document.createElement("ul");
    attributeList.id = node.id + "-" + "parameters";

    attributeList.className = "parameter";
    attributeList.style.fontWeight = "normal";

    var li = document.createElement('li');
    attributeList.appendChild(li);

    node.appendChild(attributeList);
    return node;
}

function drawParameterList(droppedElementIndex, elementID) {
    var droppedElement = droppedElements[droppedElementIndex];
    var listParent = document.getElementById(elementID + "-" + "parameters");
    var lis = listParent.getElementsByTagName("li");

    var arguments = droppedElement.arguments;

    // Deletes all elements in list to populate it again
    listParent.innerHTML = "";

    // Adds to the list the extra value
    if (droppedElement.extraValue !== undefined) {
        var li = document.createElement('li');
        var textToDisplayInList = droppedElement.extraValue;

        textNode = document.createTextNode(textToDisplayInList);
        li.appendChild(textNode);
        listParent.appendChild(li);
    }

    for (var i = 0; i < arguments.length; i++) {

        if (arguments[i].visible === undefined && (arguments[i].value === undefined || arguments[i].value === "")) {
            continue;
        }

        var li = document.createElement('li');
        var textToDisplayInList = arguments[i].name;

        if (arguments[i].value !== undefined) {
            textToDisplayInList += ": " + arguments[i].value;
        }

        textNode = document.createTextNode(textToDisplayInList);
        li.appendChild(textNode);
        listParent.appendChild(li);

    }
}

function createButtonToDeleteRow(rowID) {
    var buttonNode = document.createElement("input");
    buttonNode.setAttribute("type", "submit");
    buttonNode.setAttribute("value", "X");
    buttonNode.setAttribute("class", "btn-flat red-text");

    buttonNode.addEventListener("click", function () {
        deleteAllChildren(rowID);
        deleteElement(rowID);
    });

    function deleteElement(id) {
        droppedElements.splice(id - 1, 1);
        drawElementsFromJSON();
    }

    function deleteAllChildren(id) {
        var rowToDelete = document.getElementById(id);
        var childrensToDelete = getIdentationChilds(id - 1);

        droppedElements.splice(id - 1, childrensToDelete.length - 1);
        drawElementsFromJSON();
    }

    return buttonNode;
}