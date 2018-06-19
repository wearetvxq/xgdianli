<template lang="html">
    <div id="allmap"></div>
</template>

<script>
export default {
  props:['mapName'],
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
  //  地图遮罩层
  #allmap{
    width:90%;
    height: 200px;
    position:absolute;
    top:100px;
    margin:0 auto;
  }

</style>
