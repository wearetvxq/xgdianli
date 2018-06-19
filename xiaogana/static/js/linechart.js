app.controller('linechartCtrl', function($scope,$http,$filter,$rootScope) {
    var zsurl='http://39.108.165.149:7002'
   // var zsurl='http://192.168.188.201:7002'
    //-----------------------权限板块----------------------//
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
        //折线图
        var jiLv="";
        var jiLv2="";
        var industryData=[];
        var lineData=[];
        //----------折线图(echarts图)
        var myChart01 = echarts.init(document.getElementById('forecastLine'));
        myChart01.setOption({
              tooltip: {
                  trigger: 'axis',
              },
              xAxis: {
                  type: 'category',
                  splitLine: {show: false},
                  data: industryData,
                  axisTick: {
                      alignWithLabel: true,
                      interval: 0
                  },
                  axisLabel: {
                    textStyle: {
                        fontSize: 10
                    }
                  }
              },
              grid: {
                  top: '10%',
                  left: '2%',
                  right: '3%',
                  bottom: '5%',
                  containLabel: true
              },
              yAxis: {
                  type: 'value',
                  name: 'kW·h',
                  axisTick: {
                      show: false
                  },
                  splitLine: {
                      show: false
                  },
                  axisLabel: {
                    textStyle: {
                        fontSize: 10
                    }
                  }
              },
              series: [
                  {
                      name: "功率",
                      type: 'line',
                      data: lineData,
                      itemStyle: {
                          normal: {
                              color: "#4483EB"
                          }
                      },
                      lineStyle: {
                          normal: {
                              color: "#4483EB"
                          }
                      }
                  }
              ]
        });
        //折线图(传参函数)
        function single01(industryData,lineData){
            myChart01.setOption({
                xAxis: {
                    type: 'category',
                    data: industryData
                },
                series: [
                    {   
                        name: '功率',
                        data: lineData
                    }
                ]
            });
        }
        //折线图(接口)
        $scope.echartsData01=function(dataOn01){
            jiLv=dataOn01;
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/room_desc_show',
                data: $.param({  
                   choose_sta:$rootScope.lowBj01,
                }),
            headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                single01(response.date_list,response.load_list);
                $scope.baseStation=response.name;
                $(".la_index_mask").hide();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }

        // 导航栏选中
        $(function(){
            var dataOn01;
            var dataOn02;
            if($rootScope.lowBj01 == undefined){
            }else if($rootScope.lowBj01!=""){
               $(".tableShow01").addClass("pitchUp");
                $(".getShoot01").addClass("quiver");
                $(".tableShow02").removeClass("pitchUp");
                $(".getShoot02").removeClass("quiver");
                dataOn01=$rootScope.lowBj01;
                $scope.echartsData01(dataOn01);
            }
            $(".optFor a").each(function(){
                var ts_href=$(this).attr("href"),
                    local_path=location.hash;
                if(ts_href=="#/equipment"){
                  $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                }else if(local_path=="#/"){
                  $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
        });
        $scope.hueiTianList=function(){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/sta_data_show',
                data: $.param({  
                    sta_name: jiLv         
                }),
            headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.htList=response.sta_data_list;
                //遮罩层关闭
                $(".la_index_mask").hide();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        //点击查看发生的记录在根作用域上
        $rootScope.condition="off";
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});