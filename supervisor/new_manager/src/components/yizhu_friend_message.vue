<template>
  <div>
      <v-row style="margin-bottom:10px">
          <v-col :span="24" align="middle" >
              <v-button @click="show_sci_members">
                  SCI成员信息（展示及统计不包含已被剥夺的）
              </v-button>
              <v-button @click="show_friend_members">
                  医咖会的朋友信息
              </v-button>
          </v-col>
      </v-row>
    <div v-if="show_witch=='sci'">
        <v-row >
                <v-col :span="4" align="middle">
                    用户名
                </v-col>
                <v-col :span="4" align="middle">
                    用户邮箱
                </v-col>
                <v-col :span="8" align="middle">
                    杂志名
                </v-col>
                <v-col :span="8" align="middle">
                    成员总计： {{sci_member_list.length}} 人
                </v-col>
        </v-row>
        <v-row style="margin-top:5px" v-for="sci_member in sci_member_list" :key="sci_member.id">
            <v-col :span="4" align="middle">
                {{sci_member.user.username}}
            </v-col>
            <v-col :span="4" align="middle">
                {{sci_member.user.email}}
            </v-col>
            <v-col :span="8" align="middle">
                {{sci_member.data.magazine}}
            </v-col>
        </v-row>
    </div>

    <div v-if="show_witch=='friend'">
        <v-row >
            <v-col :span="4" align="middle">
                用户名
            </v-col>
            <v-col :span="4" align="middle">
                用户邮箱
            </v-col>
            <v-col :span="4" align="middle">
                成员类型
            </v-col>
            <v-col :span="4" align="middle">
                联系方式
            </v-col>
            <v-col :span="4" align="middle">
                是否为sci大神
            </v-col>
            <v-col :span="4" align="middle">
                成员总计： {{friend_member_list.length}} 人
            </v-col>
        </v-row>
        <v-row style="margin-top:5px" v-for="friend_member in friend_member_list" :key="friend_member.id">
            <v-col :span="4" align="middle">
                {{friend_member.user.username}}
            </v-col>
            <v-col :span="4" align="middle">
                {{friend_member.user.email}}
            </v-col>
            <v-col :span="4" align="middle">
                {{(friend_member.data.is_writer==1?"专栏作者":"")+(friend_member.data.is_writer==1&&friend_member.data.is_liaison==1?"，":"")+(friend_member.data.is_liaison==1?"工会合伙人":"")}}
            </v-col>
            <v-col :span="4" align="middle">
                {{friend_member.data.friend_mobile}}
            </v-col>
            <v-col :span="4" align="middle">
                {{Object.keys(friend_member.data.sci).length==0?"否":("发表期刊："+friend_member.data.magazine)}}
            </v-col>
        </v-row>
    </div>

  </div>
</template>

<script>

import axios from 'axios'
import hostConfig from '../../config/host.config.js'
// import httpMethods from '../methods/http_methods.js'

export default {
  name: 'yizhu_friend_message',
    data () {
        return {
            anniversary_time:2,
            show_witch:null,
            sci_member_list:[],
            friend_member_list:[]
        }
    },
    methods:{
        show_sci_members(){
            this.show_witch = "sci"
            axios.get(hostConfig.host+'/supervisor/get_sci_member/'+this.anniversary_time+'/').then((res)=>{
                if(res.data.code==200){
                    this.sci_member_list = res.data.data
                    console.log(res.data.data)
                }else{
                    this.openNotification(res.data.message)
                }
            },(error)=>{
                console.log(error)
            })
        },
        show_friend_members(){
            this.show_witch = "friend"
            axios.get(hostConfig.host+'/supervisor/get_friend_member/'+this.anniversary_time+'/').then((res)=>{
                if(res.data.code==200){
                    this.friend_member_list = res.data.data
                    console.log(res.data.data)
                }else{
                    this.openNotification(res.data.message)
                }
            },(error)=>{
                console.log(error)
            })
        },
        openNotification(message) {
            this.$notification.open({
                message: '提示：',
                description:message,
                duration: 3,
            });
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
