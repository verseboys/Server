<template>
    <div class = "common_container">
        <div class="common_center_container">
            <a-row class="common_mid_title_container" align="middle" type="flex" justify="center">
                <a-col :span="7" class="height-50 common_annex_container"><div class="common_annex1"></div><div class="common_annex2"></div></a-col>
                <a-col :span="10" class="height-50 "><div class="common_title">优秀的你快来加入吧</div></a-col>
                <a-col :span="7" class="height-50 "><div class="common_annex3"></div><div class="common_annex4"></div></a-col>
            </a-row>      
        </div>
        <div class="call_you_center_container">
            <a-row>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" :offset="4">
                            <div class="call_you_img_container">
                                <img style="width:100%;height:auto" src="/anniversary_static/img/learner.png">
                            </div>
                            <div class="call_you_title">
                                持续学习者
                            </div>
                            <div class="call_you_content">
                                每一位关注医咖会的小伙伴，都欢迎你来医咖会持续学习、阅读教程和观看视频，和医咖会一起成长，提升临床研究水平！
                            </div>
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" :offset="4">
                            <div class="call_you_img_container">
                                <img style="width:87%;height:auto" src="/anniversary_static/img/writer.png">
                            </div>
                            <div class="call_you_title">
                                专栏作者
                            </div>
                            <div class="call_you_content">
                                从文献检索到研究设计、从统计分析到论文撰写......欢迎你向医咖会投稿或开通视频课程。不论是个人还是团队，医咖会诚挚邀请你的入驻！
                            </div>
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" :offset="4">
                            <div class="call_you_img_container">
                                <img style="width:88%;height:auto" src="/anniversary_static/img/liaison.png">
                            </div>
                            <div class="call_you_title">
                                医咖会管理员
                            </div>
                            <div class="call_you_content">
                                为方便各有所长的科研工作者交流、学习和协作，医咖会将举办类型丰富的活动。欢迎成为医咖会管理员，协调组织小伙伴们参加线上、线下培训和交流活动。
                            </div>
                        </a-col>
                    </a-row>
                </a-col>
            </a-row>
        </div>
        <div v-show="!already_choose" class="call_you_center_container">
            <a-row>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" offset="4">
                            <a-checkbox class="check_box_title" name="is_learner"  @change="onChange">我要加入（可多选）</a-checkbox>
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" offset="4">
                            <a-checkbox class="check_box_title"  name="is_writer" @change="onChange">我要加入（可多选）</a-checkbox>
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="8">
                    <a-row>
                        <a-col :span="14" offset="4">
                            <a-checkbox class="check_box_title"  name="is_liaison" @change="onChange">我要加入（可多选）</a-checkbox>
                        </a-col>
                    </a-row>
                </a-col>
            </a-row>
        </div>
        <a-row v-show="!already_choose">
            <a-col :span="24" align="middle" style="margin-top:50px;">
                <a-button @click="confirm_call_you" style="height: 38px;min-width:120px;background-color: #dfcdaf;color:black;font-size:20px;">
                    {{button_content}}
                </a-button>
            </a-col>
        </a-row>
    </div>
</template>

<script>

export default {
  name: 'callYou',
  props:['already_choose'],
  data () {
    return {
        check_state:{
            is_learner:false,
            is_writer:false,
            is_liaison:false
        },
        button_content:'确认',
        timmer:null
    }
  },
  methods:{
      onChange(event){
        this.check_state[event.target.name] = event.target.checked
      },
      confirm_call_you(){
        if(this.check_state.is_learner==false&&this.check_state.is_writer==false&&this.check_state.is_liaison==false){
            this.button_content = "你还没选择哦～"
            if(this.timmer){
                clearTimeout(this.timmer)
            }
            this.timmer = setTimeout(()=>{
                this.button_content="确定"
            },1000)
            return
        }
        this.$emit('confirm_call_you',this.check_state)
      }
  },
  created:function(){
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
.common_container{
    min-height:800px;
}
.call_you_center_container{
    margin:0 auto;
    margin-top:60px;
    width:1100px
}
.call_you_title{
    color: #dfcdaf;
    font-size: 20px;
    font-weight: 700;
    margin-top:20px;
    margin-bottom:20px;
    
}
.call_you_content{
    color:#fff;
    text-align: left;
}
.check_box_title{
    color: #dfcdaf;
    font-size: 18px;
}
</style>
