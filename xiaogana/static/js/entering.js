app.controller('enteringCtrl', function($scope,$http,$filter,$state,$rootScope) {
    var zsurl='http://39.108.165.149:7002'
   // var zsurl='http://192.168.188.201:7002'
    //-----------------------权限板块----------------------//
    //地区名
    var cityName;
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
    //     cityName=getCookie("userName");
    //     maxPag();
    // }
    //-----------------------权限板块----------------------//
    function maxPag(){
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
        if($rootScope.condition == "on"){
            $state.go('entering.particulars');//显示详情
            $rootScope.condition="off";
        }else{
            $state.go('entering.enteringbatch');//默认显示机房管理
        }
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});