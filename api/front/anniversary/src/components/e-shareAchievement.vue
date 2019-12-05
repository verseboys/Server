<template>
    <div class = "common_container" id="share_achievement">
        <div class="common_center_container">
            <a-row class="common_mid_title_container" align="middle" type="flex" justify="center">
                <a-col :span="9" class="height-50 common_annex_container"><div class="common_annex1"></div><div class="common_annex2"></div></a-col>
                <a-col :span="6" class="height-50 "><div class="common_title">参与未来</div></a-col>
                <a-col :span="9" class="height-50 "><div class="common_annex3"></div><div class="common_annex4"></div></a-col>
            </a-row>
            <a-row align="middle" class="sub_title_container" type="flex" justify="center">
                <a-col :span="2"  align="middle">
                    <a-row >
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="17" :offset="1">
                    <a-row>
                        <a-col :span="24" class="sub_title_content">
                            医咖会吸引了众多热爱和关注临床研究的用户。优秀的你，可能已经发表了<span class="special_content"> SCI </span>；
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24" class="sub_title_content">
                            可能刚刚投了稿，正在等待Editor的回复；可能正在做课题，准备向高分杂志发起冲击......
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :span="24" class="sub_title_content">
                            期待未来你能够将你的研究成果来与其他伙伴们分享，你的经验，对其他伙伴无比重要！
                        </a-col>
                    </a-row>
                </a-col>
                <a-col :span="2"    align="middle">
                    <a-row >
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                        <a-col :span="8">
                            <div class="title_point"></div>
                        </a-col>
                    </a-row>
                </a-col>
            </a-row>
            <a-row style="margin-top:100px;">
                <a-col :span="14" offset="5">
                    <img style="width:100%;height:auto" src="/anniversary_static/img/share_achievement.png" >
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script>

export default {
  name: 'shareAchievement',
  data () {
    return {
    }
  },
  methods:{
  },
  created:function(){
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
.common_container{
    min-height:960px
}
.title_point{
    width: 13px;
    height:13px;
    background:#efd043;
    border-radius:50%;
    box-shadow: -3px 2px 4px 0 rgba(0, 0, 0, 0.21);
}
.sub_title_container{
    margin-top:76px;
}
.sub_title_content{
    color: #dfcdaf;
    font-weight: 700;
    font-size: 17px;
}
.special_content{
    font-size: 23px;
}
.sub_title_content{
    font-size: 18px;
}

</style>
