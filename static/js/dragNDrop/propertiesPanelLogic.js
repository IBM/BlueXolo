function hidePropertiesPanel() {
    var x = document.getElementById('propertiesPannel');
    var buttonToShowPanel = document.getElementById('toggleProperties');
    x.style.display = 'none';
}

function showPropertiesPanel() {
    var x = document.getElementById('propertiesPannel');
    var buttonToShowPanel = document.getElementById('toggleProperties');
    x.style.display = 'block';
}

function handleVisualization() {
    var propertiesPanel = document.getElementById('propertiesPannel');
    if (propertiesPanel.style.display === 'block') {
        hidePropertiesPanel();
    }
    else {
        showPropertiesPanel();
    }
}

function addExtraTextInput(propPanelNode, droppedElementIndex){
    var droppedElement = droppedElements[droppedElementIndex];
    var tempForm = document.createElement("form");

    var inputNode = document.createElement("input");
    inputNode.setAttribute('placeholder', 'Write an extra value');
    
    if(droppedElement.extraValue!== undefined){
        inputNode.setAttribute('value', droppedElement.extraValue);
    }      

    // Now it doesn't refresh the website if you press enter while typing on the form
    inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
    tempForm.appendChild(inputNode);
    propPanelNode.appendChild(tempForm);

    return propPanelNode;
}

function cleanPropertiesPanel(){
    var propPanel = document.getElementById("propertiesPannel");
    while (propPanel.hasChildNodes()) {
        propPanel.removeChild(propPanel.childNodes[0]);
    }

    var propPanelContainer = document.getElementById("propertiesPanelContainer");

    var indexOfButton = 3;
    var previousButtonNode = propPanelContainer.childNodes[indexOfButton];
    if(previousButtonNode !== undefined){
        propPanelContainer.removeChild(previousButtonNode);
    }
}

function drawPropertiesForKeywords(droppedElementIndex, elementID) {    
    var droppedElement = droppedElements[droppedElementIndex];
    var commands = droppedElement.keywordJSON;
    var checkboxCounter = 2;

    if (document.getElementById(elementID) === null) {
        hidePropertiesPanel();
        return;
    }

    cleanPropertiesPanel();

    var propPanel = document.getElementById("propertiesPannel");

    // Adds the basic data through arguments
    var titleNode = document.createElement("p");
    var keywordName = droppedElement.name;
    titleNode.innerText = "Currently editing: " + keywordName;
    titleNode.id = "currentEditing";
    propPanel.appendChild(titleNode);

    for(var j=0; j< commands.length; j++){
        arguments = commands[j].arguments;
        if(arguments === null){
            continue;
        }

        // Add arguments in the properties panel
        for (var i = 0; i < arguments.length; i++) {
            var tempForm = document.createElement("form");

            // If the command need the argument in order to work
            if (arguments[i].requirement) {
                checkboxCounter++;

                var checkbox = document.createElement('input');
                checkbox.type = "checkbox";
                checkbox.id = checkboxCounter;
                
                checkbox.setAttribute("checked", true);
                checkbox.setAttribute("disabled", true);

                // Create a label with the argument name
                var labelNode = document.createElement('label');
                labelNode.innerText = arguments[i].name;
                labelNode.htmlFor = checkboxCounter;

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            } else {
                checkboxCounter++;

                var checkbox = document.createElement('input');
                checkbox.type = "checkbox";
                checkbox.id = checkboxCounter;

                if(arguments[i].visible !== undefined){
                    checkbox.setAttribute("checked", arguments[i].visible);
                }                            

                // Create a label with the argument name
                var labelNode = document.createElement('label');
                labelNode.innerText = arguments[i].name;
                labelNode.htmlFor = checkboxCounter;

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            }

            // If the argument needs a value then add an input form
            if (arguments[i].needs_value) {
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);
                
                if(arguments[i].value!== undefined){
                    inputNode.setAttribute('value', arguments[i].value);
                }            

                // Now it doesn't refresh the website if you press enter while typing on the form
                inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
                tempForm.appendChild(inputNode);
            }

            propPanel.appendChild(tempForm);
        }        
    }

    var tempDiv = document.createElement("div");
    tempDiv.className = "center";

    var buttonNode = document.createElement("input");
    buttonNode.setAttribute("type", "submit");
    buttonNode.setAttribute("value", "Set");
    buttonNode.className = "btn";

    buttonNode.addEventListener("click", function () {
        document.getElementById('btn_play').classList.add("pulse");
        addClickEvent();
    });

    function addClickEvent() {
        saveKeywordFromInput(droppedElementIndex, elementID);
    }

    var propPanelContainer = document.getElementById("propertiesPanelContainer");
    tempDiv.appendChild(buttonNode);
    propPanelContainer.appendChild(tempDiv);

    showPropertiesPanel();
}

