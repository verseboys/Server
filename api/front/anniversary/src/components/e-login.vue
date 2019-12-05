<template>
    <div class = "modal_container">
        <div class="login_container">
            <div style="height:150px;overflow:hidden;position:relative" >
                 <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_login">
                <img style="width:100%;height:auto;" src="/anniversary_static/img/login_banner_2.png" >
            </div>
            <a-row style="margin-top:50px">
                <a-col :span="12" offset="6">
                    <a-input v-model="user_name" placeholder="输入用户名/Email" />
                </a-col>
            </a-row>
            <a-row style="margin-top:20px">
                <a-col :span="12" offset="6">
                    <a-input v-model="user_password"  type='password' placeholder="输入密码" />
                </a-col>
            </a-row>
            <a-row class="error_box">
                <a-col :span="12" v-html="error_message" offset="6"></a-col>
            </a-row>
            <a-row  align="middle">
                <a-col style="font-size:12px;text-align:left" :span="5" offset="6">
                    <a style="line-height:31px;" href="/login/?next=/#4">忘记密码?点击这里</a>
                </a-col>
                <a-col :span="8" offset="1" type="flex" align="middle">
                   <a href="/register/" style="color:black;margin-right:10px;" target="blank">注册</a>
                   <a-button @click="login" style="color:#fff;background:#3b72db">登录</a-button>
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import hostConfig from '../../config/host.config.js'
import httpMethods from '../methods/http_methods.js'

export default {
  name: 'getMedal',
  data () {
    return {
        error_message:'',
        user_name:'',
        user_password:''
    }
  },
  methods:{
      login(){
        this.error_message = ""
        if(this.user_name.trim()==""){
            this.error_message = "用户名或邮箱不能为空"
            return
        }
        httpMethods.post_form(hostConfig.host+"/front_login/",{
            username_or_email:this.user_name,
            password:this.user_password
        }).then((res)=>{
            if(res.data.code!==200){
                if(res.data.message == '出错了'){
                    this.error_message = '<div style="line-height:17px">登录不成功？赶快联系小咖帮你解决!<br>(小咖微信：xys2018ykf)</div>'
                }else{
                    this.error_message = res.data.message
                }
            }else{
                axios.get(hostConfig.host+'/already_join_anniversary/').then((res)=>{
                    if(res.data.message=="未参与"){
                        this.$emit('login_success',false,res.data.data.avatar)
                    }else if(res.data.message=="已参与"){
                        this.$emit('login_success',true,res.data.data.avatar)
                    }
                },(error)=>{
                    this.error_message = '服务器在发呆,刷新一下试试'
                    console.log(error)
                })

            }
        },(error)=>{
            console.log(error)
        })
      },
      cancel_login(){
        this.$emit('login_cancel')
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
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
.login_container{
    width: 600px;
    height: 400px;
    background-color: #f9faff;
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-300px;
    margin-top:-190px;
    z-index:5;
}
</style>
