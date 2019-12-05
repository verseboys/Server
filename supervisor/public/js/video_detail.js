//分页状态管理
class pageX{
    constructor(){
        this.comment=1
        this.comment_num=0
        this.bill_all=1
        this.bill_all_num=0
        this.bill_search=1
        this.bill_search_num=0
        this.feedback=1
        this.feedback_num=0
        this.type=null
        this.state=null
        this.val=null
    }
    getType() {
        if($('.comment_container:visible').length==1){
            this.type="comment"
            return this.type
        }else if($('.orders_all_container:visible').length==1){
            this.type="bill_all"
            return this.type
        }else if($('.orders_search_container:visible').length==1){
            this.type="bill_search"
            return this.type
        }else if($('.feedback_container:visible').length==1){
            this.type="feedback"
            return this.type
        }else{
            return
        }
    }
    add(){
        console.log(this.getType())
        if(this.getType()=="comment"){
            this.comment+=1
            if(this.comment>this.comment_num){
                this.comment=this.comment_num
            }
        }else if(this.getType()=="bill_all"){
            this.bill_all+=1
            if(this.bill_all>this.bill_all_num){
                this.bill_all=this.bill_all_num
            }
        }else if(this.getType()=="bill_search"){
            this.bill_search+=1
            if(this.bill_search>this.bill_search_num){
                this.bill_search=this.bill_search_num
            }
        }else if(this.getType()=="feedback"){
            this.feedback+=1
            if(this.feedback>this.feedback_num){
                this.feedback=this.feedback_num
            }
        }else{
            return 
        }
    }
    less(){
        if(this.getType()=="comment"){
            this.comment-=1
            if(this.comment<1){
                this.comment=1
            }
        }else if(this.getType()=="bill_all"){
            this.bill_all-=1
            if(this.bill_all<1){
                this.bill_all=1
            }
        }else if(this.getType()=="bill_search"){
            this.bill_search-=1
            if(this.bill_search<1){
                this.bill_search=1
            }
        }else if(this.getType()=="feedback"){
            this.feedback-=1
            if(this.feedback<1){
                this.feedback=1
            }
        }else{
            return 
        }
    }
    to(num){
        num=parseInt(num)
        switch(this.type){
            case "comment":this.comment=num;break;
            case "bill_all":this.bill_all=num;break;
            case "bill_search":this.bill_search=num;break;
            case "feedback":this.feedback=num;break;
        }
    }
    getPage(){
        switch(this.type){
            case "comment":return this.comment;break;
            case "bill_all":return this.bill_all;break;
            case "bill_search":return this.bill_search;break;
            case "feedback":return this.feedback;break;
        }
    }
    toLast(){
        switch(this.type){
            case "comment":this.comment=this.comment_num;break;
            case "bill_all":this.bill_all=this.bill_all_num;break;
            case "bill_search":this.bill_search=this.bill_search_num;break;
            case "feedback":this.feedback=this.feedback_num;break;
        }
    }
    getPageNum(){
        switch(this.type){
            case "comment":return this.comment_num;break;
            case "bill_all":return this.bill_all_num;break;
            case "bill_search":return this.bill_search_num;break;
            case "feedback":return this.feedback_num;break;
        }
    }
    setPageNum(num){
        num=parseInt(num)
        switch(this.type){
            case "comment":this.comment_num=num;break;
            case "bill_all":this.bill_all_num=num;break;
            case "bill_search":this.bill_search_num=num;break;
            case "feedback":this.feedback_num=num;break;
        }
    }
    openSearch(){
        this.state="search"
        this.to(1)
    }
    closeSearch(){
        this.state=null
        this.val=null
        this.to(1)
    }
    setVal(val){
        this.val=val
    }
}
let page=new pageX()
//解析查询字符串
let parseQueryString = function (str) {
    var reg = /(([^?&=]+)(?:=([^?&=]*))*)/g;
    var result = {};
    var match;
    var key;
    var value;
    while (match = reg.exec(str)) {
        key = match[2];
        value = match[3] || '';
        result[key] = decodeURIComponent(value);
    }
    return result;
}
let main_id=parseQueryString(window.location).id
let getCourseMessage=null
if(main_id!==undefined){
    //修改模式
    getCourseMessage=new Promise(function(resolve,reject){
        $.ajax({
            url:"/supervisor/alter_course/"+main_id+"/",
            type:"GET",
            success:function(data){
                let response=data.data
                if(data.code==200){
                    $("#studyName").val(response.course)
                    $("#study_introduce").html(response.course_intro)
                    $("#teacher_introduce").html(response.teach_intro)
                    if(response.price==0){
                        $(".study_price_radio:eq(0)").attr("checked",true)
                    }else{
                        $(".study_price_radio:eq(1)").attr("checked",true)
                        $(".price_input").val(response.price)
                    }
                    $(".study_img img").attr("src","/images/article_images/"+response.thumbnail+"/")
                    resolve({isCourseExist:true,data:response})
                }else{
                    alert(data.message)
                    reject()
                }
            },
            error:function(){
                alert("获取课程信息接口错误")
                reject()
            }
        })
    })
}else{
    getCourseMessage=Promise.resolve({isCourseExist:false})
}
//getObjectURL兼容
function getObjectURL(file) {
    var url = null;
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}
//时间格式化
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
let editor_handler=function(){
    let t=$(this)
    let editorContainer=$(".public_editor")
    editorContainer.show()
    CKEDITOR.instances.ask_area.setData(t.html())
    editorContainer.find(".save_button").unbind('click').removeAttr('onclick').click(function(){
        t.html(CKEDITOR.instances.ask_area.getData())
        editorContainer.hide()
    })
    editorContainer.find(".cancel_button").unbind('click').removeAttr('onclick').click(function(){
        editorContainer.hide()
    })
}
//提交基本信息
$("#study_introduce").click(editor_handler)
$("#teacher_introduce").click(editor_handler)
let submitBasic=function(response){
    let course=$("#studyName").val()
    let course_intro=$("#study_introduce").html()
    let teach_intro=$("#teacher_introduce").html()
    let thumbnail=null
    let price=null
    let priceState=$(".study_price_radio:checked")
    let imgId=null
    try{
        thumbnail=$("#study_image")[0].files[0]
    }catch(e){
        thumbnail=null
    }
    if(priceState.length==0){
        window.alert("请选择课程价格")
    }else{
        if(priceState.val()==0){
            price=0
        }else{
            if($(".price_input").val()!==""){
                price=parseFloat($(".price_input").val())
            }
        }
    } 
    let imgReady=null
    if(!response.isCourseExist){
        if(thumbnail==null){
            imgReady=Promise.reject("请上传图片")
        }else{
            imgReady=new Promise(function(resolve,reject){
                let imgForm=new FormData()
                imgForm.append("imgFile",thumbnail)
                //异步上传图片
                $.ajax({
                        url:"/extends/image_storage/article_images/",
                        type:"POST",
                        data:imgForm,
                        processData : false, 
                        contentType : false,
                        success:function(data){
                            if(data.code===200){
                                imgId=data.data
                                resolve()
                            }else{
                                reject("图片上传错误")
                            }
                        },
                        error:function(e){
                            console.log(e)
                            reject("图片上传接口错误")
                        }
                    })
            })
        }
    }else{
        if(thumbnail==null){
            imgId=response.data.thumbnail
            imgReady=Promise.resolve()
        }else{
            imgReady=new Promise(function(resolve,reject){
                let imgForm=new FormData()
                imgForm.append("imgFile",thumbnail)
                //异步上传图片
                $.ajax({
                        url:"/extends/image_storage/article_images/",
                        type:"POST",
                        data:imgForm,
                        processData : false, 
                        contentType : false,
                        success:function(data){
                            if(data.code===200){
                                imgId=data.data
                                resolve()
                            }else{
                                reject("图片上传错误")
                            }
                        },
                        error:function(e){
                            console.log(e)
                            reject("图片上传接口错误")
                        }
                    })
            })
        }
    }
    imgReady.then(function(){
        //判定是否可以上传
        if(price!==null&&imgId!==null){
            console.log({course,course_intro,teach_intro,thumbnail,price})
            let formdata=new FormData()
            formdata.append("course",course)
            formdata.append("course_intro",course_intro)
            formdata.append("teach_intro",teach_intro)
            formdata.append("thumbnail",imgId)
            formdata.append("price",price)
            if(response.isCourseExist){
                console.log(course)
                $.ajax({
                    url:"/supervisor/alter_course/"+main_id+"/",
                    type:"POST",
                    processData: false,
                    contentType: false,
                    data:formdata,
                    success:function(data){
                        alert(data.message)
                    },
                    error:function(){

                    }
                }) 
            }else{
                $.ajax({
                    url: "/supervisor/add_course/",
                    type: "POST",
                    data:formdata,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        window.alert(data.message)
                    },
                    error:function(e){
                        console.log(e)
                    }
                })
            }
        }else{
            alert("请将价格及缩略图填写完整")
        }  
    },function(e){
        window.alert(e)
    })
}
getCourseMessage.then(function(response){
    $("#basic_save").click(function(){
        submitBasic(response)
    })
})

