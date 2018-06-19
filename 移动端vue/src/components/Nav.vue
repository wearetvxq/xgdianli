<template lang="html">
     <div class="nav">
        <div class="container">
            <ul>
               <li class="line">
                  <div class="navlist">
                    <router-link to="/power">
                       <img src="../assets/images/switch.png">
                       <p>开关电源</p>
                    </router-link>
                  </div>
               </li>
               <li class="line">
                  <div class="navlist">
                    <router-link to="/battery">
                      <img src="../assets/images/batterry.png">
                      <p>蓄电池</p>
                    </router-link>
                  </div>
               </li>
               <li class="line1">
                  <div class="navlist">
                    <router-link to="/aircondition">
                        <img src="../assets/images/aircondition.png">
                        <p>空调</p>
                    </router-link>
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">
                    <router-link to="/electric">
                       <img src="../assets/images/box.png">
                       <p>交流配电箱</p>
                    </router-link>
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">
                    <router-link to="/station">
                       <img src="../assets/images/station.png">
                       <p>拉远站(交换值)</p>
                    </router-link>
                  </div>
               </li>
               <li class="line3">
                  <div class="navlist">
                     <router-link to="/steady">
                         <img src="../assets/images/system.png">
                         <p>直流远供局端</p>
                     </router-link>
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">
                    <router-link to="/cabinet">
                       <img src="../assets/images/cabinet.png">
                       <p>一体化机柜</p>
                    </router-link>
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">
                    <router-link to="/transformmer">
                       <img src="../assets/images/transformer.png">
                       <p>变压器</p>
                    </router-link >
                  </div>
               </li>
               <li class="line3">
                  <div class="navlist">
                    <router-link to="/emergency">
                       <img src="../assets/images/gearbox.png">
                       <p>应急油机</p>
                    </router-link >
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">
                    <router-link to="/tower">
                       <img src="../assets/images/tower.png">
                       <p>铁塔</p>
                    </router-link >
                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">

                  </div>
               </li>
               <li class="line2">
                  <div class="navlist">

                  </div>
               </li>
            </ul>
        </div>
     </div>
</template>

<script>
export default {


}
</script>

<style lang="scss" scoped>
      .nav{
        margin-top: 11px;
        background-color: #ffffff;
         .container{
           ul{
             width: 100%;
             display: flex;
             flex-flow: row wrap;
             li{
                 box-sizing: border-box;
                 width: 33.3%;
                 height: 100px;
                 color:#555555;
                 .navlist{
                      padding-top: 20px;
                      text-align: center;
                      img{
                        width: 28px;
                        height: 28px;
                      }
                      p{
                        padding-top: 9px;
                        font-size: 12px;
                      }
                 }
             }
             .line{
               border-top:0.5px solid #e8e6e8;
               border-bottom:0.5px solid #e8e6e8;
               border-right:0.5px solid #e8e6e8;
             }
             .line1{
               border-top:0.5px solid #e8e6e8;
               border-bottom:0.5px solid #e8e6e8;
             }
             .line2{
               border-bottom:0.5px solid #e8e6e8;
               border-right:0.5px solid #e8e6e8;
             }
             .line3{
               border-bottom:0.5px solid #e8e6e8;
             }
           }
         }
      }

</style>
