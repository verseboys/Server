<template>
    <div class = "friend_modal_container">
        <div class="friend_mobile_container">
            <div style="height:58px;overflow:hidden;position:relative" >
                 <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_mobile">
            </div>
            <a-row style="margin-top:0px;font-size:18px;">
                <a-col>
                    亲爱的伙伴，医咖会欢迎你，请留下联系方式，小咖与你细细沟通！
                </a-col>
            </a-row>
            <a-row style="margin-top:30px;">
                <a-col :span="12" offset="6">
                     <a-input @change="change" type="number" v-model="phone" style="width:200px;margin-right:20px" :placeholder="placeholder" />
                     <a-button @click="submit_phone" type="primary">提交</a-button>
                </a-col>
                <div style="width:400px;height:32px;margin-top:36px;padding-left:256px;text-align:left;font-size:10px;color:red;line-height:20px">
                    {{error_message}}
                </div>
            </a-row>
        </div>
    </div>
</template>

<script>

export default {
  name: 'friendMobile',
  data () {
    return {
        phone:'',
        placeholder:'请输入手机号',
        error_message:""
    }
  },
  methods:{
      change(){
          this.placeholder = "请输入手机号"
          this.error_message = ""
      },
      submit_phone(){
        let mobile = /^(13[0-9]{9})|(18[0-9]{9})|(14[0-9]{9})|(17[0-9]{9})|(15[0-9]{9})$/;
        let tel = /^\d{3,4}-?\d{7,9}$/;
        if(this.phone.trim()==""){
            this.placeholder = "手机号不能为空"
            return
        }
        if (!tel.test(this.phone)||!mobile.test(this.phone)){
            this.error_message = "手机号格式不正确"
            return
        }
        this.$emit("get_mobile",this.phone)
      },
      cancel_mobile(){
        this.$emit('cancel_mobile')
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
input::-webkit-outer-spin-button,input::-webkit-inner-spin-button{
   -webkit-appearance: none !important;
}
input[type="number"]{-moz-appearance:textfield;}
.friend_modal_container{
    width:100%;
    height:100%;
    position:fixed;
    top:0;
    left:0;
    background: rgba(0,0,0,0.4);
    z-index:4;
}
.friend_mobile_container{
    width: 800px;
    height: 190px;
    background-image: linear-gradient(to top, #d6bf75, #dac691 78%, #dfcdaf);
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-400px;
    margin-top:-95px;
    z-index:5;
    border-radius: 5px;
}
</style>
