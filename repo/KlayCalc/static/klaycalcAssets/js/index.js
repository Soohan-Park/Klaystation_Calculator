function calcIndex(_addr) {
    // common.js -> isValidAddr
    if (isValidAddr(_addr)) {
        $('#loading').show()
        location.href = '/account/' + _addr
    } else {
        alert("올바른 클레이튼 주소를 입력해주세요.")
    }
}


$(function () {
    $('#sidebar_index').addClass('active')
    $('#navbar_title').text('클레이스테이션 계산기')
    
    $('#loading').hide()

    $('#checkMark_T').hide()
    $('#checkMark_F').hide()
    
    
    // 글자 수 조회
    $('#addr').keyup( function () {
        var address = $(this).val()
        
        if (address.length == 0) {
            $('#checkMark_T').hide()
            $('#checkMark_F').hide()
        }
        else if (address.length == 42) {
            $('#checkMark_F').hide()
            $('#checkMark_T').show()
            $('#inputKlaytnAddr').removeClass('has-danger')
            $('#inputKlaytnAddr').addClass('has-success')
        }
        else {
            $('#checkMark_T').hide()
            $('#checkMark_F').show()
            $('#inputKlaytnAddr').removeClass('has-success')
            $('#inputKlaytnAddr').addClass('has-danger')
        }
    })

    // 주소 조회
    $('#calcBtn').click( function () {
        let addr = $('#addr').val()

        calcIndex(addr)  // In common.js
    })
})