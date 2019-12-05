jQuery.download = function(url, data, method){
	//url and data options required
	if( url && data ){ 
		//data can be string of parameters or array/object
		data = typeof data == 'string' ? data : jQuery.param(data);
		//split params into form inputs
		var inputs = '';
		jQuery.each(data.split('&'), function(){ 
			var pair = this.split('=');
			inputs+='<input type="hidden" name="'+ pair[0] +'" value="'+ pair[1] +'" />'; 
		});
		//send request
		jQuery('<form action="'+ url +'" method="'+ (method||'post') +'">'+inputs+'</form>')
		.appendTo('body').submit().remove();
	};
};

//定制化模态框
// //关闭模态框
// $(".user_download_close").click(function(e){
//     e.stopPropagation()
//     $(".user_download_alert_container").hide()
// })
// //前往个人中心
// $(".go_to_personal_center").click(function(e){
//     e.stopPropagation()
//     window.location.href="/user/?t=user"
// })

//下载按钮
$(".user_download").click(function(e){
    e.stopPropagation()
    //阻止其他元素触发请求
    let target=$(e.target)
    if(!target.hasClass("down_load_button_flag")){
        return 
    }
    let t=$(this);
    if(document.cookie==''){location.href='http://'+location.host+'/login/?next='+location.pathname+'#1';return }
    let url=t.data().href
    $.ajax({
        type:"GET",
        url:'/user_message_complete/',
        success:function(data){
            if(data.code==200){
                jQuery.download(url,{},"GET")
            }else if(data.code == 401){
                //定制化模态框
                $().user_info_alert_box() 
            }else if(data.code == 302){
                location.href='http://'+location.host+'/login/?next='+location.pathname+'#1'
            }else{
                return 
            }
        }
    })
})