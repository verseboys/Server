/*
* 关注问题
* */
var user_atten_url='';
var user_ques_page=1,user_peo_page=1,user_fan_page=1;
var user_atten_page=1
function user_atten_questions() {
    user_atten_page=user_ques_page
    $.ajax({
        url:user_link.atten_ques+user_ques_page+'/',
        type:'post',
        data:'',
        success:function (data) {
            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').html('');
            var list=data.data.attention_questions
            var str=''
            if (list) {
                str+='<ul class="list">';
                for(var i=0;i<list.length;i++) {

                    str += '                        <li>\n' +
                        '                            <a href="/question_detail/'+list[i].id+'/0/1/1/">\n' +
                        '                            <div class="user-atten-tit">' + list[i].question.replace(new RegExp('(<img[^>]+>)', 'g'),'图片').replace(new RegExp('(<[^>]+>)', 'g'),'') + '<span class="user-tag-icon">' + list[i].question_category + '</span></div>\n' +
                        '                            </a>\n' +
                        '                                <div class="user-atten-tag"><span>'+list[i].create_time+'</span><span>回答&nbsp;'+list[i].answer_count+'</span><span>关注&nbsp;'+list[i].attention_count+'</span></div>\n' +
                        '                        </li>'
                }
                str+= '                   </ul>';
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">您还没有关注问题哦~</div>\n' +
                    '            </div>'
            }

            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').append(str);
            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').append( user_page_coun(user_ques_page,data,'user_ques_page_count'));

        },
        error:function () {
            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').html('');
            var list=data.data.attention_questions
                var str=''
            if (list) {
             str+='<ul class="list">';
                for(var i=0;i<list.length;i++) {

                    str += '                        <li>\n' +
                     '                            <a href="/question_detail/'+list[i].id+'/0/1/1/">\n' +
                     '                            <div class="user-atten-tit">' + list[i].question.replace(new RegExp('(<img[^>]+>)', 'g'),'图片').replace(new RegExp('(<[^>]+>)', 'g'),'') + '<span class="user-tag-icon">' + list[i].question_category + '</span></div>\n' +
                     '                            </a>\n' +
                     '                                <div class="user-atten-tag"><span>'+list[i].create_time+'</span><span>回答&nbsp;'+list[i].answer_count+'</span><span>关注&nbsp;'+list[i].attention_count+'</span></div>\n' +
                     '                        </li>'
                    }
               str+= '                   </ul>';
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">您还没有关注问题哦~</div>\n' +
                    '            </div>'
            }

            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').append(str);
            $('.user-menu .user-menu-list[data-link=atten] div div[type=ques]').append( user_page_coun(user_ques_page,data,'user_ques_page_count'));

        }
    })
}
function user_atten_per() {
    user_atten_url='2'
    user_atten_page=user_peo_page
    $.ajax({
        url:user_atten_url,
        type:'post',
        data:'',
        success:function (data) {

        },
        error:function (data) {
            $('.user-menu .user-menu-list[data-link=atten] div div[type=user]').html('');
var str='';
            if (true) {
            str+='<ul class="user-atten-fan">\n' +
    '                    <li>\n' +
    '                        <div class="inline align-top user-atten-fan-user"><a href=""><span></span></a></div>\n' +
    '                        <div class="inline align-top user-atten-fan-box">\n' +
    '                            <a href=""><div class="user-atten-fan-name">呵呵</div></a>\n' +
    '                            <div class="user-atten-fan-content">北京大学临床流行病与统计啊现就职于北大国际医学院流行病科</div>\n' +
    '                            <div class="user-atten-fan-tag"><span>粉丝&nbsp;68</span><span>回答&nbsp;111</span></div>\n' +
    '                        </div>\n' +
    '                        <div class="inline align-cen user-atten-fan-att checked">已关注</div>\n' +
    '                    </li> <li>\n' +
    '                        <div class="inline align-top user-atten-fan-user"><a href=""><span></span></a></div>\n' +
    '                        <div class="inline align-top user-atten-fan-box">\n' +
    '                            <a href=""><div class="user-atten-fan-name">呵呵</div></a>\n' +
    '                            <div class="user-atten-fan-content">北京大学临床流行病与统计啊现就职于北大国际医学院流行病科</div>\n' +
    '                            <div class="user-atten-fan-tag"><span>粉丝&nbsp;68</span><span>回答&nbsp;111</span></div>\n' +
    '                        </div>\n' +
    '                        <div class="inline align-cen user-atten-fan-att checked">已关注</div>\n' +
    '                    </li>\n' +
    '                </ul>';
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">您还没有关注任何人哦~</div>\n' +
                    '            </div>'
            }
            $('.user-menu .user-menu-list[data-link=atten] div div[type=user]').append(str);
            $('.user-menu .user-menu-list[data-link=atten] div div[type=user]').append( user_collect_page_coun(user_fan_page,data,'user_per_page_count'));
        }
    })
}
function user_atten_fan() {
    user_atten_page=user_fan_page
    user_atten_url='3'
    $.ajax({
        url:user_atten_url,
        type:'post',
        data:'',
        success:function (data) {

        },
        error:function () {
            $('.user-menu .user-menu-list[data-link=atten] div div[type=fan]').html('');
var str='';
            if (true) {
             str+='<ul class="user-atten-fan">\n' +
                '                    <li>\n' +
                '                        <div class="inline align-top user-atten-fan-user"><a href=""><span></span></a></div>\n' +
                '                        <div class="inline align-top user-atten-fan-box">\n' +
                '                            <a href=""><div class="user-atten-fan-name">呵呵</div></a>\n' +
                '                            <div class="user-atten-fan-content">北京大学临床流行病与统计啊现就职于北大国际医学院流行病科</div>\n' +
                '                            <div class="user-atten-fan-tag"><span>粉丝&nbsp;68</span><span>回答&nbsp;111</span></div>\n' +
                '                        </div>\n' +
                '                        <div class="inline align-cen user-atten-fan-att">关注</div>\n' +
                '                    </li>\n' +
                '                    <li>\n' +
                '                        <div class="inline align-top user-atten-fan-user"><a href=""><span></span></div>\n' +
                '                        <div class="inline align-top user-atten-fan-box">\n' +
                '                            <a href=""><div class="user-atten-fan-name">呵呵</div></a>\n' +
                '                            <div class="user-atten-fan-content">北京大学临床流行病与统计啊现就职于北大国际医学院流行病科</div>\n' +
                '                            <div class="user-atten-fan-tag"><span>粉丝&nbsp;68</span><span>回答&nbsp;111</span></div>\n' +
                '                        </div>\n' +
                '                        <div class="inline align-cen user-atten-fan-att checked">互相关注</div>\n' +
                '                    </li>\n' +
                '                </ul>'
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">您还没有粉丝哦~</div>\n' +
                    '            </div>'
            }
            $('.user-menu .user-menu-list[data-link=atten] div div[type=fan]').append(str);
            $('.user-menu .user-menu-list[data-link=atten] div div[type=fan]').append( user_collect_page_coun(user_fan_page,data,'user_fan_page_count'));
        }
    })
}
$('.user-menu').append(function () {
    var str='';
    str+='<div class="user-menu-list" data-link="atten">\n' +
        // '            <div class="user-atten-top">\n' +
        // '                <ul class="user_tag_change user_tag_change_atten">\n' +
        // '                    <li class="checked" type="ques">关注的问题</li>\n' +
        // // '                    <li type="user">关注的人</li>\n' +
        // // '                    <li type="fan">粉丝</li>\n' +
        // '                </ul>\n' +
        // '            </div>\n' +
        '            <div class="user-attenbot-box">\n' +
        '            <!--关注的问题-->\n' +
        '            <div class="user-atten-bot" type="ques">\n' +
        '            </div>\n' +
        '            <!--关注的人-->\n' +
        '            <div class="hide "  type="user">\n' +
        '            </div>\n' +
        '            <!--粉丝-->\n' +
        '            <div class="hide" type="fan">\n' +
        '            </div>\n' +
        '            </div>\n' +
        '        </div>';
    return str;
})
$('.user-menu .user-menu-list[data-link="atten"]').siblings().addClass('hide');
user_atten_questions();

