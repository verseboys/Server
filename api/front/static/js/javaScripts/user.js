$('.user-menu').append(function () {
    var str='';
    str+=' <div class="user-menu-list" data-link="user">\n' +
        '            <div class="user-info">\n' +
        '                <div class="user-info-tag ">\n' +
        '                    <div class="inline checked" ajax-url="0" type="user">个人中心</div>\n' +
        '                    <div class="inline" ajax-url="1" type="pass">修改密码</div>\n' +
        '                    <div class="inline medal_button" ajax-url="2" type="medal">我的勋章</div>\n' +
        '                </div>\n' +
        '                <div class="user-info-bot">\n' +
        '                    <div>\n' +
        '                        <!--个人中心-->\n' +
        '                        <div class="user-info-usr" type="user">\n' +

        '                        </div>\n' +
        '                        <!--修改密码-->\n' +
        '                        <div class="user-info-pass row hide" type="pass">\n' +
        '                            <div class="left align-top">\n' +
        '                                <div class="user-info-title">旧密码</div>\n' +
        '                                <div class="user-info-box"><input type="password" placeholder="输入旧密码" id="user_old_password"></div>\n' +
        '                            </div>\n' +
        '                            <div class="right align-top">\n' +
        '                                <div class="user-info-title">新密码</div>\n' +
        '                                <div class="user-info-box block"><input type="password" placeholder="输入新密码" id="user_new_password"></div>\n' +
        '                                <div class="user-info-box block"><input type="password" placeholder="确认新密码" id="user_repeat_password"></div>\n' +
        '                            </div>\n' +
        '                        </div>\n' +

        '                        <div class="user-info-pass row hide" style="min-height:600px" id="user_medal" type="medal">\n' +

        '                        </div>\n' +

        
        '                    </div>\n' +
        '                    <div class="fin_toolbox">\n' +
        '                        <div class="information_box information_success_box" style="display:none"></div>\n' +
        '                        <div class="information_box information_error_box"  style="display:none"></div>\n' +
        '                        <div class="submit shadow_btn user_pg_submit disabled" >保存</div>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '            </div>\n' +
        '        </div>'
    return str;
})

$('.user-menu .user-menu-list[data-link="user"]').removeClass('hide').siblings().addClass('hide')
// $(document).on('click','.user-info .user_pg_submit',function () {
//     if($(this).hasClass("disabled")){
//         return
//     }
//     post_user_info()
// })
var user_indo_obj={
    sex:'',
    pro:'',
    job:'',
    img:''
}


var show_positive_medal = function(img_base_url,img,title,sub_title,num){
    var html = `

    <div class="medal_modal_container" style="position:fixed;width:100%;height:100%;background:rgba(0,0,0,0.4);top:0;left:0;z-index:99999;">
        <div class="medal_center_container" style="text-align:center;position:absolute;top:50%;left:50%;width:600px;height:400px;background:#fff;border-radius:3px;margin-left:-300px;margin-top:-200px;">
            <div class="cancel_medal_modal" style="width:38px;height:38px;position:absolute;top:0;right:0;margin-top:-38px;margin-right:-58px;cursor:pointer">
                <img style="width:38px;height:38px" src="/static/images/cancel.svg">
            </div>
            <div style="position:absolute;top:0;left:50%;weight:150px;height:170px;margin-left:-75px;margin-top:-85px;">
                <img style="width:150px;height:164.5px" src="${img_base_url+img}">
            </div>
            <div style="margin-top:110px">
                <div class="medal_avatar_container" style="display:inline-block;width:38px;height:38px;vertical-align:middle;margin-left:-38px;margin-right:19px";border-radius:100%>
                </div>
                <span style="font-size:20px">恭喜你获得新勋章</span>
            </div>
            <div style="font-size:38px;color:#475dd9;font-weight:700;margin-top:36px;">
                ${title}
            </div>
            <div style="margin-top:40px;padding-left:110px;padding-right:110px;line-height:20px">
                ${sub_title}
            </div>
            <div style="margin-top:28px;">
                已有<span style="color:#475dd9">${num}</span>人获得
            </div>

        </div>
    </div>
    `
    $('body').append(html)
    $(".medal_avatar_container").css({'background':$(".login-on.ques_bar_meun").css('background'),'border-radius':'100%'})
    $('.cancel_medal_modal').click(function(){
        $('.medal_modal_container').remove()
    })
}