function drawPropertiesPanel(droppedElementIndex, elementID) {
    var droppedElement = droppedElements[droppedElementIndex];
    var arguments = droppedElement.arguments;
    var checkboxCounter = 2;

    if (document.getElementById(elementID) === null) {
        hidePropertiesPanel();
        return;
    }

    // Clean previous properties panel
    var propPanel = document.getElementById("propertiesPannel");
    while (propPanel.hasChildNodes()) {
        propPanel.removeChild(propPanel.childNodes[0]);
    }

    // Adds the basic data through arguments
    var titleNode = document.createElement("p");
    var commandName = droppedElement.name;
    titleNode.innerText = "Currently editing: " + commandName;
    titleNode.id = "currentEditing";
    propPanel.appendChild(titleNode);

    if(droppedElement.category !== 1){
        propPanel = addExtraTextInput(propPanel, droppedElementIndex);
    }    

    // Add arguments in the properties panel
    for (var i = 0; i < arguments.length; i++) {
        var tempForm = document.createElement("form");

        // If the command need the argument in order to work
        if (arguments[i].requirement) {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;
            
            checkbox.setAttribute("checked", true);
            checkbox.setAttribute("disabled", true);

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        } else {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;

            if(arguments[i].visible !== undefined){
                checkbox.setAttribute("checked", arguments[i].visible);
            }                            

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        }

        // If the argument needs a value then add an input form
        if (arguments[i].needs_value) {
            var inputNode = document.createElement("input");
            inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);
            
            if(arguments[i].value!== undefined){
                inputNode.setAttribute('value', arguments[i].value);
            }            

            // Now it doesn't refresh the website if you press enter while typing on the form
            inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
            tempForm.appendChild(inputNode);
        }

        propPanel.appendChild(tempForm);
    }

    var tempDiv = document.createElement("div");
    tempDiv.className = "center";

    var buttonNode = document.createElement("input");
    buttonNode.setAttribute("type", "submit");
    buttonNode.setAttribute("value", "Set");
    buttonNode.className = "btn";

    buttonNode.addEventListener("click", function () {
        document.getElementById('btn_play').classList.add("pulse");
        addClickEvent();
    });

    function addClickEvent() {
        saveFromInput(droppedElementIndex, elementID);
    }

    propPanel.appendChild(tempDiv);
    propPanel.appendChild(buttonNode);

    showPropertiesPanel();
}

function drawPropertiesPanelWithTags(droppedElementIndex, elementID) {
    var droppedElement = droppedElements[droppedElementIndex];
    var arguments = droppedElement.arguments;
    var checkboxCounter = 2;

    if (document.getElementById(elementID) === null) {
        hidePropertiesPanel();
        return;
    }

    // Clean previous properties panel
    var propPanel = document.getElementById("propertiesPannel");
    while (propPanel.hasChildNodes()) {
        propPanel.removeChild(propPanel.childNodes[0]);
    }

    // Adds the basic data through arguments
    var titleNode = document.createElement("p");
    var commandName = droppedElement.name;
    titleNode.innerText = "Currently editing: " + commandName;
    titleNode.id = "currentEditing";
    propPanel.appendChild(titleNode);

    // Add arguments in the properties panel
    for (var i = 0; i < arguments.length; i++) {
        var tempForm = document.createElement("form");

                // If the command need the argument in order to work
        if (arguments[i].requirement) {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;
            
            checkbox.setAttribute("checked", true);
            checkbox.setAttribute("disabled", true);

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        } else {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;

            if(arguments[i].visible !== undefined){
                checkbox.setAttribute("checked", arguments[i].visible);
            }                            

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        }

        // If the argument needs value adds a input form
        if (arguments[i].needs_value) {
            if(arguments[i].name === "tags"){
                // Draw chips
                var inputNode = document.createElement("div");
                inputNode.setAttribute('class', 'chips-tags');
                inputNode.id = "chips-"+checkboxCounter;
                tempForm.appendChild(inputNode.cloneNode());

                $(function () {
                    $('.chips-tags').material_chip({
                        placeholder: 'Add Tags',
                        secondaryPlaceholder: '+Tag',
                    });
                });                 
            }
            else{
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);
                
                if(arguments[i].value!== undefined){
                    inputNode.setAttribute('value', arguments[i].value);
                }       

                // Now it doesn't refresh the website if you press enter while typing on the form
                inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
                tempForm.appendChild(inputNode);                
            }         
        }

        propPanel.appendChild(tempForm);
    }

    var tempDiv = document.createElement("div");
    tempDiv.className = "center";

    var buttonNode = document.createElement("input");
    buttonNode.setAttribute("type", "submit");
    buttonNode.setAttribute("value", "Set");
    buttonNode.className = "btn";

    buttonNode.addEventListener("click", function () {
        document.getElementById('btn_play').classList.add("pulse");
        addClickEvent();
    });

    function addClickEvent() {
        saveTagFromInput(droppedElementIndex, elementID);
    }

    propPanel.appendChild(tempDiv);
    propPanel.appendChild(buttonNode);

    showPropertiesPanel();
}

function showProperties(elementID, droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];
    
    var resultCategory = droppedElement.category;
    var tagsCategory = 1;
    var keywordsCategory = 6;

    var resultName = droppedElement.name;
    var tagsName = "tags";

    if (tagsCategory === resultCategory && tagsName === resultName) {
        drawPropertiesPanelWithTags(droppedElementIndex, elementID);
    }
    else if (keywordsCategory === resultCategory) {
        drawPropertiesForKeywords(droppedElementIndex, elementID);
    }    
    else {
        drawPropertiesPanel(droppedElementIndex, elementID);
    }
}