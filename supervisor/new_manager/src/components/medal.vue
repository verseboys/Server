<template>
  <div>
    <v-row>
      <v-col :span="3" align="middle">
        勋章名
      </v-col>
      <v-col :span="3" align="middle">
        勋章UID
      </v-col>
      <v-col :span="3" align="middle">
        是否启用
      </v-col>
      <v-col :span="8" align="middle">
        勋章图片路径
      </v-col>
      <v-col :span="6" align="middle">
        勋章描述
      </v-col>
      <v-col :span="1" align="middle">
        操作
      </v-col>
    </v-row>
    <v-row v-for="medal in medal_list" :key="medal.id" align="middle" type="flex" style="margin-top:3px;">
      <v-col :span="3" align="middle">
        {{medal.name}}
      </v-col>
      <v-col :span="3" align="middle">
        {{medal.uid}}
      </v-col>
      <v-col :span="3" align="middle">
        {{medal.is_valid==true?'是':'否'}}
      </v-col>
      <v-col :span="8" align="middle">
        {{medal.pic_url}}
      </v-col>
      <v-col :span="6" align="middle">
        {{medal.description}}
      </v-col>
      <v-col :span="1" align="middle">
        <v-button type="error" @click="delete_medal(medal.uid,medal.name)">删除</v-button>
      </v-col>
    </v-row>

    <v-row style="margin-top:5px">
      <v-col :span="3" align="middle">
        <v-input v-model="add_medal_name" placeholder="请输入勋章名"></v-input>
      </v-col>
      <v-col :span="3" align="middle">
        <v-input v-model="add_medal_uid" placeholder="请输入勋章uid"></v-input>
      </v-col>
      <v-col :span="3" align="middle">
        <v-radio v-model="add_medal_is_valid"  label="1">是</v-radio>
        <v-radio v-model="add_medal_is_valid"  label="0">否</v-radio>
      </v-col>
      <v-col :span="8" align="middle">
        <v-input v-model="add_medal_pic_url" placeholder="请输入勋章图片路径"></v-input>
      </v-col>
      <v-col :span="6" align="middle">
        <v-input v-model="add_medal_description" placeholder="请输入勋章描述信息"></v-input>
      </v-col>
      <v-col :span="1" align="middle">
        <v-button @click="add_medal">{{add_medal_button}}</v-button>
      </v-col>
    </v-row>

    <v-modal title="提示："
             :visible="asyncModalVisible"
             @ok="handleAsyncOk"
             @cancel="hideAsyncModal"
             :confirm-loading="asyncConfirmLoading">
        <p>{{message}}</p>
    </v-modal>


  </div>
</template>

<script>

import axios from 'axios'
import hostConfig from '../../config/host.config.js'
import httpMethods from '../methods/http_methods.js'

export default {
  name: 'medal',
  data () {
    return {
      message:'',
      asyncModalVisible: false,
      asyncConfirmLoading: false,
      action:null,
      actionData:null,
      medal_list: [],
      add_medal_button:'添加',

      add_medal_name:'',
      add_medal_uid:'',
      add_medal_is_valid:'',
      add_medal_pic_url:'',
      add_medal_description:''
    }
  },
  methods:{
    loadMessage(){
      axios.get(hostConfig.host+'/supervisor/get_medal/').then((res)=>{
        if(res.data.code==200){
          this.medal_list = res.data.data
        }else{
          console.log('勋章接口错误',res)
        }

      },(error)=>{
        console.log(error)
      })
    },
    showAsyncModal () {
        this.asyncModalVisible = true;
    },
    hideAsyncModal () {
        this.asyncModalVisible = false;
    },
    handleAsyncOk(){
      if(this.action == "delete_medal"){
        this.asyncConfirmLoading = true
        httpMethods.post_form(hostConfig.host+'/supervisor/delete_medal/',{
          uid:this.actionData.uid
        }).then((res)=>{
          if(res.data.code==200){
            this.asyncConfirmLoading = false
            this.hideAsyncModal ()
            this.clear_delete_medal()
            this.loadMessage()
          }else{
            console.log("删除勋章错误",res)
          }
        },(error)=>{
          console.log(error)
        })
      }else{
        alert("提示框行为不存在")
      }
    },
    clear_delete_medal(){
      this.action = null
      this.actionData = null
      this.message = null
    },
    clear_add_medal(){
      this.add_medal_name = null
      this.add_medal_uid = null
      this.add_medal_is_valid = null
      this.add_medal_pic_url = null
      this.add_medal_description = null
    },
    delete_medal(uid,name){
      this.action = "delete_medal"
      this.message = "确定要删除 "+name +" 吗"
      this.actionData = {uid}
      this.showAsyncModal()
    },
    add_medal(){
      httpMethods.post_form(hostConfig.host+'/supervisor/add_medal/',{
        medal_type:1,
        description:this.add_medal_description,
        name:this.add_medal_name,
        uid:this.add_medal_uid,
        pic_url:this.add_medal_pic_url,
        is_valid:this.add_medal_is_valid
      }).then((res)=>{
        if(res.data.code==200){
          this.clear_add_medal()
          this.loadMessage()
        }else{
          alert(res.data.message)
          this.loadMessage()
        }
      },(error)=>{
        console.log(error)
      })
    }

  },
  created(){
    this.loadMessage()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
