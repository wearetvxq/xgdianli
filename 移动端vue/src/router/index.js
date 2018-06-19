import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode:'history',
  scrollBehavior(to,from,savedPosition) {
    if(savedPosition) {
      return savedPosition
    }else {
      return { x:0, y:0 }
    }
  },
  routes: [
    {
      path: '/',
      component: (resolve) => require(['../components/Home/home.vue'], resolve)
    },
    {
      path: '/check',
      component: (resolve) => require(['../components/Check/check.vue'], resolve)
    },
    {
      path: '/equipment',
      component: (resolve) => require(['../components/Equipment/index.vue'], resolve)
    },
    {
      path: '/clean',
      component: (resolve) => require(['../components/Clean/clean.vue'], resolve)
    },
    {
      path: '/power',
      component: (resolve) => require(['../components/Switch/switch.vue'], resolve)
    },
    {
      path: '/battery',
      component: (resolve) => require(['../components/Battery/battery.vue'], resolve)
    },
    {
      path: '/aircondition',
      component: (resolve) => require(['../components/Aircondition/aircondition.vue'], resolve)
    },
    {
      path: '/steady',
      component: (resolve) => require(['../components/Steady/steady.vue'], resolve)
    },
    {
      path: '/station',
      component: (resolve) => require(['../components/Station/station.vue'], resolve)
    },
    {
      path: '/electric',
      component: (resolve) => require(['../components/Electricbox/electricbox.vue'], resolve)
    },
    {
      path: '/cabinet',
      component: (resolve) => require(['../components/Cabinet/cabinet.vue'], resolve)
    },
    {
      path: '/transformmer',
      component: (resolve) => require(['../components/Transformmer/transformmer.vue'], resolve)
    },
    {
      path: '/emergency',
      component: (resolve) => require(['../components/Emergency/emergency.vue'], resolve)
    },
    {
      path: '/tower',
      component: (resolve) => require(['../components/Irontower/irontower.vue'], resolve)
    }
  ]
})
