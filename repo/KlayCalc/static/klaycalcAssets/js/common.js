/*
    common.js
    ---
    Script for Common Pages.
*/
// Search
function calcSearch() {
    let addr = $('#search_addr').val()

    // 유효성 검증 필요
    if (isValidAddr(addr)) {
        location.href = '/account/' + addr
    } else {
        alert("ERROR")
    }

}


function isValidAddr(_addr) {
    if (_addr.length != 42) return false

    return true
}


