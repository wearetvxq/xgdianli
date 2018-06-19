app.controller('equipmentoneCtrl', function($scope,$http,$filter,$state,$rootScope) {
    var zsurl='http://39.108.165.149:7002'
   // var zsurl='http://192.168.188.201:7002'
    //-----------------------权限板块----------------------//
    //地区名
    var cityName;
    //名称
    var sta_name_list;
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
        //遮罩层
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
                if(ts_href=="#/equipment"){
                  $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                }else if(local_path=="#/"){
                  $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
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
         //延迟触发
        $scope.delay=function(){
            setTimeout(function(){
                $scope.loadList();
            },500);
        }
        //table表格
        $scope.tableChang=function(){
            setTimeout(function(){
                loadData(1,1,1,1,1);
                loadpage();
            },500);
        };
        //一级筛选条件下拉框
        $(".lg_border_box").click(function(){
            $(".lg_down_box").toggle();
            $(".lg_down_box02").hide();
            cancelBubble();
        });
        $(".lg_search_box").delegate(".lg_down_box p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnOne=p_name;
            $("#lg_down_box").val(p_name);
            setTimeout(function(){
                $(".lg_down_box").toggle();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box").hide();
        });
        //二级筛选条件下拉框
        $(".lg_border_box02").click(function(){
            $(".lg_down_box02").toggle();
            $(".lg_down_box").hide();
            cancelBubble();
        });
        $(".lg_search_box02").delegate(".lg_down_box02 p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnTwo=p_name;
            $("#lg_down_box02").val(p_name);
            setTimeout(function(){
                $(".lg_down_box02").toggle();
            },100);
            cancelBubble();
        });
       
        $("body").click(function(){
            $(".lg_down_box02").hide();
        });
         //一级筛选条件接口
        $scope.oneChange=function(){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/city_device_management',
                data: $.param({
                    choose_city: cityName
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.oneList = []
                for(var i=1;i<response.city_list.length;i++){
                    $scope.oneList.push(response.city_list[i])
                }
                $scope.sAbnOne=response.city_list[0];
                sta_name_list = cityName;
                $scope.twoChange(sta_name_list);
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.oneChange();
        $scope.twoChange=function(sta_name_list){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/sta_device_management',
                data: $.param({
                    choose_city: sta_name_list
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.twoList = []
                for(var i=1;i<response.sta_name_list.length;i++){
                    $scope.twoList.push(response.sta_name_list[i])
                }
                $scope.sAbnTwo=response.sta_name_list[0];
                $scope.tableChang();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        // $scope.twoChange();
        //table表格(接口)
        var sumShuJv=0;
        function loadList(PageIndex,sorts,sortss){
            $.ajax({
                url: zsurl+'/xiaogan/room_table_list',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {
                    choose_city:$scope.sAbnOne,
                    choose_sta:$scope.sAbnTwo,
                    sort:sorts,
                    sort_air:sortss,
                    PageIndex:PageIndex
                },
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.table_list;
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

         //点击超出频率
            $scope.flagshows = 0;
            $scope.flagshow = 1;
            $scope.ming="是否存在空调";
            $scope.name="超出频率";
            $scope.revers=false;
            $scope.sort=function(row){                
                PageIndex = $("#pagination").find('.active').attr('jp-data')
                $(".la_index_mask").show();
                $.ajax({
                url: zsurl+'/xiaogan/room_table_list',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {choose_city:$scope.sAbnOne,choose_sta:$scope.sAbnTwo,sort:row,PageIndex:PageIndex},
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.table_list;
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
                    if (row == 1){
                        $scope.flagshows = 1;
                        $scope.flagshow = 0;
                    }else{
                        $scope.flagshows = 0;
                        $scope.flagshow = 1;
                    }
                },error: function(r){  // 失败回调
                    layer.msg("加载错误："+r);
                }
            });
                if($scope.name==row){
                    $scope.revers=!$scope.revers;
                }else{
                    $scope.revers=false;
                }
                $scope.name=row;
            }

            $scope.sorts=function(row){                
                PageIndex = $("#pagination").find('.active').attr('jp-data')
                $(".la_index_mask").show();
                $.ajax({
                url: zsurl+'/xiaogan/room_table_list',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {choose_city:$scope.sAbnOne,choose_sta:$scope.sAbnTwo,sort:row,PageIndex:PageIndex},
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.table_list;
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
                    if (row == 1){
                        $scope.flagshows = 0;
                        $scope.flagshow = 1;
                    }else{
                        $scope.flagshows = 1;
                        $scope.flagshow = 0;
                    }
                },error: function(r){  // 失败回调
                    layer.msg("加载错误："+r);
                }
            });
                if($scope.name==row){
                    $scope.revers=!$scope.revers;
                }else{
                    $scope.revers=false;
                }
                $scope.name=row;
            }


            $scope.flagsorts = 0;
            $scope.flagsort = 1;
          //点击是否存在空调
            $scope.sort1=function(row){
                PageIndex = $("#pagination").find('.active').attr('jp-data')
                $(".la_index_mask").show();
                $.ajax({
                url: zsurl+'/xiaogan/room_table_list',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {choose_city:$scope.sAbnOne,choose_sta:$scope.sAbnTwo,sort_air:row,PageIndex:PageIndex},
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.table_list;
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
                    $scope.flagsorts = 1;
                    $scope.flagsort = 0;
                },error: function(r){  // 失败回调
                    layer.msg("加载错误："+r);
                }
            });
                if($scope.ming==row){
                    $scope.revers=!$scope.revers;
                }else{
                    $scope.revers=false;
                }
                $scope.ming=row;
            }

             $scope.sort2=function(row){
                PageIndex = $("#pagination").find('.active').attr('jp-data')
                $(".la_index_mask").show();
                $.ajax({
                url: zsurl+'/xiaogan/room_table_list',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {choose_city:$scope.sAbnOne,choose_sta:$scope.sAbnTwo,sort_air:row,PageIndex:PageIndex},
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.table_list;
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
                    $scope.flagsorts = 0;
                    $scope.flagsort = 1;
                },error: function(r){  // 失败回调
                    layer.msg("加载错误："+r);
                }
            });
                if($scope.ming==row){
                    $scope.revers=!$scope.revers;
                }else{
                    $scope.revers=false;
                }
                $scope.ming=row;
            }


      //点击基站空调对比
        $scope.cont=function(row){
            var arrSum=[];
            $("tbody tr").each(function(){
                var type=$(this).find('td').eq(0).find('input').prop("checked");
                if(type==true){
                    var nub=$(this).find('td').eq(2).find('.tableSpan').text();
                    arrSum.push(nub);
                }
            });
            $rootScope.xiaoganArr=arrSum;
            if($rootScope.xiaoganArr.length==2){
                $state.go('equipment.basecontrast');
            }else{
                layer.msg("请选中两个对比值");
            }
        }
     $('.check').click(function(){
            var arr=[];
            $(".check").each(function(){
                if($(this).prop("checked")==true){
                    arr.push(i);
                }
            });
            if(arr.length>2){
                return false;
            }
      });

        //分页
        function loadData(num) {
            loadList(num,$scope.flagshows,$scope.flagsorts);
            $("#PageCount").val(sumShuJv);//有多少条数据
        }
        function exeData(num, type) {
            loadData(num);
            loadpage(1);
        }
        function loadpage() {
            var myPageCount = parseInt($("#PageCount").val());
            var myPageSize = parseInt($("#PageSize").val());
            var countindex = myPageCount % myPageSize > 0 ? (myPageCount / myPageSize) + 1 : (myPageCount / myPageSize);
            $("#countindex").val(countindex);
            $.jqPaginator('#pagination', {
                totalPages: parseInt($("#countindex").val()),
                visiblePages: parseInt($("#visiblePages").val()),
                currentPage: 1,
                first: '<li class="first"><a href="javascript:;">首页</a></li>',
                prev: '<li class="prev"><a href="javascript:;"><i class="arrow arrow2"></i>上一页</a></li>',
                next: '<li class="next"><a href="javascript:;">下一页<i class="arrow arrow3"></i></a></li>',
                last: '<li class="last"><a href="javascript:;">末页</a></li>',
                page: '<li class="page"><a href="javascript:;">{{page}}</a></li>',
                onPageChange: function (num, type) {
                    if (type == "change") {
                        exeData(num, type);
                    }
                }
            });
        }
        //点击查看发生的记录在根作用域上
        $rootScope.condition="off";
        $scope.delete=function(item){
            $rootScope.indexBj01="";
            $rootScope.indexBj02="";
            $rootScope.lowBj01=item[1];
            $rootScope.lowBj02=item[2];
            $rootScope.hightBj01="";
            $rootScope.hightBj02="";
            $rootScope.condition="on";
            $state.go('equipment.equipmentdetail');//显示详情
        };
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});