$("#study_image").on("change",function(e){
    var imgURL=getObjectURL(e.target.files[0])
    $(".study_img img").attr("src",imgURL)
})
CKEDITOR.replace("ask_area", {customConfig: "../../article_text_setting.js"}, CKEDITOR.on("instanceCreated", function (n) {}))
window.escapeHtml = function(n) {
    var t;
    return t = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
        "/": "&#x2F;"
    },
        String(n).replace(/[&<>"'\/]/g, function(n) {
            return t[n]
        })
}
window.yikalink = function (num) {
    return $("body").append('<div id="shadow_box"><div class="tips_box tps_link"><div class="content_area content_link"><div class="link_name"><input placeholder="请输入内容..."/></div><div class="link_address"><input placeholder="请输入链接..."/></div></div><div class="box_btn_area"><div class="box_btn_multi_left cancel">取消</div><div class="box_btn_multi_right submit submit1">添加</div></div></div></div>'), $(document).on("click", ".submit1", function () {
        var t;

        return t = new RegExp(/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?/), t.test($(".link_address input").val()) ? (CKEDITOR.instances.ask_area.insertHtml("<a href='" + $(".link_address input").val() + "' target='_blank'>" + escapeHtml($(".link_name input").val()) + "</a>"), $("#shadow_box").remove()) : ($(".wrong_image,.wrong_link").remove(), $(".content_link").append('<div class="wrong_image"></div><div class="wrong_link">超链接格式错误</div>'), $(".tps_link").css("min-height", "13.36rem"))
    }), $(document).on("click", ".cancel", function () {
        return $("#shadow_box").remove(), $(document).off("click", ".cancel")
    })

}
// 导航栏开关
$('.hover_block').click(function(e){
    let actionFrom=$(e.currentTarget)
    let containers=$(".public_container")
    if(actionFrom.hasClass("basic_message")){
        containers.filter(".basic_message_container").removeClass("hide").siblings().addClass("hide")
    }else if(actionFrom.hasClass("content")){
        containers.filter(".content_container").removeClass("hide").siblings().addClass("hide")
    }else if(actionFrom.hasClass("price")){
        containers.filter(".price_container").removeClass("hide").siblings().addClass("hide")
        page.closeSearch()
        page.getType()
    }else if(actionFrom.hasClass("comment")){
        containers.filter(".comment_container").removeClass("hide").siblings().addClass("hide")
        page.getType()
        page.closeSearch()
        get_methods()
    }else if(actionFrom.hasClass("feedback")){
        containers.filter(".feedback_container").removeClass("hide").siblings().addClass("hide")
        page.getType()
        page.closeSearch()
        get_methods()
    }
})



    // 获取课程章节
