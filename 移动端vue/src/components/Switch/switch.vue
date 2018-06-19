<template lang="html">
     <div class="switch">
         <transition name="move">
          <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>动力设备资源清查——开关电源</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                      <span>县市:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.area">
                    </div>
                    <div class="inputlist">
                      <span>基站名称:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.station">
                      <i class="iconfont icon-locate"></i>
                    </div>
                    <div class="inputlist">
                      <span>基站编码:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.number">
                    </div>
                    <div class="inputlist">
                      <span>节点类型:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.node">
                    </div>
                    <div class="inputlist">
                      <span>基本地理位置:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.ground">
                    </div>
                    <div class="inputlist">
                      <span>生产厂家:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.produce">
                    </div>
                    <div class="inputlist">
                      <span>机架型号:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.frame">
                    </div>
                    <div class="inputlist">
                      <span>机架容量(A):</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.cap">
                    </div>
                    <div class="inputlist">
                      <span>开始使用时间:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.starttime">
                    </div>
                    <div class="inputlist">
                      <span>监控模块型号:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.monitoring">
                    </div>
                    <div class="inputlist">
                      <span>整流模块型号:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.rectification">
                    </div>
                    <div class="inputlist">
                      <span>监控模块数量:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.renumber">
                    </div>
                    <div class="inputlist">
                      <span>监控容量:</span>
                      <input type="text" name="" placeholder="请输入" v-model="Data.modulecap">
                    </div>
                    <div class="inputlist">
                      <span>负载电流(A):</span>
                      <input type="text" name="" placeholder="请输入" v-model="Data.loadele">
                    </div>
                    <div class="inputlist">
                      <span>传输及基站是否共用:</span>
                      <select v-model="Data.transmission">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>是否有二次下电功能:</span>
                      <select v-model="Data.powerdown">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>目前运行状态是否正常:</span>
                      <select v-model="Data.ifstatus">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>目前是否属于本地区停电频繁基站:</span>
                      <select v-model="Data.ifpowerdown">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>该站是否配置了固定自启油动机:</span>
                      <select v-model="Data.oil">
                        <option selected = "selected" value="">请选择</option>
                        <option>是</option>
                        <option>否</option>
                      </select>
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
                    <div class="inputlist textarea1">
                      <span>备注:</span>
                      <textarea placeholder="请输入备注" v-model="Data.desc"></textarea>
                    </div>
                    <div class="inputlist">
                      <span>填报人:</span>
                      <input type="text" name="" v-model="Data.people" placeholder="请输入" >
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
              <div class="allmap" id="allmap" v-show="positionIf"></div>

              <div class="content-footer">
                  <Button @skip="switch1"></Button>
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

