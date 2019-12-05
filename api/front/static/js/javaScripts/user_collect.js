var user_collect_page=1,page_num

$('.user-menu').append(function () {
    var str = '';
    str += ' <div class="user-menu-list" data-link="collect">\n' +

        '        </div>'
    return str;
});

$.ajax({
    url: user_link.collect_tag,
    type: 'get',
    success: function (data) {
        $('.user-menu .user-menu-list[data-link="collect"]').append(function () {
            var str = '';
            if (true) {
                str += '            <div>\n' +
                    '                <div class="user-collect-top">\n' +
                    '                    <div class="user-collect-title">我的收藏</div>\n' +
                    '                    <div class="user-collect-tag">\n' +
                    '                        <span>分类</span>\n' +
                    '                        <ul class="row user_tag_change_collect">\n' +
                    '                            <li class="checked" ajax-url="0">全部</li>';
                                                    if(data.code===200) {
                                                        var list = data.data.user_collect_category_list
                                                        for (var i = 0; i < list.length; i++) {
                                                            str += '<li ajax-url="' + list[i].id + '">' + list[i].collect_category + '</li>'
                                                        }
                                                    }
                str+='                        </ul>\n' +
                    '                    </div>\n' +
                    '                </div>\n' +
                    '                    <div class="user-collect-cho-tag row">\n' +
                    '                        <span class="tag">分类管理</span>\n' +
                    '                    </div>\n' +
                    '                    <ul class="user-collect-list">';


                    str+='                    </ul>\n' +
                    '        </div>';
                ajax_collect_data(0,1)
            } else {
                str += '<div class="no_comment">\n' +
                    '                <div class="no_comment_img"></div>\n' +
                    '                <div class="no_comment_text">目前暂无收藏~</div>\n' +
                    '            </div>'
            }
            return str;
        });
        $('.user-menu .user-menu-list[data-link="collect"]').siblings().addClass('hide')
    }
});
var user_collect_url = 'user',user_collect_type=0;
$(document.body).on('click', '.user_tag_change_collect li', function () {
    $(this).addClass('checked').siblings().removeClass('checked');
    user_collect_type = $(this).attr('ajax-url');
    user_collect_page=1
    ajax_collect_data(user_collect_type,user_collect_page)
});
function ajax_collect_data(user_collect_type,user_collect_page) {
    $.ajax({
        url: user_link.collect_ques+user_collect_type+'/'+user_collect_page+'/',
        type: 'get',
        data: '',
        success: function (data) {
            $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').html(user_collect_data(user_collect_page,data));
            addVideoAction()
        }
    })
}
/*
* 收藏数据拼接
* */
function user_collect_data(page,data) {
    var list=data.data.favorites
    var str = '';
    if(list) {
        for(var i=0;i<list.length;i++) {
            if(list[i].type== "videomodel"){
                str+=`
    <li>
        <div>
            <a href="${"/video_detail/"+list[i].video_id+"/"}" target="_blank">
                <div style="  width: 182px;height: 105px;border-radius: 5px ;display: inline-block;vertical-align: top">
                    <img src="${"/images/article_images/"+list[i].thumbnail}" style="width:100%;height:105px;border-radius: 5px ">
                </div>
            </a>
            <div style="display:inline-block">
                <a href="${"/video_detail/"+list[i].video_id+"/"}" target="_blank">
                    <div style="  font-family: PingFangSC;
                      font-size: 18px;
                      font-weight: normal;
                      font-style: normal;
                      font-stretch: normal;
                      line-height: 18px;
                      letter-spacing: normal;
                      text-align: left;
                      color: #000000;
                      margin-left: 18px;
                      ">
                        ${list[i].title}
                    </div>
                </a>
                <div style="margin-top:70px;margin-left:15px;line-height: 18px;"><span style="font-size: 13px;height: 18px;display: inline-block" class="user-coll video-coll" data-vid="${list[i].video_id}" data-collect-id="${list[i].collect_category}"><span class="inner_text">取消收藏</span></span></div>
            </div>
        </div>
    </li>`
            }else{
            str += '  <li>\n' +
                ' <a href="/question_detail/' + list[i].question_id + '/0/1/1/"><div class="user-collect-list-title">' + list[i].question_content.replace(new RegExp('(<img[^>]+>)', 'g'), '图片').replace(new RegExp('(<[^>]+>)', 'g'), '') + '</div></a>';
            if (list[i].answer_username_avatar) {
                str += '<div class="inline user-collect-list-img"><a href="javascript:;"><span class="user" style="background: url(/images/avatar/' + list[i].answer_username_avatar + ') no-repeat;background-size: cover;"></span></a></div>'
            } else {
                str += '<div class="inline user-collect-list-img"><a href="user_detail.html?t=collect"><span class="user"></span></a></div>'
            }

            str += '                            <div class="inline user-collect-list-text">\n' +
                '                                <a href="javascript:;"><div class="user-collect-list-name">' + list[i].answer_username + '</div></a>\n';

            if (new RegExp('(<img[^>]+>)', 'g').test(list[i].answer_content)) {
                var s = list[i].answer_content.replace(new RegExp('(<img[^>]+>)', 'g'), '图片').replace(new RegExp('(<[^>]+>)', 'g'), '')
                str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '<span style="display: none">' + list[i].answer_content + '</span><span class="color-link pointer" >展开</span></div>\n';

            } else {
                var s = list[i].answer_content.replace(new RegExp('(<img[^>]+>)', 'g'), '图片').replace(new RegExp('(<[^>]+>)', 'g'), '')
                if (getBt(s) > 184) {
                    str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '<span style="display: none">' + list[i].answer_content + '</span><span class="color-link pointer">展开</span></div>\n';
                } else {
                    str += '                        <div class="user-collect-list-artic">' + autoAddEllipsis(s, 184) + '</div>\n';
                }
            }
            //str+='                                <div class="user-collect-list-artic"> '+list[i].answer_content+'</div>\n' ;
                var pris = list[i].is_praise === 1 ? ("已赞" + list[i].praise_count) : list[i].praise_count
            str += '                                <div class="user-collect-list-tag"><span>' + list[i].answer_create_time + '</span><span class="user-comm">评论 ' + list[i].answer_count + '</span><span class="user-fig pointer"  ques_id="' + list[i].answer_id + '">' + pris + '</span><span class="user-coll collect" ans_id="' + list[i].answer_id + '" ans_tag="">取消收藏</span></div>\n' +
                '                            </div>                                \n                                ' +
                '                                                        </li>'
            }
        }


        $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').css('border','solid 1px #eaeaf1')
    }else {
        str += '<li style=" background-color: #F2F3F4;"><div class="no_comment">\n' +
            '                <div class="no_comment_img"></div>\n' +
            '                <div class="no_comment_text">目前暂无收藏~</div>\n' +
            '            </div></li>';
        $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').css('border','none')
    }
    $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').next().remove();
    document.documentElement.scrollTop=0
    $('.user-menu .user-menu-list[data-link="collect"] .user-collect-list ').after(user_collect_page_coun(page,data))
    return str;
}

