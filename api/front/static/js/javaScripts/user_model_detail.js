var model_type={
    user:{

    },
    collect:{
        type:true,
        src:'../pbulic/javaScripts/user_collect_detial.js'
    },
    atten:{
        type:true,
        src:'../pbulic/javaScripts/user_atten.js'
    },
    ask_ques:{
        type:true,
        src:"../pbulic/javaScripts/user_question_ask.js"
    },
    ans_ques:{
        type:true,
        src:'../pbulic/javaScripts/user_question_ans.js'
    },
    mess:{
        type:true,
        src:'../pbulic/javaScripts/user_message.js'
    }
};
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
    user_bar_con();
    function user_bar_con() {
        var str='';
        str+='<div class="user-bar-top">\n' +
            '            <div class="user-bar-top-img text-cen"><span class="" style=""></span></div>\n' +
            '            <div class="user-bar-top-name text-cen"><span>李医生</span></div>\n' +
            '            <div class="user-bar-top-des"><span>简介简介简介简介简介简介简介简介简介简介简介简介简介简介简介简介简介简介简介</span></div>\n' +
            '            <div class="user-bar-top-num text-cen font-14">\n' +
            '                <div class="inline after_line relative">\n' +
            '                    <span class="block line-height25">粉丝</span>\n' +
            '                    <span class="block line-height25">11</span>\n' +
            '                </div><div class="inline line-height25">\n' +
            '                    <span class="block line-height25">回答</span>\n' +
            '                    <span class="block line-height25">11</span>\n' +
            '                </div>\n' +
            '            </div>\n' +
            '            <div class="user-bar-btn" data-link="user" style="background-color: #4990e2;color: #fff;font-weight: 300;border: none" type="1">+关注</div>\n' +
            '        </div>';
        str+=' <div class="user-bar-bot">\n' +
            '            <div class="user-bar-tag" data-link="collect">他的收藏</div>\n' +
            '            <div class="user-bar-tag" data-link="atten">他的关注</div>\n' +
            '            <div class="user-bar-bot-line"></div>\n' +
            '            <div class="user-bar-tag" data-link="ask_ques">他的提问</div>\n' +
            '            <div class="user-bar-tag" data-link="ans_ques">他的回答</div>\n' +
            '        </div>';
        $('.user-bar').html(str)
        $('.user-menu').removeClass('hide')
    };
    $('.user-bar').on('click','.user-bar-bot .user-bar-tag',function (e) {
        var model_val= $(this).attr('data-link');
        if(model_type[model_val].type){
            var sc=document.createElement('script');
            sc.src=model_type[model_val].src;
            document.head.appendChild(sc);
            model_type[model_val].type=false;
        }else{
            $('.user-menu .user-menu-list[data-link='+model_val+']').removeClass('hide').siblings().addClass('hide');
            switch (model_val){
                case "mess":
                    user_got_mess();
            }
        }
        document.documentElement.scrollTop=0
        $(this).addClass('user-bar-left-checked').siblings().removeClass('user-bar-left-checked')
    });

    $('.user-bar').on('click','.user-bar-btn',function (e) {


        var model_val= $(this).attr('type');
        switch (model_val){
            case "1":
                $(this).html('已关注');
                $(this).attr("type","3");
                $(this).css("background-color","#ddeff9").css("color","#4990e2")
               break;
            case "2":
                $(this).html('+关注');
                $(this).attr("type","1");
                $(this).css("background-color","#4990e2").css("color","#fff").css('font-weight','200')
                break;
            case "3":
                $(this).html('互相关注');
                $(this).attr("type","2");
                $(this).css("background-color","#ddeff9").css("color","#4990e2")
                break;
        }
        // $('.user-menu .user-menu-list[data-link="user"]').removeClass('hide').siblings().addClass('hide')
        // $('.user-bar .user-bar-bot .user-bar-tag').removeClass('user-bar-left-checked').siblings().removeClass('user-bar-left-checked')
    })
    $('.user-bar .user-bar-bot .user-bar-tag[data-link=collect]').trigger('click')
    /*
    * 个人中心 && 修改密码
    * */
    var user_info_url='user'
    $(document.body).on('click','.user-info-tag div',function () {
        $(this).addClass('checked').siblings().removeClass('checked');
        user_info_url=$(this).attr('ajax-url');
        var type=$(this).attr('type');
        $('.user-info .user-info-bot div div[type='+type+']').removeClass('hide').siblings().addClass('hide')
        $.ajax({
            url:url,
            data:'',
            type:'post',
            success:function (data) {

            }
            ,error:function () {

            }
        })
    });



    /*
    * 性别选择
    * */
    $(document.body).on('click',' .user-info-box .chooser',function () {
        var _self=$(this);
        var type=_self.attr('type');
        if(_self.hasClass('chooser_active')){
            _self.removeClass('chooser_active');
            _self.next('.chooser_list').addClass('hide');
        }else {
            _self.addClass('chooser_active');
            _self.next('.chooser_list').removeClass('hide');
        }
        switch (type){
            case "sex":
                $('.chooser[type=desk]').removeClass('chooser_active');
                $('.chooser[type=desk]').next('.chooser_list').addClass('hide');
                $('.chooser[type=pro]').removeClass('chooser_active');
                $('.chooser[type=pro]').next('.chooser_list').addClass('hide');
                _self.next('.chooser_list').on('click','.chooser_item',function () {
                    _self.html($(this).html());
                    _self.removeClass('chooser_active')
                    _self.next('.chooser_list').addClass('hide');
                })
                break
            case "desk":
                $('.chooser[type=sex]').removeClass('chooser_active');
                $('.chooser[type=sex]').next('.chooser_list').addClass('hide');
                $('.chooser[type=pro]').removeClass('chooser_active');
                $('.chooser[type=pro]').next('.chooser_list').addClass('hide');
                user_got_desk(_self)
                _self.next('.chooser_list').on('click','.chooser_item',function () {
                    _self.next('.chooser_list').html('')
                    user_got_desk(_self,{id:$(this).attr('cid')})

                })
                break
            case "pro":
                $('.chooser[type=sex]').removeClass('chooser_active');
                $('.chooser[type=sex]').next('.chooser_list').addClass('hide');
                $('.chooser[type=desk]').removeClass('chooser_active');
                $('.chooser[type=desk]').next('.chooser_list').addClass('hide');
                break
        }

    })

    $('.user-menu').on('click','.user-coll',function () {
        if ($(this).html() == "取消收藏") {
            $(this).html('收藏')
        } else if ($(this).html() == '收藏') {
            $(this).html('取消收藏')
        }
    })

    fix_foot()

})

