<template lang="html">
     <div class="switch">
         <transition name="move">
            <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>填写表格——基站专业清理</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                      <span>基站名称:</span>
                      <input type="text" name=""   placeholder="点击定位获取基站名称" readonly="readonly" v-model="Data.station">
                      <i class="iconfont icon-locate" @click="getPosition"></i>
                    </div>
                    <div class="inputlist">
                      <span>基站编码:</span>
                      <input type="text" name=""   placeholder="点击定位获取编码" readonly="readonly" v-model="Data.number">
                    </div>
                    <div class="inputlist">
                      <span>综资名称:</span>
                      <input type="text" name=""   placeholder="点击定位获取综资名称" readonly="readonly" v-model="Data.synergy">
                      <i class="iconfont icon-locate" @click="getPosition"></i>
                    </div>
                    <div class="inputlist">
                      <span>基站详细地址:</span>
                      <input type="text" name=""   placeholder="点击定位获取详细地址" readonly="readonly" v-model="Data.address">
                      <i class="iconfont icon-locate" @click="getPosition"></i>
                    </div>
                    <div class="inputlist">
                      <span>维护级别:</span>
                      <select class="" name="" v-model="Data.rank" >
                         <option selected = "selected"  value="">请选择</option>
                         <option>普通</option>
                         <option>高等级</option>
                      </select>
                    </div>
                    <div class="inputlist">
                      <span>机房类型:</span>
                      <select class="" name="" v-model="Data.jifang">
                         <option selected = "selected"  value="" >请选择</option>
                         <option>一体化</option>
                         <option>自建机房</option>
                         <option>租赁机房</option>
                      </select>

                    </div>
                    <div class="inputlist">
                      <span>铁塔类型:</span>
                      <select class="" name="" v-model="Data.tieta">
                         <option selected = "selected"    value="">请选择</option>
                         <option>美化天线</option>
                         <option>四角塔</option>
                         <option>三角塔</option>
                         <option>拉线塔</option>
                         <option>楼面抱杆</option>
                         <option>路灯杆</option>
                      </select>

                    </div>
                    <div class="inputlist">
                      <span>基站类型:</span>
                      <select class="" name="" v-model="Data.jizhan" >
                         <option selected = "selected"  value="">请选择</option>
                         <option>2G+4G</option>
                         <option>3G+4G</option>
                         <option>2G+3G+4G</option>
                         <option>2G</option>
                         <option>3G</option>
                         <option>4G</option>
                      </select>

                    </div>
                    <div class="inputlist">
                      <span>铁塔高度:</span>
                      <input type="text" name="" placeholder="请输入" v-model="Data.height">
                    </div>
                    <div class="inputlist">
                      <span>是否移交:</span>
                      <select class="" name="" v-model="Data.transfer" >
                         <option selected = "selected" value="">请选择</option>
                         <option>全部移交</option>
                         <option>机房移交</option>
                         <option>铁塔移交</option>
                      </select>

                    </div>
                    <div class="inputlist">
                      <span>共享家数:</span>
                      <select class="" name="" v-model="Data.shared" >
                         <option selected = "selected"  value="">请选择</option>
                         <option>电信</option>
                         <option>联通</option>
                         <option>电信+联通</option>
                      </select>

                    </div>
                    <div class="inputlist textarea">
                      <span>拍摄照片:</span>
                      <img class="ammeterImg" :src="imgUrl" v-if="ammeterImgIf"/>
                      <div class="picture" v-else >
                          <i class="iconfont icon-paizhao" v-model="Data.pic"></i>
                          <input class="getImg" accept="image/*" type="file" @change="getImg"/>
                      </div>
                      <p class="uploadphoto">拍照上传照片</p>
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
                <Button @skip="clean"></Button>
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
axios.defaults.baseURL = "http://192.168.188.178:91/xiaogan/phone/"   // 开发环境

