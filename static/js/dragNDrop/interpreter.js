class Interpreter{

	constructor(parametersSaver, dropCreator){
	this.parametersSaver = parametersSaver;
	this.dropCreator = dropCreator;
	}	

	translate(){
		var script = document.getElementById("terminal").value;

		document.getElementById("dragDropSpace").innerHTML = '';

		var lines = script.split(/\n/g);

		commentCounter = 0;
		forCounter = 0;
		variableCounter = 0;
		commandCounter = 0;
		tagCounter = 0;

		for (var i=0; i<lines.length; i++){

			var identationLevel = 0;
			var parameters = [];

			if(lines[i] === ''){
				return;
			}

			while (lines[i].charAt(0) == '\t'){
				lines[i] = lines[i].substring(1);
				identationLevel++;
			}

			if(lines[i].charAt(0) === "#"){
				parameters.push(lines[i].substring(1));

				var originalNodeID = "comment-drag-drop";
				commentCounter++;
				var newID = "comment"+commentCounter;
			}
			else if(lines[i].substring(0,2) === "${"){
				var lineStructure = lines[i].split(" ");
				var varName = lineStructure[0];
				varName = varName.substring(2, varName.length - 1 );
				var varValue = lineStructure[1];

				parameters.push(varName);
				parameters.push(varValue);

				var originalNodeID = "variable-drag-drop";
				variableCounter++;
				var newID = "variable"+variableCounter;
			}
			else if(lines[i].substring(0,6).toLowerCase() === "[tags]"){
				var lineStructure = lines[i].split("  ");
				for(var i=1; i<lineStructure.length; i++){
					parameters.push(lineStructure[i]);
				}

				var originalNodeID = "tag-drag-drop";
				tagCounter++;
				var newID = "tag"+tagCounter;
			}   
			else if(lines[i].substring(0,4).toLowerCase() === ":for"){
				var lineStructure = lines[i].split(" ");
				parameters.push(lineStructure[1]);
				parameters.push(lineStructure[3]);

				var originalNodeID = "for-drag-drop";

				forCounter++;
				var newID = "for"+forCounter;
			}                   
			else{
				parameters.push(lines[i].substring(7));

				var originalNodeID = "command-drag-drop";
				commandCounter++;
				var newID = "command"+commandCounter;
			}

			var newNode = document.getElementById(originalNodeID).cloneNode(true);
			newNode.id = newID;
			newNode.className = "drop-" + (identationLevel+1);

			this.dropCreator.createElementInTable(newNode);

			this.parametersSaver.saveToID(newNode.id, parameters);
		}
	}
}