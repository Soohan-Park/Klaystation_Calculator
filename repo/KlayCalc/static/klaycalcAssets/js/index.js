function calcIndex(_addr) {
    // common.js -> isValidAddr
    if (isValidAddr(_addr)) {
        location.href = '/account/' + _addr
    } else {
        alert("ERROR")
    }

}


$(function () {
    $('#sidebar_index').addClass('active')
    $('#navbar_title').text('Main')
    $('#navbar_title').click( function () {
        alert('이스터에그')
    } )


    $('#calcBtn').click( function () {
        let addr = $('#addr').val()

        calcIndex(addr)  // In common.js
    })
})