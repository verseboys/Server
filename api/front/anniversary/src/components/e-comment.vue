<template >
  <div id="comment" class = "common_container">
    <div class="common_center_container">
      <a-row style="margin-bottom:80px;">
        <a-col :span="6">
          <img style="width:100%" src="/anniversary_static/img/comment_banner_left.png" >
        </a-col>
        <a-col :span="12">
          <div class="comment_guide" style="font-size:25px">
            对于<span style="font-weight:700">“线上直播”、“线下沙龙”</span>的主题和形式
          </div>
          <div class="comment_guide" style="font-size:25px">
            你有什么想法？
          </div>
          <div class="comment_guide" style="font-size:25px">
            对于医咖会，你有什么想说的话？
          </div>
          <div class="comment_guide" style="font-size:25px">
            请畅所欲言吧！
          </div>
          <div class="comment_guide" style="font-size:25px">
            筛选后公开显示的优质留言用户，
          </div>
          <div class="comment_guide" style="font-size:25px;font-weight:700;">
            可获得“活动积极分子”勋章一枚！
          </div>
        </a-col>
        <a-col :span="6">
          <img style="width:100%" src="/anniversary_static/img/comment_banner_right.png" >
        </a-col>
      </a-row>
      <a-row class="common_title_container" align="middle" type="flex" justify="center">
        <a-col :span="24" style="color:#dfcdaf">
          －　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－　－
        </a-col>
      </a-row>
      <a-row class="comment_subtitle_container" align="middle" type="flex" justify="center">
        <a-col :span="1" class="height-30 "><img style="width:85%;height:auto" src="/anniversary_static/img/comment.svg" alt=""></a-col>
        <a-col :span="23" class="height-30 "><div class="comment_subtitle">精选留言</div></a-col>
      </a-row>
      <a-row>
        <a-col class="comment_inputter_container" :span="24" align="middle" type="flex" justify="center">
          <a-textarea class="comment_inputter" v-model="user_comment" :placeholder="placeholder" :rows="4" :autosize="{ minRows: 4 ,maxRows:6}" />
        </a-col>
        <a-col :span="2" :offset="22" align="right">
          <a-button class="submit_btn"  @click="putComment" style="width:70px;height:30px;background:">留言</a-button>
        </a-col>
      </a-row>
      <a-row class="special_comment_container">

        <!-- 一条留言 -->
          <a-col :span="24" class="special_comment" v-for="item in comments" :key="item.id">
            <a-row class="special_comment_head">
              <a-col :span="1" class="avatar_container">
                <img class="avatar" :src="'/images/avatar/'+(item.user.avatar==null?'user_static.svg':item.user.avatar)" alt="">
              </a-col>
              <a-col :span="22" align="left" class="user_name_container " >
                {{item.user.username}}
              </a-col>
              <a-col :span="1" align="left" class="like_container" justify="center">
                <img class="like" @click="change_like(item.id)" :src="item.is_praise==1?'/anniversary_static/img/like_active.svg':'/anniversary_static/img/like_negative.svg'">
                {{item.like_num}}
              </a-col>
            </a-row>
            <a-row class="special_comment_body">
              <a-col :span="24" class="comment_body_content" align="left">
                <a-row>
                  <a-col :span="24">
                    {{item.comments}}
                  </a-col>
                  <a-col  :span="24">
                    <div class="time_container">
                      {{new Date(item.create_time).toLocaleString('chinese', { hour12: false })}}
                    </div>
                  </a-col>
                </a-row>
              </a-col>
              <!-- 一条回复 -->
              <a-col :span="24" class="reply_container" v-if="item.reply">
                <a-row>
                  <!-- 回复的尖角 -->
                  <a-col :span="1" :offset="2">
                    <div class="reply_angle"></div>
                  </a-col>
                  <a-col class="reply" :span='24'>
                    <a-row>
                      <a-col :span='24'>
                        {{item.reply.user_name}}：{{item.reply.content}}
                      </a-col>
                      <a-col :span='24' class="time_container">
                        {{new Date(item.reply.create_time).toLocaleString('chinese', { hour12: false })}}
                      </a-col>
                    </a-row>
                  </a-col>
                </a-row>
              </a-col>
            </a-row>
          </a-col>

      </a-row>
      <!-- 分页 -->
      <a-row class="page_container">
        <a-col :span="24" align="center" >
             <a-pagination :total="page_count*10"  @change="getComments(page)" v-model="page"></a-pagination>
        </a-col>
      </a-row>
      <!-- 登录提示框 -->
      <section>
        <a-modal
            v-model="go_login_visible"
            title="提示："

            @ok="go_login_ok"
            
            @cancel="go_login_cancel"
            okText="确定"
            cancelText="取消"
            >
          <p>不登录无法参与活动哦～ 先去登录吧</p>
        </a-modal>
      </section>
      <!-- 补全信息提示框 -->

      <!-- <section>
        <a-modal
            v-model="full_information_visible"
            title="提示："
            @ok="full_information_ok"
            @cancel="full_information_cancel"
            okText="确定"
            cancelText="取消"
            >
          <p>您的个人信息不全哦～ 要不要去补全呢</p>
        </a-modal>
      </section> -->
      <div class = "modal_container" v-show="information_visible">
        <div class="information_container" >
            <div style="height:244px;overflow:hidden;position:relative" >
                 <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="cancel_information">
                <img style="width:100%;height:auto;" src="/anniversary_static/img/sci_banner_2.png" >
            </div>
            <a-row >
                <a-col :span="24" style="font-size:18px;line-height:40px;margin-top:50px;">
                    如果留言被精选，勋章将于24小时内<br>
                    赠送给你，稍后请去个人中心查看吧
                </a-col>
            </a-row>
            <a-row  style="margin-top:20px">
                <a-col>
                  <a-button @click="cancel_information(true)" type="primary">前往个人中心</a-button>
                </a-col>
            </a-row>
        </div>
      </div>

      <div class = "modal_container" v-show="full_information_visible">
        <div class="information_container" >
            <div style="height:240px;overflow:hidden;position:relative" >
                 <img style="width:50px;height:50px;position:absolute;cursor:pointer;right:0;margin-top:10px;margin-right:10px;" src="/anniversary_static/img/cancel.svg" @click="full_information_cancel">
                <img style="width:100%;height:auto;" src="/anniversary_static/img/sci_banner_2.png" >
            </div>
            <a-row >
                <a-col :span="24" style="font-size:18px;line-height:40px;margin-top:40px;">
                    如果留言被精选，勋章将于24小时内<br>
                    赠送给你，稍后请去个人中心查看吧
                </a-col>
            </a-row>
            <a-row style="margin-top:20px">
                <a-col style="font-size:10px;">
                  小咖发现你的个人资料不完整,快去个人中心完善<br>
                  一下职业资料，否则会影响勋章的赠送和后续活动的参加！
                </a-col>
            </a-row>
            <a-row  style="margin-top:20px">
                <a-col>
                  <a-button @click="full_information_ok" type="primary">个人信息完善</a-button>
                </a-col>
            </a-row>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import hostConfig from '../../config/host.config.js'
