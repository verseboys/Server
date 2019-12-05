<template>
    <div class = "banner_container" style="position:relative" id="big_banner">
        <div style="width:100%;height:1400px;background: url(/anniversary_static/img/big_banner.png) no-repeat center top;">
            <!-- <img style="width:100%;height:auto;position:relative;top:50%;left:0%;overflow:hidden;transforman:translate(-50%,-50%)" src="/anniversary_static/img/big_banner.png"> -->
        </div> 
    </div>
</template>

<script>

export default {
  name: 'bigBanner',
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
.banner_container{
    background-color: #475DD9;
    padding-bottom:50px;
}
</style>
