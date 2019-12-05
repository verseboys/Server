import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import medal from '@/components/medal'
import anniversary_comment from '@/components/anniversary_comment'
import user_medal from '@/components/user_medal'
import yizhu_friend_message from '@/components/yizhu_friend_message'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/medal',
      name: 'medal',
      component: medal
    },
    {
      path: '/anniversary_comment',
      name: 'anniversary_comment',
      component: anniversary_comment
    },
    {
      path: '/user_medal',
      name: 'user_medal',
      component: user_medal
    },
    {
      path:'/yizhu_friend_message',
      name: 'yizhu_friend_message',
      component: yizhu_friend_message
    }
  ]
})
