function selectServerSide(config) {
    $.ajax({
        url: config.url,
        type: "GET",
        data: config.data,
        success: function (data) {
            var _select = document.getElementById(config.container);
            data.forEach(function (value) {
                var _option = document.createElement('option');
                _option.setAttribute('value', value.id);
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