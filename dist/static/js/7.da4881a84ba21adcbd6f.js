webpackJsonp([7],{Oeoe:function(t,e){},ogzq:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s("teIl"),i=s("qkow"),n={data:function(){return{mainarea:!1,selected:null,person:null,phone:null,sheetVisible:!1,options:["12","34","56"],actions:[{name:"拍照",methods:"photoing"},{name:"从相册选择",methods:"selecting"}]}},mounted:function(){this.mainarea=!0},methods:{Upload:function(){this.sheetVisible=!0}},components:{Header:a.a,Button:i.a}},v={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"switch"},[s("transition",{attrs:{name:"move"}},[s("div",{directives:[{name:"show",rawName:"v-show",value:t.mainarea,expression:"mainarea"}],staticClass:"content"},[s("div",{staticClass:"content-header"},[s("h5",[t._v("动力设备资源清查——开关电源")])]),t._v(" "),s("div",{staticClass:"content-wrapper"},[s("div",{staticClass:"inputlist"},[s("span",[t._v("县市分公司:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("汉川")]),t._v(" "),s("option",[t._v("孝感")]),t._v(" "),s("option",[t._v("安陆")])])]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("基站名称:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}}),t._v(" "),s("i",{staticClass:"iconfont icon-locate"})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("基站编码:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("节点类型:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("基本地理位置:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("汉川")]),t._v(" "),s("option",[t._v("城区")]),t._v(" "),s("option",[t._v("乡镇")])])]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("生产厂家:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("机架型号:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("机架容量(A):")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("开始使用时间:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("监控模块型号:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("整流模块型号:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("监控模块数量:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",value:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("监控容量:")]),t._v(" "),s("input",{attrs:{type:"text",name:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("负载电流(A):")]),t._v(" "),s("input",{attrs:{type:"text",name:"",placeholder:"请输入"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("传输及基站是否共用:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("是")]),t._v(" "),s("option",[t._v("否")])])]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("是否有二次下电功能:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("是")]),t._v(" "),s("option",[t._v("否")])])]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("目前是否属于本地区停电频繁基站:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("是")]),t._v(" "),s("option",[t._v("否")])])]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("该站是否配置了固定自启油动机:")]),t._v(" "),s("select",[s("option",{attrs:{selected:"selected",value:""}},[t._v("请选择")]),t._v(" "),s("option",[t._v("是")]),t._v(" "),s("option",[t._v("否")])])]),t._v(" "),s("div",{staticClass:"inputlist textarea"},[s("span",[t._v("拍摄照片:")]),t._v(" "),s("div",{staticClass:"picture"},[s("i",{staticClass:"iconfont icon-paizhao",on:{click:t.Upload}})]),t._v(" "),s("p",{staticClass:"uploadphoto"},[t._v("拍照上传照片")])]),t._v(" "),s("div",{staticClass:"inputlist textarea1"},[s("span",[t._v("备注:")]),t._v(" "),s("textarea",{attrs:{placeholder:"请输入备注"}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("填报人:")]),t._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.person,expression:"person"}],attrs:{type:"text",name:"",placeholder:"请输入"},domProps:{value:t.person},on:{input:function(e){e.target.composing||(t.person=e.target.value)}}})]),t._v(" "),s("div",{staticClass:"inputlist"},[s("span",[t._v("联系电话:")]),t._v(" "),s("input",{directives:[{name:"model",rawName:"v-model",value:t.phone,expression:"phone"}],attrs:{type:"text",name:"",placeholder:"请输入"},domProps:{value:t.phone},on:{input:function(e){e.target.composing||(t.phone=e.target.value)}}})])]),t._v(" "),s("mt-actionsheet",{attrs:{actions:t.actions},model:{value:t.sheetVisible,callback:function(e){t.sheetVisible=e},expression:"sheetVisible"}}),t._v(" "),s("div",{staticClass:"content-footer"},[s("Button")],1)],1)])],1)},staticRenderFns:[]};var l=s("vSla")(n,v,!1,function(t){s("Oeoe")},"data-v-a8f3b182",null);e.default=l.exports}});
//# sourceMappingURL=7.da4881a84ba21adcbd6f.js.map