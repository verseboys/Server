var model_type={
    user:{
        type:true,
        src:'/static/js/javaScripts/user.js'
    },
    collect:{
        type:true,
        src:'/static/js/javaScripts/user_collect.js'
    },
    atten:{
        type:true,
        src:'/static/js/javaScripts/user_atten.js'
    },
    ask_ques:{
        type:true,
        src:"/static/js/javaScripts/user_question_ask.js"
    },
    ans_ques:{
        type:true,
        src:'/static/js/javaScripts/user_question_ans.js'
    },
    mess:{
        type:true,
        src:'/static/js/javaScripts/user_message.js'
    },
    order:{
        type:true,
        src:'/static/js/javaScripts/user_order.js'
    }
};
var user_link={
    ask_ques:'/my_questions/',//我的提问
    collect_ques:'/my_collect/',//收藏问答
    collect_tag:'/user_collect_category_list/',//收藏标签
    atten_ques:'/my_attention_questions/',//关注的问题
    atten_ing:'/attention_question/',//关注问题
    praise_ing:'praise_answer',//点赞
    collect_ing:'/collect_answer/',//收藏
    ans_ques:'/my_answers/',//回答问题
}
// $.ajax({
//     url:'',
//     type:'post',
//     success:function (data) {
//
//     }
//     ,error:function () {
//
//     }
// })
var user_page=1
var user_info_chose={
    "username":"",
    "corporation":"",
    "jobtitle":"",
    "signature":"",
    "mobile":"",
    "gender":"",
    "profession":"",
    "email":""
}
$(document).ready(function () {
    function loca(href) {
        var obj={}
        href=encodeURI(href);
        href=href.split('?')[1];
        try{
            href = href.split('&');
            for (var i = 0; i < href.length; i++) {
                var a = href[i].split('=')[0]
                var b = href[i].split('=')[1]
                obj[a] = b;
            }
            return obj
        }catch (e){
            console.log(e)
        }

    }
    user_bar_con();
    function user_bar_con() {
        $.ajax({
            url:'/user_info/',
            type:'get',
            success:function (data) {
                var str = '';
                str += '<div class="user-bar-top">\n' +
                    '            <div class="user-bar-top-img text-cen"><span class="" style="background:url(/images/avatar/' + data.data.avatar + ') center; background-size: cover;     border-radius: 100%;"></span></div>\n' +
                    '            <div class="user-bar-top-name"  style="text-align: center"><span>' + data.data.username + '</span></div>\n';
                if (data.data.signature) {
                    if (getBt(data.data.signature) <= 26){
                        str += '            <div class="user-bar-top-des"  style="text-align: center"><span>' + (data.data.signature ? data.data.signature : "这个人很懒，没有简介") + '</span></div>\n';
                }else {
                        str +=  '            <div class="user-bar-top-des "><span>' + (data.data.signature ? data.data.signature : "这个人很懒，没有简介") + '</span></div>\n';
                    }
                }else {
                    str +='            <div class="user-bar-top-des" style="text-align: center"><span>' + (data.data.signature ? data.data.signature : "这个人很懒，没有简介") + '</span></div>\n';
                }

                    str+='            <div class="user-bar-top-num text-cen font-14">\n' +
                    '                <div class="inline after_line relative">\n' +
                    '                    <span class="block line-height25">粉丝</span>\n' +
                    '                    <span class="block line-height25">0</span>\n' +
                    '                </div><div class="inline line-height25">\n' +
                    '                    <span class="block line-height25">回答</span>\n' +
                    '                    <span class="block line-height25">'+data.data.answer_count+'</span>\n' +
                    '                </div>\n' +
                    '            </div>\n' +
                    '            <div class="user-bar-btn" data-link="user" >编辑个人资料</div>\n' +
                    '        </div>';

                str += ' <div class="user-bar-bot">\n' +
                    '            <div class="user-bar-tag" data-link="collect">我的收藏</div>\n' +
                    '            <div class="user-bar-tag" data-link="atten">我的关注</div>\n' +
                    '            <div class="user-bar-bot-line"></div>\n' +
                    '            <div class="user-bar-tag" data-link="ask_ques">我的提问</div>\n' +
                    '            <div class="user-bar-tag" data-link="ans_ques">我的回答</div>\n' +
                    '            <div class="user-bar-bot-line"></div>\n' +
                    '            <div class="user-bar-tag" data-link="mess">我的消息</div>\n' +
                    '            <div class="user-bar-tag" data-link="order">我的订单</div>\n'+
                    '        </div>';
                $('.user-bar').html(str)
                $('.user-menu').removeClass('hide');
                var hre=loca(window.location.href);
                if(hre.t){
                    if(hre.t==='user'){
                        var sc = document.createElement('script');
                        sc.src = model_type['user'].src;
                        document.head.appendChild(sc);
                        model_type['user'].type=false
                    }else {
                        var a='.user-bar .user-bar-bot .user-bar-tag[data-link='+hre.t+']'
                        $('.user-bar .user-bar-bot .user-bar-tag[data-link='+hre.t+']').trigger('click');
                    }
                }else {
                    var sc = document.createElement('script');
                    sc.src = model_type['user'].src;
                    document.head.appendChild(sc);
                    model_type['user'].type=false
                }
            }

        })

    };
    $('.user-bar').on('click', '.user-bar-bot .user-bar-tag', function (e) {
        var model_val = $(this).attr('data-link');
        //首次点击加载脚本
        if (model_type[model_val].type) {
            var sc = document.createElement('script');
            sc.src = model_type[model_val].src;
            document.head.appendChild(sc);
            model_type[model_val].type = false;
        } else {
            console.log(1,$('.user-menu .user-menu-list[data-link=' + model_val + ']'))
            console.log(2,$('.user-menu .user-menu-list[data-link=' + model_val + ']').siblings())
            $('.user-menu .user-menu-list[data-link=' + model_val + ']').removeClass('hide').siblings().addClass('hide');
            switch (model_val) {
                case "mess":
                    user_got_mess();
            }
        }
        switch (model_val){
            // case 'collect':
            //     user_page=user_collect_page
            //     break;
            // case 'atten':
            //     user_page=user_atten_page;
            //     break;
            // case 'ask_ques':
            //     user_page=user_ask_ques_page
            //     break;
            // case 'ans_ques':
            //     user_page=user_ans_ques_page
            //     break;
            //
            // case 'mess':
            //     user_page=user_mess_page
            //     break;

        }
        document.documentElement.scrollTop=0
        $(this).addClass('user-bar-left-checked').siblings().removeClass('user-bar-left-checked')
    })
    $('.user-bar').on('click', '.user-bar-btn', function (e) {
        var model_val = $(this).attr('data-link');
        if (model_type[model_val].type) {
            var sc = document.createElement('script');
            sc.src = model_type[model_val].src;
            document.head.appendChild(sc);
            model_type[model_val].type = false;
        } else {
            // $('.user-menu .user-menu-list[data-link=' + model_val + ']').removeClass('hide').siblings().addClass('hide');
            // switch (model_val) {
            //     case "mess":
            //         user_got_mess();
            // }
            $('.user-menu .user-menu-list[data-link="user"]').removeClass('hide').siblings().addClass('hide')
            $('.user-bar .user-bar-bot .user-bar-tag').removeClass('user-bar-left-checked').siblings().removeClass('user-bar-left-checked')
        }

    })

    /*
    * 页码
    * */
    window.user_page_coun= function (page,data,name) {
        var str = '';
        var str_li = '';
        if (Number(page) !== 1) {
            str_li += '<li class="first disabled" jp-role="first" jp-data="1"><a href="javascript:;">首页</a></li>';
            str_li += '<li class="prev disabled" jp-role="prev" jp-data="'+(page-1)+'"><a href="javascript:;">上一页</a></li>';
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
            if (data.data.page_count !== 1 && Number(page) !== data.data.page_count) {
                str_li += ' <li class="next" jp-role="next" jp-data="'+ (Number(page)+1)+'"><a href="javascript:;">下一页</a></li>';
                str_li += '<li class="last" jp-role="last" jp-data="'+ data.data.page_count+'"><a href="javascript:;">尾页</a></li>'
            }
            str += ' <div class="compents_paginator_list mar-top38 text-rig" id="'+name+'">\n' +
                '                    <ul class="compents_paginator paginator">'
            str+=str_li;
            str+= '                    </ul>\n' +
                '                    <ul class="compents_paginator paginator_controller">\n' +
                '                        <li class="page_number">'+data.data.page_count+'</li>\n' +
                '                        <li class="page_saver"><input ></li>\n' +
                '                        <li class="page_ender">页</li>\n' +
                '                    </ul>\n' +
                '                </div>'
        }

        document.documentElement.scrollTop=0


        return str;
    }
    // $('.user-menu').on('click','.user-coll',function () {
    //
    //     var self=$(this)
    //     $.ajax({
    //         url:'/collect_answer/'+self.attr('pid')+'/',
    //         type:'get',
    //         success:function (data) {
    //             if(data.data.is_collect===1){
    //                 self.html('收藏')
    //             }else {
    //                 self.html('取消收藏')
    //             }
    //         }
    //     })
    // })
    $(document.body).on('click', '.collect', function () {
        var self = $(this)
        var s = $(this).html();
        var st = s.replace(new RegExp('(<[^>]+>)', 'g'), '');
        var ans = $(this).attr('ans_id');
        var tag = $(this).attr('ans_tag');
        if (st === '收藏') {
            box.user.tar = self
            $.ajax({
                url: '/user_collect_category_list/',
                type: 'get',
                success: function (data) {
                    box.collect_lists = data.data.user_collect_category_list;
                    box.user.ans_id = ans
                    check_type(7);

                    if (data.code === 200) {

                    }
                }
            })
        } else {
            AJAX({
                url: '/collect_answer/' + ans + '/0/',
                type: 'get',
                data: {},
                fn: function () {
                    self.html(s.replace('取消收藏', '收藏'));
                }
            })

        }
    })

    $( document).on('click','.user-collect-cho-tag .tag',function () {
        $.ajax({
            url: '/user_collect_category_list/',
            type: 'get',
            success: function (data) {
                if(data.code===200){
                    var list=data.data.user_collect_category_list
                    box.collect_lists=list;
                }else {
                    box.collect_lists =[]

                }
                    check_type(21)
            }

        })

    })
    fix_foot();


})



//收藏夹
// Vue.comment('pc-collect-watch',{
//     template:'<div class="neko_shadow_box" v-if="check_type===21">\n' +
//     '        <div class="pc2_collect pc2_watch_collect">\n' +
//     '            <div class="font-18 line-height25 pad-bot20 color-liter-grey f-200">收藏夹</div>\n' +
//     '            <div class="">\n' +
//     '                <ul class="collect_list">\n' +
//     '                    <li><span class="collect_text">统计方法</span><span class="right collect_del">删除</span><span class="right collect_change">编辑</span></li>\n' +
//     '                </ul>\n' +
//     '                <div class="push-coll mar-top10 line-height36 color-link font-18 text-left"><span class="pointer">+创建收藏夹</span></div>\n' +
//     '            </div>\n' +
//     '            <div class="text-cen">\n' +
//     '                <div class="btn-collect-close inline align-cen">取消</div>\n' +
//     '                <div class="mar-left20 btn-collect inline align-cen">提交</div>\n' +
//     '            </div>\n' +
//     '        </div>\n' +
//     '    </div>'
//     , props:['check_type','lists'],
//     data:function () {
//         return {
//             chose:{}
//         }
//     },
// })