var show_negative_medal = function(img_base_url,img,title,sub_title,num){
    var html = `

    <div class="medal_modal_container" style="position:fixed;width:100%;height:100%;background:rgba(0,0,0,0.4);top:0;left:0;z-index:99999;">
        <div class="medal_center_container" style="text-align:center;position:absolute;top:50%;left:50%;width:600px;height:400px;background:#fff;border-radius:3px;margin-left:-300px;margin-top:-200px;">
            <div class="cancel_medal_modal" style="width:38px;height:38px;position:absolute;top:0;right:0;margin-top:-38px;margin-right:-58px;cursor:pointer">
                <img style="width:38px;height:38px" src="/static/images/cancel.svg">
            </div>
            <div style="position:absolute;top:0;left:50%;weight:150px;height:170px;margin-left:-75px;margin-top:-85px;">
                <img style="width:150px;height:164.5px" src="${img_base_url+img}">
            </div>
            <div style="margin-top:110px">
                <span style="font-size:20px">尚未获得，仍需努力</span>
            </div>
            <div style="font-size:38px;color:#475dd9;font-weight:700;margin-top:36px;">
                ${title}
            </div>
            <div style="margin-top:40px;padding-left:110px;padding-right:110px;line-height:20px">
                ${sub_title}
            </div>
            <div style="margin-top:28px;">
                已有<span style="color:#475dd9">${num}</span>人获得
            </div>
        </div>
    </div>
    `
    $('body').append(html)
    $('.cancel_medal_modal').click(function(){
        $('.medal_modal_container').remove()
    })
}
// 限定勋章下显示的描述字数
// var handle_description_show = function(raw_description,keep_length){
//     var len = 0;
//     var description = '';
//     for (var i=0; i<raw_description.length; i++) {
//         if (raw_description.charCodeAt(i)>127) {
//             len += 2;
//         } else {
//             len ++;
//         }
//         if(len>=keep_length && i<raw_description.length-1){
//             description+=raw_description[i]
//             return description+'...'
//         }else{
//             description+=raw_description[i]
//         }
//     }
//     return raw_description;
// }
var anniversary_img_base_url = '/static/images/'
var img_base_url = '/ss/v1/files/'
$.ajax({
    url:'/get_achievements/',
    type:'get',
    success:function (data) {
        user_medals = data.data.user_medals
        let user_medal_id_list = user_medals.map((medal)=>{return medal['medal__id']});
        receive_time = {}
        user_medals.forEach(medal => {
            receive_time[medal['medal__id']] = new Date(medal['create_time']).getFullYear()
        });

        all_medals = data.data.medals.map((medal)=>{
            switch(medal.uid){
                case 'old_bird':
                    medal.name = '医咖会见证者·' + (receive_time[medal.id] || '2018')
                    medal.description = `感谢有你，${receive_time[medal.id] || '2018'}年和医咖会共庆两周岁`
                    medal.pic_ss_key = 'old_bird.png'
                    medal.pic_negative_ss_key = 'old_bird_negative.png'
                    return medal
                case 'sci_god':
                    medal.name = 'SCI大神'
                    medal.description = 'Respect！Respect！Respect！'
                    medal.pic_ss_key = 'sci_god.png'
                    medal.pic_negative_ss_key = 'sci_god_negative.png'
                    return medal
                case 'yizhu_friend':
                    medal.name = '医咖会的朋友'
                    medal.description = '请收下小咖的感激和敬意'
                    medal.pic_ss_key = 'yizhu_friend.png'
                    medal.pic_negative_ss_key = 'yizhu_friend_negative.png'
                    return medal
                case 'positive_man':
                    medal.name = '活动积极分子'
                    medal.description = '活动积极参与者，沙龙聚会需要你'
                    medal.pic_ss_key = 'positive_man.png'
                    medal.pic_negative_ss_key = 'positive_man_negative.png'
                    return medal
                default:
                    return medal
            }
        })

        //记录用户已有勋章  key为勋章id 以key是否存在判断获得状态
        user_medals = {}
        for(medal of all_medals){
            if(user_medal_id_list.indexOf(medal.id)!==-1){
                user_medals[medal.id] = 1
            }
        }

        let html = ``

        all_medals.forEach((medal)=>{
            html+=`
                <div class="left" style="width:200px;height:300px;">
                    <div class="${medal['medal_type']!=='1'?'show_medal_common':'show_medal'}" style="width:150px;margin-top:55px;margin-left:25px;background:white;cursor:pointer;"
                        data-count="${medal.count}"
                        data-name="${medal.name}"
                        data-description="${medal.description}"
                        data-receive-state="${user_medals[medal.id]?true:false}"
                        data-medal="${user_medals[medal.id]?medal.pic_ss_key:medal.pic_negative_ss_key}"
                    >
                    ${
                        medal['medal_type']!=='1'?
                            `<img src="${img_base_url + (user_medals[medal.id]?medal.pic_ss_key:medal.pic_negative_ss_key) + '/url'}" style="width:100%;height:auto">`
                        :
                            `<img src="${anniversary_img_base_url + (user_medals[medal.id]?medal.pic_ss_key:medal.pic_negative_ss_key)}" style="width:100%;height:auto">`

                    }
                        <div class="medal_title" style="margin-top:25px;font-weight:700;text-align:center">
                            ${medal.name}
                        </div>
                    </div>
                </div>
            `
        })

        
        $("#user_medal").html(html)

        $(".show_medal").click(function(){
            var data = $(this).data()
            if(data.receiveState){
                show_positive_medal(anniversary_img_base_url,data.medal,data.name,data.description,data.count)
            }else{
                show_negative_medal(anniversary_img_base_url,data.medal,data.name,data.description,data.count)
            }
        })

        $(".show_medal_common").click(function(){
            var data = $(this).data()
            if(data.receiveState){
                show_positive_medal(img_base_url,data.medal+'/url',data.name,data.description,data.count)
            }else{
                show_negative_medal(img_base_url,data.medal+'/url',data.name,data.description,data.count)
            }
        })



    },
    error:function(error){
        console.log(error)
    }    
})

