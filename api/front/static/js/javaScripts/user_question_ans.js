var user_ans_ques_page=1
$('.user-menu').append(function () {
    var str = '';
    str += ' <div class="user-menu-list" data-link="ans_ques"></div>';

    return str;
})
$('.user-menu .user-menu-list[data-link=ans_ques]').removeClass('hide').siblings().addClass('hide');
function user_ans_ques() {
    $.ajax({
        url: user_link.ans_ques+user_ans_ques_page+'/',
        type: 'post',
        success: function (data) {
            $('.user-menu .user-menu-list[data-link="ans_ques"]').html(function () {
                return   user_ans_ques_data(data)
            })
        }
    })
}
user_ans_ques();

function user_ans_ques_data(data) {
    var str='';

    if(data.code===200) {
        str += '            <ul class="user-collect-list mar-Top0">\n'
            var list=data.data.my_answers;

        for(var i=0;i<list.length;i++){
            str+='                <li>\n' +
                '                    <a href="/question_detail/'+list[i].question_id+'/0/1/1/"><div class="user-collect-list-title">'+list[i].question_content.replace(new RegExp('(<img[^>]+>)', 'g'),'图片').replace(new RegExp('(<[^>]+>)', 'g'),'')+'</div></a>\n' +
                '                    <div class="inline user-collect-list-img"><a href="javsscript:;"><span class="user" style="background: url('+'/images/avatar/'+list[i].answer_user_avatar+'); background-size: cover;"></span></a></div>\n' +
                '                    <div class="inline user-collect-list-text">\n' +
                '                        <a href="javsscript:;"><div class="user-collect-list-name">'+list[i].answer_user_username+' </div></a>\n' ;
            if(new RegExp('(<img[^>]+>)', 'g').test(list[i].answer_comment)){
                var s= list[i].answer_comment.replace(new RegExp('(<img[^>]+>)', 'g'), '图片').replace(new RegExp('(<[^>]+>)', 'g'), '')
                    str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '<span style="display: none">' + list[i].answer_comment + '</span><span class="color-link pointer" >展开</span></div>\n';

            }else {
                var s = list[i].answer_comment.replace(new RegExp('(<img[^>]+>)', 'g'), '图片').replace(new RegExp('(<[^>]+>)', 'g'), '')
                if (getBt(s) > 184) {
                    str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '<span style="display: none">' + list[i].answer_comment + '</span><span class="color-link pointer">展开</span></div>\n';
                } else {
                    str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '</div>\n';
                }

            }
            var pris = list[i].praise_count === 1 ? ("已赞 " + list[i].praise_count) : list[i].praise_count
                str+='                        <div class="user-collect-list-tag"><span>'+list[i].answer_create_time+'</span><span class="user-comm">评论 '+list[i].child_answer_count+'</span><span class="user-fig pointer"  ques_id="'+ list[i].answer_id+'">'+ pris+'</span></div>\n' +
                '                    </div>\n' +
                '                                                                                                                                        </li>\n' ;
        }



            str+='            </ul>';
        // if(getBt(str)>=184){
        //     str+= '<div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可 <span class="color-link">展开</span></div>'
        // }else {
        //     str+= '<div class="user-collect-list-artic">一项新的治疗措施是否值得临床推广，除了要求具备足够的疗效外，还应当要求具备一定的安全性。疗效和安全性对于治疗措施的评价是同等重要的，在研究过程中研究者需要综合权衡，然后判断该措施是否可 </div>'
        // }

        str+=user_page_coun(user_ans_ques_page,data,'user_ans_page_count')
    }else {
        str += '<div class="no_comment">\n' +
            '                <div class="no_comment_img"></div>\n' +
            '                <div class="no_comment_text">您还没有回答过问题哦~</div>\n' +
            '            </div>'
    }
return str
}

$(document).on('click', '#user_ans_page_count li', function (e) {
    if ($(this).hasClass('page')) {
        user_ans_ques_page = Number($(this).attr('jp-data'));
        user_ans_ques()
    }
    if ($(this).hasClass('prev')) {
        user_ans_ques_page--;
        user_ans_ques()
    }
    if ($(this).hasClass('next')) {
        user_ans_ques_page++;
        user_ans_ques()
    }
    if ($(this).hasClass('first')) {
        user_ans_ques_page = 1;
        user_ans_ques()
    }
    if ($(this).hasClass('last')) {
        user_ans_ques_page = page_num;
        user_ans_ques()
    }


})
$(document).on('keyup','#user_ans_page_count input',function (e) {
    if(e.keyCode===13){
        user_ans_ques_page=$(this).val();
        user_ans_ques()
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})
$(document).on('click','.user-menu-list[data-link="ans_ques"] .user-collect-list-artic span.pointer',function () {
    var a=$(this).prev().html();
    $(this).parent().html(a)
})