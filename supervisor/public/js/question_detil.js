/*
* tag_list      标签列表
* page          问题页码
* child_page：  评论页码
* ques_id :     问题id
* ques_type:    问题分类
* ques_type_id: 问题分类id
* ques_user:    问题作者
* ques_time:    问题时间
*
* ans_id  :     评论id;
* ans_user :    评论人名
* ans_time:     评论时间
* */
var tag_list,child_page,ques_id,ques_type,ques_user,ques_time,ques_type_id;

var ques_id=null,ans_id=0,par_page=1,child_page=1;
function loca(href) {
    var obj={}
    href=encodeURI(href).replace('#','');
    href=href.split('?')[1];
    try{
        href = href.split('&');
        for (var i = 0; i < href.length; i++) {
            var a = href[i].split('=')[0]
            var b = href[i].split('=')[1]
            obj[a] = b;
        }
        if(!obj.p){

            window.location.href='question.html'
        }
        return obj
    }catch (e){

        window.location.href='question.html'
    }

}

    ques_id = loca(window.location.href).p

detil()
// $('#container').removeClass('hide');
//绑定问题表头
function detil() {
    AJAX({
        url:'/supervisor/question_detail/'+ques_id+'/'+ans_id+'/'+par_page+'/'+child_page+'/',
        type:'get',
        data:'',
        fn:function (data) {
            $('#container').removeClass('hide');
            $('#uesr_ques_box').html('');
            $('#uesr_ques_box').next().remove();
            if(data.code==200){
                data=data.data;
                tag_list=data.question_category_list;
                page=data.current_parent_page;
                ques_id=data.question_id;
                ques_type=data.question_category;
                ques_user=data.question_author;
                ques_time=data.question_create_time;
                ques_type_id=data.question_category_id
                //    头像
                if(!!data.question_author_avatar){
                    $('.user_ques_top .user_quer_left .user-box').css('background', 'url(/images/avatar/'+ data.question_author_avatar+ ') no-repeat')
                }
                //问题
                $('.user_ques_top .user_top_title').html(data.content);

                //标签
                $('.user_ques_top .icon-title-tag').html(ques_type);
                $('.user_ques_top .reset_chose').attr('ques_type_id',ques_type_id);
                $('.user_ques_top .reset_chose').attr('ques_id',ques_id);

                //问题作者
                $('.user_ques_top  .ques_user_title').html(ques_user)

                //提问时间
                $('.user_ques_top  .ques_time_title').html(ques_time)


                //没有评论
                if(!data.answers){
                    $('#uesr_ques_box').html('<div class="comment_box min-heihgt-178">' +
                        '<div class="no_comment">' +
                        '<div class="no_comment_img"></div>' +
                        '<div class="no_comment_text">目前暂无回答，快来抢沙发~</div>' +
                        '</div>' +
                        '</div>');
                    $('#content').css('heihgt','auto')
                    return;
                }

                //评论
                var ans_box=document.createDocumentFragment();
                var ans=data.answers;
                for(var i=0;i<ans.length;i++){
                    var div=CREATE_TAG('div')
                    div.className="user_ques_con";
                    var div_left    = $("<div class='inline user_quer_left'></div>").html(function () {
                        if(ans[i].answer_user_avatar){
                            return '<span class="user-box" style="background:url(/images/avatar/'+ans[i].answer_user_avatar +') no-repeat"></span>';
                        }else{
                            return '<span class="user-box"></span>';
                        }
                    });
                    $(div).append(div_left)
                    var div_right=$('<div class=" user_quer_right"></div>');
                    div_right.append('<div class="user_top_title line-height30" id="'+ans[i].answer_id+'">'+ans[i].answer_username+'</div>');
                    div_right.append('<div class="user_top_content">'+ans[i].comment+'</div>');
                    div_right.append('<div><textarea></textarea></div>')
                    var ask_box;
                    if(ans[i].child_answers){
                        var ans_inner=  $('<div class="ques_aks_text mar-top15"></div>');
                        var ul_box=$('<ul class="ques_aks_list"></ul>')
                        var ans_child=ans[i].child_answers;
                        //子评论列表
                        for(var j=0;j<ans_child.length;j++){
                            var oLis=$('<li></li>')
                            oLis.append('<div class="user_top_content">'+ans_child[j].comment+'</div>');
                            oLis.append('<div><textarea></textarea></div>')
                            ask_box=$('<div class="font-14 line-height30 mar-top10 color-gre"></div>');
                            if(ans_child[j].relay_to){
                                ask_box.append('<span class="mar-rig40 user_con_usr"><span>'+ans_child[j].answer_username+'</span>&nbsp;回复&nbsp;<span>'+ans_child[j].relay_to+'</span></span>')
                            }else{
                                ask_box.append('<span class="mar-rig40 user_con_usr"><span>'+ans_child[j].answer_username+'</span></span>')
                            }
                            ask_box.append('<span class="user_con_time">'+ans_child[j].create_time+'</span>');
                            ask_box.append('<span class="right">'+'<span class="ques_user_del" ans_id="'+ans_child[j].answer_id+'" ques_id="'+ques_id+'" hash_id="'+ans[i].answer_id+'">删除</span>'+'</span>');
                            // ask_box.append('<span class="right">'+'<span class="ques_user_text">编辑</span>&nbsp;|&nbsp;<span class="ques_user_del" ans_id="'+ans_child[j].answer_id+'" ques_id="'+ques_id+'" hash_id="'+ans[i].answer_id+'">删除</span>'+'</span>');

                            oLis.append(ask_box)
                            ul_box.append(oLis);
                        }
                        ans_inner.append(ul_box);
                        //分页列表
                        ans_inner.append(PAGE_LIST(1,{page:ans[i].current_child_page,count:ans[i].child_page_count}, ans[i].answer_id))

                        div_right.append(ans_inner)
                    }
                    else{
                        ask_box=$('<div class="font-14 line-height30 mar-top10 color-gre"></div>');
                        ask_box.append('<span class="user_con_time">'+ans[i].create_time+'</span>');
                        ask_box.append('<span class="right">'+'<span class="ques_user_del" ans_id="'+ans[i].answer_id+'" ques_id="'+ques_id+'" hash_id="'+ans[i].answer_id+'">删除</span>'+'</span>');
                        // ask_box.append('<span class="right">'+'<span class="ques_user_text">编辑</span>&nbsp;|&nbsp;<span class="ques_user_del" ans_id="'+ans[i].answer_id+'" ques_id="'+ques_id+'" hash_id="'+ans[i].answer_id+'">删除</span>'+'</span>');

                        div_right.append(ask_box)
                    }
                    $(div).append(div_right);
                    ans_box.appendChild(div);
                    $('#uesr_ques_box')[0].appendChild(ans_box);
                }
                $('#uesr_ques_box').after(PAGE_LIST(0,{page:data.current_parent_page,count:data.parent_page_count},0))

            }
        }

    })
}



