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
        $('#loading').show()
        location.href = '/account/' + addr
    } else {
        alert("올바른 클레이튼 주소를 입력해주세요.")
    }

}


function isValidAddr(_addr) {
    if (_addr.length != 42) return false
    if (!(_addr[0] == '0' && _addr[1] == 'x')) return false

    return true
}