new Promise((resolve)=>{
        $.ajax({
            url: "/supervisor/course_section/",
            type: "GET",
            success: function (data) {
                console.log(data)
                    if(data.code==200){     
                        let html=`<option value="" disabled selected>选择新章节</option>`
                        for(let a in data.data.course_list){
                            html+=`<option value="${data.data.course_list[a].id}">${data.data.course_list[a].category}</option>`
                        }
                        $("#chapter_selector").html(html)
                        resolve()
                    }else{
                        alert("章节信息获取错误")
                    }
            },
            error:function(e){
                alert("获取课程章节接口错误")
                console.log(e)
            }
        })
    }).then(()=>{
        let changeTarget=null
        let changeChaptor=function(e){
            console.log($(this))
            $("#chapter_selector").unbind("change").change(changeChaptor)
            changeTarget=e
            let course_id=$(e.target).val()
            $.ajax({
                url: "/supervisor/course_video/"+course_id+"/",
                type: "GET",
                success: function (data) {
                    if(data.code!==200){
                        console.log(data.message)
                        data.data=[]
                    }
                    console.log(data.data)
                    let html=``
                    for(let a in data.data){
                        html+=
                        `
                        <div>
                            <div class="study_container" style="display:block">
                                <div class="study_title">
                                    <span class="study_number">课时${+a+1}</span>
                                    <span class="content_circle_small"></span>
                                    <input type="text" class="chapter_input" value="${data.data[a].title}" disabled><span class="chapter_edit " data-vid="${data.data[a].video_id}">编辑</span><span class="chapter_delete" data-vid="${data.data[a].video_id}" data-title="${data.data[a].title}">删除</span>
                                </div>
                            </div>
                            <div class="add_study_container" >

                            </div>
                        </div>
                        `
                    }
                    html+=`
                    <div class="add_study_container" >
                    <div class="add_study_title">
                        <span class="study_number"></span>
                        <span class="content_circle_small"></span>
                        <div type="text" class="chapter_input"  style="text-align:center;cursor:pointer;display:inline-block;vertical-align:middle;line-height:32px">+添加新课时</div>
                    </div>
                    <div class="study_content_container" style="display:none">
                    </div>
                    </div>
                    `
                    $(".chapter_container").html(html)
                    //课时删除
                    $(".chapter_delete").click(function(e){
                        let clickTargetData=$(e.target).data()
                        if(window.confirm("是否删除课时："+clickTargetData.title)){
                            $.ajax({
                                url:"/supervisor/delete_video/"+clickTargetData.vid+"/",
                                type:"GET",
                                success:function(data){
                                    if(data.code==200){
                                        changeChaptor(changeTarget)
                                    }else{
                                        window.alert("删除失败")
                                    }
                                },
                                error:function(){
                                    window.alert("删除接口错误")
                                }
                            })
                        }else{
                            return
                        }
                    })
                    //课时编辑
                    $(".chapter_edit").click(function(e){
                        $('.study_content').hide()
                        let clickTarget=$(e.target)
                        let targetAddContainer=clickTarget.parent().parent().siblings(".add_study_container")
                        let video_id=clickTarget.data().vid
                        $.ajax({
                            url: "/supervisor/alter_video/"+video_id+"/",
                            type: "GET",
                            success:function(data){
                                console.log(data)
                                let response=data.data
                                let html=`
                                <div class="study_content" style="display:block">
                                    <table></table>
                                    <div class="study_name">
                                        课时名称：<input type="text" name="study_name" value="${response.title}">
                                    </div>
                                    <div class="study_point">
                                        <!-- 点击打开一个公共的富文本 -->
                                        本节要点:
                                        <div class="point_html_container">
                                            ${response.course_main}    
                                        </div>
                                    </div>
                                    <div class="study_summary">
                                        摘&nbsp&nbsp&nbsp&nbsp要：
                                        <div class="summary_html_container">
                                            ${response.summary}    
                                        </div>
                                    </div>
                                    <div class="video_id">
                                        视频ID：<input type="text" name="video_id" value="${response.polyv_vid}">
                                    </div>
                                    <div class="video_time">
                                        <!-- 是数字还是字符串 -->
                                        视频时长：<input type="text" name="video_time" value="${response.video_time}">
                                    </div>
                                    <div class="tag_state">
                                        标签状态：<input type="radio" name="tag_state" value="0" ${response.is_pay===0?"checked":""}><label for="free">免费</label>
                                                <input type="radio" name="tag_state" value="2" ${response.is_pay===2?"checked":""}><label for="comming">更新中</label>
                                                <input type="radio" name="tag_state" value="1" ${response.is_pay===1?"checked":""}><label for="charge">收费</label>
                                    </div>
                                    <div class="release_state">
                                        发布状态：<input type="radio" name="release_state" value="1"  ${response.status===1?"checked":""}><label for="finish">已发布</label>
                                                <input type="radio" name="release_state" value="2"  ${response.status===2?"checked":""}><label for="draft">草稿</label>
                                    </div>
                                    <div class="release_date">
                                            <!-- new Date(new Date(response.create_time).getTime()+8*60*60*1000)-->
                                        发布时间：<input type="datetime-local" name="release_date" value="${response.create_time}">
                                    </div>
                                    <div class="download_file">
                                        资料下载：<ul class="file_container">
                                                    <li class="one_file">测试1<button type="button" class="delete_button" data-file-id="">删除</button></li>
                                                    <li class="one_file">测试2<button type="button" class="delete_button" data-file-id="">删除</button></li>
                                                </ul>
                                                <div>
                                                        <a href="javascript:;" class="file add_button">+添加
                                                            <input type="file" name="video_file" id="" style="display:inline-block">
                                                        </a>
                                                </div>
                                    </div>
                                    <div class="img_min">
                                        缩略图：<div class="real_img_min_container img_min_container">
                                                    <input type="file" style="display:block;opacity:0;position:absolute;top:0;left:0;z-index:10" class="img_min_container"> 
                                                    <img src="${response.thumbnail=="null"?"":"/images/article_images/"+response.thumbnail}" style="display:inline-block;position:absolute;top:0;left:0;z-index:1" class="img_min_container">
                                                </div>
                                    </div>
                                    <div class="teacher_introduction_container">
                                        讲者简介(仅科研项目使用)：
                                        <br>
                                        <div class="teacher_introduction_html_container">
                                            ${response.teacher_introduction}
                                        </div>
                                    </div>
                                    <div class="save_cancel_container">
                                        <div  class="save_button">保存</div>
                                        <div  class="cancel_button">取消</div>
                                    </div>
                                </div>
                                `
                                targetAddContainer.html(html)
                                let files=[]
                                let deleteFiles=[]
                                let uploadFiles=[]
                                //给本节要点与摘要绑定富文本
                                targetAddContainer.find(".point_html_container").click(editor_handler)
                                targetAddContainer.find(".summary_html_container").click(editor_handler)
                                targetAddContainer.find(".teacher_introduction_html_container").click(editor_handler)
                                //拿到原有的文件列表
                                for(let a of response.video_related_data){
                                    files.push({name:a.file_name,state:"old",file_id:a.id})
                                }
                                let compileFileList=function(){
                                    let html=``
                                    for(let file of files){
                                        //新旧文件状态判定
                                        html+=`
                                            <li class="one_file">${file.name}<button type="button" class="delete_button" data-file-id="${file.state=="old"?file.file_id:""}">删除</button></li>
                                        `
                                    }
                                    let fileListContainer=targetAddContainer.find('.file_container')
                                    fileListContainer.html(html)
                                    //绑定删除事件(新旧文件靠data判定)
                                    targetAddContainer.find('button.delete_button').click(function(e){
                                        let deleteButton=$(e.target)
                                        let fileIndex=fileListContainer.children().index(deleteButton.parent())
                                        if(deleteButton.data().fileId==""){
                                            files.splice(fileIndex,1)
                                            compileFileList()
                                        }else{
                                            //删除原有文件
                                            deleteFiles.push(files.splice(fileIndex,1)[0])
                                            compileFileList()
                                        }
                                    })
                                }
                                compileFileList()
                                targetAddContainer.find("input[name='video_file']").on('change',function(e){
                                    if(e.target.files[0]!=undefined){
                                        files.push(e.target.files[0])
                                        compileFileList()
                                    }else{
                                        //关闭上传框
                                        return
                                    }
                                })
                                //缩略图
                                let imgFile=null
                                targetAddContainer.find("input.img_min_container").on('change',function(e){
                                    imgFile=e.target.files[0]
                                    var imgURL=getObjectURL(imgFile)
                                    targetAddContainer.find("img.img_min_container").attr("src",imgURL)
                                })
                                //点击保存
                                targetAddContainer.find(".save_button").click(function(){
                                    //保存返回的file哈希
                                    let fileId=[]
                                    //保存返回的img哈希
                                    let imgId=response.thumbnail
                                    let imgUpload=imgFile===null?Promise.resolve():new Promise(function(resolve,reject){
                                        //上传图片
                                        let imgForm=new FormData()
                                        imgForm.append('imgFile',imgFile)
                                        $.ajax({
                                            url:"/extends/image_storage/article_images/",
                                            type:"POST",
                                            data:imgForm,
                                            processData : false, 
                                            contentType : false,
                                            success:function(data){
                                                if(data.code===200){
                                                    imgId=data.data
                                                    resolve()
                                                }else{
                                                    alert("图片上传错误")
                                                    reject()
                                                }
                                            },
                                            error:function(e){
                                                alert("图片上传接口错误")
                                                console.log(e)
                                                reject()
                                            }
                                        })
                                    })      
                                    //上传文件(多个文件分次上传)
                                    for(let a of files){
                                        if(a.state===undefined)
                                        uploadFiles.push(a)
                                    }
                                    let fileUploadPromise=new Promise(function(solve,wrong){
                                        let fileUpload=null
                                        function uploadFile(file){
                                                if(file==undefined){
                                                    //最后一次promise这里面嵌套其余上传逻辑
                                                    solve()
                                                    return 
                                                }
                                                let fileForm=new FormData()
                                                fileForm.append("file_info",file)
                                                fileUpload=new Promise(function(resolve,reject){
                                                    $.ajax({
                                                        url:"/extends/upload_file/video/",
                                                        type:"POST",
                                                        data:fileForm,
                                                        processData : false, 
                                                        contentType : false,
                                                        success:function(data){
                                                            if(data.code===200){
                                                                fileId.push(data.data)
                                                                resolve(uploadFiles.pop())
                                                            }else{
                                                                alert("文件上传错误")
                                                                console.log(data.message)
                                                                reject()
                                                            }
                                                        },
                                                        error:function(e){
                                                            alert("文件上传接口错误")
                                                            console.log(e)
                                                            reject()
                                                        }
                                                    })
                                                }).then((file)=>{
                                                    uploadFile(file)
                                                },()=>{wrong("上传错误")})
                                        }
                                        //多文件异步上传(继发)
                                        uploadFile(uploadFiles.pop())
                                    })
                                    fileUploadPromise.then(function(){
                                        //多文件异步删除
                                        let fileDeletePromise=new Promise(function(solve,wrong){
                                            let fileDelete=null
                                            function deleteFile(file){
                                                    if(file==undefined){
                                                        //最后一次promise这里面嵌套其余上传逻辑
                                                        solve()
                                                        return 
                                                    }
                                                    fileDelete=new Promise(function(resolve,reject){
                                                        $.ajax({
                                                            url:"/supervisor/delete_video_related_data/"+file.file_id+"/",
                                                            type:"GET",
                                                            success:function(data){
                                                                if(data.code===200){
                                                                    console.log(deleteFiles)
                                                                    resolve(deleteFiles.pop())
                                                                }else{
                                                                    alert("文件删除错误")
                                                                    console.log(data.message)
                                                                    reject()
                                                                }
                                                            },
                                                            error:function(e){
                                                                alert("文件删除接口错误")
                                                                console.log(e)
                                                                reject()
                                                            }
                                                        })
                                                    }).then((file)=>{
                                                        deleteFile(file)
                                                    },()=>{wrong("删除错误")})
                                            }
                                            //多文件异步删除(继发)
                                            deleteFile(deleteFiles.pop())
                                        })
                                        fileDeletePromise.then(function(){
                                            Promise.all([imgUpload]).then(function(){
                                                let changeVideoMessage=new FormData()
                                                //课时名称
                                                changeVideoMessage.append("title",targetAddContainer.find("input[name='study_name']").val())
                                                //本接要点(富文本)
                                                changeVideoMessage.append("course_main",targetAddContainer.find("div.point_html_container").html())
                                                //摘要(富文本)
                                                changeVideoMessage.append("summary",targetAddContainer.find("div.summary_html_container").html())
                                                //保利id
                                                changeVideoMessage.append("polyv_id",targetAddContainer.find("input[name='video_id']").val().trim())
                                                //课程id
                                                changeVideoMessage.append("course_id",response.course_id+"")
                                                //视频收费状态
                                                changeVideoMessage.append("is_pay",targetAddContainer.find("input[name='tag_state']:checked").val())
                                                //视频发布状态
                                                changeVideoMessage.append("status",targetAddContainer.find("input[name='release_state']:checked").val())
                                                //视频时长
                                                changeVideoMessage.append("video_time",targetAddContainer.find("input[name='video_time']").val())
                                                //视频创建时间
                                                //new Date(new Date(response.create_time).getTime()+8*60*60*1000)
                                                changeVideoMessage.append("create_time",new Date(new Date($("input[name='release_date']").val()).getTime()).Format("yyyy-MM-dd hh:mm:ss"))
                                                //视频附件
                                                //fileId.push(imgId)
                                                for(let a in fileId){
                                                    changeVideoMessage.append("video_realted_data", fileId[a])
                                                }
                                                //视频缩略图
                                                changeVideoMessage.append("thumbnail",imgId)
                                                //科研项目用讲者简介
                                                changeVideoMessage.append("teacher_introduction",targetAddContainer.find("div.teacher_introduction_html_container").html())
                                                // console.log("xx",{
                                                //         "title":targetAddContainer.find("input[name='study_name']").val(),
                                                //         "course_main":targetAddContainer.find("div.point_html_container").html(),
                                                //         "summary":targetAddContainer.find("div.summary_html_container").html(),
                                                //         "polyv_id":targetAddContainer.find("input[name='video_id']").val().trim(),
                                                //         "course_id":response.course_id+"",
                                                //         "is_pay":targetAddContainer.find("input[name='tag_state']:checked").val(),
                                                //         "status":targetAddContainer.find("input[name='release_state']:checked").val(),
                                                //         "video_time":targetAddContainer.find("input[name='video_time']").val(),
                                                //         "create_time":new Date(response.create_time).Format("yyyy-MM-dd hh:mm:ss"),
                                                //         "video_related_data":fileId
                                                //     })
                                        
                                                $.ajax({
                                                    url:"/supervisor/alter_video/"+video_id+"/",
                                                    type:"POST",
                                                    data:changeVideoMessage,
                                                    contentType:false,
                                                    processData:false,
                                                    success:function(data){
                                                        window.alert(data.message)
                                                    },
                                                    error:function(){

                                                    }
                                                })
                                            })
                                        },function(message){console.log(message)})  
                                        
                                    },function(message){console.log(message)})


                                })
                                //点击取消
                                targetAddContainer.find(".cancel_button").click(function(){
                                    changeChaptor(changeTarget)
                                })
                            },
                            error:function(){
                                alert("获取视频信息接口错误")
                            }
                        })
                        targetAddContainer.find(".study_content").show()
                    })
                    //课时添加
                    $(".chapter_input").click(function(){
                        $('.study_content').hide()
                        let targetAddContainer=$(this).parent().siblings(".study_content_container")
                        targetAddContainer.show()
                                let html=`
                                <div class="study_content" style="display:block">
                                    <table></table>
                                    <div class="study_name">
                                        课时名称：<input type="text" name="study_name" value="">
                                    </div>
                                    <div class="study_point">
                                        <!-- 点击打开一个公共的富文本 -->
                                        本节要点:
                                        <div class="point_html_container"> 
                                        </div>
                                    </div>
                                    <div class="study_summary">
                                        摘&nbsp&nbsp&nbsp&nbsp要：
                                        <div class="summary_html_container"> 
                                        </div>
                                    </div>
                                    <div class="video_id">
                                        视频ID：<input type="text" name="video_id" value="">
                                    </div>
                                    <div class="video_time">
                                        <!-- 是数字还是字符串 -->
                                        视频时长：<input type="text" name="video_time" value="">
                                    </div>
                                    <div class="tag_state">
                                        标签状态：<input type="radio" name="tag_state" value="0" ><label for="free">免费</label>
                                                <input type="radio" name="tag_state" value="2" ><label for="comming">更新中</label>
                                                <input type="radio" name="tag_state" value="1" ><label for="charge">收费</label>
                                    </div>
                                    <div class="release_state">
                                        发布状态：<input type="radio" name="release_state" value="1" ><label for="finish">已发布</label>
                                                <input type="radio" name="release_state" value="2" ><label for="draft">草稿</label>
                                    </div>
                                    <div class="release_date">
                                        发布时间：<input type="datetime-local" name="release_date" value="">
                                    </div>
                                    <div class="download_file">
                                        资料下载：<ul class="file_container">
                                                </ul>
                                                <div>
                                                        <a href="javascript:;" class="file add_button">+添加
                                                            <input type="file" name="video_file" id="" style="display:inline-block">
                                                        </a>
                                                </div>
                                    </div>
                                    <div class="img_min">
                                        缩略图：<div class="real_img_min_container img_min_container">
                                                    <input type="file" style="display:block;opacity:0;position:absolute;top:0;left:0;z-index:10" class="img_min_container"> 
                                                    <img src="" style="display:inline-block;position:absolute;top:0;left:0;z-index:1" class="img_min_container">
                                                </div>
                                    </div>
                                    <div class="teacher_introduction_container">
                                        讲者简介(仅科研项目使用)：
                                        <br>
                                        <div class="teacher_introduction_html_container"></div>
                                    </div>
                                    <div class="save_cancel_container">
                                        <div  class="save_button">保存</div>
                                        <div  class="cancel_button">取消</div>
                                    </div>
                                </div>
                                `
                                targetAddContainer.html(html)
                                let files=[]
                                let uploadFiles=[]
                                //给本节要点与摘要绑定富文本
                                targetAddContainer.find(".point_html_container").click(editor_handler)
                                targetAddContainer.find(".summary_html_container").click(editor_handler)
                                targetAddContainer.find(".teacher_introduction_html_container").click(editor_handler)
                                let compileFileList=function(){
                                    let html=``
                                    for(let file of files){
                                        html+=`
                                            <li class="one_file">${file.name}<button type="button" class="delete_button" >删除</button></li>
                                        `
                                    }
                                    let fileListContainer=targetAddContainer.find('.file_container')
                                    fileListContainer.html(html)
                                    //绑定删除事件
                                    targetAddContainer.find('button.delete_button').click(function(e){
                                        let deleteButton=$(e.target)
                                        let fileIndex=fileListContainer.children().index(deleteButton.parent())
                                        files.splice(fileIndex,1)
                                        compileFileList()
                                    })
                                }
                                compileFileList()
                                targetAddContainer.find("input[name='video_file']").on('change',function(e){
                                    if(e.target.files[0]!=undefined){
                                        files.push(e.target.files[0])
                                        compileFileList()
                                    }else{
                                        //关闭上传框
                                        return
                                    }
                                })
                                //缩略图
                                let imgFile=null
                                targetAddContainer.find("input.img_min_container").on('change',function(e){
                                    imgFile=e.target.files[0]
                                    var imgURL=getObjectURL(imgFile)
                                    targetAddContainer.find("img.img_min_container").attr("src",imgURL)
                                })
                                //点击保存
                                targetAddContainer.find(".save_button").click(function(){
                                    //保存返回的file文件名
                                    let fileId=[]
                                    //保存返回的img哈希
                                    let imgId=null
                                    let imgUpload=imgFile===null?Promise.resolve():new Promise(function(resolve,reject){
                                        //上传图片
                                        let imgForm=new FormData()
                                        imgForm.append('imgFile',imgFile)
                                        $.ajax({
                                            url:"/extends/image_storage/article_images/",
                                            type:"POST",
                                            data:imgForm,
                                            processData : false, 
                                            contentType : false,
                                            success:function(data){
                                                if(data.code===200){
                                                    imgId=data.data
                                                    resolve()
                                                }else{
                                                    alert("图片上传错误")
                                                    reject()
                                                }
                                            },
                                            error:function(e){
                                                alert("图片上传接口错误")
                                                console.log(e)
                                                reject()
                                            }
                                        })
                                    })      
                                    //上传文件(多个文件分次上传)
                                    for(let a of files){
                                        if(a.state===undefined)
                                        uploadFiles.push(a)
                                    }
                                    let fileUploadPromise=new Promise(function(solve,wrong){
                                        let fileUpload=null
                                        function uploadFile(file){
                                                if(file==undefined){
                                                    solve()
                                                    return 
                                                }
                                                let fileForm=new FormData()
                                                fileForm.append("file_info",file)
                                                fileUpload=new Promise(function(resolve,reject){
                                                    $.ajax({
                                                        url:"/extends/upload_file/video/",
                                                        type:"POST",
                                                        data:fileForm,
                                                        processData : false, 
                                                        contentType : false,
                                                        success:function(data){
                                                            if(data.code===200){
                                                                fileId.push(data.data)
                                                                resolve(uploadFiles.pop())
                                                            }else{
                                                                alert("文件上传错误")
                                                                console.log(data.message)
                                                                reject()
                                                            }
                                                        },
                                                        error:function(e){
                                                            alert("文件上传接口错误")
                                                            console.log(e)
                                                            reject()
                                                        }
                                                    })
                                                }).then((file)=>{
                                                    uploadFile(file)
                                                },()=>{wrong("上传错误")})
                                        }
                                        //多文件异步上传(继发)
                                        uploadFile(uploadFiles.pop())
                                    })
                                    fileUploadPromise.then(function(){
                                        imgUpload.then(function(){
                                            console.log(fileId)
                                            let changeVideoMessage=new FormData()
                                            //课时名称
                                            changeVideoMessage.append("title",targetAddContainer.find("input[name='study_name']").val())
                                            //本接要点(富文本)
                                            changeVideoMessage.append("course_main",targetAddContainer.find("div.point_html_container").html())
                                            //摘要(富文本)
                                            changeVideoMessage.append("summary",targetAddContainer.find("div.summary_html_container").html())
                                            //保利id
                                            changeVideoMessage.append("polyv_id",targetAddContainer.find("input[name='video_id']").val().trim())
                                            //课程id
                                            changeVideoMessage.append("course_id",$("#chapter_selector").val())
                                            //视频收费状态
                                            changeVideoMessage.append("is_pay",targetAddContainer.find("input[name='tag_state']:checked").val())
                                            //视频发布状态
                                            changeVideoMessage.append("status",targetAddContainer.find("input[name='release_state']:checked").val())
                                            //视频时长
                                            changeVideoMessage.append("video_time",targetAddContainer.find("input[name='video_time']").val())
                                            //视频创建时间
                                            //console.log(new Date(targetAddContainer.find("input[name='release_date']").val()).Format("yyyy-MM-dd hh:mm:ss"))
                                            changeVideoMessage.append("create_time",new Date(targetAddContainer.find("input[name='release_date']").val()).Format("yyyy-MM-dd hh:mm:ss"))
                                            //视频附件
                                            for(let a in fileId){
                                                changeVideoMessage.append("video_related_data",fileId[a])
                                            }
                                            //视频缩略图
                                            changeVideoMessage.append("thumbnail",imgId)
                                            //科研项目用讲者简介
                                            changeVideoMessage.append("teacher_introduction",targetAddContainer.find("div.teacher_introduction_html_container").html())
                                            $.ajax({
                                                url:"/supervisor/add_video/",
                                                type:"POST",
                                                data:changeVideoMessage,
                                                contentType:false,
                                                processData:false,
                                                success:function(data){
                                                    console.log(data)
                                                    if(data.code==200){
                                                        changeChaptor(changeTarget)
                                                    }else{
                                                        alert("添加失败")
                                                    }
                                                },
                                                error:function(e){
                                                    alert("课时添加接口错误")
                                                }
                                            })
                                        })
                                    },function(message){console.log(message)})  
                                })
                                //点击取消
                                targetAddContainer.find(".cancel_button").click(function(){
                                    changeChaptor(changeTarget)
                                })
                            
                    })

                },
                error:function(e){
                    alert("获取课程章节下课时"+e)
                }
            })
        }    
        $("#chapter_selector").change(changeChaptor)
    })



