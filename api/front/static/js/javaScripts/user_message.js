var user_mess_page=1
$('.user-menu').append(function () {
    var str='';
    str+='<div class="user-menu-list" data-link="mess">\n' +
        '            <ul class="user-mess">\n' +
        '            </ul>\n' +
        '        </div>'
    return str;
})
user_got_mess(1)
function user_got_mess(p) {
    $.ajax({
        url:'/my_messages/'+p+'/',
        type:'post',
        success:function (data) {
            if(data.code!==200){
                $('.user-menu .user-menu-list[data-link="mess"]').siblings().addClass('hide')
                return
            }
            var list=data.data.messages
            $('.user-menu .user-menu-list[data-link="mess"]').html(function () {
                var str = '';
                if (list) {
                    str+='<ul class="user-mess">'
                    for(var i=0;i<list.length;i++){
                        str += '                <li>\n' +
                            '                    <div class="user-mess-user"><span style="background: url(/images/avatar/'+list[i].replay_user_avatar+') no-repeat;background-size: cover;"></span></div>\n' +
                            '                    <div class="user-mess-content" >\n' +
                            '             <div class="color-link pointer" link="/question_detail/'+ list[i].question_id+'/0/1/1/">' +list[i].replay_name+'<span class="color-title">&nbsp;                回答了&nbsp;</span>'+list[i].question+'<span class="mar-left25 color-liter-grey">'+list[i].create_time+'</span><span class="right color-title ans_message"></span></div>\n' +
                            '                        <div class="mar-top10 wid-605">'+list[i].replay_answer+'</div>\n' +
                            '                    </div>\n' +
                            '                </li>'

                    }
                    str+='</ul>'
                    str += user_page_coun(p, data, 'user_message_page_count')
                } else {
                    str += '<div class="no_comment">\n' +
                        '                <div class="no_comment_img"></div>\n' +
                        '                <div class="no_comment_text">目前暂无消息~</div>\n' +
                        '            </div>'
                }
                return str;

            })
            $('.user-menu .user-menu-list[data-link="mess"]').siblings().addClass('hide')
        }
    })
}
$(document).on('click','#user_message_page_count .paginator li',function () {
    user_got_mess($(this).attr('jp-data'))
})
$(document).on('keyup', '.page_saver input', function (e) {
    if (e.keyCode === 13) {
        user_got_mess($(this).val())
        $(this).val('').blur();
    } else {
        if ($(this).val() > page_num) {
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g, ''))
    }
})
$(document).on('click','.user-mess-content .color-link',function () {
    window.open($(this).attr('link'))
})
$('.user-menu-list .user-mess-content').on('click','.ans_message',function () {

})
