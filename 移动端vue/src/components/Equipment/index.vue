<template>
  <div class="hello">
     <transition name="move">
         <div class="content" v-show="mainarea">
               <div class="content-header">
                   <h5>动力设备资源清查</h5>
               </div>
               <div class="content-wrapper">
                   <div class="wrapper">
                       <p>设备类型</p>
                   </div>
                   <div class="nav-content">
                      <Nav></Nav>
                   </div>
               </div>
      </div>
     </transition>
  </div>
</template>

<script>
import Header from '../Header.vue'
import Nav from '../Nav.vue'
export default {
  name: 'HelloWorld',
  data () {
    return {
       mainarea:false
    }
  },
  created(){

  },
  mounted(){
    this.mainarea = true
  },
  methods:{
    handleBack(){

    },
    personal(){

    }
  },
  components:{
    Header,
    Nav
  }
}
</script>

<style lang="scss" scoped>
  .hello{
    margin-top: -30px;
    font-size: 14px;
    .content{
      padding-left: 10px;
      padding-right: 10px;
      &.move-enter-active,
        &.move-leave-active {
            transition: all 0.3s;
            opacity: 0.8;
        }
        &.move-enter,
        &.move-leave-active {
            transition: all 0.3s;
            transform: translate3d(-100%, 0, 0);
            opacity: 0.8;
        }
      .content-header{
        display: flex;
        h5{
          color:#101010;
          font-size: 14px;
          margin-top: -10px;
        }
      }
      .content-wrapper{
        .wrapper{
         margin-top: 15px;
         display: flex;
         font-size: 12px;
        }
        .nav-content{

        }
      }
    }
  }
</style>
/*
  覆盖mint-ui 默认样式
*/
<style lang="scss">
   .mint-header.is-fixed {
     background-color: #555555;
   }
   .mint-header-title{
     font-size: 16px;
     font-weight: 700;
   }
   .mint-button {
     font-weight: 700;
   }
   .mint-button-text{
     font-weight: 700;
   }

</style>
