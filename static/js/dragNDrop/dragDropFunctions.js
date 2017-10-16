function allowDrop(ev) {
	ev.preventDefault();
}

function drag(ev) {
	ev.dataTransfer.setData("text", ev.target.id);
}

function moveDroppedElement(ev) {
	var elementID = ev.dataTransfer.getData("text");
	var belongsToPanel = elementID.slice(elementID.length-9);

	if(belongsToPanel !== "drag-drop"){
		drop(ev);
		var originalNode = document.getElementById(elementID);
		if(originalNode !== null){
			//Delete the node
			rowNode.parentNode.removeChild(rowNode);
		}	
	}
}

function startDragDroppedElement(ev) {
	ev.dataTransfer.setData("text", ev.target.id);
	createEmptyRowsBetweenCommands();
}

function dropBeforeThisElement(ev){
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

function moveElements(movedFromID, movedToID){
	var childrensToMove = getIdentationChilds(movedFromID-1);

	var lastEmptyRow = 0;
	var firstEmptyRow = 1;

	if(movedFromID == firstEmptyRow && movedToID != lastEmptyRow){
		movedToID--;
		movedFromID--;

		var lastIndexToBeMoved = movedFromID + childrensToMove.length;
		var sliced = droppedElements.slice(movedFromID, lastIndexToBeMoved);		

		for(var i=0; i<sliced.length; i++){	
			droppedElements.splice(movedToID+i, 0, sliced[i]);
		}

		droppedElements.splice(movedFromID, childrensToMove.length);

	}
	else if(movedToID == lastEmptyRow){
		movedToID--;
		movedFromID--;

		var lastIndexToBeMoved = movedFromID + childrensToMove.length;
		var sliced = droppedElements.slice(movedFromID, lastIndexToBeMoved);
		droppedElements.splice(movedFromID, childrensToMove.length);

		for(var i=0; i<sliced.length; i++){	
			droppedElements.push(sliced[i]);
		}
	}	
	else{
		movedToID--;
		movedFromID--;
		for(var i=0; i<childrensToMove.length; i++){
			var tempElement = droppedElements[movedFromID+i];
			droppedElements.splice(movedFromID+i, 1);
			droppedElements.splice(movedToID+i, 0, tempElement);
		}
	}
}

function createEmptyRowsBetweenCommands(){
	var dragDropSpace = document.getElementById('dragDropSpace');
	var nextRow = dragDropSpace.firstChild;
	var tempEmptyRows = 0;
	
	var td = document.createElement("tr");
	td.id = "temporary-row-"+tempEmptyRows;

	var textNode = document.createElement("div");
	textNode.className = "temporaryRow";
	td.append(textNode);

	td.setAttribute('ondrop', 'dropBeforeThisElement(event)');
	dragDropSpace.append(td);

    while(nextRow.nextSibling !== null){
    	tempEmptyRows++;
		var td = document.createElement("tr");
		td.id = "temporary-row-"+tempEmptyRows;
		
		var textNode = document.createElement("div");		
		textNode.className = "temporaryRow";
		td.append(textNode);

		td.setAttribute('ondrop', 'dropBeforeThisElement(event)');
		dragDropSpace.append(td);

        dragDropSpace.insertBefore(td, nextRow);	
        nextRow = nextRow.nextSibling;
    }
}

function getIdentationChilds(movedFromID){
	var childrenIDs = [];
	childrenIDs.push(movedFromID);

	var parentIdentation = droppedElements[movedFromID].indentation;	

	for(var i=movedFromID+1; i<droppedElements.length; i++){

		var identationOfNext = droppedElements[i].indentation;
		if(parentIdentation < identationOfNext){
			childrenIDs.push(i);			
		}
		else{
			return childrenIDs;
		}
	}

	return childrenIDs;
}

function getLastIdentationChild(movedFromID){
	var parentIdentation = droppedElements[movedFromID].indentation;	

	for(var i=movedFromID+1; i<droppedElements.length; i++){
		var identationOfNext = droppedElements[i].indentation;
		if(parentIdentation >= identationOfNext){
			break;
		}
	}

	return i;
}

function deleteTemporaryRows(){
	var dragDropSpace = document.getElementById('dragDropSpace');
	var temporaryDivs = document.getElementsByClassName("temporaryRow");
    while(temporaryDivs.length > 0){
        dragDropSpace.removeChild(temporaryDivs[0].parentNode);
    }
}

function drop(ev){
	ev.preventDefault();
	deleteTemporaryRows();
	
	if(movingElement){
		movingElement = false;
		return;
	}

	if(ev.dataTransfer === undefined){
		return;
	}

	var data = ev.dataTransfer.getData("text");
	// You can only drag the correct elements
	if(document.getElementById(data) === null){
		return;
	}

	var nodeCopy = document.getElementById(data).cloneNode(true);
	var elementID = ev.dataTransfer.getData("text");
	nodeCopy.id = getNewID(elementID);         
	var targetID = ev.target.id;


	nodeCopy.className = getNewClass(ev.target.className);
	var commandID = elementID.split("-")[0];
	var indentation = nodeCopy.className.split("-")[1];	

	var targetRow = ev.target.parentNode.parentNode.id;

	if(targetRow !== ""){
		var addElementInThisPosition = getLastIdentationChild(targetRow-1);
		addElementToJSONInIndex(indentation, commandID, addElementInThisPosition);
	}else{
		addElementToJSON(indentation, commandID);
	}			

	var belongsToPanel = elementID.slice(elementID.length-9);
	var dragAndDropPanel = "drag-drop";
	if(belongsToPanel !== dragAndDropPanel){
		// Deletes the original node because it was moved (it is not a copy)
		var originalNode = document.getElementById(elementID);
		var rowNode = originalNode.parentNode;
		rowNode.parentNode.removeChild(rowNode);
	} 		
}

function getNewID(elementID){
	var commandName = elementID.split("-")[0];
	var found = false;
	var newID;

	counterJSON.forEach(function(commandCounter) {
    	if(commandCounter.name === commandName){
    		commandCounter.counter++;
    		found = true;

			newID = commandName + "-" + commandCounter.counter;		
    	}
	});


	if(!found){
		counterJSON.push({
			name: commandName,
			counter: 1
		});

		var newPosition = counterJSON.length-1
		newID = counterJSON[newPosition].name + "-" + 1;
	}

	return newID;
}

function resetDropCounters(){
	while(counterJSON.length>0){
		counterJSON.pop(); 
	}
	elementsInTable = 0;
}

function getNewClass(targetClass){
	if(targetClass === "drop-area"){
		return "drop-0";
	}
	else if(targetClass === "drop-0"){
		return "drop-1";
	}
	else if(targetClass === "drop-1"){
		return "drop-2";
	}
	else if(targetClass === "drop-2"){
		return "drop-3";                
	}
	else if(targetClass === "drop-3"){
		return "drop-4";              
	}
	else if(targetClass === "drop-4"){
		return "drop-5";             
	}
	else if(targetClass === "drop-5"){
		return "drop-6";              
	}
	else if(targetClass === "drop-6"){
		return "drop-7";              
	}            
	else if(targetClass === "drop-7"){
		alert("Profunidad máxima alcanzada");
		return false;
	}else{
		return "drop-1";
	}
}