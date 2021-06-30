import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Resources from '@/components/Resources'
import Messages from '@/components/Messages'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/resources',
      name: 'resources',
      component: Resources
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    }
  ]
})
