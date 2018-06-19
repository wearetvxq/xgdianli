app.controller('enteringdetailCtrl', function($scope,$http,$filter,$state,$rootScope) {
    var zsurl='http://39.108.165.149:7002'
    // var zsurl='http://192.168.188.201:7002'
    //-----------------------权限板块----------------------//
    //获取cookie
    var ming;
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
        
        //table表格
        $scope.tableChang=function(){
            setTimeout(function(){
                loadData(1);
            },500);
        };
        //表格接口
        var sumShuJv=0;
        var jiLv = "";
        var jiLv2 ="";
        function loadList(dataOn01,dataOn02){
            jiLv=dataOn01;
            jiLv2=dataOn02;
            $.ajax({
                url: zsurl+'/xiaogan/table_device_desc',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {
                    sta_name:$rootScope.lowBj01,
                    type:$('.sb').val()
                },
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.result;
                    $scope.rowCount=response.rowCount;
                    //防止分页插件报错
                    if($scope.rowCount==0){
                        sumShuJv=1;
                    }else{
                        sumShuJv=$scope.rowCount;
                    }
                    $scope.$applyAsync();
                    //遮罩层关闭
                    $(".la_index_mask").hide();
                },error: function(r){  // 失败回调
                    layer.msg("加载错误："+r);
                }
            });
        }
         //删除
        var preOne;
        var preTwo;
        var preThree;
        var preFour;
        var preFive;
        $("tbody").delegate(".checkA","click",function(){  
            console.log($(this).parent().parent().parent().find('input#ip_0').val());
            console.log($(this).parent().parent().parent().find('input#ip_1').val());
            console.log($(this).parent().parent().parent().find('input#ip_2').val());
            console.log($(this).parent().parent().parent().find('input#ip_3').val());
            console.log($(this).parent().parent().parent().find('input#ip_4').val());  
            $rootScope.preOne=preOne=$(this).parent().parent().parent().find('input#ip_0').val();          
            $rootScope.preTwo=preTwo=$(this).parent().parent().parent().find('input#ip_1').val();          
            $rootScope.preThree=preThree=$(this).parent().parent().parent().find('input#ip_2').val();
            $rootScope.preFour=preFour=$(this).parent().parent().parent().find('input#ip_3').val();
            $rootScope.preFive=preFive=$(this).parent().parent().parent().find('input#ip_4').val();
             $http({
                method: 'POST',
                url: zsurl+'/xiaogan/device_remove',
                data: $.param({  
                    choose_sta:$rootScope.preOne,
                    device_type:$rootScope.preTwo,
                    device_pow:$rootScope.preThree,
                    produce:$rootScope.preFour,
                    sb_type:$rootScope.preFive
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                if(response.status_code==1){
                    layer.msg("删除成功!");
                }else{
                    layer.msg("删除失败!");
                }
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        });
        
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
                dataOn02=$rootScope.lowBj02;
                loadList(dataOn01,dataOn02);
            }
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
        //分页
        function loadData(num) {
           loadList(num);
           $("#PageCount").val(sumShuJv);//有多少条数据
        }
        function exeData(num, type) {
            loadData(num);
            loadpage();
        }
        //点击查看发生的记录在根作用域上
        $rootScope.condition="off";
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});