//标签列表

function TAG_LIST(opt) {
    /*
    * opt.item :    已选标签id
    * opt.id ：      问题id
    * opt.fn：       回调函数
    * */
    var data=tag_list;
    AJAX({
        url:'/supervisor/question_category_list/',
        type:'get',
        fn:function (data) {
            if(data.code!==200){
                alert(data.message);
                return
            }
            var data=data.data.question_category_list;
            var str = '';
            for (var i = 0; i < data.length; i++) {
                if (data[i].id !== opt.item) {
                    str += '<span class="icon-title-tag" p_id="' + data[i].id + '" p_text="' + data[i].category + '">' + data[i].category + '</span>'
                }
            }
            opt.fn(str);
        }
    })

}
//创建标签
function CREATE_TAG(str) {
    return document.createElement(str);
}

/*
* list     {
*               page:页数，
*               count:总页码
*           }
* */
function PAGE_LIST(item,list,ans) {
    if(list.count<=1){
        return
    }

    var list_box,page,count,start,end;
    page=list.page;
    count=list.count;
    if(item===0){
        ans=0;
        list_box=$('<div class="page_list text-rig mar-rig70 out_page-list"></div>');
page=Number(par_page)

    }else if(item===1){
        list_box=$('<div class="page_list text-cen"></div>')
page=Number(child_page);
    }
    var  ul_box=$('<ul></ul>');
    if(page!==1){
        ul_box.append('<li class="first" p_id="1" ans_id="'+ans+'">首页</li>')
        ul_box.append('<li class="prev" p_id="'+(page-1)+'" ans_id="'+ans+'">上一页</li>')
    }
    if (count - Number(page) > 2 && Number(page) > 2 && count > 5) {
        start = Number(page) - 3;
        end = Number(page) + 2
    }
    else if (count - Number(page) <= 2 && count > 5) {
        start = pagecount - 6;
        end = pagecount;
    }
    else if (Number(page) <= 2 && count > 5) {
        start = 0;
        end = 5
    }
    else if (count <= 5) {
        start = 0;
        end = count;
    }
    // if(count- Number(page) >2 && Number(page) >2){
    //     start=Number(page)-2;
    //     end=Number(page)+2
    // } else if(count-Number(page)<=2){
    //     start=count-4;
    //     end=count;
    // } else if(Number(page)<=2 && count>=5){
    //     start=1;
    //     end=5
    // } else if(count<=5){
    //     start=1;
    //     end=page;
    // }

    for (var i = start; i < end; i++) {
        if (Number(page) === (i + 1)) {
            ul_box.append('<li class="page checked" p_id="'+ (Number(i)+1)+'" ans_id="'+ans+'">'+ (Number(i) + 1)+'</li>')
        }else {
            ul_box.append('<li class="page" p_id="' + (Number(i) + 1) + '" ans_id="'+ans+'">' + (Number(i) + 1) + '</li>')
        }
    }
    if(count!==page){
         ul_box.append('<li class="next" p_id="'+(page+1)+'" ans_id="'+ans+'">下一页</li>')
        ul_box.append('<li class="last" p_id="'+count+'" ans_id="'+ans+'">尾页</li>')
    }
    list_box.append(ul_box);
    list_box.append(' <span>共 '+count+' 页，跳至</span>')
    list_box.append('&nbsp;<input type="text" page="'+count+'" ans_id="'+ans+'">&nbsp;');
    list_box.append('<span>页</span>');
    // $(this).append(list_box);
    return list_box;
}