var user_ask_ques_page=1
$('.user-menu').append(function () {
    var str='';
    str+=' <div class="user-menu-list" data-link="ask_ques">\n' +
        '</div>'
    return str;
})
$('.user-menu .user-menu-list[data-link=ask_ques]').removeClass('hide').siblings().addClass('hide');
user_ask_ques()
function user_ask_ques() {
    $.ajax({
        url:user_link.ask_ques+user_ask_ques_page+'/',
        data:'',
        type:'post',
        success:function (data) {
            var list=data.data.my_questions

            $('.user-menu .user-menu-list[data-link="ask_ques"]').html(function () {
                var str='';
                if (list) {
                    str+= '            <ul class="user-ask-ques">' ;
                    for(var i=0;i<list.length;i++){

                        str+= '                <li>\n' +
                            '                    <a href="/question_detail/'+ list[i].id+'/0/1/1/"><div class="user-ask-ques-tit">'+list[i].content.replace(new RegExp('(<img[^>]+>)', 'g'),'图片').replace(new RegExp('(<[^>]+>)', 'g'),'')+'</div></a>\n' +
                            '                    <div class="user-atten-tag"><span>'+list[i].create_time+'</span><span>回答&nbsp;'+list[i].answer_count+'</span><span>关注&nbsp;'+list[i].attention_question_count+'</span></div>\n' +
                            '                </li>\n'
                    }
                    str+='            </ul>'
                    str+=user_page_coun(user_ask_ques_page,data,'user_ask_page_count')
                } else {
                    str += '<div class="no_comment">\n' +
                        '                <div class="no_comment_img"></div>\n' +
                        '                <div class="no_comment_text">目前暂无提问~</div>\n' +
                        '            </div>'
                }
                return str;
            })
        }
    })
}


$(document).on('click', '#user_ask_page_count li', function (e) {
    if ($(this).hasClass('page')) {
        user_ask_ques_page = Number($(this).attr('jp-data'));
        user_ask_ques()
    }
    if ($(this).hasClass('prev')) {
        user_ask_ques_page--;
        user_ask_ques()
    }
    if ($(this).hasClass('next')) {
        user_ask_ques_page++;
        user_ask_ques()
    }
    if ($(this).hasClass('first')) {
        user_ask_ques_page = 1;
        user_ask_ques()
    }
    if ($(this).hasClass('last')) {
        user_ask_ques_page = page_num;
        user_ask_ques()
    }

})
$(document).on('keyup','#user_ask_page_count input',function (e) {
    if(e.keyCode===13){
        user_ask_ques_page=$(this).val();
        user_ask_ques()
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})