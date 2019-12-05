<template>
  <div>
    <v-alert type="success" align="middle"   :message="alert_message" v-show="show_alert"  show-icon></v-alert>
      <v-row>
        <v-col :span="4" align="middle">
            用户勋章查询
        </v-col>
        <v-col :span="10" align="middle" offset="10">
            操作
        </v-col>
      </v-row>
      <v-row>
            <v-col :span="4" align="middle">
                <v-input v-model="user_name" placeholder="请输入要查询的用户昵称"></v-input>
            </v-col>
            <v-col :span="10" offset="10" align="middle">
                <v-button @click = "search_user_by_name">用户查询</v-button>
            </v-col>
      </v-row>
      <v-row style="margin-top:15px">
        <v-col :span="4" align="middle">
            用户ID
        </v-col>
        <v-col :span="6" align="middle">
            用户昵称
        </v-col>
        <v-col :span="4" align="middle">
            勋章详情
        </v-col>
        <v-col :span="4" align="middle" offset="3">
            操作
        </v-col>
      </v-row>
    <v-row style="margin-top:15px" v-for="user in user_list" :key = "user.id"  align="middle">
        <v-col :span="4" align="middle">
            {{user.id}}
        </v-col>
        <v-col :span="6" align="middle">
            {{user.username}}
        </v-col>
        <v-col :span="4" align="middle" >
            <v-button @click="get_user_medal(user.id)">
                勋章详情
            </v-button>
        </v-col>
        <v-col :span="4" align="middle" offset="3">
            <v-popconfirm  title="确定剥夺SCI勋章吗?" placement="top"  @confirm="drop_sci(user.id)">
                <v-button>
                    剥夺SCI勋章
                </v-button>
            </v-popconfirm>
            <v-popconfirm  title="确定剥夺全部勋章吗?" placement="top"  @confirm="drop_all(user.id)">
                <v-button>
                    剥夺全部勋章
                </v-button>
            </v-popconfirm>
            <v-popconfirm  title="确定恢复SCI勋章吗?" placement="top"  @confirm="give_sci(user.id)">
                <v-button>
                    恢复SCI勋章
                </v-button>
            </v-popconfirm>
            <v-popconfirm  title="确定恢复全部勋章吗?" placement="top"  @confirm="give_all(user.id)">
                <v-button>
                    恢复全部勋章
                </v-button>
            </v-popconfirm>

        </v-col>
    </v-row>

    <v-row>
        <v-col :span="24" align="middle">
            <v-pagination
            :value="page"
            :total="page_count*page_size"
            :page-size="page_size"
            @change="change_page"
            show-quick-jumper
            size="small"
            :simple="false"
            >
            </v-pagination>
        </v-col>
    </v-row>
    <v-modal title="勋章信息详情"
             :visible="medalDetailVisible"
             @cancel="medalDetailCancel"
             @ok="medalDetailCancel"
             cancelText = '关闭'
             >
            <v-row  v-if="user_medal_list.length!==0">
                <v-col :span="12" align="middle">
                    勋章名
                </v-col>
                <v-col :span="12" align="middle">
                    勋章状态
                </v-col>
            </v-row>
            <v-row v-for="medal in user_medal_list" :key="medal.id">
                <v-col :span="12" align="middle">
                    {{medal.medal_name+"勋章"}}
                </v-col>
                <v-col v-if="medal.is_disabled===false" style="color:green"  :span="12" align="middle">
                    正常
                </v-col>
                <v-col v-if="medal.is_disabled===true" style="color:red" :span="12" align="middle">
                    已剥夺
                </v-col>
            </v-row>
            <v-row>
                <v-col v-if="user_medal_list.length==0" :span="24" align="middle">
                    用户没有勋章
                </v-col>
            </v-row>
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
        user_name:'',
        page:1,
        page_count:1,
        page_size:20,
        user_list:[],
        user_medal_list:[],

        medalDetailVisible:false,
        show_alert:false,
        alert_message:'',
    }
  },
  methods:{
    medalDetailCancel(){
        this.medalDetailVisible = false
        this.user_medal_list = []
    },
    change_page(page){
        this.page = page
        this.search_user_by_name()
    },
    search_user_by_id(){

    },
    search_user_by_name(){
        httpMethods.post_form(hostConfig.host+'/supervisor/search_user/'+this.page+'/',{
            search_key_words:this.user_name
        }).then((res)=>{
            if(res.data.code==200){
                this.page_count = res.data.data.pageCount
                this.user_list = res.data.data.users
            }
        },(error)=>{
            console.log(error)
        })
    },
    get_user_medal(user_id){
        this.medalDetailVisible = true
        httpMethods.post_form(hostConfig.host+'/supervisor/get_user_medal/',{
            user_id
        }).then((res)=>{
            if(res.data.code == 200){
                this.user_medal_list = res.data.data
            }else{
                console.log('获取用户勋章详情错误',res)
            }
        },(error)=>{
            console.log(error)
        })
    },
    drop_sci(user_id){
        axios.get(hostConfig.host+'/supervisor/disable_user_medal/sci/'+user_id+'/').then((res)=>{
            if(res.data.code == 200){
                this.openNotification('剥夺SCI勋章成功')
            }else{
                this.openNotification(res.data.message)
            }
        },(error)=>{
            console.log(error)
        })
    },
    drop_all(user_id){
        axios.get(hostConfig.host+'/supervisor/disable_user_medal/all/'+user_id+'/').then((res)=>{
            if(res.data.code == 200){
                this.openNotification('剥夺全部勋章成功')
            }else{
                this.openNotification(res.data.message)
            }
        },(error)=>{
            console.log(error)
        })
    },
    give_sci(user_id){
        axios.get(hostConfig.host+'/supervisor/restore_user_medal/sci/'+user_id+'/').then((res)=>{
            if(res.data.code == 200){
                this.openNotification('恢复sci勋章成功')
            }else{
                this.openNotification(res.data.message)
            }
        },(error)=>{
            console.log(error)
        })
    },
    give_all(user_id){
        axios.get(hostConfig.host+'/supervisor/restore_user_medal/all/'+user_id+'/').then((res)=>{
            if(res.data.code == 200){
                this.openNotification('恢复全部勋章成功')
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
