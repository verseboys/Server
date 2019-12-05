<template>
    <div  class = "common_container" id="event_list">
        <div class="common_center_container">
            <a-row class="common_mid_title_container" align="middle" type="flex" justify="center">
                <a-col :span="9" class="height-50 common_annex_container"><div class="common_annex1"></div><div class="common_annex2"></div></a-col>
                <a-col :span="6" class="height-50 "><div class="common_title">见证过去</div></a-col>
                <a-col :span="9" class="height-50 "><div class="common_annex3"></div><div class="common_annex4"></div></a-col>
            </a-row>
                <a-row class="common_sub_title_container" align="middle" type="flex" justify="center">
                <a-col :span="24">
                    <div class="common_sub_title">医咖会公众号开办<span class="special_num_1"> 2 </span>年,共发布<span class="special_num_1"> 600+ </span>篇文章<br>曾经我们一起见证</div>
                </a-col>
            </a-row>

            <a-row  id="event_1"  class="one_item">
                <a-row>
                    <a-col :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            2016年8月27日
                        </div>
                        <div class="date_angle"></div>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="space-around" align="middle">
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a-row >
                                <a-col :span="24" :class="{animated:event_1, fadeInLeft:event_1,hide:!event_1}" >
                                    <img src="/anniversary_static/img/event_list_1.png" class="event_list_1 box_shadow_1">
                                </a-col>
                            </a-row>
                        </div>
                    </a-col>
                    <a-col :span="2" class="event_list_1_center_container">
                        <div class="event_list_1_center_item">
                             
                        </div>
                    </a-col>
                    <a-col :span="11"  align="middle" >
                        <a href="https://mp.weixin.qq.com/s/FzuTJ7pS7bM2EGw4Rouxww" target="blank">
                            <div class="event_list_1_fix_container" :class="{animated:event_1, fadeInRight:event_1,hide:!event_1}" >
                                <a-row>
                                    <a-col :span="24" >
                                        <img src="/anniversary_static/img/event_list_1_img.png" class="event_list_1_img">
                                    </a-col>
                                </a-row>
                                <a-row>
                                    <a-col :span="24" class="event_list_1_content">
                                        中国经典：预防糖尿病，20年随访结果
                                    </a-col>
                                </a-row>
                            </div>
                        </a>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col class="divide_item_container">
                        <div class="divide_item_center">

                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row id="event_2"  class="one_item">
                <a-row>
                    <a-col  :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            2017年1月5日
                        </div>
                        <div class="date_angle"></div>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="space-around" align="middle">
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a href="https://mp.weixin.qq.com/s/-GxIvwhAuUw0AfKriBiP7Q" target="blank">
                                <div class="event_list_1_fix_container" :class="{animated:event_2, fadeInLeft:event_2,hide:!event_2}"> 
                                    <a-row>
                                        <a-col :span="24" >
                                            <img src="/anniversary_static/img/event_list_2_img.png" class="event_list_1_img">
                                        </a-col>
                                    </a-row>
                                    <a-row>
                                        <a-col :span="24" class="event_list_1_content">
                                            《Circulation：中国卒中患病率、发病率和死亡率》
                                        </a-col>
                                    </a-row>
                                </div>
                            </a>
                        </div>
                    </a-col>
                    <a-col :span="2" class="event_list_1_center_container">
                        <div class="event_list_1_center_item">
                             
                        </div>
                    </a-col>
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a-row >
                                <a-col :span="24"  :class="{animated:event_2, fadeInRight:event_2,hide:!event_2} " >
                                    <img src="/anniversary_static/img/event_list_2.png" class="event_list_1 box_shadow_2">
                                </a-col>
                            </a-row>
                        </div>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col class="divide_item_container">
                        <div class="divide_item_center">

                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row  id="event_3"  class="one_item">
                <a-row>
                    <a-col :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            2018年1月12日
                        </div>
                        <div class="date_angle"></div>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="space-around" align="middle">
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a-row >
                                <a-col :span="24" :class="{animated:event_3, fadeInLeft:event_3,hide:!event_3}">
                                    <img src="/anniversary_static/img/event_list_3.png" class="event_list_1 box_shadow_1">
                                </a-col>
                            </a-row>
                        </div>
                    </a-col>
                    <a-col :span="2" class="event_list_1_center_container">
                        <div class="event_list_1_center_item">
                             
                        </div>
                    </a-col>
                    <a-col :span="11"  align="middle" >
                        <a href="https://mp.weixin.qq.com/s/c1IEh0YPpy1B__TinBY9bQ" target="blank">
                            <div class="event_list_1_fix_container" :class="{animated:event_3, fadeInRight:event_3,hide:!event_3}">
                                <a-row>
                                    <a-col :span="24" >
                                        <img src="/anniversary_static/img/event_list_3_img.png" class="event_list_1_img">
                                    </a-col>
                                </a-row>
                                <a-row>
                                    <a-col :span="24" class="event_list_3_content">
                                        《50种SPSS教程、10种样本量计算教程...<br>全部为你整理在这里!》
                                    </a-col>
                                </a-row>
                            </div>
                        </a>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col class="divide_item_container">
                        <div class="divide_item_center">

                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row  id="event_4" class="one_item">
                <a-row>
                    <a-col :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            2018年4月13日
                        </div>
                        <div class="date_angle"></div>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="space-around" align="middle">
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a href="https://mp.weixin.qq.com/s/1gXAGUyIEqJJW-6Ps7zxqg" target="blank">
                                <div class="event_list_1_fix_container" :class="{animated:event_4, fadeInLeft:event_4,hide:!event_4}">
                                    <a-row>
                                        <a-col :span="24" >
                                            <img src="/anniversary_static/img/event_list_4_img.png" class="event_list_1_img">
                                        </a-col>
                                    </a-row>
                                    <a-row>
                                        <a-col :span="24" class="event_list_1_content">
                                            医咖会Stata系列视频教程正式开课！
                                        </a-col>
                                    </a-row>
                                </div>
                            </a>
                        </div>
                    </a-col>
                    <a-col :span="2" class="event_list_1_center_container">
                        <div class="event_list_1_center_item">
                             
                        </div>
                    </a-col>
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a-row >
                                <a-col :span="24" :class="{animated:event_4, fadeInRight:event_4,hide:!event_4}">
                                    <img src="/anniversary_static/img/event_list_4.png" class="event_list_1 box_shadow_2">
                                </a-col>
                            </a-row>
                        </div>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col class="divide_item_container">
                        <div class="divide_item_center">

                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row id="event_5"  class="one_item">
                <a-row>
                    <a-col  :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            2018年6月30日
                        </div>
                        <div class="date_angle"></div>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="space-around" align="middle">
                    <a-col :span="11"  align="middle" >
                        <div  >
                            <a-row >
                                <a-col :span="24" :class="{animated:event_5, fadeInLeft:event_5,hide:!event_5}">
                                    <img src="/anniversary_static/img/event_list_5.png" class="event_list_1 box_shadow_1">
                                </a-col>
                            </a-row>
                        </div>
                    </a-col>
                    <a-col :span="2" class="event_list_1_center_container">
                        <div class="event_list_1_center_item">
                             
                        </div>
                    </a-col>
                    <a-col :span="11"  align="middle" >
                        <a href="https://mp.weixin.qq.com/s/W-0JcEttrAk2TINcXRoI3w" target="blank">
                            <div class="event_list_1_fix_container"  :class="{animated:event_5, fadeInRight:event_5,hide:!event_5}">
                                <a-row>
                                    <a-col :span="24" >
                                        <img src="/anniversary_static/img/event_list_5_img.png" class="event_list_1_img">
                                    </a-col>
                                </a-row>
                                <a-row>
                                    <a-col :span="24" class="event_list_1_content">
                                        【合集】75篇SPSS统计操作教程，全在这里！
                                    </a-col>
                                </a-row>
                            </div>
                        </a>
                    </a-col>
                </a-row>
                <a-row>
                    <a-col class="divide_item_container" style="height:190px">
                        <div class="divide_item_center" style="height:190px">

                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row  id="event_6"  class="one_item">
                <a-row>
                    <a-col :span="8" :offset="8"  align="middle" type="flex" justify="center">
                        <div class="date_container">
                            未完待续...
                        </div>
                    </a-col>
                </a-row>
            </a-row>

            <a-row>
                <a-col :span="24">
                <div class="separate"></div>
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script>

