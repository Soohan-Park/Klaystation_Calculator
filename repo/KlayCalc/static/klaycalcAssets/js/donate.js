// CSRF Setup - For POST Method.
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
////////////////////////////////


$(function () {
    $('#sidebar_donate').addClass('active')
    $('#navbar_title').text('커피 한 잔')

    $('#loading').hide()

    // 기부 주소 유효성 체크
    $.post(
        '/checkDonateAddr/',
        { 'donateAddr' : $('#donateAddr').text() },
        (res) => {
            if (res == 'False') {  // 주소가 다를 경우
                alert('기부 주소가 변조되었습니다. 곤리자에게 문의해 주세요.')
            }
        }
    )

    
    // 주소 복사
    $('#copyAddr').click( function () {
        // Copy Address.
        // input box가 hidden 처리되면 안됨.
        $('#copyDonateAddr').select()
        document.execCommand('copy')

        alert("Copied!")
    })
})