$.ajax({
    url:'/user_info/',
    type:'get',
    success:function (data) {
        var data=data.data;
        user_indo_obj.img=data.avatar
        $('.user-menu .user-menu-list[data-link="user"] .user-info-usr').append(function () {
            var str='';
            str+= '                            <div class="user-info-title">基本信息</div>\n' +
                '                            <div class="row">\n' +
                '                                <div class="user-info-box">\n' +
                '                                    <div class=" pointer">\n' +
                '                                        <input type="file" accept="image/*" class="hide" id="trueName">\n' +
                '                                        <label for="trueName" class="pointer">\n' +
                '                                            <div class="selector_img" style="    background-image: url(/images/avatar/'+ data.avatar+');background-size:cover;border-radius: 100%"></div>\n' +
                '                                            <div class="selector_text">选择头像</div>\n' +
                '                                        </label>\n' +
                '                                    </div>\n' +
                '                                </div>\n' +
                '                                <div class="user-info-box">\n' +
                '                                    <div class="wi1">' ;
            if(data.username){
                str+= '                                        <input type="text" placeholder="用户名" value="'+data.username+'" id="user_username">\n' ;
            }else {
                str += '                                        <input type="text" placeholder="用户名" id="user_username"> \n';
            }
            // if(data.fullname){
            //     str+= '                                        <input type="text" placeholder="真实姓名" value="'+data.fullname+'" id="user_fullname">\n' ;
            // }else {
            //     str += '                                        <input type="text" placeholder="真实姓名" id="user_fullname"> \n';
            // }
            str+= '                                    </div>\n' +
                '                                </div>\n' +
                '                                <div class="user-info-box">\n' ;
            if(data.gender===0){
                user_indo_obj.sex=0
                str+='                                    <div class="chooser" type="sex">男</div>\n';
            }else if(data.gender===1){
                user_indo_obj.sex=1
                str+='                                    <div class="chooser" type="sex">女</div>\n';
            }
            else if(data.gender===2){
                user_indo_obj.sex=2
                str+='                                    <div class="chooser" type="sex">保密</div>\n';
            }
            else {
                user_indo_obj.sex=''
                str+='                                    <div class="chooser" type="sex">性别</div>\n';
            }


            str+='                                    <div class="chooser_list hide">\n' +
                '                                        <div class="chooser_item no_next" cid="0">男</div>\n' +
                '                                        <div class="chooser_item no_next" cid="1">女</div>\n' +
                '                                        <div class="chooser_item no_next" cid="2">保密</div>\n' +
                '                                    </div>\n' +
                '                                </div>\n' +
                '                            </div>\n' +
                '                            <div class="user-info-title">职业资料</div>\n' +
                '                            <div class="row">\n' +
                '                                <div class="user-info-box">\n' +
                '                                    <div class="wi1">\n'
            if(data.corporation){
                str+= '                                        <input type="text" placeholder="单位" value="'+data.corporation+'" id="user_corporation">\n'
            }else {
                str += '                                        <input type="text" placeholder="单位" id="user_corporation">\n'
            }
            str+='                                    </div>\n' +
                '                                </div>\n' +
                '                                <div class="user-info-box">\n' ;
            if(data.profession) {
                user_indo_obj.pro=data.profession;
                $.ajax({
                    url:"/front_professional_sections/"+data.profession+'/',
                    type:'get',
                    success:function (data) {
                        $('.user-info-usr .user-info-box div[type=desk]').html(data.data.professionalSections[0].department_name)
                    }
                })
                str+=   '                                    <div class="chooser" type="desk"></div>\n' ;
            }else {
                str+=   '                                    <div class="chooser" type="desk">专业科室</div>\n' ;
            }
            str+='                                    <div class="chooser_list hide">\n' +
                '                                    </div>\n' +
                '                                </div>\n' +
                '                                <div class="user-info-box">\n'
            if(data.jobTitle) {
                user_indo_obj.job=data.jobTitle;
                $.ajax({
                    url:"/front_job_title/"+data.jobTitle+'/',
                    type:'get',
                    success:function (data) {
                        $('.user-info-usr .user-info-box div[type=pro]').html(data.data.jobTitles[0].job_name)
                    }
                })
                str+='                                    <div class="chooser" type="pro"></div>\n'
            }else {
                str+='                                    <div class="chooser" type="pro">职称</div>\n';
            }
            str+=   '                                    <div class="chooser_list hide">\n' +
                '                                    </div>\n' +
                '                                </div>\n' +
                '                            </div>\n' +
                '                            <div class="user-info-title">联系方式</div>\n' +
                '                            <div class="row">\n' +
                '                                <div class="user-info-box">\n' ;

            if(data.mobile){
                str+='                                    <input type="tel" title="此项暂时禁止修改"  disabled="disabled"  placeholder="手机号" value="'+data.phone+'" id="user_mobile">\n' ;
            }else {
                str+='                                    <input type="tel" title="此项暂时禁止修改"  disabled="disabled"  placeholder="手机号" id="user_mobile">\n' ;
            }


            str+=  '                                </div>\n' +
                '                                <div class="user-info-box">\n' ;
            if(data.email){
                str+= '                                    <input type="email" title="此项暂时禁止修改" disabled="disabled" placeholder="邮箱" value="'+data.email+'" id="user_email">\n' ;
            }
            else{
                str+= '                                    <input type="email" title="此项暂时禁止修改" disabled="disabled" placeholder="邮箱" id="user_email">\n' ;
            }


            str+=   '                                </div>\n' +
                '                            </div>\n' +
                '                            <div class="user-info-title">一句话简介</div>\n' +
                '                            <div class="row mar-bot40">\n'
            if(data.signature){
                str+=  '                                <div class="user-info-box width-1"><input type="text" placeholder="(28个字以内)" value="'+data.signature+'" id="user_signature"></div>\n'
            }else {
                str+=  '                                <div class="user-info-box width-1"><input type="text" placeholder="(28个字以内)" id="user_signature"></div>\n'
            }


            str+=     '                            </div>\n'
            return str;
        })

        var inputter_id_list = ['#trueName','#user_username','#user_fullname','#user_corporation','#user_mobile','#user_email','#user_signature',"#user_old_password","#user_new_password","#user_repeat_password"]
        inputter_id_list.forEach((id)=>{
            $(id).on('input',()=>{
                $(".user_pg_submit").removeClass('disabled')
            })
        })
        $(".chooser_item").click(function(){
            $(".user_pg_submit").removeClass('disabled')
        })
    }

});

