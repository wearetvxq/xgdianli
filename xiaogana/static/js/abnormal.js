app.controller('abnormalCtrl', function($scope,$http,$filter,$state,$rootScope) {
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
    if(getCookie("userName") == ''){
        alert("参数异常,将返回主系统!");
        window.location="public.html#/index";
    }else{
        cityName=getCookie("userName");
        maxPag();
    }
    //-----------------------权限板块----------------------//
    function maxPag(){
        //遮罩层
        $(".la_index_mask").show();
        // 导航栏选中
         $(function(){
        $(".optFor a").each(function(){
          var ts_href=$(this).attr("href"),
              local_path=location.hash;
          if(ts_href==local_path){
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
        //table表格
        $scope.tableChang=function(){
            setTimeout(function(){
                loadData(1);
                loadpage(1);
                 $http({
                method: 'POST',
                url: zsurl+'/xiaogan/jump_err_count',
                data: $.param({
                    choose_city: $scope.sAbnOne
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.lowNub=response.count;
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
            },500);
        };
        //一级筛选条件下拉框
        $(".lg_border_box").click(function(){
            $(".lg_down_box").toggle();
            cancelBubble();
        });
        $(".lg_search_box").delegate(".lg_down_box p","click",function(){
            var p_name=$(this).text();
            $scope.sAbnOne=p_name;
            setTimeout(function(){
                $(".lg_down_box").toggle();
            },100);
            cancelBubble();
        });
        $("body").click(function(){
            $(".lg_down_box").hide();
        });
        //一级筛选条件接口
        $scope.oneChange=function(){
            $http({
                method: 'POST',
                url: zsurl+'/xiaogan/city_voltage_jump',
                data: $.param({
                    choose_city: cityName
                }),
                headers:{'Content-type':'application/x-www-form-urlencoded'}
            }).success(function (response) {
                $scope.oneList=response.city_list;
                $scope.sAbnOne=response.city_list[0];
                $scope.tableChang();
            }).error(function(r){
                layer.msg("加载错误："+r);
            });
        }
        $scope.oneChange();
        $scope.lowChange=function(){
	        $http({
	            method: 'POST',
	            url: zsurl+'/xiaogan/jump_err_count',
	            data: $.param({
                    choose_city: cityName
                }),
	            headers:{'Content-type':'application/x-www-form-urlencoded'}
	        }).success(function (response) {
	            $scope.lowNub=response.count;
	        }).error(function(r){
	            layer.msg("加载错误："+r);
	        });
	    }
        //table表格(接口)
        var sumShuJv=0;
        function loadList(PageIndex){
            $.ajax({
                url: zsurl+'/xiaogan/table_jump_err',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {city:$scope.sAbnOne,PageIndex:PageIndex},
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.page_resultList;
                    // $scope.pageCount=response.pageCount;
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
        //分页
        function loadData(num) {
            loadList(num);
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
            $rootScope.lowBj01=item[0];
            $rootScope.lowBj02=item[3];
            $rootScope.hightBj01="";
            $rootScope.hightBj02="";
            $rootScope.condition="on";
            $state.go('particulars');//显示详情
        };
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});