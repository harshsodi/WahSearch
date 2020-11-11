import Vue from 'vue'
import Router from 'vue-router'
import homepage from '@/pages/homepage'
import result from '@/pages/result'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    }, {
      path: '/result',
      redirect: '/home'
    }, {
      path: '/home',
      name: 'homepage',
      component: homepage
    }, {
      path: '/result/:searchText',
      name: 'result',
      component: result
    }
  ]
})
