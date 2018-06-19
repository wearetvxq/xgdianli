<template lang="html">
     <footer>
          <div class="footer-item border">
              <i class="footer-icon iconfont icon-keybord"></i>
          </div>
          <div class="footer-item border">
              <router-link :to="{
                    path:'check',
                    query: {
                        code: code,
                        name: name,
                        bh: bh
                    }
                }">
                <i class="footer-icon iconfont icon-category"></i>
                <span class="footer-title">抄表</span>
              </router-link>
          </div>
          <div class="footer-item border">
              <router-link to="/equipment">
                <i class="footer-icon iconfont icon-category"></i>
                <span class="footer-title">设备资源管理</span>
              </router-link>
          </div>
          <div class="footer-item">
              <router-link :to="{
                    path:'clean',
                    query: {
                        name: name,
                    }
                }">
                <i class="footer-icon iconfont icon-category"></i>
                <span class="footer-title">基站专业清理</span>
              </router-link>
          </div>
     </footer>
</template>
<script>
const name1="火车站艳阳天";
const rooturl="http://192.168.188.178:91/xiaogan/phone/"
export default {
    name1,
    rooturl,
    data () {
        return {
            code:'4000458047',
            name:"火车站艳阳天",
            bh:"0000436386",//电表编号
        }
    },
    created(){
        localStorage.setItem("name", this.name);
    }
}
</script>

<style lang="scss" scoped>
footer {
    width: 100%;
    height: 48px;
    z-index: 10000;
    position: fixed;
    display: flex;
    bottom: 0;
    left: 0;
    background-color: #f5f5f7;
    box-shadow: 0 -2px 9px rgba(0, 0, 0, .1);

    .footer-item {
        align-items: flex-end;
        justify-content: center;
        flex: 1 1 auto;
        text-align: center;

        & a {
            text-decoration: none;
            line-height: 40px;
        }

        .footer-title {
            font-size: 12px;
            margin-top: -1px;
            color:#4a4a4a;
        }
        .icon-keybord{
          position: relative;
          top:10px;
        }
        .icon-category{
          position: relative;
          top:2px;
        }
        .footer-icon{
          font-size: 20px;
          margin-top: 10px;
        }

    }
    .border{
      border-right: 1px solid #e9e9ea;
    }
}
</style>