export default {
     data(){
       return{
          mainarea:false,
          selected:null,
          person:null,
          phone:null,
          sheetVisible:false,
          ammeterImgIf:false,
          positionIf:false,
          options:['12','34','56'],
          name:"",
          Data:{
            station:"",
            number:"",
            synergy:"",
            address:"",
            rank:"",         //selected
            jifang:"",       //selected
            tieta:"",        //selected
            jizhan:"",       //selected
            height:"",
            transfer:"",     //selected
            shared:"",       //selected
            pic:'',
          },
          // station:"",
          // number:"",
          // synergy:"",
          // address:"",
          // rank:"",         //selected
          // jifang:"",       //selected
          // tieta:"",        //selected
          // jizhan:"",       //selected
          // height:"",
          // transfer:"",     //selected
          // shared:"",       //selected
          // pic:'',
          // selected:'',
          actions:[
            {name:'拍照',methods:'photoing'},
            {name:'从相册选择',methods:'selecting'}
          ],
          type: 'tab',
          address_detail: null,
          center: {lng: 116.40387397, lat: 39.91488908}
       }
     },
     created(){
       this.name=this.$route.query.name;
     },
     methods:{
       Upload(){
         this.sheetVisible = true
       },
      //  定位
       getPosition(){
        let map = new BMap.Map('allmap');
        let point = new BMap.Point(this.center.lng, this.center.lat)
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
                    // x_code: lngLat.lng,
                    // y_code: lngLat.lat,
                    x_code: '120.25155029369263',
                    y_code: '30.16567767483513', 
                    name: self.name,
                    code:"",
                    bh:"",
                 }   
              }).then(res=>{
                if(res.data.code==-1){
                  Toast({
                    message: '基站获取失败',
                    duration:500,
                  });
                }else if(res.data.code==0){
                  self.Data.station=res.data.station;
                  self.Data.number=res.data.number;
                  self.Data.synergy=res.data.address2;
                  self.Data.address=res.data.address;
                  self.Data.dianbiao_id=res.data.dianbiao_id;
                };
              })
              let dress = gc.getLocation(pt, function(rs){
                let addComp = rs.addressComponents;
                // self.Data.synergy=addComp.province+addComp.district+addComp.city+addComp.street+addComp.streetNumber
                // self.Data.address=addComp.province+addComp.district+addComp.city+addComp.street+addComp.streetNumber
              })
            }
          },{ enableHighAccuracy: true });
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
        clean(){
          let formData = new FormData();
          formData.append("station",this.Data.station);
          formData.append("number",this.Data.number);
          formData.append("synergy",this.Data.synergy);
          formData.append("address",this.Data.address);
          formData.append("rank",this.Data.rank);
          formData.append("jifang",this.Data.jifang);
          formData.append("tieta",this.Data.tieta);
          formData.append("jizhan",this.Data.jizhan);
          formData.append("height",this.Data.height);
          formData.append("transfer",this.Data.transfer);
          formData.append("shared",this.Data.shared);
          formData.append("pic",this.Data.pic);
          // formData.append("dianbiao_id",this.Data.dianbiao_id);
          let config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          };
          if(this.Data.station&&this.Data.number&&this.Data.synergy&&this.Data.address&&this.Data.rank&&this.Data.jifang&&this.Data.tieta&&
          this.Data.jizhan&&this.Data.height&&this.Data.transfer&&this.Data.shared&&this.Data.pic){
            axios.post("clean",formData,config).then(res=>{
              if(res.data.code==-1){
                Toast({
                  message: '数据提交失败',
                  duration:500,
                });
              }else if(res.data.code==0){
                Toast({
                  message: '数据提交成功',
                  duration:500,
                });
                this.$router.go(0)
              };
            })
          }else {
              Toast({
                message: '请完善信息',
                duration:500,
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
              that.Data.pic=that.imgUrl;
              that.ammeterImgIf=true;
            };
          })
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
          top:100px;
          margin:0 auto;
         }
         .content-footer{
           margin: 20px 0;
         }
       }
     }
</style>
