function calcPer(_value) {
    var target = $('#' + _value)
    
    $('#calcMenu').text( target.text() )
    $('#calcReward').text( target.attr('value') )
}


$(function () {
    $('#sidebar_account').addClass('active')
    $('#navbar_title').text('나의 KLAY 보상')

    $('#loading').hide()

    // Calc Default Setting
    $('#calcMenu').text( $('#calcDay').text() )
    calcPer('calcDay')

    $('a[name=calcPeriod]').click( function () {
        let id = $(this).attr('id')

        calcPer(id)
    })
})