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

function addExtraTextInput(propPanelNode, droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];
    var tempForm = document.createElement("form");

    var inputNode = document.createElement("input");
    inputNode.setAttribute('placeholder', 'Write an extra value');

    if (droppedElement.extraValue !== undefined) {
        inputNode.setAttribute('value', droppedElement.extraValue);
    }

    // Now it doesn't refresh the website if you press enter while typing on the form
    inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
    tempForm.appendChild(inputNode);
    propPanelNode.appendChild(tempForm);

    return propPanelNode;
}

function cleanPropertiesPanel() {
    var propPanel = document.getElementById("propertiesPannel");
    while (propPanel.hasChildNodes()) {
        propPanel.removeChild(propPanel.childNodes[0]);
    }

    var propPanelContainer = document.getElementById("propertiesPanelContainer");

    var indexOfButton = 3;
    var previousButtonNode = propPanelContainer.childNodes[indexOfButton];
    if (previousButtonNode !== undefined) {
        propPanelContainer.removeChild(previousButtonNode);
    }
}

function getIfArgumentIsEmpty(argument) {
    var hasValue = false;
    var isChecked = undefined;

    if (argument.value !== undefined || argument.value !== "") {
        hasValue = true;
    }
    if (argument.needs_value && argument.visible !== undefined) {
        isChecked = argument.visible;
    }

    if (argument.needs_value && !hasValue) {
        return false;
    }
    else if (argument.requirement || isChecked !== undefined || argument.visible) {
        return false;
    }
    else {
        return true;
    }
}

function drawKeywordsProperties(keywordJSON) {
    var checkboxCounter = 2;

    var propPanel = document.getElementById("propertiesPannel");
    commands = keywordJSON;

    for (var j = 0; j < commands.length; j++) {
        arguments = commands[j].arguments;

        if (arguments === null) {
            continue;
        }

        // Add arguments in the properties panel 
        for (var i = 0; i < arguments.length; i++) {

            if (getIfArgumentIsEmpty(arguments[i])) {
                continue;
            }

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

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            } else {
                checkboxCounter++;

                var checkbox = document.createElement('input');
                checkbox.type = "checkbox";
                checkbox.id = checkboxCounter;

                if (arguments[i].visible !== undefined) {
                    checkbox.setAttribute("checked", arguments[i].visible);
                }

                // Create a label with the argument name 
                var labelNode = document.createElement('label');
                labelNode.innerText = arguments[i].name;
                labelNode.htmlFor = checkboxCounter;

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            }

            // If the argument needs a value then add an input form 
            if (arguments[i].needs_value) {
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);

                if (arguments[i].value !== undefined) {
                    inputNode.setAttribute('value', arguments[i].value);
                }

                // Now it doesn't refresh the website if you press enter while typing on the form 
                inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
                tempForm.appendChild(inputNode);
            }

            propPanel.appendChild(tempForm);
        }
    }

    return checkboxCounter;
}

