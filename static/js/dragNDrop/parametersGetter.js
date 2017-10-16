function getParametersByID(elementID) {
    var dropppedElement = document.getElementById(elementID + "-" + "parameters");

    if (dropppedElement === null) {
        return;
    }

    var lis = dropppedElement.getElementsByTagName("li");

    var parameters = [];
    for (var i = 0; i < lis.length; i++) {
        parameters.push(lis[i].innerText);
    }
    return parameters;
}

function getValuesByID(elementID) {
    var lis = document.getElementById(elementID + "-" + "parameters").getElementsByTagName("li");
    var parameters = [];
    for (var i = 0; i < lis.length; i++) {
        var argumentName = lis[i].innerText.split(":")[0];
        var checked = lis[i].innerText.split(":")[1];
        var value = lis[i].innerText.split(":")[2];

        if (value === undefined) {
            value = checked;
        }

        var parameter = {
            "checked": checked,
            "value": value,
            "argument_Name": argumentName,
        }
        parameters.push(parameter);
    }
    return parameters;
}

function getParametersByCommand(elementType) {
    var parameters = [];

    parametersJSON.forEach(function (commandJSON) {
        if (commandJSON.name === elementType) {
            parameters = commandJSON.arguments;
        }
    });

    return parameters;
}

function getAllValuesInTable() {
    var dragNDrop = document.getElementById("dragDropSpace");
    var rowsInTable = dragNDrop.children;
    rowsInTable = Array.from(rowsInTable);
    var allValues = [];

    rowsInTable.forEach(function (row) {
        var commandInRowID = row.children[1].id;
        var commandValues = getValuesByID(commandInRowID);

        var newKeywordValue = {
            "id": commandInRowID.split("-")[0],
            "values": commandValues,
        };
        allValues.push(newKeywordValue);

    });
    return allValues
}