$('.compents_paginator1').on('click', 'li', function (e) {
    if ($(this).hasClass('page')) {
        page.to(Number($(this).attr('jp-data')))
        get_methods()
    }
    if ($(this).hasClass('prev')) {
        page.less()
        get_methods()
    }
    if ($(this).hasClass('next')) {
        page.add()
        get_methods()
    }
    if ($(this).hasClass('first')) {
        page.to(1);
        get_methods()
    }
    if ($(this).hasClass('last')) {
        page.toLast()
        get_methods()
    }


})
$('.compents_paginator1').on('keyup','input',function (e) {
    if(e.keyCode===13){
        page.to($(this).val())
        get_methods();
        $(this).val('').blur();
    } else {
        if($(this).val()>page.getPageNum()){
            $(this).val(page.getPageNum());
        }
        $(this).val($(this).val().replace(/[^0-9]/g,''))
    }
})

function compilePage(data){
    console.log(777,data)
    //封装
    var str_li = '';
    if (page.getPage() !== 1) {
        str_li += '<li class="first disabled" jp-role="first" jp-data="1"><a href="javascript:;">首页</a></li>';
        str_li += '<li class="prev disabled" jp-role="prev" jp-data="0"><a href="javascript:;">上一页</a></li>';
    }
    //pagecount
    page.setPageNum(data.data.page_count)
    var start,last;
    if (page.getPageNum() > 1) {
        if(page.getPageNum()- Number(page.getPage()) >2 && Number(page.getPage()) >2){
            start=Number(page.getPage())-3;
            last=Number(page.getPage())+2
        }
        else if(page.getPageNum()-Number(page.getPage())<=2&&page.getPageNum()>=5){
            start=page.getPageNum()-5;
            last=page.getPageNum();
        }
        else if(Number(page.getPage())<=2 && page.getPageNum()>=5){
            start=0;
            last=5
        }
        else if(page.getPageNum()<=5){
            start=0;
            last=page.getPageNum();
        }
        for (var p = start; p < last; p++) {
            if (Number(page.getPage()) === (p + 1)) {
                str_li += '<li class="page active" jp-role="page" jp-data="' + (p + 1) + '"><a href="javascript:;">' + (p + 1) + '</a></li>';
            } else {
                str_li += '<li class="page" jp-role="page" jp-data="' + (p + 1) + '"><a href="javascript:;">' + (p + 1) + '</a></li>';
            }
        }
    }
    if (page.getPageNum() !== 1 && page.getPage() !== page.getPageNum()) {
        str_li += ' <li class="next" jp-role="next" jp-data="2"><a href="javascript:;">下一页</a></li>';
        str_li += '<li class="last" jp-role="last" jp-data="5"><a href="javascript:;">尾页</a></li>'
    }
    $('.compents_paginator1 .paginator:visible').html(str_li);
    $('.page_number1:visible').html(page.getPageNum());
    // page_num = data.data.page_count;
    // if (page.getPageNum() === 1) {
    //     $('.paging_container').hide()
    // } else {
    //     $('.paging_container').show()
    // }
    $('.content:visible')[0].scrollTop = 0
}