/*
* 个人中心 && 修改密码
* */
var user_info_url='/user_info/';
var user_info_pass='user'
$(document.body).on('click','.user-info-tag div',function (t) {
    // 个人中心,修改密码,我的勋章三部分导航
    $(this).addClass('checked').siblings().removeClass('checked');
    // user_info_url=$(this).attr('ajax-url');
    user_info_pass=$(this).attr('type');
    if($(t.target).hasClass("medal_button")){
        $(".submit").hide()
    }else{
        $(".submit").show()
    }
    $('.user-info .user-info-bot div div[type='+user_info_pass+']').removeClass('hide').siblings().addClass('hide')
    hide_message_box()
    $(".user_pg_submit").addClass("disabled")
});
function hide_message_box(){
    $('.user-info-bot').find(".information_error_box").hide()
    $('.user-info-bot').find(".information_success_box").hide()
}
function show_error_message(message){
    $('.user-info-bot').find(".information_success_box").hide()
    $('.user-info-bot').find(".information_error_box").html(message).show()
}
function show_success_message(message){
    $('.user-info-bot').find(".information_error_box").hide()
    $('.user-info-bot').find(".information_success_box").html(message).show()
    setTimeout(()=>{
        $('.user-info-bot').find(".information_success_box").hide()
    },1500)
}
function post_user_info() {
    if(user_info_pass==="user") {
        hide_message_box()
        $.ajax({
            url: user_info_url,
            data: {
                signature: $('#user_signature').val(),
                avatar: user_indo_obj.img,
                fullname: $('#user_fullname').val(),
                username: $('#user_username').val(),
                gender: user_indo_obj.sex,
                corporation: $('#user_corporation').val(),
                profession_id: user_indo_obj.pro,
                job_id: user_indo_obj.job,
                phone: $('#user_mobile').val(),
                email: $('#user_email').val(),

            },
            type: 'post',
            success: function (data) {
                if(data.code==200){
                    $('.user-bar .user-bar-top-name span').html($('#user_username').val());
                    $('.user-bar .user-bar-top-img span').css('background','url(/images/avatar/'+user_indo_obj.img+') no-repeat').css('background-size','cover');
                    $('.user-bar .user-bar-top-des span').html($('#user_signature').val());
                    show_success_message("保存成功")
                    $(".user_pg_submit").addClass("disabled")
                    // window.location.reload()
                }else{
                    show_error_message(data.message)
                }
            }
        })
    }else if(user_info_pass==="pass"){
        hide_message_box()
        var new_password = $('#user_new_password').val()
        var repeat_password = $('#user_repeat_password').val()
        if((new_password.length<4||repeat_password.length<4)||((new_password.length>16||repeat_password.length>16))){
            show_error_message("请输入4-16位长度的密码!")
            return
        }
        if(new_password!==repeat_password){
            show_error_message("两次密码不一致!")
            return
        }
        $.ajax({
            url: '/reset_password/',
            data: {
                old_password:$('#user_old_password').val(),
                new_password:$('#user_new_password').val(),
                repeat_password:$('#user_repeat_password').val()
            },
            type: 'post',
            success: function (data) {
                if(data.code===200){
                    show_success_message("密码修改成功")
                    $(".user_pg_submit").addClass("disabled")
                    $('#user_old_password').val('')
                    $('#user_new_password').val('')
                    $('#user_repeat_password').val('')
                }else {
                    show_error_message(data.message)
                }
            }
        })
    }
}


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
                user_indo_obj.sex=$(this).attr('cid')
                _self.removeClass('chooser_active')
                _self.next('.chooser_list').addClass('hide');
            })
            break
        case "desk":
            $('.chooser[type=sex]').removeClass('chooser_active');
            $('.chooser[type=sex]').next('.chooser_list').addClass('hide');
            $('.chooser[type=pro]').removeClass('chooser_active');
            $('.chooser[type=pro]').next('.chooser_list').addClass('hide');
            user_got_desk(_self,{id:0})
            _self.next('.chooser_list').on('click','.chooser_item',function () {
                user_got_desk(_self,{id:$(this).attr('cid'),text:$(this).attr('text')})

            })
            break
        case "pro":
            $('.chooser[type=sex]').removeClass('chooser_active');
            $('.chooser[type=sex]').next('.chooser_list').addClass('hide');
            $('.chooser[type=desk]').removeClass('chooser_active');
            $('.chooser[type=desk]').next('.chooser_list').addClass('hide');
            user_got_pro(_self,{id:0})
            _self.next('.chooser_list').on('click','.chooser_item',function () {
                user_got_pro(_self,{id:$(this).attr('cid'),text:$(this).attr('text')})

            })
            break
    }

})




