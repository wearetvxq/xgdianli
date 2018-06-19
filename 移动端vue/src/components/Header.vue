<template lang="html">
  <div class="header">
    <mt-header fixed title="中国移动孝感分公司">
       <router-link to="/" slot="left">
          <mt-button icon="back" @click="Back()">返回</mt-button>
       </router-link>
       <mt-button slot="right">
             <i class="iconfont icon-people"></i>
       </mt-button>
    </mt-header>
  </div>
</template>

<script>
export default {
  methods:{
    Back(){
      this.$router.go(-1)
      this.$emit('goback')
    }
  }

}
</script>
<style lang="css" scoped>
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
