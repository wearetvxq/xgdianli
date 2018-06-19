app.controller('enteringindividuallyCtrl', function($scope,$http,$filter) {
    var zsurl='http://39.108.165.149:7002'
   // var zsurl='http://192.168.188.201:7002'
    //-----------------------权限板块----------------------//
    //  //地区名
    var cityName;
    var sta_list;
    var type_air_list;
    var sbtype;
    var producelist;
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
    // if(getCookie("userName") == ''){
    //     alert("参数异常,将返回主系统!");
    //     window.location="public.html#/index";
    // }else{
    //     maxPag();
    // }
    //-----------------------权限板块----------------------//
    function maxPag(){
      //遮罩层开启
      $(".la_index_mask").show();
      // 导航栏选中
         $(function(){
            $(".tableShow01").removeClass("pitchUp");
            $(".getShoot01").removeClass("quiver");
            $(".tableShow02").addClass("pitchUp");
            $(".getShoot02").addClass("quiver");
            $(".optFor a").each(function(){
                var ts_href=$(this).attr("href"),
                    local_path=location.hash;
                if(ts_href=="#/entering"){
                  $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                }else if(local_path=="#/"){
                  $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
        });
      //阻止事件冒泡
      function getEvent(){
          if(window.event){return window.event;}
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
     //一级地区选择下拉框
        $(".lg_border_box").click(function(){
            $(".lg_down_box").toggle();
            $(".lg_down_box02").hide();
            $(".lg_down_box03").hide();
            $(".lg_down_box04").hide();
            $(".lg_down_box05").hide();
            cancelBubble();
        });
        $(".lg_search_box").delegate(".lg_down_box p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnOne=p_name;
            $("#lg_down_box").val(p_name);
            setTimeout(function(){
                $(".lg_down_box").toggle();
                $(".lg_down_box02").hide();
                $(".lg_down_box03").hide();
                $(".lg_down_box04").hide();
                 $(".lg_down_box05").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box").hide();
        });
          //二级基站名称下拉框
        $(".lg_border_box02").click(function(){
            $(".lg_down_box02").toggle();
            $(".lg_down_box").hide();
            $(".lg_down_box03").hide();
            $(".lg_down_box04").hide();
             $(".lg_down_box05").hide();
            cancelBubble();
        });
        $(".lg_search_box02").delegate(".lg_down_box02 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnTwo=p_name;
            $("#lg_down_box02").val(p_name);
            setTimeout(function(){
                $(".lg_down_box02").toggle();
                 $(".lg_down_box").hide();
                 $(".lg_down_box03").hide();
                 $(".lg_down_box04").hide();
                  $(".lg_down_box05").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box02").hide();
        });
           //三级设备名称下拉框
        $(".lg_border_box03").click(function(){
            $(".lg_down_box03").toggle();
            $(".lg_down_box").hide();
            $(".lg_down_box02").hide();
            $(".lg_down_box04").hide();
             $(".lg_down_box05").hide();
            cancelBubble();
        });
        $(".lg_search_box03").delegate(".lg_down_box03 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnThere=p_name;
             $("#lg_down_box03").val(p_name);
            setTimeout(function(){
                $(".lg_down_box03").toggle();
                 $(".lg_down_box").hide();
                 $(".lg_down_box02").hide();
                 $(".lg_down_box04").hide();
                  $(".lg_down_box05").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box03").hide();
        });
        //四级生产厂家下拉框
        $(".lg_border_box04").click(function(){
            $(".lg_down_box04").toggle();
            $(".lg_down_box").hide();
            $(".lg_down_box02").hide();
            $(".lg_down_box03").hide();
             $(".lg_down_box05").hide();
            cancelBubble();
        });
        $(".lg_search_box04").delegate(".lg_down_box04 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnFour=p_name;
             $("#lg_down_box04").val(p_name);
            setTimeout(function(){
                $(".lg_down_box04").toggle();
                 $(".lg_down_box").hide();
                 $(".lg_down_box02").hide();
                 $(".lg_down_box03").hide();
                  $(".lg_down_box05").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box04").hide();
        });
           //五级型号下拉框
        $(".lg_border_box05").click(function(){
            $(".lg_down_box05").toggle();
            $(".lg_down_box").hide();
            $(".lg_down_box02").hide();
            $(".lg_down_box03").hide();
             $(".lg_down_box04").hide();
            cancelBubble();
        });
        $(".lg_search_box05").delegate(".lg_down_box05 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnFive=p_name;
             $("#lg_down_box05").val(p_name);
            setTimeout(function(){
                $(".lg_down_box05").toggle();
                 $(".lg_down_box").hide();
                 $(".lg_down_box02").hide();
                 $(".lg_down_box03").hide();
                 $(".lg_down_box04").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box05").hide();
        });
        //六级功率下拉框
        $(".lg_border_box06").click(function(){
            $(".lg_down_box06").toggle();
            $(".lg_down_box").hide();
            $(".lg_down_box02").hide();
            $(".lg_down_box03").hide();
            $(".lg_down_box04").hide();
            $(".lg_down_box05").hide();
            cancelBubble();
        });
        $(".lg_search_box06").delegate(".lg_down_box06 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnSix=p_name;
             $("#lg_down_box06").val(p_name);
            setTimeout(function(){
                $(".lg_down_box06").toggle();
                 $(".lg_down_box").hide();
                 $(".lg_down_box02").hide();
                 $(".lg_down_box03").hide();
                 $(".lg_down_box04").hide();
                 $(".lg_down_box05").hide();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box06").hide();
        });
        //一级地区选择接口
        $scope.oneChange=function(){
            $http({
                method: 'GET',
                url: zsurl+'/xiaogan/add_one_city',
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
               $scope.oneList = []
               for(var i=0;i<response.city_list.length;i++){
                   $scope.oneList.push( response.city_list[i])
               }
                $scope.sAbnOne=response.city_list[0];
                $scope.twoChange();
                $scope.thereList=response.shebei_list;
                $scope.sAbnThere=response.shebei_list[0];
                $scope.fourChange();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.oneChange();
        //二级基站名称接口
        $scope.twoChange=function(sta_list){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/add_sta_name',
                data: $.param({
                    choose_city: sta_list
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
              $scope.twoList = []
               for(var i=1;i<response.sta_list.length;i++){
                   $scope.twoList.push( response.sta_list[i])
               }
                $scope.sAbnTwo=response.sta_list[0];
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.test=function(){
        }
        // $scope.twoChange();
        //三级设备选择
         $scope.thereChange=function(){
        }
        // $scope.thereChange();
        // 四级生产厂家接口
        $scope.fourChange=function(sbtype){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/air_add_produce_make',
                data: $.param({
                    choose_type:sbtype
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
               $scope.fourList = []
               if(response.producelist){
                for(var i=1;i<response.producelist.length;i++){
                  $scope.fourList.push(response.producelist[i])               
                  $scope.cj = response.producelist[0]
                }
              }
                type_air_list=sbtype;
                $scope.fiveChange(type_air_list);
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
         // $scope.fourChange();
         // 五级型号接口
        $scope.fiveChange=function(type_air_list){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/air_type',
                data: $.param({
                    produce:$scope.sAbnFour,
                    choose_air:$scope.sAbnThere
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.fiveList=response.type_air_list;
                $scope.sAbnFive=response.type_air_list[0];
                $(".la_index_mask").hide();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.test2=function(){
        }
         // $scope.fiveChange();
        //点击提交按钮
          $("#upload-button").click(function(){
          if($("#lg_down_box").val() == "" ||$("#lg_down_box02").val() == "" || $("#lg_down_box03").val() == "" || $("#lg_down_box04").val() == "" || $("#lg_down_box05").val() == "" || $("#lg_down_box06").val() == ""){
              layer.msg("选择信息不能为空,请完善!")
              return false;
          }else{
            $scope.tijiaoButton();
          }
        })
      //提交按钮
      $scope.tijiaoButton=function(){
          var formData = new FormData($( "#uploadForm" )[0]);  
          $http({
              method: 'POST',
              url: zsurl+'/xiaogan/add_one_import',
              data: $.param({  
                      choose_area:$scope.sAbnOne,
                      choose_sta: $scope.sAbnTwo,
                      choose_device: $scope.sAbnThere,
                      choose_product: $scope.sAbnFour,
                      choose_type: $scope.sAbnFive,
                      choose_pow:$scope.sAbnSix
                  }),  
            headers:{'Content-type':'application/x-www-form-urlencoded'}
          }).success(function (response) {
              if(response.flag==1){
                   layer.msg("提交成功!");
              }else{
                  layer.msg("提交失败!");
              }
              $(".la_index_mask").hide();
          }).error(function(r){
              layer.msg("加载错误："+r);
          });
      }
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});