/*
* 页码
* */
 function user_collect_page_coun(page,data) {
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
        str += ' <div class="compents_paginator_list mar-top38 text-rig" id="user_collect_page_coun">\n' +
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
$(document).on('click', '#user_collect_page_coun li', function (e) {
    if ($(this).hasClass('page')) {
        user_collect_page = Number($(this).attr('jp-data'));
        ajax_collect_data(user_collect_type,user_collect_page)
    }
    if ($(this).hasClass('prev')) {
        user_collect_page--;
        ajax_collect_data(user_collect_type,user_collect_page)
    }
    if ($(this).hasClass('next')) {
        user_collect_page++;
        ajax_collect_data(user_collect_type,user_collect_page)
    }
    if ($(this).hasClass('first')) {
        user_collect_page = 1;
        ajax_collect_data(user_collect_type,user_collect_page)
    }
    if ($(this).hasClass('last')) {
        user_collect_page = page_num;
        ajax_collect_data(user_collect_type,user_collect_page)
    }


})
$(document).on('keyup','#user_collect_page_coun input',function (e) {
    if(e.keyCode===13){
        user_collect_page=$(this).val();
        ajax_collect_data(user_collect_type,user_collect_page);
        $(this).val('').blur();
    } else {
        if($(this).val()>page_num){
            $(this).val(page_num);
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})
/*
* 收藏夹
* */

$(document).on('click', '.user-menu-list[data-link="collect"] .user-collect-list-artic span.pointer', function () {
    var a = $(this).prev().html();
    $(this).parent().html(a)
})
// 视频取消收藏
let addVideoAction=function () {
    $(".video-coll").click(function () {
        let t = $(this)
        let t_data = t.data()
        if (t_data.recollect == 1) {
            t.data('recollect', 3)
            t.find(".inner_text").html("取消收藏")
            $.ajax({
                url: "/front_favorites/" + t_data.vid + "/" + t_data.collectId + "/3/",
                type: "get",
                success: function (data) {
                    if (data.code == 200) {
                        t.data('recollect', 0)
                    } else {
                        return
                    }
                }
            })
        } else if (t_data.recollect == undefined || t_data.recollect == 0) {
            t.data('recollect', 3)
            t.find(".inner_text").html("收藏")
            $.ajax({
                url: "/front_favorites/" + t_data.vid + "/" + t_data.collectId + "/3/",
                type: "get",
                success: function (data) {
                    if (data.code == 200) {
                        t.data('recollect', 1)
                    } else {
                        return
                    }
                }
            })
        } else {
            return
        }
    })
}
