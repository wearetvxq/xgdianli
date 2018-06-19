<template lang="html">
     <div class="button">
         <p @click="send">点击提交</p>
     </div>
</template>

<script>
export default {
  props:['buttonName'],
  data() {
      return {
      }
  },
  methods: {
    send() {
      this.$emit('skip');
    }
  }
}
</script>

<style lang="scss" scoped>
    .button{
      font-size: 14px;
      font-weight: 400;
      color:#ffffff;
      text-align: center;
      background: #8ed959;
      width: 80%;
      margin:0 auto;
      box-sizing: border-box;
      padding:0 12px;
      height: 35px;
      line-height: 35px;
      margin-top: 15px;
      border-radius:5px;
    }

</style>