$(document.body).on('click','.user_tag_change_atten li',function () {
    $(this).addClass('checked').siblings().removeClass('checked');
    var type=$(this).attr('type');
    $('.user-menu .user-menu-list[data-link=atten] div div[type='+type+']').removeClass('hide').siblings().addClass('hide')
   switch (type){
       case "ques":
           user_atten_questions();
           break;
       case "user":
           user_atten_per();
           break;
       case "fan":
           user_atten_fan();
           break;
   }
});

/*
* 关注*/
$('.user-menu .user-menu-list[data-link=atten] div div[type=user]').on('click','.user-atten-fan-att',function () {
    if($(this).hasClass('checked')) {

        $(this).removeClass('checked').html('关注');


    }else {

        $(this).addClass('checked').html('已关注');


    }
})
$('.user-menu .user-menu-list[data-link=atten] div div[type=fan]').on('click','.user-atten-fan-att',function () {
    if($(this).hasClass('checked')){


        $(this).removeClass('checked').html('关注');


    }else {


        $(this).addClass('checked').html('互相关注');


    }

})



function user_collect_page_coun(page,data,name) {
    var str = '';
    var str_li = '';
    if (page !== 1) {
        str_li += '<li class="first disabled" jp-role="first" jp-data="1"><a href="javascript:;">首页</a></li>';
        str_li += '<li class="prev disabled" jp-role="prev" jp-data="0"><a href="javascript:;">上一页</a></li>';
    }
    var pagecount = data.data.page_count, start, last;
    page_num=pagecount;
    if (data.data.page_count > 1) {
        if (pagecount - Number(page) > 2 && Number(page) > 2 && pagecount > 5) {
            start = Number(page) - 3;
            last = Number(page) + 2
        }
        else if (pagecount - Number(page) <= 2 && pagecount > 5) {
            start = pagecount - 6;
            last = pagecount;
        }
        else if (Number(page) <= 2 && pagecount > 5) {
            start = 0;
            last = 5
        }
        else if (pagecount <= 5) {
            start = 0;
            last = pagecount;
        }
        for (var p = start; p < last; p++) {
            if (Number(page) === (p + 1)) {
                str_li += '<li class="page active" jp-role="page" jp-data="' + (p + 1) + '"><a href="javascript:;">' + (p + 1) + '</a></li>';
            } else {
                str_li += '<li class="page" jp-role="page" jp-data="' + (p + 1) + '"><a href="javascript:;">' + (p + 1) + '</a></li>';
            }
        }
        if (data.data.page_count !== 1 && page !== data.data.page_count) {
            str_li += ' <li class="next" jp-role="next" jp-data="2"><a href="javascript:;">下一页</a></li>';
            str_li += '<li class="last" jp-role="last" jp-data="5"><a href="javascript:;">尾页</a></li>'
        }
        str += ' <div class="compents_paginator_list mar-top38 text-rig" id="'+name+'">\n' +
            '                    <ul class="compents_paginator paginator">'
        str+=str_li;
        str+= '                    </ul>\n' +
            '                    <ul class="compents_paginator paginator_controller">\n' +
            '                        <li class="page_number">'+data.data.page_count+'</li>\n' +
            '                        <li class="page_saver"><input id="page_saver"></li>\n' +
            '                        <li class="page_ender">页</li>\n' +
            '                    </ul>\n' +
            '                </div>'
    }




    return str;
}
$(document).on('click', '#user_ques_page_count li', function (e) {
    if ($(this).hasClass('page')) {
        user_ques_page = Number($(this).attr('jp-data'));
        user_atten_questions()
    }
    if ($(this).hasClass('prev')) {
        user_ques_page--;
        user_atten_questions()
    }
    if ($(this).hasClass('next')) {
        user_ques_page++;
        user_atten_questions()
    }
    if ($(this).hasClass('first')) {
        user_ques_page = 1;
        user_atten_questions()
    }
    if ($(this).hasClass('last')) {
        user_ques_page = page_num;
        user_atten_questions()
    }


})
$(document).on('keyup','#user_ques_page_count input',function (e) {
    if(e.keyCode===13){
        user_ques_page=$(this).val();
        user_atten_questions()
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})
$(document).on('click', '#user_fan_page_count li', function (e) {
    if ($(this).hasClass('page')) {
        user_ques_page = Number($(this).attr('jp-data'));
        user_atten_questions()
    }
    if ($(this).hasClass('prev')) {
        user_ques_page--;
        user_atten_questions()
    }
    if ($(this).hasClass('next')) {
        user_ques_page++;
        user_atten_questions()
    }
    if ($(this).hasClass('first')) {
        user_ques_page = 1;
        user_atten_questions()
    }
    if ($(this).hasClass('last')) {
        user_ques_page = page_num;
        user_atten_questions()
    }


})
$(document).on('keyup','#user_fan_page_count input',function (e) {
    if(e.keyCode===13){
        user_ques_page=$(this).val();
        user_atten_questions()
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})
$(document).on('click', '#user_per_page_count li', function (e) {
    if ($(this).hasClass('page')) {
        user_ques_page = Number($(this).attr('jp-data'));
        user_atten_questions()
    }
    if ($(this).hasClass('prev')) {
        user_ques_page--;
        user_atten_questions()
    }
    if ($(this).hasClass('next')) {
        user_ques_page++;
        user_atten_questions()
    }
    if ($(this).hasClass('first')) {
        user_ques_page = 1;
        user_atten_questions()
    }
    if ($(this).hasClass('last')) {
        user_ques_page = page_num;
        user_atten_questions()
    }


})
$(document).on('keyup','#user_per_page_count input',function (e) {
    if(e.keyCode===13){
        user_ques_page=$(this).val();
        user_atten_questions()
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})

