/*
    *This function populates selects "collection" (in Keywords, Testcases and TestSuites) and "phases" in Testcases
    
    *Because it needs to recover all phases that belong to the product it is an async function
    It recovers the data and then create options DOM objects within

    *If there were a previous value saved, the option with this ID would be selected
*/

function selectServerSide(config, selectIndex) {
    $.ajax({
        url: config.url,
        type: "GET",
        data: config.data,
        success: function (data) {
            var _select = document.getElementById(config.container);
            data.forEach(function (value) {
                var _option = document.createElement('option');
                _option.setAttribute('value', value.id);                

                if(value.id == selectIndex && selectIndex !== undefined){
                    _option.setAttribute('selected', true);
                }

                if (value.version) {
                    _option.innerHTML = value.name + ' - ' + value.version;
                } else {
                    _option.innerHTML = value.name;
                }
                _select.appendChild(_option);
                setTimeout(function () {
                    $('select').material_select();
                }, 100)
            })
        }, error: function (err) {
            console.log('Error retrive products: ' + err)
        }
    })
}