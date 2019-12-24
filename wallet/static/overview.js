$('document').ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#id_phone_number_validation_button").click(function() {
        const URL = '/accounts/phone_activation';
        const phone_number =  $.trim($("#id_phone_number_field").val());
        $.post(URL, {'phone_number': phone_number}, function(){
            confirmation.open();
        });
    });

    $("#id_phone_number_confirmation_button").click(function() {
        const URL = '/accounts/phone_validation';
        const validation_code =  $.trim($("#id_phone_validation_code_field").val());
        $.post(URL, {'code': validation_code}, function(){
            $("#id_phone_number_confirmation_button").insertAfter('<p>Number successfully validated</p>')
            setTimeout(function(){confirmation.close()}, 5000);
        });
    });
    
    $("#id_phone_code_resend_button").click(function() {
        const URL = '/accounts/phone_resend_code';
        $.get(URL, function(){
            $("#id_phone_code_resend_button").insertAfter('<p>New validation SMS sent</p>')
        });
    });
});
