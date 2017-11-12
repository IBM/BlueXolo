function addKeywordToJSON(indentation, keywordID) {
    $.ajax({
        url: "/apis/keywords/" + keywordID + "/",
        type: 'GET',
        data: {
            id: keywordID,
        },
        success: function (data) {
            var keywordName = data.name;
            var keywordArguments = data.arguments;
            var valuesAsString = data.values;
            var keywordValues = JSON.parse(valuesAsString.replace(/&quot;/g, '"'));
            var keywordCategory = 6;

            droppedElements.push({
                id: keywordID,
                name: keywordName,
                category: keywordCategory,
                position: droppedElements.length,
                indentation: indentation,
                keywordJSON: keywordValues,
                arguments: keywordArguments,
                extraValue: undefined,
            });
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding element to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addElementToJSON(indentation, commandID) {

    $.ajax({
        url: "{% url 'api-commands' %}",
        type: 'GET',
        data: {
            id: commandID,
            extra: 1 //0 retorna sin argumentos, 1 con argumentos
        },
        success: function (data) {
            var commandName = data.results[0].name;
            var commandArguments = data.results[0].arguments;
            var commandCategory = data.results[0].source[0].category;
            var commandSource = data.results[0].source[0];

            droppedElements.push({
                id: commandID,
                name: commandName,
                category: commandCategory,
                position: droppedElements.length,
                indentation: indentation,
                arguments: commandArguments,
                source: commandSource,
                extraValue: undefined,
            });
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding element to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addElementToJSONInIndex(indentation, commandID, addElementInThisPosition) {

    $.ajax({
        url: "{% url 'api-commands' %}",
        type: 'GET',
        data: {
            id: commandID,
            extra: 1 //0 retorna sin argumentos, 1 con argumentos
        },
        success: function (data) {
            var commandName = data.results[0].name;
            var commandArguments = data.results[0].arguments;
            var commandCategory = data.results[0].source[0].category;
            var commandSource = data.results[0].source[0];

            var droppedElement = {
                id: commandID,
                name: commandName,
                category: commandCategory,
                position: droppedElements.length,
                indentation: indentation,
                arguments: commandArguments,
                source: commandSource,
                extraValue: undefined,
            };
            droppedElements.splice(addElementInThisPosition, 0, droppedElement);
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding element to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}