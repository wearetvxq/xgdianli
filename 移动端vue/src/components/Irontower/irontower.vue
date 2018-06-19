<template lang="html">
     <div class="switch">
         <transition :name="slidename">
            <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>铁塔</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                        <span>县市:</span>
                        <select  v-model="Data.area">
                          <option selected = "selected" value="">请选择</option>
                          <option>孝南区</option>
                          <option>汉川</option>
                          <option>孝感</option>
                          <option>安陆</option>
                          <option>云梦</option>
                        </select>
                    </div>
                    <div class="inputlist">
                      <span>基站名称:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.name">
                      <i class="iconfont icon-locate"></i>
                    </div>
                    <div class="inputlist">
                      <span>详细地点:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.address">
                    </div>
                    <div class="inputlist">
                      <span>铁塔公司站址编码:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.code">
                    </div>
                    <div class="inputlist">
                      <span>基站类型:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.type">
                    </div>
                    <div class="inputlist">
                      <span>电费是否有铁塔公司支付:</span>
                      <select  v-model="Data.money">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>铁塔类别:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.tower">
                    </div>
                    <div class="inputlist">
                      <span>铁塔高度(m):</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.height">
                    </div>
                    <div class="inputlist">
                      <span>机房类型:</span>
                      <select class="" name="" v-model="Data.type2">
                        <option selected = "selected"  value="">请选择</option>
                        <option>自建机房</option>
                        <option>租赁机房</option>
                        <option>RRU拉远</option>
                        <option>无机房</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>移交类型:</span>
                      <select class="" name=""  v-model="Data.type3">
                        <option selected = "selected"  value="">请选择</option>
                        <option>已移交</option>
                        <option>移交塔</option>
                        <option>移交机房</option>
                        <option>新建</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>是否共享:</span>
                      <select  v-model="Data.shore">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>铁塔共享用户数:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.users">
                    </div>
                    <div class="inputlist">
                      <span>铁塔共享清单:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.list">
                    </div>
                    <div class="inputlist">
                      <span>RRU是否安装在铁塔上:</span>
                      <select  v-model="Data.anzhuang">
                        <option selected = "selected"  value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>天线数量:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.tian">
                    </div>
                    <div class="inputlist textarea">
                      <span>拍摄照片:</span>
                      <img class="ammeterImg" :src="imgUrl" v-if="ammeterImgIf"/>
                      <div class="picture" v-else>
                          <i class="iconfont icon-paizhao"  v-model="Data.pic">
                            <input class="getImg" accept="image/*" type="file" @change="getImg"/>
                          </i>
                      </div>
                      <p class="uploadphoto" @click="getImgAgain">拍照上传照片</p>
                    </div>
                    <div class="inputlist">
                      <span>填报人:</span>
                      <input type="text" name="" v-model="Data.person" placeholder="请输入" >
                    </div>
                    <div class="inputlist">
                      <span>联系电话:</span>
                      <input type="text" name="" v-model="Data.phone" placeholder="请输入">
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
import { Toast } from 'mint-ui';
import axios from 'axios';
import BMap from 'BMap';
axios.defaults.baseURL = "http://192.168.188.178:91/xiaogan/equipment/"   // 开发环境

export default {
     data(){
       return{
          slidename:'slide-go',
          mainarea:false,
          selected:null,
          person:null,
          phone:null,
          sheetVisible:false,
          options:['12','34','56'],
          actions:[
            {name:'拍照',methods:'photoing'},
            {name:'从相册选择',methods:'selecting'}
          ],
          Data:{
            area:"",
            name:"",
            address:"",
            code:"",
            type:"",
            money:"",
            tower:"",
            height:"",
            type2:"",
            typ3:"",
            shore:"",
            users:"",
            list:"",
            anzhuang:"",
            tian:"",
            pic:'',
            dianbiao_id:"",
          },
       }
     },
     methods:{
       Upload(){
         this.sheetVisible = true
       },
       handleBack(){
         this.slidename = 'slide-back'
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
