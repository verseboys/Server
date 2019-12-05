var user_order_page=1,user_order_type=0,page_num

var empty_order=`
                <div class="empty_order">
                    暂无订单信息~
                </div>
            `
function compile_user_orders(state){
    $.ajax({
        type:"get",
        url:"/my_orders/"+state+"/",
        success:function(data){
                var str = '';
                str += ` <div class="user-menu-list" data-link="order">
                            <div class="user-collect-top list_title_container">
                                <div class="user-collect-title list_title">
                                    我的订单
                                </div>
                                <div class="user-collect-tag">
                                <span>分类</span>
                                <ul class="row user_tag_change_collect">
                                    <li class="${state==3?'checked':''}" data-ajax-url="3">全部</li>
                                    <li class="${state==1?'checked':''}" data-ajax-url="1">待支付</li>
                                    <li class="${state==2?'checked':''}" data-ajax-url="2">已完成</li>
                                    <li class="${state==0?'checked':''}" data-ajax-url="0">已失效</li>
                                </ul>
                                </div>
                            </div>
                            <div class="user_order_list">


            ${!data.data.order_list?empty_order:(()=>{
                let html=``
                for(let a in data.data.order_list){
                    html+=`
                    <div class="user-collect-list" style="border: 1px solid rgb(234, 234, 241);margin-bottom:19px;">
                    <div style="padding:0">
                        <div class="order_title">
                            <img src="/static/images/order.svg" style="vertical-align: middle;">
                            <span class="order_id">
                                订单编号：${data.data.order_list[a].order_id}
                            </span>
                            <span class="order_time">
                            ${new Date(data.data.order_list[a].create_time).toLocaleString("CN",{hour12:false})}
                            </span>
                            <!--<img src="/static/images/delete_order.png" class="delete_order" style="display:inline-block">-->
                        </div>
                        <div class="order_content">
                            <div class="order_content_inner">
                                <img src="/images/article_images/${data.data.order_list[a].thumbnail}" class="order_img">
                                <div class="order_content_detail">
                                    <div class="order_name">
                                    ${data.data.order_list[a].course}
                                    </div>
                                    <div class="order_price">
                                    ￥&nbsp;${data.data.order_list[a].price}
                                    </div>
                                </div>
                                <div class="order_state">
                                    ${(()=>{
                                        if(data.data.order_list[a].status==0){
                                            return  '<div class="state_others">已失效</div>'
                                        }else if(data.data.order_list[a].status==2){
                                            return  '<div class="state_others">已支付</div>'
                                        }else{
                                            return   '<div class="state_waiting"><div class="waiting">待支付</div><div class="pay_right_now" data-id='+data.data.order_list[a].order_id+'> 马上支付</div></div>'
                                        }
                                    })()}
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                    `
                }
                return html
            })()}

                            </div>
                        </div>
                        `
            let user_menu= $('.user-menu')
            user_menu.find(".user-menu-list").addClass("hide")
            user_menu.append(str)
            bindChangeState()
            bindPayAction()
        }
    })

}
function bindChangeState(){
    $(".user_tag_change_collect li:visible").unbind("click").click(function(){
        let state=$(this).data().ajaxUrl
        if(state==$(".user_tag_change_collect li.checked").data().ajaxUrl){
            return
        }else{
            compile_user_orders(state)
        }
    })
}
function bindPayAction(){
    $(".pay_right_now").unbind("click").click(function(){
        sessionStorage.setItem("order_id",$(this).data().id)
        sessionStorage.setItem("type","get")
        //TODO:修改url
        location.href='/front_create_orders/'
    })
}
compile_user_orders(3)
bindChangeState()
bindPayAction()


$('.user-menu .user-menu-list[data-link="order"]').siblings().addClass('hide')
//暂无分页
// $(document.body).on('click', '.user_tag_change_collect li', function () {
//     $(this).addClass('checked').siblings().removeClass('checked');
//     user_order_type = $(this).data().ajaxUrl
//     user_order_page=1
//     ajax_order_data(user_order_type,user_order_page)
// });
// var ajax_order_data=function(user_order_type,user_order_page){

// }
