<template lang="html">
     <div class="switch">
         <transition name="move">
           <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>基站抄表</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                      <span>基站名称:</span>
                      <input type="text" name=""  placeholder="点击定位获取名称" readonly="readonly"  v-model="Data.station" >
                      <i class="iconfont icon-locate" @click="getPosition"></i>
                    </div>
                    <div class="inputlist">
                      <span>上月日均耗电量:</span>
                      <input type="text" name=""  placeholder="点击定位获取上月日均耗电量"  readonly="readonly" v-model="Data.last">
                    </div>
                    <div class="inputlist">
                      <span>电表示数:</span>
                      <input type="text" name="" placeholder="请输入" v-model="Data.meter">
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
                      <span>本月日均耗电量:</span>
                      <input type="text" name="" placeholder="请输入(默认单位 kwh)" v-model="Data.now" @input="countProportion">
                    </div>
                    <div class="inputlist">
                      <span>上月/本月日耗电比:</span>
                      <input type="text" name=""  placeholder="上月/本月日耗电比" readonly="readonly" v-model="Data.percentage">
                    </div>
                    <div class="inputlist textarea1">
                      <span>清查原因:</span>
                      <textarea placeholder="请输入备注" v-model="Data.reason"></textarea >
                    </div>
              </div>
              <mt-actionsheet
                :actions="actions"
                v-model="sheetVisible">
              </mt-actionsheet>
              <!--百度地图-->
              <!--<Map class="allmap" id="allmap" v-show="positionIf"></Map>-->
              <div class="allmap" id="allmap" v-show="positionIf"></div>
              <div class="content-footer">
                  <Button @skip="check" ></Button>
              </div>
         </div>
         </transition>
     </div>
</template>

<script>
import Header from '../Header.vue';
import Button from '../Button.vue';
import { Toast } from 'mint-ui';
import axios from 'axios';
import BMap from 'BMap';
axios.defaults.baseURL = "http://192.168.188.178:91/xiaogan/phone/"   // 开发环境

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
          ],
          
          ammeterImgIf:false,
          positionIf:false,
          tijiao:true,
          code:"",
          name:"",
          bh:"",
          Data:{
            station:"",
            last:"",
            meter:"",
            now:"",
            percentage:"",
            reason:"",
            pic:"",
            x_code:"",
            y_code:"",
            dianbiao_id:"",
          },
          imgUrl:"",
          type: 'tab',
          address_detail: null,
          center: {lng: 116.40387397, lat: 39.91488908}
       }
     },
     created(){
       this.name=this.$route.query.name;
       this.code=this.$route.query.code;
       this.bh=this.$route.query.bh;
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
              let gc = new BMap.Geocoder();
              let pt = new BMap.Point(r.point.lng, r.point.lat);
              let lngLat=r.point.lng+","+r.point.lat;
              axios.get("code",{
                  params:{
                    // x_code: self.Data.x_code,
                    // y_code: self.Data.y_code,
                    //测试数据////////////////////////////////////////////////////////////////
                    x_code: '120.25155029369263',
                    y_code: '30.16567767483513',
                    code:self.code,
                    name: self.name,
                    bh:self.bh
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
                    message: '基站获取失败，请确认周围是否有基站',
                    duration:1000,
                  });
                  this.$router.go(-1)
                }else if(res.data.code==0){
                  self.Data.station=res.data.station;
                  self.Data.last=res.data.last;
                  self.Data.dianbiao_id=res.data.dianbiao_id;
                };
              })
              
            }
          },{ enableHighAccuracy: true });
          // 地图显示
          // if (r.point) {
          //   let markers = new BMap.Marker(r.point);
          //   map.addOverlay(markers)
          //   map.panTo(r.point)
          //   map.centerAndZoom(r.point, 16);
          //   self.positionIf=true;
          //   setTimeout(function(){
          //     self.positionIf=false;
          //   },1000);
          // }
        })
       },
       check(){
          let formData = new FormData();
          formData.append("station",this.Data.station);
          formData.append("last",this.Data.last);
          formData.append("meter",this.Data.meter);
          formData.append("now",this.Data.now);
          formData.append("percentage",this.Data.percentage);
          formData.append("reason",this.Data.reason);
          formData.append("pic",this.Data.pic);
          // formData.append("x_code",this.Data.x_code);
          // formData.append("y_code",this.Data.y_code);
          formData.append("x_code",'120.25155029369263');
          formData.append("y_code",'30.16567767483513');
          formData.append("dianbiao_id",this.Data.dianbiao_id);
          let config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          };
          if(this.Data.reason){
            if(this.Data.station&&this.Data.last&&this.Data.meter&&this.Data.now&&this.Data.percentage&&
            this.Data.pic&&this.Data.x_code&&this.Data.y_code&&this.Data.dianbiao_id){
              axios.post("reading",formData,config).then(res=>{
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
          }else if(this.Data.percentage>0.7){
            Toast({
                  message: '月耗比大于70% 请填写清查原因',
                  duration:1000,
            });
          }else {
            if(this.Data.station&&this.Data.last&&this.Data.meter&&this.Data.now&&this.Data.percentage&&
            this.Data.pic&&this.Data.x_code&&this.Data.y_code&&this.Data.dianbiao_id){
              axios.post("reading",formData,config).then(res=>{
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
      // 计算耗电比
      countProportion(){
        if(this.Data.last&&this.Data.now){
          this.Data.percentage=this.Data.last/this.Data.now;
        }else{
          this.Data.percentage=null;
        }
      }
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
        //  地图遮罩层
         .allmap{
            width:90%;
            height: 200px;
            position:absolute;
            top:0;
            left:0;
            right:0;
            bottom:0;
            margin:auto;
         }
         .content-footer{
           margin: 20px 0;
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

         }
       }
     }
</style>
