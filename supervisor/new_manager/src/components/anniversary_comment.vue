<template>
  <div>
    <v-row justify="center" type="flex">
      <v-button @click="changeShowWitch(2)">
        显示全部
      </v-button>
      <v-button @click="changeShowWitch(0)" style="margin:0 10px">
        仅显示未展示留言
      </v-button>
      <v-button @click="changeShowWitch(1)">
        仅显示已展示留言
      </v-button>

    </v-row>
    <v-row style="margin:10px 0">
      <v-col :span="3" align="middle">
        用户名
      </v-col>
      <v-col :span="10" align="middle">
        留言内容
      </v-col>
      <v-col :span="4" align="middle">
        回复内容
      </v-col>
      <v-col :span="2" align="middle">
        留言状态
      </v-col>
      <v-col :span="5" align="middle">
        操作
      </v-col>
    </v-row>

    <v-row v-for="comment in comment_list" :key="comment.id" style="margin-top:5px;">
      <v-col :span="3" align="middle">
        {{comment.user.username}}
      </v-col>
      <v-col :span="10" align="middle">
        {{comment.comments}}
      </v-col>
      <v-col :span="4" align="middle">
        <!-- {{new Date(comment.create_time).toLocaleString('chinese', { hour12: false })}} -->
        {{comment.reply?(comment.reply.user_name+":"+comment.reply.content):'无回复'}}
      </v-col>
      <v-col :span="2" align="middle">
        {{comment.is_publish?'已展示':'未展示'}}
      </v-col>
      <v-col :span="5" align="middle">
        <v-button @click="change_show_state(comment)">
          展示状态
        </v-button>
        <v-button @click="showAsyncModal(comment.id)">
          回复
        </v-button>
      </v-col>
    </v-row>
    <v-row>
      <v-col :span="24" align="middle">
        <v-pagination
          :value="page"
          :total="page_count*page_size"
          :page-size="page_size"
          @change="loadMessage"
          show-size-changer
          @sizechange="pageSizeChange"
          show-quick-jumper
          size="small"
          :simple="false"
          :show-total="showTotal">
        </v-pagination>
      </v-col>
    </v-row>

    <v-modal title="展示状态修改"
             :visible="stateModalVisible"
             @ok="handleStateOk"
             @cancel="stateModalCancel"
             :confirm-loading="stateConfirmLoading">
            <p>
                {{change_state_alert}}
            </p>
    </v-modal>

    <v-modal title="留言回复"
             :visible="asyncModalVisible"
             @ok="handleAsyncOk"
             @cancel="handleAsyncCancel"
             :confirm-loading="asyncConfirmLoading">
        <v-input-group size="large">
            <v-col span="6">
                <v-input v-model="reply_name" placeholder="请输入回复人姓名"></v-input>
            </v-col>
            <v-col span="18">
                <textarea style="width:100%;height:100%"  v-model="reply_content"  placeholder="请输入回复内容"></textarea>
            </v-col>
        </v-input-group>
    </v-modal>

  </div>
</template>

<script>

import axios from 'axios'
import hostConfig from '../../config/host.config.js'
import httpMethods from '../methods/http_methods.js'

export default {
  name: 'anniversary_comment',
  data () {
    return {
      is_loading:false,
      page_size:10,
      page:1,
      page_count:1,
      showWitch:2,
      comment_list:[],
      reply_name:'',
      reply_content:'',
      reply_comment_id:null,

      change_state_id:null,
      change_state_state:null,
      change_state_alert:'',
      
      stateModalVisible:false,
      stateConfirmLoading:false,
      asyncModalVisible: false,
      asyncConfirmLoading: false
    }
  },
  methods:{
    change_show_state(comment){
      this.change_state_id = comment.id
      this.change_state_state = comment.is_publish
      this.change_state_alert = "是否要将用户 "+ comment.user.username +" 的评论状态修改为 " +(comment.is_publish?"不展示":"展示")
      this.stateModalVisible = true
    },
    stateModalCancel(){
      this.stateModalVisible = false
    },
    handleStateOk(){
       axios.get(hostConfig.host+'/supervisor/change_activity_comment_state/'+this.change_state_id+'/'+(this.change_state_state==true?0:1)+'/').then((res)=>{
        if(res.data.code==200){
          this.loadMessage(this.page)
          this.stateModalVisible = false
        }
       },(error)=>{
         console.log(error)
       })
    },
    changeShowWitch(num){
      this.showWitch = num
      this.page = 1
      this.loadMessage(1)
    },
    loadMessage(page){
      console.log(page)
      if(this.is_loading == true){
        return
      }
      this.is_loading = true
      axios.get(hostConfig.host+'/supervisor/get_activity_comments/twoYear/'+page+'/'+this.page_size+'/'+this.showWitch+'/').then((res)=>{
        if(res.data.code==200){
          console.log(res)
          this.comment_list = res.data.data.comments
          this.page_count = res.data.data.page_count
          this.page = Number(res.data.data.page)
          this.is_loading = false
        }else{
          console.log('勋章接口错误',res)
        }

      },(error)=>{
        console.log(error)
      })
    },
    showTotal(total,totalPages){
      console.log('showtotal',total,totalPages)
    },
    pageSizeChange(page,pageSize){
      this.page_size = pageSize
      this.loadMessage(1)
    },
    showAsyncModal (comment_id) {
      this.reply_comment_id = comment_id
      this.asyncModalVisible = true;
    },
    handleAsyncOk () {
      let t = this
      this.asyncConfirmLoading = true;
      httpMethods.post_form(hostConfig.host+'/supervisor/reply_user_comment/',{
        comment_id:this.reply_comment_id,
        content:this.reply_content,
        reply_user:this.reply_name
      }).then((res)=>{
        if(res.data.code==200){
          t.asyncModalVisible = false;
          t.asyncConfirmLoading = false;
          t.loadMessage(t.page)
          t.reply_content = ''
        }else{
          t.asyncModalVisible = false;
          t.asyncConfirmLoading = false;
          console.log('添加回复错误',res)
          alert(res.data.message)
        }

      },(error)=>{
        console.log(error)
      })
      // setTimeout(() => {
      //     this.asyncModalVisible = false;
      //     this.asyncConfirmLoading = false;
      // }, 2000);
    },

    handleAsyncCancel () {
      this.asyncModalVisible = false;
    }
  },
  created(){
    this.loadMessage(1)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


</style>
