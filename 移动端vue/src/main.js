// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Mint from 'mint-ui'
//import 'mint-ui/lib/style.css'
Vue.use(Mint)

//组件按需引入
import { Button , Header } from 'mint-ui';
//Vue.component('m-button', Button);

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
