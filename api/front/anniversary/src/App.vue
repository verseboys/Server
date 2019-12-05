<template>
  <div id="app"  ondragstart="return false;" style="padding-right:-27px;overflow-x:hidden" >
    <div v-if="show_alert" style="width:320px;height:80px;position:fixed;top:30%;left:50%;z-index:999;margin-left:-160px;margin-top:-40px">
      <a-alert  :message="alert_title" :description="alert_message" type="success" />
    </div>
    <iframe style="display:none" src="//cdn.mediecogroup.com/anniversary/bgm1.mp3" allow="autoplay" loop="-1"  id="audio"></iframe>
    <e-big-banner v-show="!onlyComment" />
    <e-event-list  v-show="!onlyComment" :event_1="event_1" :event_2="event_2" :event_3="event_3" :event_4="event_4" :event_5="event_5"/>
    <e-share-achievement  v-show="!onlyComment" />
    <e-card-gallery-instance v-show="!onlyComment"/>
    <e-call-you  v-show="!onlyComment" :already_choose="already_choose" @confirm_call_you="confirm_call_you" />
    <e-more-activaties />
    <e-comment  />
    <e-get-medal  :style="modal_style" v-if="modal_exist"  @close_modal="close_modal" @close_loading="close_loading" :avatar="avatar" :medal="medal" :got_num="got_num" :medal_name="medal_name" :want_to_say="want_to_say"/>
    <e-loading  v-show="loading_visable&&!onlyComment" />
    <e-login  v-show="login_visable&&!onlyComment" @login_success="login_success" @login_cancel="login_cancel" />
    <e-sci  @start_get_sci="start_get_sci" @cancel_sci="cancel_sci"  v-show="sci_visiable&&!onlyComment"/>
    <e-friend-mobile @cancel_mobile="cancel_mobile" @get_mobile="get_mobile" v-if="friend_mobile_exist&&!onlyComment"/>
    <e-door @toComment="toComment" @restart="restart" v-if="already_join&&!onlyComment" />
  </div>
</template>

<script>
import axios from 'axios'
import hostConfig from '../config/host.config.js'
import httpMethods from './methods/http_methods.js'
import eComment from './components/e-comment.vue'
import eEventList from './components/e-eventList.vue'
import eShareAchievement from './components/e-shareAchievement.vue'
import eCallYou from './components/e-callYou.vue'
import eMoreActivaties from './components/e-moreActivaties.vue'
import eBigBanner from './components/e-big-banner.vue'
import eGetMedal from './components/e-get-medal.vue'
import eLoading from './components/e-loading.vue'
import eLogin from './components/e-login.vue'
import eSci from './components/e-sci.vue'
import eFriendMobile from './components/e-friendMobile.vue'
import eDoor from './components/e-door.vue'
import ECardGalleryInstance from './components/ECardGalleryInstance.vue'


import $ from "jquery";

