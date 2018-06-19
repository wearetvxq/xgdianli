<template lang="html">
     <div class="home">
        <div class="headline">
            <p>星期三 上午 10:00</p>
        </div>
        <div class="info">
            <div class="wrapper">
                <div class="top">
                  <img src="../../assets/images/bg.jpg" alt="">
                  <p class="welcome">嗨,欢迎关注! 点击领取新人礼</p>
                </div>
                <div class="bottom">
                   <p>欢迎来到中国移动</p>
                   <img src="../../assets/images/logo.png" alt="">
                </div>
            </div>
        </div>
        <div class="footer">
            <WFooter></WFooter>
        </div>
     </div>

</template>

<script>
import WHeader from '../W_Header.vue'
import WFooter from '../Footer.vue'
export default {
   data(){
     return{

     }
   },
   components:{
     WHeader,
     WFooter
   }

}
</script>
<style lang="scss" scoped>
    .home{
      .headline{
        display: flex;
        background-color: #cecece;
        width: 128px;
        height: 18px;
        position: absolute;
        left: 28%;
        top:100px;
        display: flex;
        border-radius:5px;
        line-height: 18px;
        p{
          color: #fff;
          font-size: 12px;
          font-weight: 700;
          margin-left: 5px;
        }
      }
      .info{
        width: 90%;
        margin: 0 15px;

        .wrapper{
          height: 192px;
          background-color: #fff;
          border-radius: 3px;
          margin: 0 auto;
          margin-top: 142px;
          .top{
               .welcome{
                 color:#fff;
                 font-size: 14px;
                 font-weight: 700;
                 position: absolute;
                 top:265px;
                 left: 20px;
               }
               img{
                 width: 100%;
                 height: 154px;
               }
          }
          .bottom{
            display: flex;
            justify-content: space-between;
            p{
              color: #000;
              margin-top: 10px;
              margin-left: 5px;
              font-size: 12px;
            }
            img{
              margin-right:5px;
              width: 70px;
              height: 34px;
            }
          }
        }
      }
    }




</style>
