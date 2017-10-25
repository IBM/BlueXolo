function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", document.getElementsByName('csrfmiddlewaretoken')[0].value);
        }
    }
});

function drawMessage(msg, _class) {
    var _class_color = _class || '';
    var _msg = $('<span class="' + _class_color + '">' + msg + '</span>');
    Materialize.toast(_msg, 12000);
}