import Footer from '../Footer.vue'
axios.defaults.baseURL = Footer.rooturl   // 开发环境
// console.log(Footer.name1)
export default {
     data(){
       return{
         name1:Footer.name1,
          mainarea:false,
          selected:null,
          sheetVisible:false,
          options:['12','34','56'],
          actions:[
            {name:'拍照',methods:'photoing'},
            {name:'从相册选择',methods:'selecting'}
          ],
          ammeterImgIf:false,
          positionIf:false,
          tijiao:true,
          code:"",
          name:"",
          bh:"",
          Data:{
            type:"1",
            area:"",
            station:"",
            number:"",
            node:"",
            ground:"",
            produce:"",
            frame:"",
            cap:"",
            starttime:"",
            monitoring:"",
            rectification:"",
            renumber:"",
            modulecap:"",
            loadele:"",

            transmission:"",
            powerdown:"",
            ifstatus:"",
            ifpowerdown:"",
            oil:"",
            desc:"",
            people:"",
            phone:"",
            pic:"",

            dianbiao_id:"",
            person:"",
            phone:"",
          },
          imgUrl:"",
          type: 'tab',
          address_detail: null,
          center: {lng: 116.40387397, lat: 39.91488908}
       }
     },
    created(){
       this.name=localStorage.getItem("name");
      // console.log(Footer.name);
      console.log(this.name1);
     },
     methods:{
       Upload(){
         this.sheetVisible = true
       },
      getPosition(){
        let map = new BMap.Map('allmap');
        let point = new BMap.Point(this.center.lng, this.center.lat);
        this.Data.x_code=point.lng;
        this.Data.y_code=point.lat;
        map.centerAndZoom(point, 10);
        map.enableScrollWheelZoom(true);
        map.enableDoubleClickZoom(true);
        let self = this; 
        let geolocation = new BMap.Geolocation();
        geolocation.getCurrentPosition((r) => {
          let myGeo = new BMap.Geocoder();
          myGeo.getLocation(new BMap.Point(r.point.lng, r.point.lat), function(result){ 
            if (result){
              //根据当前位置经纬度解析成地址
              // let gc = new BMap.Geocoder();
              // let pt = new BMap.Point(r.point.lng, r.point.lat);
              // let lngLat=r.point.lng+","+r.point.lat;
              axios.get("code",{
                  params:{
                    // x_code: self.Data.x_code,
                    // y_code: self.Data.y_code,
                    //测试数据////////////////////////////////////////////////////////////////
                    x_code: '120.25155029369263',
                    y_code: '30.16567767483513',
                    code:self.code,
                    name: self.name,
                    bh:self.bh,
                  }
              }).then(res=>{
                if(res.data.code==10003){
                  Toast({
                    message: res.data.code.msg,
                    duration:1000,
                  });
                  this.$router.go(-1);
                }else if(res.data.code==-1){
                  Toast({
                    message: '数据获取失败',
                    duration:1000,
                  });
                  this.$router.go(-1)
                }else if(res.data.code==0){
                  self.Data.area=res.data.area;
                  self.Data.station=res.data.station;
                  self.Data.number=res.data.number;
                  self.Data.ground=res.data.address;
                  self.Data.dianbiao_id=res.data.dianbiao_id;
                };
              })
            }
          },{ enableHighAccuracy: true });
        })
      },
      switch1(){
          let formData = new FormData();
          formData.append("type",this.Data.type);
          formData.append("area",this.Data.area);
          formData.append("station",this.Data.station);
          formData.append("number",this.Data.number);
          formData.append("node",this.Data.node);
          formData.append("ground",this.Data.ground);
          formData.append("produce",this.Data.produce);
          formData.append("frame",this.Data.frame);
          formData.append("cap",this.Data.cap);
          formData.append("starttime",this.Data.starttime);
          formData.append("monitoring",this.Data.monitoring);
          formData.append("rectification",this.Data.rectification);
          formData.append("renumber",this.Data.renumber);
          formData.append("modulecap",this.Data.modulecap);
          formData.append("loadele",this.Data.loadele);
          formData.append("transmission",this.Data.transmission);
          formData.append("powerdown",this.Data.powerdown);
          formData.append("ifstatus",this.Data.ifstatus);
          formData.append("ifpowerdown",this.Data.ifpowerdown);
          formData.append("oil",this.Data.oil);
          formData.append("desc",this.Data.desc);
          formData.append("people",this.Data.people);
          formData.append("phone",this.Data.phone);
          formData.append("pic",this.Data.pic);
          formData.append("dianbiao_id",this.Data.dianbiao_id);
          let config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          };
          if(
            this.Data.type&&
            this.Data.area&&
            this.Data.station&&
            this.Data.number&&
            this.Data.node&&
            this.Data.ground&&
            this.Data.produce&&
            this.Data.frame&&
            this.Data.cap&&
            this.Data.starttime&&
            this.Data.monitoring&&
            this.Data.rectification&&
            this.Data.renumber&&
            this.Data.modulecap&&
            this.Data.loadele&&
            this.Data.transmission&&
            this.Data.powerdown&&
            this.Data.ifstatus&&
            this.Data.ifpowerdown&&
            this.Data.oil&&
            this.Data.desc&&
            this.Data.people&&
            this.Data.phone&&
            this.Data.pic
            ){
              axios.post("equipment",formData,config).then(res=>{
                if(res.data.code==-1){
                  Toast({
                    message: '数据提交失败',
                    duration:1000,
                  });
                }else if(res.data.code==0){
                  Toast({
                    message: '数据提交成功',
                    duration:1000,
                  });
                  this.$router.go(0)
                };
              })
            }else {
                Toast({
                  message: '请完善信息',
                  duration:1000,
                });
            }
       },
      
       getImg (e) {
        let file = e.target.files[0];
        let formData = new FormData();
        formData.append("files",file);
        let config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        };
        let that=this;
        axios.post("upload",formData,config).then(res=>{
          if(res.data.code==-1){
            Toast({
              message: '图片上传失败',
              duration:500,
            });
          }else if(res.data.code==0){
            that.imgUrl="http://"+res.data.url;
            console.log(that.imgUrl);
            that.Data.pic=that.imgUrl;
            that.ammeterImgIf=true;
          };
        })
      },
      getImgAgain(){
          // this.ammeterImgIf=false;
          this.getImg();
      },
     },
     mounted(){
        this.mainarea = true;
        this.getPosition();
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
                font-size: 8px;
                position: absolute;
                right: -35px;
                top:10px;
                color: #b5b5b5;

              }
              .icon-down{
                font-size: 8px;
                position: absolute;
                top:15px;
                right: -35px;
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
             .ammeterImg{
                  width:60px;
                  height:60px;
              }
             .picture{
                width: 60px;
                height: 60px;
                background-color: #ececec;
                .getImg{
                    opacity:0;
                }
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