import httpMethods from '../methods/http_methods.js'

export default {
  name: 'comment',
  data () {
    return {
      go_login_visible:false,
      full_information_visible:false,
      information_visible:false,
      placeholder:'您的留言在精选后上墙哦～',
      user_comment:'',
      pre_page:1,
      page:1,
      pagesize:30,
      // 总页数
      page_count:0,
      comments:[],
      is_click:false
    }
  },
  methods:{
     getComments: function (page) {
      axios.get(hostConfig.host+"/get_activity_comments/twoYear/"+page+"/"+this.pagesize+"/")
      .then((response)  =>  {
        console.log(response)
        let data = response.data.data
        this.comments = data.comments
        this.page = data.page
        this.page_count = data.page_count
      }, (error)  =>  {
        console.log(error)
      })
    },
    putComment:function(){
      if(this.is_click){
        return
      }
      this.is_click = true
      if(this.user_comment.trim()==""){
        this.user_comment = ""
        this.placeholder = "提交的留言不能为空哦～"
        this.is_click = false
        return
      }
      httpMethods.post_form(
        hostConfig.host+"/add_activity_comments/",
        {topic_type:"twoYear",comments:this.user_comment}
      ).then((response)=>{
        if(response.data.code==302){
          // 未登录
          this.go_login_showModal()
          this.is_click = false
        }else if(response.data.code==200){
          this.user_comment = ""
          if(response.data.message=="留言提交成功,用户信息不完整"){
            //TODO:信息不完整
            this.full_information_showModal()
            this.is_click = false
            return
          }
          this.information_showModal()
          this.is_click = false
        }
      },(error)=>{
        this.is_click = false
        console.log(error)
      })
    },
    change_like:function(comment_id){
      axios.get(hostConfig.host+'/activity_comment_like/'+comment_id+'/').then((response)=>{
        if(response.data.code==302){
          // 未登录
         this.go_login_showModal()
        }else if(response.data.code==200){
          this.getComments(this.page)
        }
      },(error)=>{
        console.log(error)
      })
    },    
    go_login_showModal:function() {
      this.go_login_visible = true
    },
    go_login_ok(){
      this.go_login_visible = false
      location.href=hostConfig.host+'/login/?next='+location.pathname+'#1'
    },
    go_login_cancel:function(){
      this.go_login_visible = false
    },
    full_information_showModal:function(){
      this.full_information_visible = true
      this.$parent.lock_scroll()
    },
    information_showModal(){
      this.information_visible = true
      this.$parent.lock_scroll()
    },
    full_information_ok:function(){
      window.open(hostConfig.host+'/user/?next='+location.pathname+'#1')
      this.full_information_visible = false
      this.$parent.unlock_scroll()
    },
    full_information_cancel:function(){
      this.full_information_visible = false
      this.$parent.unlock_scroll()
    },
    cancel_information(to_user_center){
      if(to_user_center){
        window.open(hostConfig.host+'/user/?next='+location.pathname+'#1')
      }
      this.information_visible = false
      this.$parent.unlock_scroll()
    }
  },
  created:function(){
    this.getComments(1)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
  .modal_container{
      width:100%;
      height:100%;
      position:fixed;
      top:0;
      left:0;
      background: rgba(0,0,0,0.4);
      z-index:6;
  }
  .information_container{
      width: 660px;
      height: 500px;
      background-color: #f9faff;
      position:fixed;
      top:50%;
      left:50%;
      margin-left:-300px;
      margin-top:-200px;
      z-index:5;
  }
  .comment_guide{
    color:#dfcdaf;
    margin-bottom:33px;
  }
  .comment_subtitle{
    margin-left:10px;
  }
  .comment_subtitle_container{
    height:30px;
    color:#02f2e8;
    text-align:left;
    font-size:19px;
    font-weight: 500;
    margin-bottom:15px;
  }
  .comment_inputter{
    background: #475ad7;
    color: white;
  }
  .submit_btn{
     width: 70px;
     height: 30px;
     background-color: #dfcdaf;
     color:black;
  }
  .submit_btn:focus,.submit_btn:hover{
    background-color: #dfcdaf!important;
    color:black!important;
  }
  .comment_inputter_container{
    margin-bottom:20px;
  }
  .special_comment_container{
    margin-top:70px
  }
  .special_comment{
    border-bottom:1px solid rgba(255,255,255,0.5);
    margin-top:20px;
  }
  .user_name_container{
    color:white;
    height: 38px;
    line-height: 38px;
  }
  .avatar_container{
    height:38px;
  }
  .avatar{
    width:38px;
    height:38px;
    border-radius: 50%;
  }
  .special_comment_head{
    margin-bottom:20px;
  }
  .comment_body_content{
    color:white;
    margin-bottom:20px;
  }
  .reply_angle{
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 0 16px 16px 16px;
    border-color: transparent transparent #818ee3 transparent;
  }
  .reply{
    background:#818ee3;
    border-radius:3px;
    text-align: left;
    color:white;
    line-height: 20px;
    padding-left:20px;
    padding-right:20px;
    padding-top:10px;
    padding-bottom:10px;
  }
  .reply_container{
    margin-bottom:20px;
  }
  .like_container{
    color:white;
  }
  .like{
    cursor: pointer;
    width:15px;
    height:auto;
  }
  .page_container{
    margin-top:30px;
    margin-bottom:30px;
  }
  .time_container{
    margin-top:5px;
    font-size:10px;
  }
</style>
