<template>
    <div class = "get_medal_modal_container">
        <div class="get_medal_container">
            <img  style="position:fixed;top:45%;left:50%;margin-top:-100px;margin-left:-100px;" src="/anniversary_static/img/gift_loading.svg" >
            <div style="color:white;position:fixed;top:52%;left:50%;margin-left:-37px;">
                LOADING···
            </div>
        </div>
    </div>
</template>

<script>

export default {
  name: 'getMedal',
  data () {
    return {
    }
  },
  methods:{
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style  scoped>
.get_medal_modal_container{
    width:100%;
    height:100%;
    position:fixed;
    top:0;
    left:0;
    background: rgba(0,0,0,0.4);
    z-index:6;
}
.get_medal_container{
    width: 600px;
    height: 380px;
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-300px;
    margin-top:-190px;
    z-index:7;
    border-radius: 5px;
}
</style>
