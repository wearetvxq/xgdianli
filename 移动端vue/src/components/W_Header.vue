<template lang="html">
  <div class="header">
    <mt-header fixed title="中国移动孝感分公司">
       <router-link to="/" slot="left">
          <mt-button icon="back">微信</mt-button>
       </router-link>
       <mt-button slot="right">
             <i class="iconfont icon-people"></i>
       </mt-button>
    </mt-header>
  </div>
</template>

<script>
export default {


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
