app.controller('equipmentdetailCtrl', function($scope,$http,$filter,$state,$rootScope) {
    // var zsurl='http://39.108.165.149:7002'
    var zsurl='http://192.168.188.201:7002'
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
        // 
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
                url: zsurl+'/xiaogan/one_room_desc',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {
                    choose_sta:$rootScope.lowBj01,
                    sta_pow:$rootScope.lowBj02
                },
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.two_g_list;
                    $scope.importList2=response.four_g_list;
                    $scope.importList3=response.kt_list;
                    $scope.baseStation=response.Biasc[0];
                    $scope.baseStationPower=response.sta_pow;
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
        function baseStation(){
             for(var i=0;i<response.Biasc.length;i++){
                $scope.baseStation.push(response.Biasc[i]);
                 loadList(dataOn01,dataOn02);
            }
        }

         //点击查看折线图
        $scope.line=function(row){
            var arraySum=[];
            $("div span").each(function(){
                var nub=$('.xq').find('span').text();
                arraySum.push(nub);
            });
            $rootScope.xiaoganArray=arraySum;
            $state.go('equipment.linechart');
        }
        //修改 取消
        var preserveOne;
        var preserveTwo;
        var preserveThree;
        $("tbody").delegate(".compile","click",function(){    
            $rootScope.preserveOne=preserveOne=$(this).parent().parent().parent().find('input#ip_0').val();          
            $rootScope.preserveTwo=preserveTwo=$(this).parent().parent().parent().find('input#ip_1').val();          
            $rootScope.preserveThree=preserveThree=$(this).parent().parent().parent().find('input#ip_2').val();
            $(this).parent().parent().parent().find('input').css({"border":"1px solid #ddd"});
            $(this).parent().parent().parent().find('input').attr("disabled",false);
            $(this).hide();
            $(this).siblings(".putIn").show();
            $(this).siblings(".revocation").show();
        });
        $("tbody").delegate(".revocation","click",function(){
            $rootScope.preserveOne=preserveOne=$(this).parent().parent().parent().find('input#ip_0').val();
            $rootScope.preserveTwo=preserveTwo=$(this).parent().parent().parent().find('input#ip_1').val();
            $rootScope.preserveThree=preserveThree=$(this).parent().parent().parent().find('input#ip_2').val();
            $(this).parent().parent().parent().find('input').css({"border":"none"});
            $(this).parent().parent().parent().find("input").attr("disabled",true);
            $(this).hide();
            $(this).siblings(".putIn").hide();
            $(this).siblings(".compile").show();
        });

        //修改提交
        $("tbody").delegate(".putIn","click",function(){
            $(this).parent().parent().parent().find('input').css({"border":"none"});
            $(this).parent().parent().parent().find("input").attr("disabled",true);
            $(this).hide();
            $(this).siblings(".compile").show();
            $(this).siblings(".revocation").hide();
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/update_room_desc',
                data: $.param({  
                    choose_sta: $rootScope.lowBj01,
                    old_produce:$rootScope.preserveOne,
                    old_type: $rootScope.preserveTwo,
                    old_pow: $rootScope.preserveThree,
                    new_produce:$(this).parent().parent().parent().find('input#ip_0').val(),
                    new_type:$(this).parent().parent().parent().find('input#ip_1').val(),
                    new_pow:$(this).parent().parent().parent().find('input#ip_2').val(),
                    sb:$(this).siblings('.sb').val()
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                console.log(response.status_code);
                if(response.status_code==1){
                   layer.msg("修改成功!");
                   loadList($rootScope.lowBj02);
                }else{
                    layer.msg("修改失败!");
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
                if(ts_href=="#/equipment"){
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