<template>
    <div class = "modal_container">
        <div class="login_container">
            <a-row style="margin-top:320px">
                <a-col>
                    <a-button style="margin-right:20px" @click="restart">
                        重新开始旅途
                    </a-button>
                    <a-button type="primary" @click="toComment">
                        前往“话题征集”
                    </a-button>
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
    }
  },
  methods:{
      restart(){
          this.$emit('restart')
      },
      toComment(){
          this.$emit('toComment')
      }
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
.login_container{
    width: 600px;
    height: 400px;
    background:url('/anniversary_static/img/door.svg');
    background-size: 100% 100%;
    position:fixed;
    top:50%;
    left:50%;
    margin-left:-300px;
    margin-top:-190px;
    z-index:5;
}
</style>
