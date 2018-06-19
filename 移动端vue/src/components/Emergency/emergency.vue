<template lang="html">
     <div class="switch">
          <transition name="move">
             <div class="content" v-show="mainarea">
              <div class="content-header">
                  <h5>动力设备资源清查——应急油机</h5>
              </div>
              <div class="content-wrapper">
                    <div class="inputlist">
                        <span>县市分公司:</span>
                        <select v-model="Data.area">
                          <option selected = "selected" value="">请选择</option>
                          <option>汉川</option>
                          <option>孝感</option>
                          <option>安陆</option>
                        </select>
                    </div>
                    <div class="inputlist">
                      <span>厂家:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.name">
                    </div>
                    <div class="inputlist">
                      <span>品牌:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.ping">
                    </div>
                    <div class="inputlist">
                      <span>型号:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.number">
                    </div>
                    <div class="inputlist">
                      <span>功率(KW):</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.gong">
                    </div>
                    <div class="inputlist">
                      <span>数量:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.cap">
                    </div>
                    <div class="inputlist">
                      <span>存放地点:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.dress">
                    </div>
                    <div class="inputlist">
                      <span>开始使用时间:</span>
                      <input type="text" name="" value="" placeholder="请输入" v-model="Data.c">
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
                  <Button @skip="emergency"></Button>
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
          mainarea:false,
          selected:null,
          person:null,
          phone:null,
          sheetVisible:false,
          ammeterImgIf:false,
          positionIf:false,
          tijiao:true,
          imgUrl:"",
          options:['12','34','56'],
          actions:[
            {name:'拍照',methods:'photoing'},
            {name:'从相册选择',methods:'selecting'}
          ],
          Data:{
            area:"",
            name:"",
            ping:"",
            number:"",
            gong:"",
            cap:"",
            dress:"",
            c:"",
            desc:"",
            pic:"",
            person:"",
            phone:"",
            x_code:"",
            y_code:"",
            dianbiao_id:"",
          },
       }
     },
     methods:{
       Upload(){
         this.sheetVisible = true
       },
         //  定位
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
                    x_code: '120.25155029369263',
                    y_code: '30.16567767483513',
                    code: self.code,
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
                  self.station=res.data.station;
                  self.last=res.data.last;
                  self.dianbiao_id=res.data.dianbiao_id;
                };
              })
              
            }
          },{ enableHighAccuracy: true });
        })
       },
      //  提交
       emergency(){
          let formData = new FormData();
          formData.append("area",this.Data.area);
          formData.append("name",this.Data.name);
          formData.append("ping",this.Data.ping);
          formData.append("number",this.Data.number);
          formData.append("gong",this.Data.gong);
          formData.append("cap",this.Data.cap);
          formData.append("dress",this.Data.dress);
          formData.append("c",this.Data.c);
          formData.append("desc",this.Data.desc);
          formData.append("pic",this.Data.pic);
          // 测试数据
          // formData.append("x_code",this.Data.x_code);
          // formData.append("y_code",this.Data.y_code);
          formData.append("x_code",'120.25155029369263');
          formData.append("y_code",'30.16567767483513');
          formData.append("dianbiao_id",this.Data.dianbiao_id);
          console.log(this.Data.area);
          let config = {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
          };
          if(this.Data.area&&this.Data.name&&this.Data.ping&&this.Data.number&&this.Data.gong&&
          this.Data.cap&&this.Data.dress&&this.Data.c&&this.Data.desc&&this.Data.pic&&
            this.Data.person&&this.Data.phone&&this.Data.dianbiao_id){
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
      // 上传图片
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
      },
      getImgAgain(){
          // this.ammeterImgIf=false;
          this.getImg();
      },
     
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