export default {
  name: 'App',
  components: {
    eComment,
    eEventList,
    eShareAchievement,
    eCallYou,
    eMoreActivaties,
    eBigBanner,
    eGetMedal,
    eLoading,
    eLogin,
    eSci,
    eFriendMobile,
    eDoor,
    ECardGalleryInstance
  },
  data(){
    return{
      modal_exist:false,
      loading_visable:false,
      login_visable:false,
      sci_visiable:false,
      friend_mobile_exist:false,
      is_user_login:null,
      already_join:false,
      //用户头像路径
      avatar:'',
      medal:'',
      got_num:200,
      medal_name:'',
      want_to_say:'',
      user_choose :{},

      already_show_login:false,
      already_show_old_bird:false,
      already_show_sci:false,
      already_choose:false,
      modal_style:'display:none',
      onlyComment:false,

      event_1:false,
      event_2:false,
      event_3:false,
      event_4:false,
      event_5:false,

      show_alert:false,
      alert_timmer:null,
      alert_title:"",
      alert_message:""

    }
  },
  beforeCreate(){
    // this.not_observe_scroll()
    // document.documentElement.scrollTop = 0
    // window.addEventListener('beforeunload', e => {
    //   document.documentElement.scrollTop = 0
    // });
  },
  created(){
    document.title="医咖会两周年"
  },
  beforeUpdate(){
  },
  beforeMount(){

  },
  mounted(){

    let windowH = $(window).height()
    let scrollTop = $(document).scrollTop()
    let windowScrollTop = $(window).scrollTop()
    let bigBannerH = $("#big_banner").height()
    let eventListH = $("#event_list").height()

    if(scrollTop>=bigBannerH+eventListH-windowH){
      this.already_show_old_bird = true
    }

    if(scrollTop>=bigBannerH+eventListH+250){
      this.already_show_sci = true
    }

    this.is_user_login = null
    axios.get(hostConfig.host + "/is_user_login/",{withCredentials: true}).then((res)=>{
        if(res.data.message=="已登录"){
          this.is_user_login = true
          this.avatar = res.data.data.avatar==null?'user_static.svg':res.data.data.avatar
          axios.get(hostConfig.host+'/already_join_anniversary/').then((res)=>{
              if(res.data.message=="未参与"){
                  this.already_join = false
              }else if(res.data.message=="已参与"){
                  this.lock_scroll()
                  this.already_join = true
              }
          },(error)=>{
              console.log(error)
          })
        }else{
          this.is_user_login = false
        }
    },(error)=>{
      console.log(error)
    })
    this.observe_scroll()
  },
  methods:{
    loadMore(){

      if(this.is_user_login===null){
        return
      }
      let windowH = $(window).height()
      let scrollTop = $(document).scrollTop()
      let bigBannerH = $("#big_banner").height()
      let eventListH = $("#event_list").height()
      let event_1_H = $("#event_1").height()
      let event_2_H = $("#event_2").height()
      let event_3_H = $("#event_3").height()
      let event_4_H = $("#event_4").height()
      let event_5_H = $("#event_5").height()
      let event_6_H = $("#event_6").height()
      let event_1_P = $("#event_1").position().top
      let event_2_P = $("#event_2").position().top
      let event_3_P = $("#event_3").position().top
      let event_4_P = $("#event_4").position().top
      let event_5_P = $("#event_5").position().top
      let event_6_P = $("#event_6").position().top
      let shareAchievementH = $("#share_achievement").height()

      // 滚入动画列表
      if(event_1_H+event_1_P+bigBannerH-scrollTop<=windowH){
        this.event_1 = true
      }
      if(event_2_H+event_2_P+bigBannerH-scrollTop<=windowH){
        this.event_2 = true
      }
      if(event_3_H+event_3_P+bigBannerH-scrollTop<=windowH){
        this.event_3 = true
      }
      if(event_4_H+event_4_P+bigBannerH-scrollTop<=windowH){
        this.event_4 = true
      }
      if(event_5_H+event_5_P+bigBannerH-scrollTop<=windowH){
        this.event_5 = true
      }
      if(scrollTop>=(bigBannerH-windowH)&&!this.is_user_login){
        if(!this.already_show_login){
          this.lock_scroll(scrollTop)
          this.login_visable = true;
        }
      }

      if(scrollTop>=bigBannerH+eventListH-windowH){
        if(!this.already_show_old_bird){
          this.lock_scroll(scrollTop)
          this.loading_visable = true
          httpMethods.post_form(hostConfig.host+"/get_achievemnet/",{uid:'old_bird'}).then((res)=>{
            if(res.data.code==200||res.data.code==400||res.data.code==401){
              this.medal = "old_bird.svg"
              this.got_num = res.data.data.medal_count
              this.medal_name = "医咖会见证者·2018"
              this.want_to_say = "感谢有你，2018年和医咖会共庆两周岁"
              this.modal_exist = true
            }
          },(error)=>{
            console.log(error)
          })
        }
      }

      if(scrollTop>=bigBannerH+eventListH+250){
        if(!this.already_show_sci){
          this.lock_scroll(scrollTop)
          this.sci_visiable = true
        }
      }



    },
    observe_scroll(){
      $(document).on("scroll", this.loadMore.bind(this));
      this.$nextTick(() => {
          this.$root.$el.addEventListener('scroll', ()=>{})
      })
    },
    not_observe_scroll(){
      $(document).off("scroll")
    },
    modal_visable(){
      this.modal_style = 'display:block'
    },
    modal_invisable(){
      this.modal_style = 'display:none'
    },
    close_modal(is_medal){
      this.unlock_scroll()
      this.modal_exist = false
      if(is_medal){
        this.alert_user("勋章获取成功","可在『个人中心』查看获得的勋章哦~")
      }
    },
    close_loading(medal){
      this.loading_visable = false
      this.modal_visable()
      if(medal=='old_bird.svg'){
        this.already_show_old_bird = true
      }else if(medal=='sci_god.svg'){
        this.already_show_sci = true
      }
    },
    login_success(already_join,avatar){
      this.already_join = already_join
      this.avatar = avatar==null?'user_static.svg':avatar
      if(already_join){
        this.login_visable = false
        this.already_show_login = true
      }else{
        this.unlock_scroll()
        this.login_visable = false
        this.already_show_login = true
        this.alert_user('登录成功','背起小包包，旅途开始喽！')
      }
    },
    login_cancel(){
      this.login_visable = false;
      this.unlock_scroll()
      this.not_observe_scroll()
      let $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
      let scrollTop = $(document).scrollTop()
      $body.animate({scrollTop: scrollTop-20}, 500);
      setTimeout(()=>{
        this.observe_scroll()
      },1000)
    },
    lock_scroll(height){
      this.not_observe_scroll()
      if(!height){
        let top=$(document).scrollTop();
        $(document).on('scroll.unable',function (e){
          $(document).scrollTop(top);
        })
      }else{
        $(document).on('scroll.unable',function (e){
          $(document).scrollTop(height);
        })
      }
    },
    unlock_scroll(){
      $(document).off("scroll.unable");
      this.observe_scroll()
    },
    cancel_sci(){
      this. sci_visiable = false
      this.unlock_scroll()
      this.already_show_sci = true
    },
    start_get_sci(magazine){
      this.sci_visiable = false
      this.modal_invisable()
      this.loading_visable = true
      httpMethods.post_form(hostConfig.host+"/get_achievemnet/",{
            uid:'sci_god',
            magazine:magazine
      }).then((res)=>{
          if(res.data.code==200||res.data.code==400||res.data.code==401){
            this.medal = "sci_god.svg"
            this.got_num = res.data.data.medal_count
            this.medal_name = "SCI大神"
            this.want_to_say = "Respect! Respect! Respect!"
            this.modal_exist = true
          }
      },(error)=>{
          console.log(error)
      })
    },
    confirm_call_you(user_choose){
      this.already_choose = true
      this.modal_invisable()
      if(user_choose.is_writer === true || user_choose.is_liaison === true){
        this.lock_scroll()
        this.user_choose = user_choose
        this.friend_mobile_exist = true

        return
      }else{
        this.loading_visable = true
        httpMethods.post_form(hostConfig.host+"/get_achievemnet/",{
          uid:'yizhu_friend',
          is_learner:1
        }).then((res)=>{
            if(res.data.code==200||res.data.code==400||res.data.code==401){
              this.medal = "yizhu_friend.svg"
              this.got_num = res.data.data.medal_count
              this.medal_name = "医咖会的朋友"
              this.want_to_say = "请收下小咖的感激和敬意"
              this.modal_exist = true
            }
        },(error)=>{
            console.log(error)
        })
      }
    },
    get_mobile(mobile){
        this.friend_mobile_exist = false
        this.loading_visable = true
        httpMethods.post_form(hostConfig.host+"/get_achievemnet/",{
          uid:'yizhu_friend',
          is_learner:this.user_choose.is_learner+0,
          is_writer:this.user_choose.is_writer+0,
          is_liaison:this.user_choose.is_liaison+0,
          mobile:Number(mobile)
        }).then((res)=>{
            if(res.data.code==200||res.data.code==400||res.data.code==401){
              this.medal = "yizhu_friend.svg"
              this.got_num = res.data.data.medal_count
              this.medal_name = "医咖会的朋友"
              this.want_to_say = "请收下小咖的感激和敬意"
              this.modal_exist = true
            }
        },(error)=>{
            console.log(error)
        })
    },
    cancel_mobile(){
      this.user_choose = {}
      this.already_choose = false
      this.friend_mobile_exist = false
      this.unlock_scroll()
    },
    restart(){
      this.already_join = false
      this.unlock_scroll()
      this.not_observe_scroll()
      $(document).off("scroll")
      let $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
      $body.animate({scrollTop: 0}, 500);
      setTimeout(()=>{
        this.observe_scroll()
        this.already_show_old_bird = false
        this.already_show_sci = false
      },500)
    },
    toComment(){
      this.already_show_old_bird = true
      this.already_show_sci = true
      this.unlock_scroll()
      this.onlyComment = true
      let $body = (window.opera) ? (document.compatMode == "CSS1Compat" ? $('html') : $('body')) : $('html,body');
      $body.animate({scrollTop: 0}, 500);
    },
    alert_user(alert_title,alert_message){
      if(this.alert_timmer!==null){
        clearTimeout(this.alert_timmer)
      }
      this.show_alert = true;
      this.alert_title = alert_title
      this.alert_message = alert_message
      this.alert_timmer = setTimeout(()=>{
        this.show_alert = false
      },3000)
    }
  }
}
</script>

<style>
#app {
  font-family: '微软雅黑','Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top:0px;
  margin-right: -calc(100vw - 100%);
}
body{
  margin:0;
}
</style>
