<template>
    <div class = "modal_container">
        <div class="sci_container" v-if="!is_user_choose">
            <div style="height:160px;overflow:hidden;position:relative" >
                <!--  <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_sci"> -->
                <img style="width:100%;height:auto;" src="/anniversary_static/img/sci_banner.png" >
            </div>
            <a-row class="a_button_container">
                <a-col :span="24">
                    <a-button type="primary" class="a_button" @click="choose_sci(0)">
                        我已经发表SCI啦
                    </a-button>
                </a-col>
            </a-row>
            <a-row class="a_button_container">
                <a-col :span="24"> 
                    <a-button type="primary"  class="a_button"  @click="choose_sci(1)">
                        刚投了稿，正在等待回复
                    </a-button>
                </a-col>
            </a-row>
            <a-row class="a_button_container">
                <a-col :span="24">
                    <a-button type="primary" class="a_button"  @click="choose_sci(2)">
                        正在做课题，力争发高分
                    </a-button>
                </a-col>
            </a-row>
            <a-row class="a_button_container">
                <a-col :span="24">
                    <a-button type="primary" class="a_button"  @click="choose_sci(3)">
                        刚刚起步还需要努力
                    </a-button>
                </a-col>
            </a-row>
        </div>

        <div class="sci_container" v-if="is_user_choose&&show_state==0">
            <div style="height:165px;overflow:hidden;position:relative;background:#627bf9" >
                <!--  <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_sci"> -->
                <img style="width:100%;height:auto;" src="/anniversary_static/img/sci_banner.svg" >
            </div>
            <a-row style="margin-top:50px;">
                <a-col>
                    <a-input class="inner_block"  @change="change" v-model="magazine" :placeholder="placeholder"/>
                </a-col>
            </a-row>
            <a-row style="margin-top:40px;">
                <a-col>
                    <a-button class="inner_block" @click="confirm" type="primary">确认</a-button>
                </a-col>
            </a-row>
            <a-row style="margin-top:10px;">
                <a-col>
                    <a-button class="inner_block" @click="cancel">取消</a-button>
                </a-col>
            </a-row>
            <a-row style="margin-top:30px">
                <a-col style="color:#c1c1c1;font-size:10px">
                    小咖提示：如果有意乱填，小咖伤心之下会收回所有勋章哦！
                </a-col>
            </a-row>
        </div>

        <div class="sci_container" v-if="is_user_choose&&(show_state==1||show_state==2||show_state==3)">
            <div style="height:244px;overflow:hidden;position:relative" >
                 <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_sci">
                <img style="width:100%;height:auto;" src="/anniversary_static/img/sci_banner_2.png" >
            </div>
            <a-row v-show="show_state==1" style="height:196px">
                <a-col :span="24" style="font-size:30px;line-height:186px;margin-top:10px;">
                    Woo！鼓掌！你真的是太优秀了！
                </a-col>
            </a-row>
            <a-row v-show="show_state==2" style="height:196px">
                <a-col :span="24" style="font-size:30px;line-height:40px;margin-top:62px;">
                    跟我念句话，你是最棒的,<br>
                    重重重复这句话，你是最棒哒！
                </a-col>
            </a-row>
            <a-row v-show="show_state==3" style="height:196px">
                <a-col :span="24" style="font-size:30px;line-height:40px;margin-top:62px;">
                    跟我念句话，你是最棒的,<br>
                    重重重复这句话，你是最棒哒！
                </a-col>
            </a-row>
        </div>

    </div>
</template>

<script>
import hostConfig from '../../config/host.config.js'
import httpMethods from '../methods/http_methods.js'

export default {
  name: 'eSci',
  data () {
    return {
        is_user_choose:false,
        show_state:3,
        magazine:'',
        placeholder:'请输入杂志名称'
    }
  },
  methods:{
      cancel_sci(){
        this.$emit('cancel_sci')
      },
      choose_sci(state){
        switch(state){
            case 0:
            this.show_state = 0
            this.is_user_choose = true
            break
            case 1:
            this.show_state = 1
            this.is_user_choose = true
            break
            case 2:
            this.show_state = 2
            this.is_user_choose = true
            break
            case 3:
            this.show_state = 3
            this.is_user_choose = true
            break
        }
      },
      cancel(){
            this.is_user_choose = false
      },
      confirm(){
        if(this.magazine.trim()==""){
            this.placeholder = "杂志名称不能为空哦"
            return
        }
        this.$emit("start_get_sci",this.magazine) 
      },
      change(){
          this.placeholder = "请输入杂志名称"
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
.inner_block{
    width:200px;
    height:37px;
}
.a_button_container{
    margin-top:25px;
}
.a_button{
    width:186px;
    height:40px;
}
.error_box{
    height:35px;
    line-height:35px;
    margin-top:10px;
    text-align:left;
    color:red;
    font-size:12px;
}
.modal_container{
    width:100%;
    height:100%;
    position:fixed;
    top:0;
    left:0;
    background: rgba(0,0,0,0.4);
    z-index:6;
}
.sci_container{
    width: 700px;
    height: 460px;
    background-color: #f9faff;
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-350px;
    margin-top:-230px;
    z-index:5;
}
</style>
