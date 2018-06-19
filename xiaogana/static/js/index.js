app.controller('indexCtrl', function($scope,$http,$filter,$rootScope) {
    console.log("index")
    var zsurl='http://39.108.165.149:7002'
    // var zsurl='http://192.168.188.178:99'
    //-----------------------权限板块----------------------//
    //地区名
    var cityName;
    //获取url后缀j和参数
    var pathUrl=location.hash;
    //存入cookie
    function setCookie(name,value){
      document.cookie=name+"="+value;
    }
    //获取cookie
    function getCookie(name){  
        var arr=document.cookie.split("; ");
        for(var i=0;i<arr.length;i++){
            var arr2=arr[i].split("=");
            if(arr2[0]==name){
                return arr2[1]; //如果有，就弹出value
            }
        }
        return '';  //如果没有就弹空（''）
    }
    //url进行判断是否带有后缀
    var diQv=['all','安陆','大悟','汉川','孝昌','孝南','应城','云梦'];
    if(pathUrl=="#/index"){
        if(getCookie("userName") == ''){
            alert("参数异常,将返回主系统!");
            window.location="public.html#/index";
        }else{
            cityName=getCookie("userName");
            maxPag();
        }
    }else{
        var pathUrl02=decodeURI(location.hash.split("?")[1].split("=")[1]);
        var verify = new RegExp(pathUrl02);
        if(verify.test(diQv)){
            setCookie("userName",pathUrl02);
            cityName=getCookie("userName");
            maxPag();
        }else{
            layer.msg("参数异常,将返回主系统!");
            window.location="public.html#/index";
        }
    }
    //-----------------------权限板块----------------------//
    function maxPag(){
        //遮罩层
        $(".la_index_mask").show();
        //遮罩层状态值
        var Loading01=0;
        var Loading02=0;
        var Loading03=0;
        function loadType(){
            if(Loading01==1&&Loading02==1&&Loading03==1){
                setTimeout(function(){
                    $(".la_index_mask").hide();
                },500);
            }
        }
        // 导航栏选中
        $(function(){
            $(".optFor a").each(function(){
                var ts_href=new RegExp($(this).attr("href"));
                var local_path=location.hash;
                if(ts_href.test(local_path)){
                  $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                }else if(local_path=="#/"){
                  $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
        });
        // 点击切换小按钮
        //告警量展示
        $scope.tipeShow=function(){
            $http({
                method: 'POST',
                url:zsurl+'/xiaogan/count_warning',
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                Loading03=1;
                $scope.normalSum=response.count_warning[1][1];
                $scope.normalBx=response.count_warning[1][2];
                $scope.emergencySum=response.count_warning[2][1];
                $scope.emergencyBx=response.count_warning[2][2];
                $scope.abnormitySum=response.count_warning[0][1];
                $scope.abnormityBx=response.count_warning[0][2];
                loadType();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.tipeShow();
        //地图预测坐标点(接口)
        $scope.lxMap=function(name){
            //遮罩层
            $(".la_index_mask").show();
            $http({
                method: 'POST',
                url:zsurl+'/xiaogan/get_xy',
                data: $.param({
                        colour: "",
                        sta_no: name,
                        choose_city: cityName
                    }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                //百度离线地图
                var map = new BMap.Map("container02",{minZoom:8,maxZoom:17});      //设置卫星图为底图
                var point = new BMap.Point(113.935725,30.927948);    // 创建点坐标 122.4575, 30.7315
                map.centerAndZoom(point,13);                     // 初始化地图,设置中心点坐标和地图级别。
                map.addControl(new BMap.NavigationControl());
                map.enableScrollWheelZoom();                  // 启用滚轮放大缩小。
                var b = new BMap.Bounds(new BMap.Point(109.00, 30.50),new BMap.Point(120.00, 32.30));
                    try {   
                        BMapLib.AreaRestriction.setBounds(map, b);
                    } catch (e) {
                        alert(e);
                    }
                //大头针点区
                var points =[];
                var lng_latData=response.x_y_colour_1;
                for(var i in lng_latData){
                    points.push([lng_latData[i][0],lng_latData[i][1],lng_latData[i][2],lng_latData[i][3]]);
                }
                var points_le=points.length;
                for(var j=0;j<points_le;j++){
                    if(points[j][2]=="red"){
                        var sizeSum=25*points[j][3]/100;
                        var pt = new BMap.Point(points[j][0], points[j][1]);
                        var myIcon = new BMap.Icon("static/baidu/images/wap.png", new BMap.Size(sizeSum,sizeSum) ,{imageSize : new BMap.Size(sizeSum,sizeSum)});
                        var marker2 = new BMap.Marker(pt,{icon:myIcon});  // 创建标注
                        map.addOverlay(marker2); // 将标注添加到地图中
                        marker2.addEventListener("click",attribute);//添加点击事件
                    }else if(points[j][2]=="yellow"){
                        var sizeSum=30*points[j][3]/100;
                        var pt = new BMap.Point(points[j][0], points[j][1]);
                        var myIcon02 = new BMap.Icon("static/baidu/images/wap2.png", new BMap.Size(sizeSum,sizeSum) ,{imageSize : new BMap.Size(sizeSum,sizeSum)});
                        var marker2 = new BMap.Marker(pt,{icon:myIcon02});  // 创建标注
                        map.addOverlay(marker2); // 将标注添加到地图中
                        marker2.addEventListener("click",attribute);//添加点击事件
                    }else if(points[j][2]=="green"){
                        var sizeSum=30*points[j][3]/100;
                        var pt = new BMap.Point(points[j][0], points[j][1]);
                        var myIcon03 = new BMap.Icon("static/baidu/images/wap3.png", new BMap.Size(sizeSum,sizeSum) ,{imageSize : new BMap.Size(sizeSum,sizeSum)});
                        var marker2 = new BMap.Marker(pt,{icon:myIcon03});  // 创建标注
                        map.addOverlay(marker2); // 将标注添加到地图中
                        marker2.addEventListener("click",attribute);//添加点击事件
                    }
                }
                //滚动时信息框消失
                var domt1=document.getElementById("container02");
                var scrollFunc=function(e){
                    e=e || window.event;
                    $(".message").hide();
                }
                /*注册事件*/
                if(document.addEventListener){
                    domt1.addEventListener('DOMMouseScroll',scrollFunc,false);
                }//W3C
                domt1.onmousewheel=scrollFunc;//IE/Opera/Chrome
                //遮罩层
                Loading01=1;
                if(Loading01==1){
                    loadType();
                }else{
                    $(".la_index_mask").hide();
                }
                function attribute(e){
                    var lng_x=e.target.getPosition().lng;
                    var lat_y=e.target.getPosition().lat;
                    $scope.mapTable(lng_x,lat_y);
                };
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.lxMap("全部");
        //js信息框
        var axis_x=0;
        var axis_y=0;
        $("body").click(function(){
            var e = window.event || arguments.callee.caller.arguments[0]; 
            axis_x=e.clientX+6;
            axis_y=e.clientY-310;
            $(".message").hide();
        });
        //阻止事件冒泡
        function getEvent(){
            if(window.event)    {return window.event;}
              func=getEvent.caller;
              while(func!=null){
                  var arg0=func.arguments[0];
                  if(arg0){
                      if((arg0.constructor==Event || arg0.constructor ==MouseEvent
                          || arg0.constructor==KeyboardEvent)
                          ||(typeof(arg0)=="object" && arg0.preventDefault
                          && arg0.stopPropagation)){
                           return arg0;
                      }
                  }
                  func=func.caller;
            }
            return null;
        }
        function cancelBubble(){
            var e=getEvent();
            if(window.event){
              //e.returnValue=false;//阻止自身行为
              e.cancelBubble=true;//阻止冒泡
            }else if(e.preventDefault){
              //e.preventDefault();//阻止自身行为
              e.stopPropagation();//阻止冒泡
            }
        }
        $(".buttomXi").click(function(){
            cancelBubble();
        });
        //小弹框(接口)
        $scope.mapTable=function(lng_x,lat_y){
            $http({
                method: 'POST',
                url:zsurl+'/xiaogan/sta_name_list',
                data: $.param({
                        x:lng_x,
                        y:lat_y,
                        choose_city: cityName
                    }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.jiZhanName=response.sta_list;
                $(".message").show();
                $(".message").css({"top":axis_y+"px",left:axis_x+"px"});
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        //异常列表Top10
        $(".moreNub").click(function(){
            $(".hint").remove();
            //遮罩层
            $(".la_index_mask").show();
        });
        $scope.topTable=function(type){
            $http({
                method: 'POST',
                url:zsurl+'/xiaogan/sta_list_top10',
                data: $.param({
                        more: type,
                        choose_city: cityName
                    }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.rightEacharts=response.sta_list;
                //遮罩层
                Loading02=1;
                if(Loading02==1){
                    loadType();
                }else{
                    $(".la_index_mask").hide();
                }
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.topTable("");
        //点击查看发生的记录在根作用域上
        $rootScope.condition="off";
        $scope.record=function(val){
            $rootScope.indexBj01 = val[0];
            $rootScope.indexBj02 = val[1];
            $rootScope.lowBj01="";
            $rootScope.lowBj02="";
            $rootScope.hightBj01="";
            $rootScope.hightBj02="";
            $rootScope.condition="on";
        };
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});