export default {
  name: 'eventList',
  props:['event_1','event_2','event_3','event_4','event_5'],
  data () {
    return {
    }
  },
  created:function(){
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
/* .animated {
    animation-duration: 0.8s;
    animation-fill-mode: both;
} */
.hide{
    display: none;
}
.separate{
    height:157px;
}
.special_num_1{
    color:#02f2e8;
}
.common_title{
    color:#02f2e8;
    font-weight: 700;
}
.special_num_2{
    color:#f8e71c;
    font-size: 30px;
}
.date_container{
    background: #dfcdaf;
    width: 200px;
    text-align:center;
    height: 44px;
    font-size: 20px;
    line-height:44px;
    font-weight: 700;
}   
.one_item{
}
.date_angle{
    /* width: 0;
    height: 0;
    border-style: solid;
    border-width: 16px 16px 16px 16px;
    border-color: #dfcdaf transparent transparent transparent; */
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 16px 16px 0 16px;
    border-color: #dfcdaf transparent transparent transparent;
    position:relative;
    z-index:2;
}
.common_sub_title{
    color: #dfcdaf;
    font-size: 20px;
    margin-top:25px;
}
.event_list_1{
    width:440px;
    height:150px;
}
.box_shadow_1{
    box-shadow: -20px 13px 20px 1px #4353b8
}
.box_shadow_2{
    box-shadow: 20px 13px 20px 1px #4353b8
}

.event_list_1_img{
    width:378px;
    height:auto;
}
.event_list_1_fix_container{
    width:378px;
}
.event_list_1_content{
    background: #fff;
    color:black;
    height: 55px;
    line-height:55px;
    font-size: 16px;
}
.event_list_1_center_container{
    height:218px;
}
.event_list_1_center_item{
    height:223px;
    background:#fff;
    width:5px;
    margin:0 auto;
    position:relative;
    top:-5px;
    z-index:1;
}
.divide_item_container{
    height:60px;
}
.divide_item_center{
    width:5px;
    margin:0 auto;
    background:#fff;
    height:100%;
    position:relative;
    left:0px;
}
.event_list_3_content{
    background: #fff;
    color:black;
    height: 55px;
    line-height:27.5px;
    font-size: 16px;
}
#event_list{
    position: relative;
}
#event_1,#event_2,#event_3,#event_4,#event_5,#event_6{
    position: relative;
}
</style>