function drawPropertiesForTestcases(droppedElementIndex, elementID) {
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

    var keywordsCategory = 6;
    var testcaseCategory = 7;

    for (var j = 0; j < commands.length; j++) {
        arguments = commands[j].arguments;
        if (arguments === null) {
            continue;
        }

        if (commands[j].category === keywordsCategory) {
            checkboxCounter = drawKeywordsProperties(commands[j].keywordJSON);
            continue;
        }

        // Add arguments in the properties panel 
        for (var i = 0; i < arguments.length; i++) {

            if (getIfArgumentIsEmpty(arguments[i])) {
                continue;
            }

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

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            } else {
                checkboxCounter++;

                var checkbox = document.createElement('input');
                checkbox.type = "checkbox";
                checkbox.id = checkboxCounter;

                if (arguments[i].visible !== undefined) {
                    checkbox.setAttribute("checked", arguments[i].visible);
                }

                // Create a label with the argument name
                var labelNode = document.createElement('label');
                labelNode.innerText = arguments[i].name;
                labelNode.htmlFor = checkboxCounter;

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            }

            // If the argument needs a value then add an input form
            if (arguments[i].needs_value) {
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);

                if (arguments[i].value !== undefined) {
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
    tempDiv.className = "center section";

    var buttonNode = document.createElement("input");
    buttonNode.setAttribute("type", "submit");
    buttonNode.setAttribute("value", "Set");
    buttonNode.className = "btn";

    buttonNode.addEventListener("click", function () {
        document.getElementById('btn_play').classList.add("pulse");
        addClickEvent();
    });

    function addClickEvent() {
        saveTestcaseFromInput(droppedElementIndex, elementID);
    }

    var propPanelContainer = document.getElementById("propertiesPanelContainer");
    tempDiv.appendChild(buttonNode);
    propPanelContainer.appendChild(tempDiv);

    showPropertiesPanel();
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

    for (var j = 0; j < commands.length; j++) {
        arguments = commands[j].arguments;

        if (arguments === null) {
            continue;
        }

        // Add arguments in the properties panel
        for (var i = 0; i < arguments.length; i++) {

            if (getIfArgumentIsEmpty(arguments[i])) {
                continue;
            }

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

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            } else {
                checkboxCounter++;

                var checkbox = document.createElement('input');
                checkbox.type = "checkbox";
                checkbox.id = checkboxCounter;

                if (arguments[i].visible !== undefined) {
                    checkbox.setAttribute("checked", arguments[i].visible);
                }

                // Create a label with the argument name
                var labelNode = document.createElement('label');
                labelNode.innerText = arguments[i].name;
                labelNode.htmlFor = checkboxCounter;

                labelNode.setAttribute("onclick", "fixScroll(event)");

                tempForm.appendChild(checkbox);
                tempForm.appendChild(labelNode);
            }

            // If the argument needs a value then add an input form
            if (arguments[i].needs_value) {
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);

                if (arguments[i].value !== undefined) {
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
    tempDiv.className = "center section";

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

function fixScroll(event) {
    event.preventDefault();

    var thisBelongsTo = event.target.htmlFor;
    var checkboxToClick = document.getElementById(thisBelongsTo);

    checkboxToClick.click();
}

function drawPropertiesPanel(droppedElementIndex, elementID) {
    var droppedElement = droppedElements[droppedElementIndex];
    var arguments = droppedElement.arguments;
    var checkboxCounter = 2;

    if (document.getElementById(elementID) === null) {
        hidePropertiesPanel();
        return;
    }

    cleanPropertiesPanel();

    var propPanel = document.getElementById("propertiesPannel");

    // Adds the basic data through arguments
    var titleNode = document.createElement("p");
    var commandName = droppedElement.name;
    titleNode.innerText = "Currently editing: " + commandName;
    titleNode.id = "currentEditing";
    propPanel.appendChild(titleNode);

    if (droppedElement.category !== 1) {
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

            labelNode.setAttribute("onclick", "fixScroll(event)");

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        } else {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;

            if (arguments[i].visible !== undefined) {
                checkbox.setAttribute("checked", arguments[i].visible);
            }

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            labelNode.setAttribute("onclick", "fixScroll(event)");

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        }

        // If the argument needs a value then add an input form
        if (arguments[i].needs_value) {
            var inputNode = document.createElement("input");
            inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);

            if (arguments[i].value !== undefined) {
                inputNode.setAttribute('value', arguments[i].value);
            }

            // Now it doesn't refresh the website if you press enter while typing on the form
            inputNode.setAttribute('onkeypress', 'return event.keyCode != 13');
            tempForm.appendChild(inputNode);
        }

        propPanel.appendChild(tempForm);
    }

    var tempDiv = document.createElement("div");
    tempDiv.className = "center section";

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

    var propPanelContainer = document.getElementById("propertiesPanelContainer");
    tempDiv.appendChild(buttonNode);
    propPanelContainer.appendChild(tempDiv);

    showPropertiesPanel();
}

function convertArrayIntoChipsData(array) {
    var chipsData = [];

    for (var i = 0; i < array.length; i++) {
        var newTag = {
            tag: array[i]
        }
        chipsData.push(newTag);
    }

    return chipsData;
}

function drawPropertiesPanelWithTags(droppedElementIndex, elementID) {
    var droppedElement = droppedElements[droppedElementIndex];
    var arguments = droppedElement.arguments;
    var checkboxCounter = 2;

    if (document.getElementById(elementID) === null) {
        hidePropertiesPanel();
        return;
    }

    cleanPropertiesPanel();

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

            labelNode.setAttribute("onclick", "fixScroll(event)");

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        } else {
            checkboxCounter++;

            var checkbox = document.createElement('input');
            checkbox.type = "checkbox";
            checkbox.id = checkboxCounter;

            if (arguments[i].visible !== undefined) {
                checkbox.setAttribute("checked", arguments[i].visible);
            }

            // Create a label with the argument name
            var labelNode = document.createElement('label');
            labelNode.innerText = arguments[i].name;
            labelNode.htmlFor = checkboxCounter;

            labelNode.setAttribute("onclick", "fixScroll(event)");

            tempForm.appendChild(checkbox);
            tempForm.appendChild(labelNode);
        }

        // If the argument needs value adds a input form
        if (arguments[i].needs_value) {
            if (arguments[i].name === "tags") {
                // Draw chips
                var inputNode = document.createElement("div");
                inputNode.setAttribute('class', 'chips-tags');
                inputNode.id = "chips-" + checkboxCounter;
                tempForm.appendChild(inputNode.cloneNode());

                if (arguments[i].value) {
                    var tagsData = arguments[i].value.split("; ");
                    tagsData = convertArrayIntoChipsData(tagsData);
                }

                $(function () {
                    $('.chips-tags').material_chip({
                        data: tagsData,
                        placeholder: 'Add Tags',
                        secondaryPlaceholder: '+Tag',
                    });
                });
            }
            else {
                var inputNode = document.createElement("input");
                inputNode.setAttribute('placeholder', 'Write a value for ' + arguments[i].name);

                if (arguments[i].value !== undefined) {
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
    tempDiv.className = "center section";

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

    var propPanelContainer = document.getElementById("propertiesPanelContainer");
    tempDiv.appendChild(buttonNode);
    propPanelContainer.appendChild(tempDiv);

    showPropertiesPanel();
}

function showProperties(elementID, droppedElementIndex) {
    var droppedElement = droppedElements[droppedElementIndex];

    var resultCategory = droppedElement.category;
    var tagsCategory = 1;
    var keywordsCategory = 6;
    var testcaseCategory = 7;

    var resultName = droppedElement.name;
    var tagsName = "tags";

    if (tagsCategory === resultCategory && tagsName === resultName) {
        drawPropertiesPanelWithTags(droppedElementIndex, elementID);
    }
    else if (keywordsCategory === resultCategory) {
        drawPropertiesForKeywords(droppedElementIndex, elementID);
    }
    else if (testcaseCategory === resultCategory) {
        drawPropertiesForTestcases(droppedElementIndex, elementID);
    }
    else {
        drawPropertiesPanel(droppedElementIndex, elementID);
    }
}