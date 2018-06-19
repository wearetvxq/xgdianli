<template lang="html">
     <div class="switch">
         <transition name="move">
           <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>动力设备资源清查——变压器</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                        <span>县市分公司:</span>
                        <select value="" placeholder="请选择" >
                          <option>汉川</option>
                          <option>孝感</option>
                          <option>安陆</option>
                        </select>
                    </div>
                    <div class="inputlist">
                      <span>地点:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                      <i class="iconfont icon-locate"></i>
                    </div>
                    <div class="inputlist">
                      <span>厂家:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>品牌:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>型号:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>功率(KVA):</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>数量:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>开始使用时间:</span>
                      <input type="text" name="" value="" placeholder="请输入">
                    </div>

                    <div class="inputlist textarea">
                      <span>拍摄照片:</span>
                      <div class="picture">
                          <i class="iconfont icon-paizhao" @click="Upload"></i>
                      </div>
                      <p class="uploadphoto">拍照上传照片</p>
                    </div>
                    <div class="inputlist textarea1">
                      <span>备注:</span>
                      <textarea placeholder="请输入备注"></textarea>
                    </div>
                    <div class="inputlist">
                      <span>填报人:</span>
                      <input type="text" name="" v-model="person" placeholder="请输入">
                    </div>
                    <div class="inputlist">
                      <span>联系电话:</span>
                      <input type="text" name="" v-model="phone" placeholder="请输入">
                    </div>
              </div>
              <mt-actionsheet
                :actions="actions"
                v-model="sheetVisible">
              </mt-actionsheet>
              <div class="content-footer">
                  <Button></Button>
              </div>
         </div>
         </transition>
     </div>
</template>

<script>
import Header from '../Header.vue'
import Button from '../Button.vue'

export default {
     data(){
       return{
          mainarea:false,
          selected:null,
          person:null,
          phone:null,
          sheetVisible:false,
          options:['12','34','56'],
          actions:[
            {name:'拍照',methods:'photoing'},
            {name:'从相册选择',methods:'selecting'}
          ]
       }
     },
     methods:{
       Upload(){
         this.sheetVisible = true
       }
     },
     mounted(){
       this.mainarea = true
     },
     components:{
         Header,
         Button
     }

}
</script>

<style lang="scss" scoped>
     .switch{
         margin-top: -30px;
       .content{
         padding-left: 10px;
         padding-right: 10px;
         &.move-enter-active,
         &.move-leave-active {
             transition: all 0.2s;
             opacity: 0.8;
         }
         &.move-enter,
         &.move-leave-active {
             transition: all 0.2s;
             transform: translate3d(100%, 0, 0);
             opacity: 0.8;
         }
         .content-header{
           display: flex;
           h5{
             color:#101010;
             font-weight: 700;
             font-size: 14px;
             margin-top: -10px;

           }
         }
         .content-wrapper{
           margin-top: 12px;
           .inputlist{
             position: relative;
              display: flex;
              align-items: center;
              margin: 3px 0;
              height: 46px;
              background-color: #fff;
              border-radius:2px;
              .icon-locate{
                font-size: 16px;
                position: absolute;
                right: 12px;
                color: #b5b5b5;
              }
              .icon-up{
                font-size: 3px;
                position: absolute;
                right: 12px;
                top:14px;
                color: #b5b5b5;

              }
              .icon-down{
                font-size: 3px;
                position: absolute;
                top:22px;
                right: 12px;
                color: #b5b5b5;
              }
              select{
                width: 70%;
                height: 24px;
                outline: none;
                border-radius: 5px;
                margin-left: 5px;
                padding-left: 5px;
                font-size: 12px;
                margin-right: 8px;
                border:1px solid #f1f1f1;

                background-color:transparent;




              }
              input{
                width: 70%;
                height: 24px;
                outline: none;
                border:1px solid #f1f1f1;
                border-radius: 5px;
                margin-left: 5px;
                padding-left: 5px;
                font-size: 12px;
                margin-right: 8px;

                text-indent: 0;
                background: transparent;

                resize:none;

                -webkit-appearance:none;  /*清除浏览器默认的样式 */
                line-height: normal;   //光标问题





              }
              span{
                width: 25%;
                color: #6b6b6b;
                margin-left: 5px;
                margin-right: 10px;
                padding-top: 8px;
                font-size: 12px;
                font-weight: 400;
                white-space:pre-wrap;
                word-wrap : break-word ;
                overflow: hidden ;
              }
           }
           .textarea{
             display: flex;
             justify-content: flex-start;
             height: 90px;
             .picture{
                width: 60px;
                height: 60px;
                background-color: #ececec;
                .icon-paizhao:before{
                  position: relative;
                  top:20px;
                }
             }
             .uploadphoto{
               font-size: 12px;
               margin-left: 10px;
               margin-top: 40px;
               color: #c5c5c5;
             }
             span{
               margin-top:-30px;
             }
           }
           .textarea1{
             display: flex;
             height: 68px;
             textarea{
               border:1px solid #f1f1f1;
               margin-right: 12px;
               width: 70%;
               height: 40px;
               outline: none;
             }
           }
         }
         .content-footer{
           margin: 20px 0;
         }
       }
     }
</style>
