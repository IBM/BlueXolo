var jsonAPIURL = {
    commands: "/apis/commands/",
    keywords: "/apis/keywords/",
    testcases: "/apis/testcases/",
}

// Unit testing
// testAJAX();
function testAJAX(){
    $.ajax({
        url: jsonAPIURL.commands,
        type: 'GET',
        data: {
            id: 2,
            extra: 1 //0 retorna sin argumentos, 1 con argumentos
        },
        success: function (data) {
            console.log("Unit testing in testAJAX in jsonManipulator.js was successfully completed");
            console.log(data);
        },
        error: function (error) {
            console.log("Unit testing in testAJAX in jsonManipulator.js got an error");
            console.log(error);            
            return false;
        }
    });
}

function addTestcaseToJSON(indentation, testcaseID) {
    $.ajax({
        url: jsonAPIURL.testcases + testcaseID + "/",
        type: 'GET',
        data: {
            id: testcaseID,
        },
        success: function (data) {
            var testcaseName = data.name;
            var testcaseArguments = data.arguments;
            var valuesAsString = data.values;
            var testcaseValues = JSON.parse(valuesAsString.replace(/&quot;/g, '"'));
            var testcaseCategory = 7;

            droppedElements.push({
                id: testcaseID,
                name: testcaseName,
                category: testcaseCategory,
                position: droppedElements.length,
                indentation: indentation,
                keywordJSON: testcaseValues,
                arguments: testcaseArguments,
                extraValue: undefined,
            });
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding a testcase to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addTestcaseToJSONInIndex(indentation, testcaseID, addElementInThisPosition){
    $.ajax({
        url: jsonAPIURL.testcases + testcaseID + "/",
        type: 'GET',
        data: {
            id: testcaseID,
        },
        success: function (data) {
            var testcaseName = data.name;
            var testcaseArguments = data.arguments;
            var valuesAsString = data.values;
            var testcaseValues = JSON.parse(valuesAsString.replace(/&quot;/g, '"'));
            var testcaseCategory = 7;

            var droppedElement = {
                id: testcaseID,
                name: testcaseName,
                category: testcaseCategory,
                position: droppedElements.length,
                indentation: indentation,
                keywordJSON: testcaseValues,
                arguments: testcaseArguments,
                extraValue: undefined,
            };
            droppedElements.splice(addElementInThisPosition, 0, droppedElement);
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding a testcase to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addKeywordToJSON(indentation, keywordID) {
    $.ajax({
        url: jsonAPIURL.keywords + keywordID + "/",
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
            console.log("Error while adding a keyword to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addKeywordToJSONInIndex(indentation, keywordID, addElementInThisPosition){

    $.ajax({
        url: jsonAPIURL.keywords + keywordID + "/",
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

            var droppedElement = {
                id: keywordID,
                name: keywordName,
                category: keywordCategory,
                position: droppedElements.length,
                indentation: indentation,
                keywordJSON: keywordValues,
                arguments: keywordArguments,
                extraValue: undefined,
            };
            droppedElements.splice(addElementInThisPosition, 0, droppedElement);
            drawElementsFromJSON();
        },
        error: function (error) {
            console.log("Error while adding a keyword to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addElementToJSON(indentation, commandID) {

    $.ajax({
        url: "/apis/commands/",
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
            console.log("Error while adding command to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}

function addElementToJSONInIndex(indentation, commandID, addElementInThisPosition) {

    $.ajax({
        url: "/apis/commands/",
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
            console.log("Error while adding command to JSON after being dropped");
            console.log(error);
            return false;
        }
    });
}