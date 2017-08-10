var main = function(){
/********************************
			AJAX STUFF
*********************************/
//Getting CSRF token and applying it
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

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

//AJAX Function - Alert Later
	$('#alert_later').on('submit', function(e){
		//Prevents normal function from executing
		e.preventDefault();
		data = $('#id_date').val();
		$('#id_date').val('');
		$.ajax({
			data: {date: data},
			url: $(this).attr('action'),
			method: $(this).attr('method'),
			success: function(data){
				console.log('later');
			},
		});
	});

//AJAX Function - Alert Recurring
	$('#alert_recurring').on('submit', function(e){
		e.preventDefault();
		day = $('#id_day').val();
		time = $('#id_time').val();
		$('#id_day').val('');
		$('#id_time').val('');
		$.ajax({
			data: {day: day, time: time},
			url: $(this).attr('action'),
			method: $(this).attr('method'),
			success: function(data) {
				console.log('recurring');
			},
		});
	});

};

$(document).ready(main)