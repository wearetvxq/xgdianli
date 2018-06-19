app.controller('enteringbatchdetailCtrl', function($scope,$http,$filter,$state,$rootScope) {
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
                loadData(1);
                loadpage();
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
        //表格接口
        var sumShuJv=0;
        var jiLv = "";
        var jiLv2 ="";
        function loadList(PageIndex){
            $.ajax({
                url: zsurl+'/xiaogan/table_device_desc_sb',
                type : "POST",
                dataType: "json",
                async: false, 
                data : {
                    sta_name:$rootScope.lowBj01,
                    PageIndex:PageIndex
                },
                success : function(response){
                    $scope.columnText=response.title;
                    $scope.importList=response.resultlist;
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
    
        //分页
        function loadData(num) {
            loadList(num);
            $("#PageCount").val(sumShuJv);//有多少条数据
        }
        function exeData(num, type) {
            loadData(num);
            loadpage();
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
                        console.log(num,8888)
                    }
                }
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