//绑定订单校验功能
let bindBillAction=function () {
    $(".bill_action").unbind("click").click(function () {
        let bill_id = $(this).data().id
        $.ajax({
            type:"get",
            url:"/supervisor/supervisor_alipay_order_status/"+bill_id+"/",
            success:function (data) {
                alert(data.message)
            }
        })
    })
}
//分页内容动态渲染
function get_methods() {
    let pageType=page.getType()
    if(pageType=="comment"){
        AJAX({
            type: page.state=="search"?'post':'get',
            url: page.state=="search"?'/supervisor/search_video_comment/'+ page.getPage()+'/':'/supervisor/video_comments/' + page.getPage()+'/',
            data: page.state=="search"?page.val:null,
            fn: function (data) {
                if (data.code!==200) {
                    console.log(data.message)
                    return
                }
                // 动态生成部分
                let html=``;
                console.log(data)
                for(let a in data.data.comments){
                    html+=`
                    <div class="one_real_comment">
                        <textarea cols="30" rows="10" class="comment_message" disabled>${data.data.comments[a].comment}</textarea> 
                        <div class="one_real_uname">${data.data.comments[a].username}</div>
                        <div class="one_real_comment_time">
                            <span>${new Date(data.data.comments[a].create_time).toLocaleDateString()}</span>
                            <span style="margin-left:30px">${new Date(data.data.comments[a].create_time).toLocaleTimeString()}</span>
                        </div>
                        <div class="one_real_action">
                            <span class="delete_comment" data-id="${data.data.comments[a].id}">删除</span>
                        </div>
                    </div>
                    <div class="divide_comment"></div>
                    `
                }
                let comment_container=$(".real_comment_container")
                comment_container.html(html)
                //删除事件
                comment_container.find(".delete_comment").click(function(){
                    if(confirm("确认删除该评论")){
                        let delete_id=$(this).data().id
                        $.ajax({
                            url:"/supervisor/delete_video_comment/"+delete_id+"/",
                            type:"GET",
                            success:function(data){
                                if(data.code==200){
                                    get_methods()
                                }else{
                                    alert("删除失败")
                                }
                            },
                            error:function(e){
                                console.log(e)
                                alert("删除接口错误")
                            }
                        })
                    }else{
                        return
                    }
                })
                compilePage(data)
            }
        })
    }else if(pageType=="bill_all"){
        AJAX({
            type:'get',
            url:'/supervisor/order_list/'+page.getPage()+'/',
            fn:function(data){
                console.log(3333,data)
                let order_list=data.data.order_list
                if (data.code!==200) {
                    console.log(data.message)
                    return
                }
                //动态生成订单列表
                let html=``;
                let price=0
                for(let a in data.data.order_list){
                    if(data.data.order_list[a].status === 2){
                        price += parseFloat(data.data.order_list[a].price)
                    }
                    html+=`
                        <div class="one_bill ${a&1===1?'bill_diff_bg':''}">
                        <span class="bill_number">${data.data.order_list[a].order_id}</span>
                        <span>${data.data.order_list[a].course}</span>
                        <span>${data.data.order_list[a].username}</span>
                        <span>${data.data.order_list[a].price}</span>
                        <span>${data.data.order_list[a].type==1?'支付宝':'微信'}</span>
                        <span class="bill_number">${data.data.order_list[a].relevance_order}</span>
                        <span>${(()=>{
                            if(data.data.order_list[a].status===0){
                                return '已失效'
                            }else if(data.data.order_list[a].status===1){
                                return '未支付'
                            }else{
                                return '已支付'
                            }
                        })()}</span>
                        <span class="bill_action"  data-id="${data.data.order_list[a].order_id}"><a>校验</a></span>
                        </div>
                    `
                }
                let billContainer=ordersAllContainer.find(".orders_detail_body")
                // let priceContainer=ordersAllContainer.find(".price_sum")
                billContainer.html(html)
                // priceContainer.html(`本页订单金额总计：${price}元`)
                $(".price_sum_all:visible").html(`订单金额总计：${parseFloat(data.data.amount)}元`)
                compilePage(data)
                bindBillAction()
            }
        })
    }else if(pageType=="bill_search"){
        AJAX({
            type:'post',
            url:'/supervisor/search_order/'+page.getPage()+'/',
            data:page.val,
            fn:function(data){
                let html=``;
                let price=0
                if(data.code!==200){
                    alert(data.message)
                }else{
                    if(data.data.order_list.length==0){
                        alert('未找到复合条件的订单')
                        return
                    }else{
                        for(let a in data.data.order_list){
                            if (data.data.order_list[a].status === 2) {
                                price += parseFloat(data.data.order_list[a].price)
                            }
                            html+=`
                                <div class="one_bill ${a&1===1?'bill_diff_bg':''}">
                                <span class="bill_number">${data.data.order_list[a].order_id}</span>
                                <span>${data.data.order_list[a].course}</span>
                                <span>${data.data.order_list[a].username}</span>
                                <span>${data.data.order_list[a].price}</span>
                                <span>${data.data.order_list[a].type==1?'支付宝':'微信'}</span>
                                <span class="bill_number">${data.data.order_list[a].relevance_order}</span>
                                <span>${(()=>{
                                    if(data.data.order_list[a].status===0){
                                        return '已失效'
                                    }else if(data.data.order_list[a].status===1){
                                        return '未支付'
                                    }else{
                                        return '已支付'
                                    }
                                })()}</span>
                                <span class="bill_action" data-id="${data.data.order_list[a].order_id}"><a>校验</a></span>
                                </div>
                            `
                        }
                        let billContainer=ordersSearchContainer.find(".orders_detail_body")
                        // let priceContainer=ordersSearchContainer.find(".price_sum")
                        billContainer.html(html)
                        // priceContainer.html(`本页订单金额总计：${price}元`)
                        $(".price_sum_all:visible").html(`订单金额总计：${parseFloat(data.data.amount)}元`)
                        compilePage(data)
                        bindBillAction()
                    }
                }
            }
        })
    }else if(pageType=="feedback"){
        //反馈搜索功能暂无
        AJAX({
            type: page.state=="search"?'post':'get',
            url: page.state=="search"?'暂无此接口'+ page.getPage()+'/':'/supervisor/user_feed_back/' + page.getPage()+'/',
            data: page.state=="search"?page.val:null,
            fn:function(data){
                console.log(data)
                if(data.code==200){
                    let html=``;
                    for(let a in data.data.user_feed_back_list){
                        html+=`
                            <div class="one_real_comment">
                                <textarea cols="30" rows="10" class="comment_message" disabled>
                                ${data.data.user_feed_back_list[a].content}
                                </textarea> 
                                <div class="one_real_uname">
                                ${data.data.user_feed_back_list[a].username__username}
                                </div>
                                <div class="one_real_connection">
                                ${data.data.user_feed_back_list[a].iphone}
                                </div>
                                <div class="one_real_comment_time">
                                    <span>${new Date(data.data.user_feed_back_list[a].create_time).toLocaleDateString()}</span>
                                    <span style="margin-left:30px">${new Date(data.data.user_feed_back_list[a].create_time).toLocaleTimeString()}</span>
                                </div>
                                <div class="one_real_action">
                                    <span class="check_feedback" data-id="${data.data.user_feed_back_list[a].id}" data-img="${data.data.user_feed_back_list[a].image}">详情</span>
                                </div>
                            </div>
                            <div class="divide_comment"></div>
                        `
                    }
                    $(".real_feedback_container").html(html)
                    compilePage(data)
                    //点击详情
                    $(".check_feedback").click(function(){
                        $('.feedback_background').removeClass("hide")
                        let t = $('.check_feedback')
                        $.ajax({
                            type:'get',
                            url:'/supervisor/user_feed_back_detail/'+t.data().id+'/',
                            success:function(data){
                                //TODO:字段匹配
                                let html=``
                                html+=`
                                <div style="height:96px;line-height:96px">
                                    <div class="feedback_cancel">
                                        <span class="feedback_cancel_button">关闭</span>
                                    </div>
                                    <span class="feedback_content">
                                        用户：
                                    </span>
                                    <span  class="feedback_content" style="color:#000">
                                        ${data.data.username}
                                    </span>
                                </div>
                                <div style="margin-bottom:20px;">
                                    <span class="feedback_content">联系方式：</span><br>
                                    <span  class="feedback_content" style="color:#000">
                                        ${data.data.iphone}
                                    </span> 
                                </div>
                                <div style="margin-bottom:20px;">
                                    <span class="feedback_content">反馈内容：</span><br>
                                    <span  class="feedback_content" style="color:#000">
                                        ${data.data.content}
                                    </span>
                                </div>
                                <div class="feed_back_img">
                                    <img src="/images/article_images/${t.data().img}">
                                </div>
                                `
                                $(".feedback_detail_container").html(html)
                                //关闭详情页面
                                $(".feedback_cancel_button").click(function(){
                                    $(".feedback_background").addClass("hide")
                                })
                            }
                        })
                    })
                }
            }
        })
    }else{
        return
    }
}
//评论搜索
function search_list() {
     val = {'comment': $('.title_search input').val()}
    if(val.comment!==""){
        page.getType()
        page.openSearch()
        page.setVal(val)
        get_methods()
    }else{
        page.closeSearch()
        get_methods()
    }
}
//搜索触发
$('.search_trigger').click(search_list)
$('.title_search input').keyup(function (e) {
    if (e.keyCode === 13) {
        search_list()
    }
})
//富文本设定
$(document).on("change", "#yika_img_upload", function () {
    var oMyForm;
    var _self = this;
    if (!this['value'].match(/.jpg|.gif|.png|.bmp|.JPEG|svg|/i)) {
        return
    }
    var oMyForm = new FormData();
    oMyForm.append("imgFile", $('#yika_img_upload')[0].files[0]);
    $.ajax({
        type: 'post',
        url: '/extends/image_storage/article_images/',
        data: oMyForm,
        dataType: 'json',
        contentType: false,
        processData: false,
        success: function (e) {
            if(e.code!==200){
                alert(e.message);
                return
            }
            CKEDITOR.instances.ask_area.insertHtml("<img src='/images/article_images/" + e.data + "'>")
        }
    })
})
window.onresize=function(){
    $("#content").css({left:"250px"})
}
//更新订单搜索页面信息
function updateCourselist(){
    $.ajax({
        type:'get',
        url:'/supervisor/course_list/',
        success:function(data){
            if(data.code==200){
                let html=``
                for(let a in data.data.course_list){
                    html+=`<option value="${data.data.course_list[a].course_id}">${data.data.course_list[a].course}</option>`
                }
                course_select.html(html)
            }
        }
    })
}
updateCourselist()
//交易管理
let ordersAll = $(".orders_all")
let ordersSearch = $(".orders_search")
let ordersAllContainer=$(".orders_all_container")
let ordersSearchContainer=$(".orders_search_container")
ordersAll.click(function(){
    if(ordersAll.hasClass("orders_active")){
        return;
    }else{
        ordersAll.addClass("orders_active")
        ordersSearch.removeClass("orders_active")
        ordersAllContainer.removeClass("hide")
        ordersSearchContainer.addClass("hide")
        page.getType()
    }
})
ordersSearch.click(function(){
    if(ordersSearch.hasClass("orders_active")){
        return;
    }else{
        ordersSearch.addClass("orders_active")
        ordersAll.removeClass("orders_active")
        ordersSearchContainer.removeClass("hide")
        ordersAllContainer.addClass("hide")
        page.getType()
    }
})

//全部订单更新按钮
$(".orders_flash_button").click(function(){
    page.getType()
    page.to(1)
    get_methods()
})
//订单搜索
let time_start=$(".time_start")
let time_end=$(".time_end")
let order_state=$(".orders_state")
let course_select=$(".name_search_condition")
function search_order(){
    let val={
        start_time:time_start.val(),
        end_time:time_end.val(),
        course:course_select.val(),
        status:order_state.val(),
    }
    page.setVal(val)
    page.to(1)
    get_methods()
}
//查询按钮
$(".orders_search_button").click(search_order)
//订单查询更新按钮
$(".search_flash_button").click(function(){
    page.to(1)
    get_methods()
})
let width=null
let close_width=null
$(".nav_cursor").click(function () {
    $('.nav').toggleClass("close_nav")
    $(this).toggleClass("close_nav_button")
    var left=0
    if($('.nav').hasClass("close_nav")){
         left = parseFloat($("#content").css("left")) - 224
        width=$("#content").css("width")
        $("#content").css("width", "98%")
    }else {
        close_width = $("#content").css("width")
        left = parseFloat($("#content").css("left")) + 224
        $("#content").css("width", width)
    }

    $("#content").css("left",left+"px")
})