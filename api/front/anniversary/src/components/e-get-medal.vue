<template>
    <div class = "get_medal_modal_container">

        <div class="get_medal_container">
            <div class="medal_container animated fadeInDownBig delay-0.5s" >
                <img style="width:100%;" :src="medal_url" alt="">
            </div>
            <div class="replace"></div>
            <div class="user_avatar_container">
                <img class="avatar" :src="avatar_url"> 恭喜你获得新勋章
            </div>
            <div class="medal_name">
                {{medal_name}}
            </div>
            <div class="want_to_say">
                {{want_to_say}}
            </div>
            <div class="button_container">
                <a-button class="get_button" @click="close_modal">点击领取</a-button>
            </div>
            <div class="got_num">
                已有<span style="color:#475dd9">{{got_num}}</span>人获得
            </div>
        </div>
    </div>
</template>

<script>

export default {
  name: 'getMedal',
  props:['medal','avatar','got_num','medal_name','want_to_say'],
  data () {
    return {
        medal_url:'',
        avatar_url:'',
        avatar_complete:false,
        medal_complete:false,
        time_over:false
    }
  },
  methods:{
    close_modal(){
        this.$emit("close_modal",true)
    }
  },
  created:function(){
    let medalImg = new Image()
    let avatarImg = new Image()
    medalImg.src ='/anniversary_static/img/'+this.medal
    avatarImg.src = '/images/avatar/'+this.avatar
    medalImg.onload = () => {
        this.medal_url = medalImg.src
        this.medal_complete = true
        if(this.avatar_complete&&this.time_over){
            this.avatar_complete = false
            this.medal_complete = false
            this.time_over = false
            this.$emit('close_loading',this.medal)
        }
    }
    medalImg.onerror = medalImg.onload
    avatarImg.onload = ()=>{
        this.avatar_url = avatarImg.src
        this.avatar_complete = true
        if(this.medal_complete&&this.time_over){
            this.avatar_complete = false
            this.medal_complete = false
            this.time_over = false
            this.$emit('close_loading',this.medal)
        }
    }
    avatarImg.onerror = avatarImg.onload
  },
  mounted:function(){
      setTimeout(()=>{
            this.time_over = true
            if(this.avatar_complete&&this.medal_complete){
                this.avatar_complete = false
                this.medal_complete = false
                this.time_over = false
                this.$emit('close_loading',this.medal)
            }
      },1000)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
.avatar{
    width:38px;
    height:38px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right:10px;
}
.get_medal_modal_container{
    width:100%;
    height:100%;
    position:fixed;
    top:0;
    left:0;
    background: rgba(0,0,0,0.4);
    z-index:4;
}
.get_medal_container{
    width: 600px;
    height: 380px;
    background-color: #f9faff;
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-300px;
    margin-top:-190px;
    z-index:5;
    border-radius: 5px;
}
.medal_container{
    position:absolute;
    top:0;
    left:50%;
    width:300px;
    height:232px;
    margin-left:-150px;
    margin-top:-110px;
}
.replace{
    height:100px;
}
.user_avatar_container{
    font-size:18px;
    text-align:center
}
.medal_name{
    font-size:32px;
    color: #475dd9;
    margin-top:25px;
    -webkit-text-stroke: 1px #475dd9;
}
.want_to_say{
    margin-top:25px;
}
.button_container{
    margin-top:15px;
    margin-bottom:15px;
}
.got_num{
    font-size: 13px;
}
.get_button{
    background:#475dd9;
    color: #f9faff;
    height:40px;
    width:110px;
}
.get_button:hover,get_button:focus{
    background:#475dd9!important;
    color: #f9faff!important;
}
</style>