/*
* 获取科室
* */
var data=  {
    "message": "",
    "code": 200,
    "data": {
        "professionalSections": [{
            "section_grade": 1,
            "professional_section_id": null,
            "id": 1,
            "department_name": "临床医学"
        }, {
            "section_grade": 1,
            "professional_section_id": null,
            "id": 2,
            "department_name": "中医和中西医结合"
        }, {
            "section_grade": 1,
            "professional_section_id": null,
            "id": 3,
            "department_name": "公共卫生与预防医学"
        }, {
            "section_grade": 1,
            "professional_section_id": null,
            "id": 4,
            "department_name": "药学"
        }, {
            "section_grade": 1,
            "professional_section_id": null,
            "id": 5,
            "department_name": "基础医学"
        }, {
            "section_grade": 1,
            "professional_section_id": null,
            "id": 6,
            "department_name": "医学相关"
        }]
    }
}

function user_got_desk(tar,obj) {
    AJAX({
        type: 'get',
        url: '/front_professional_sections/2/',
        data: {},
        fn: function (data) {

        },
        error: function () {
            var list=data.data.professionalSections
            if (data.data.professionalSections.length > 1) {
                tar.next('.chooser_list').html(function () {
                    var str='';
                    for(var i=0;i<list.length;i++){
                        str+='<div class="chooser_item" cid="'+list[i].id+'">'+list[i].department_name+'</div>'
                    }
                    return str;
                })
                data.data.professionalSections.length=0;
            }else {
                tar.next('.chooser_list').html();
                user_info_chose.profession=obj.id
                tar.removeClass('chooser_active')
                tar.next('.chooser_list').addClass('hide');
            }
        }
    })
}

/*
* 页码
* */
window.user_page_coun=function user_page_coun(data) {
    var str='';
    str+=' <div class="compents_paginator_list mar-top38 text-rig">\n' +
        '                    <ul class="compents_paginator paginator">\n' +
        '                        <li class="first disabled" jp-role="first" jp-data="1"><a href="javascript:;">首页</a></li>\n' +
        '                        <li class="prev disabled" jp-role="prev" jp-data="0"><a href="javascript:;">上一页</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="1"><a href="javascript:;">1</a></li>\n' +
        '                        <li class="page active" jp-role="page" jp-data="2"><a href="javascript:;">2</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="3"><a href="javascript:;">3</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="4"><a href="javascript:;">4</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="5"><a href="javascript:;">5</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="6"><a href="javascript:;">6</a></li>\n' +
        '                        <li class="page" jp-role="page" jp-data="7"><a href="javascript:;">7</a></li>\n' +
        '                        <li class="next" jp-role="next" jp-data="2"><a href="javascript:;">下一页</a></li>\n' +
        '                        <li class="last" jp-role="last" jp-data="5"><a href="javascript:;">尾页</a></li>\n' +
        '                    </ul>\n' +
        '                    <ul class="compents_paginator paginator_controller">\n' +
        '                        <li class="page_number">7</li>\n' +
        '                        <li class="page_saver"><input id="page_saver"></li>\n' +
        '                        <li class="page_ender">页</li>\n' +
        '                    </ul>\n' +
        '                </div>'
    return str;
}


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