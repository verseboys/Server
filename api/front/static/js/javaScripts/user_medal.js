var user_mess_page=1
$('.user-menu').append(function () {
    var str='';
    str+='<div class="user-menu-list" data-link="medal">\n' +
        '            <ul class="user-mess">\n' +
        '            </ul>\n' +
        '        </div>'
    return str;
})
user_got_medal(1)
function user_got_medal() {
    $.ajax({
        url:'/get_achievements/',
        type:'get',
        success:function (data) {
            if(data.code!==200){
                $('.user-menu .user-menu-list[data-link="medal"]').siblings().addClass('hide')
                return
            }
            let medal_list=data.data
        }
    })
}

