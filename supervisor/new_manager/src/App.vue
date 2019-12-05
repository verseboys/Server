<template>
    <div id="components-layout-demo-top-side">
        <v-layout style="height:100%;">
            <v-header>
                <div class="logo"></div>
                <!-- 顶部导航 -->
                <!-- <v-menu theme="dark" mode="horizontal" :data="menuData1" style="line-height: 64px"></v-menu> -->
            </v-header>
            <v-layout>
                <v-sider :width="200" style="background: #fff">
                    <v-menu mode="inline" :data="menuData2" style="height:100%" @item-click="change_nav"></v-menu>
                </v-sider>
                <v-layout style="padding:0 24px 24px;">
                    <v-breadcrumb style="margin:12px 0">
                        <v-breadcrumb-item >{{nav_1}}</v-breadcrumb-item>
                        <v-breadcrumb-item >{{nav_2}}</v-breadcrumb-item>
                        <v-breadcrumb-item >{{nav_3}}</v-breadcrumb-item>
                    </v-breadcrumb>
                    <v-content style="background: #fff; padding: 24px; margin: 0; min-height: 280px"><router-view/></v-content>
                </v-layout>
            </v-layout>
        </v-layout>
    </div>
</template>

<script>
    export default {
        name:"APP",
        data() {
            return {
                nav_1:'',
                nav_2:'',
                nav_3:'',
                // menuData1: [{
                //     name: 'nav 1'
                // },{
                //     name: 'nav 2',
                //     selected: true
                // },{
                //     name: 'nav 3'
                // }],
                menuData2: [{
                    name: '周年活动',
                    icon: 'notification',
                    expand: true,
                    children: [{
                        name: '勋章管理',
                        href:'#/medal'
                    },{
                        name: '留言管理',
                        href:'#/anniversary_comment'
                    },{
                        name: '用户勋章管理',
                        href:'#/user_medal'
                    },{
                        name: '成员信息管理',
                        href:'#/yizhu_friend_message'
                    }]
                }
                // ,{
                //     name: 'subnav 2',
                //     icon: 'laptop',
                //     children: [{
                //         name: 'option5'
                //     },{
                //         name: 'option6'
                //     },{
                //         name: 'option7'
                //     },{
                //         name: 'option8'
                //     }]
                // },{
                //     name: 'subnav 3',
                //     icon: 'notification',
                //     children: [{
                //         name: 'option9'
                //     },{
                //         name: 'option10'
                //     },{
                //         name: 'option11'
                //     },{
                //         name: 'option12'
                //     }]
                // }
                ]
            }
        },
        methods:{
          change_nav(nav_list){
            for(let index in nav_list){
              this['nav_'+(Number(index)+1)] = nav_list[index].name
            }
            console.log(this.nav_1)
            // this.nav1l = name
          }
        }
    }
</script>

<style>
  #components-layout-demo-top-side .logo {
      width: 120px;
      height: 31px;
      background: #333;
      border-radius: 6px;
      margin: 16px 28px 16px 0;
      float: left;
  }
  #components-layout-demo-top-side {
    /* height: 100%; */
  }
</style>