/*
* 获取科室
* */


function user_got_desk(tar,obj) {
    AJAX({
        type: 'get',
        url: '/front_professional_sections/'+obj.id+'/',
        data: {},
        fn: function (data) {
            tar.next('.chooser_list').html('')
            var list=data.data.professionalSections
            if (list.length > 1) {
                tar.next('.chooser_list').html(function () {
                    var str='';
                    for(var i=0;i<list.length;i++){
                        str+='<div class="chooser_item" cid="'+list[i].id+'" text="'+list[i].department_name+'">'+list[i].department_name+'</div>'
                    }
                    return str;
                })

            }else {
                tar.html(obj.text);
                user_info_chose.profession=obj.id;
                user_indo_obj.pro=obj.id
                tar.removeClass('chooser_active')
                tar.next('.chooser_list').addClass('hide');
                $('.user_pg_submit').removeClass("disabled")
            }
        },
        error: function () {
            tar.next('.chooser_list').html('')
            var list=data.data.professionalSections
            if (data.data.professionalSections.length > 1) {
                tar.next('.chooser_list').html(function () {
                    var str='';
                    for(var i=0;i<list.length;i++){
                        str+='<div class="chooser_item" cid="'+list[i].id+'" text="'+list[i].department_name+'">'+list[i].department_name+'</div>'
                    }
                    return str;
                })

            }else {
                tar.html(obj.text);
                user_info_chose.profession=obj.id;
                user_indo_obj.pro=obj.id
                tar.removeClass('chooser_active')
                tar.next('.chooser_list').addClass('hide');
            }
        }
    })
}
function user_got_pro(tar,obj) {
    AJAX({
        type: 'get',
        url: '/front_job_title/'+obj.id+'/',
        data: {},
        fn: function (data) {
            tar.next('.chooser_list').html('')
            var list=data.data.jobTitles
            if (data.data.jobTitles.length > 1) {
                tar.next('.chooser_list').html(function () {
                    var str='';
                    for(var i=0;i<list.length;i++){
                        str+='<div class="chooser_item" cid="'+list[i].id+'" text="'+list[i].job_name+'">'+list[i].job_name+'</div>'
                    }
                    return str;
                })

            }else {
                tar.html(obj.text);
                user_info_chose.profession=obj.id;
                user_indo_obj.job=obj.id;
                tar.removeClass('chooser_active')
                tar.next('.chooser_list').addClass('hide');
                $('.user_pg_submit').removeClass("disabled")
            }
        },
        error: function () {
            tar.next('.chooser_list').html('')
            var list=data.data.professionalSections
            if (data.data.professionalSections.length > 1) {
                tar.next('.chooser_list').html(function () {
                    var str='';
                    for(var i=0;i<list.length;i++){
                        str+='<div class="chooser_item" cid="'+list[i].id+'" text="'+list[i].department_name+'">'+list[i].department_name+'</div>'
                    }
                    return str;
                })

            }else {
                tar.html(obj.text);
                user_info_chose.profession=obj.id;
                user_indo_obj.job=obj.id;
                tar.removeClass('chooser_active')
                tar.next('.chooser_list').addClass('hide');
            }
        }
    })
}
$(document).on("change", "#trueName", function () {
    var oMyForm;
    var _self = this;
    if (!this['value'].match(/.jpg|.gif|.png|.bmp|.JPEG|svg|/i)) {
        $().alert_box('请选择图片格式上传')
        return
    }
    var oMyForm = new FormData();
        oMyForm.append("imgFile", $('#trueName')[0].files[0]);
        $.ajax({
            type: 'post',
            url: '/extends/image_storage/avatar/',
            data: oMyForm,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function(e) {
                user_indo_obj.img=e.data;
                $('.user-info-box .selector_img').css('background-image','url(/images/avatar/'+e.data+')').css('background-size', 'cover;')
            }

        })
})