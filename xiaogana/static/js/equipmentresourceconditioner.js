app.controller('equipmentresourceconditionerCtrl', function ($scope, $http, $filter, $state, $rootScope) {
    var zsurl = 'http://192.168.188.178:91/xiaogan/statistics'
    //-----------------------权限板块----------------------//
    //地区名
    var cityName = "武汉";
    //获取cookie
    // if(getCookie("userName") == ''){
    //     alert("abnomal参数异常,将返回主系统!");
    //     window.location="public.html#/index";
    // }else{
    //     cityName=getCookie("userName");
    //     maxPag();
    // }
    //-----------------------权限板块----------------------//
        // --------------------日历--------------------//
    var datepicker1 = $('#datetimepicker1').datetimepicker({
        locale: moment.locale('zh-cn'),
        format: 'yyyy-mm-dd',//显示格式
        todayHighlight: 1,//今天高亮
        minView: "month",//设置只显示到月份
        startView:2,
        forceParse: 0,
        showMeridian: 1,
        autoclose: true,//选择后自动关闭
        language: 'zh-CN',
        weekStart: 1, 
    }).on("changeDate", function () {
        $('#datetimepicker1').datetimepicker('setStartDate', $("#datetimepicker1").val());
    });
    $('#datetimepicker2').datetimepicker({
        locale: moment.locale('zh-cn'),
        format: 'yyyy-mm-dd',//显示格式
        todayHighlight: 1,//今天高亮
        minView: "month",//设置只显示到月份
        startView:2,
        forceParse: 0,
        showMeridian: 1,
        autoclose: true,//选择后自动关闭
        language: 'zh-CN',
        weekStart: 1, 
    }).on("changeDate", function () {
        $('#datetimepicker2').datetimepicker('setStartDate', $("#datetimepicker2").val());
    });

        // --------------------搜索--------------------//
    $scope.search=function(){
        search(1);
    }
    var pageid=3;
    function search(page){
        let url= zsurl + '/inventory/'+pageid;
        let starttime=$scope.dateOne;
        let endtime=$scope.dateTwo;
        $scope.selPage= page || 1;
        $http({
            method: "get",
            params: {
                page: page,
                size:'10',
                starttime:starttime,
                endtime:endtime,
                // starttime:'2000-1-1',
                // endtime:'2100-1-1',
                area:$scope.area,
                station:$scope.station,
                Produce:$scope.Produce,
                frame:$scope.frame,
                ktpower:$scope.ktpower,
                kttype:$scope.kttype,
                people:$scope.people,
            },
            url:url,
            headers: { 'Content-type': 'application/x-www-form-urlencoded' }
        }).success(function (response) {
            // --------------------分页--------------------//
            $scope.total = response.total;//数据总条数
            $scope.items=response.result;//部分详细数据
            //分页总数
            $scope.pageSize = 10;
            $scope.pages = Math.ceil($scope.total / $scope.pageSize); //分页数11
            $scope.newPages = $scope.pages > 5 ? 5 : $scope.pages;//最大分页数5
            if($scope.selPage==1){
                $scope.pageList = [];
                //分页要repeat的数组
                for (var i = 0; i < $scope.newPages; i++) {
                    $scope.pageList.push(i + $scope.selPage);
                }
            }
        }).error(function (r) {
            layer.msg("加载错误：" + r);
        });
    }
    // 进入先加载第一页
    search(1);
        // --------------------分页--------------------//
    //当前选中页索引
    $scope.selectPage = function (page) {
        page=page||1;
        // 触发事件的范围
        if (page < 1 || page > $scope.pages) return;
        //最多显示分页数5
        if (page > 2) {
            //因为只显示5个页数，大于2页开始分页转换
            var newpageList = [];
            for (var i = (page - 3) ; i < ((page + 2) > $scope.pages ? $scope.pages : (page + 2)) ; i++) {
                newpageList.push(i + 1);
            }
            $scope.pageList = newpageList;
        }
        $scope.selPage = page;
        search(page);//选择页获取
        $scope.isActivePage(page);//选中页渲染
    };
    //设置当前选中页样式
    $scope.isActivePage = function (page) {
        return $scope.selPage == page;
    };
    //上一页
    $scope.Previous = function () {
        $scope.selectPage($scope.selPage - 1);
    }
    //下一页
    $scope.Next = function () {
        $scope.selectPage($scope.selPage + 1);
    };

        // --------------------图片--------------------//
    //获取图片url
    $scope.getimg=function(pic){
        console.log(pic[0]);
        $scope.url=pic[0];
        console.log($scope.url);
    }

        // --------------------导出--------------------//
    $scope.export=function(){
        let url= zsurl + '/inventory/export/'+pagid;
        let starttime=$scope.dateOne;
        let endtime=$scope.dateTwo;
        // $http.get(url,{
        $http({
            method: "get",
            params: {
                page: $scope.selPage,
                size:'10',
                starttime:starttime,
                endtime:endtime,
                // starttime:'2001-1-1',
                // endtime:'2019-1-1',
                area:$scope.area,
                name:$scope.name,
            },
            url:url,
            headers: { 'Content-type': 'application/x-www-form-urlencoded' }
        }).success(function (response) {
            if(response.code==0){
                $scope.url = response.url;//数据总条数
                console.log($scope.url)
                window.location.href ="http://"+$scope.url;
            }
        }).error(function (r) {
            layer.msg("加载错误：" + r);
        });
    }
    
    function maxPag() {
        //遮罩层
        // $(".la_index_mask").show();
        // 导航栏选中
        $(function () {
            $(".optFor a").each(function () {
                var ts_href = $(this).attr("href"),
                    local_path = location.hash;
                if (ts_href == local_path) {
                    $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                } else if (local_path == "#/") {
                    $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
        });
        //阻止事件冒泡
        function getEvent() {
            if (window.event) { return window.event; }
            func = getEvent.caller;
            while (func != null) {
                var arg0 = func.arguments[0];
                if (arg0) {
                    if ((arg0.constructor == Event || arg0.constructor == MouseEvent
                        || arg0.constructor == KeyboardEvent)
                        || (typeof (arg0) == "object" && arg0.preventDefault
                            && arg0.stopPropagation)) {
                        return arg0;
                    }
                }
                func = func.caller;
            }
            return null;
        }
        function cancelBubble() {
            var e = getEvent();
            if (window.event) {
                //e.returnValue=false;//阻止自身行为
                e.cancelBubble = true;//阻止冒泡
            } else if (e.preventDefault) {
                //e.preventDefault();//阻止自身行为
                e.stopPropagation();//阻止冒泡
            }
        }
        
        //table表格
        $scope.tableChang = function () {
            setTimeout(function () {
                loadData(1);
                loadpage(1);
                $http({
                    method: 'POST',
                    url: zsurl + '/xiaogan/jump_err_count',
                    data: $.param({
                        choose_city: $scope.sAbnOne
                    }),
                    headers: { 'Content-type': 'application/x-www-form-urlencoded' }
                }).success(function (response) {
                    $scope.lowNub = response.count;
                }).error(function (r) {
                    layer.msg("加载错误：" + r);
                });
            }, 500);
        };
        //一级筛选条件下拉框
        $(".lg_border_box").click(function () {
            $(".lg_down_box").toggle();
            cancelBubble();
        });
        $(".lg_search_box").delegate(".lg_down_box p", "click", function () {
            var p_name = $(this).text();
            $scope.sAbnOne = p_name;
            setTimeout(function () {
                $(".lg_down_box").toggle();
            }, 100);
            cancelBubble();
        });
        $("body").click(function () {
            $(".lg_down_box").hide();
        });
        //一级筛选条件接口
        $scope.oneChange = function () {
            $http({
                method: 'POST',
                url: zsurl + '/xiaogan/city_voltage_jump',
                data: $.param({
                    choose_city: cityName
                }),
                headers: { 'Content-type': 'application/x-www-form-urlencoded' }
            }).success(function (response) {
                $scope.oneList = response.city_list;
                $scope.sAbnOne = response.city_list[0];
                $scope.tableChang();
            }).error(function (r) {
                layer.msg("加载错误：" + r);
            });
        }
        $scope.oneChange();
        $scope.lowChange = function () {
            $http({
                method: 'POST',
                url: zsurl + '/xiaogan/jump_err_count',
                data: $.param({
                    choose_city: cityName
                }),
                headers: { 'Content-type': 'application/x-www-form-urlencoded' }
            }).success(function (response) {
                $scope.lowNub = response.count;
            }).error(function (r) {
                layer.msg("加载错误：" + r);
            });
        }
        //table表格(接口)
        var sumShuJv = 0;
        function loadList(PageIndex) {
            $.ajax({
                url: zsurl + '/xiaogan/table_jump_err',
                type: "POST",
                dataType: "json",
                async: false,
                data: { city: $scope.sAbnOne, PageIndex: PageIndex },
                success: function (response) {
                    $scope.columnText = response.title;
                    $scope.importList = response.page_resultList;
                    // $scope.pageCount=response.pageCount;
                    $scope.rowCount = response.rowCount;
                    //防止分页插件报错
                    if ($scope.rowCount == 0) {
                        sumShuJv = 1;
                    } else {
                        sumShuJv = $scope.rowCount;
                    }
                    $scope.$applyAsync();
                    //遮罩层关闭
                    $(".la_index_mask").hide();
                }, error: function (r) {  // 失败回调
                    layer.msg("加载错误：" + r);
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
        $rootScope.condition = "off";
        $scope.delete = function (item) {
            $rootScope.indexBj01 = "";
            $rootScope.indexBj02 = "";
            $rootScope.lowBj01 = item[0];
            $rootScope.lowBj02 = item[3];
            $rootScope.hightBj01 = "";
            $rootScope.hightBj02 = "";
            $rootScope.condition = "on";
            $state.go('particulars');//显示详情
        };

    }

    $scope.openModel = function() {
        var modalInstance = $modal.open({
            templateUrl : 'modal.html',//script标签中定义的id
            controller : 'modalCtrl',//modal对应的Controller
            resolve : {
                data : function() {//data作为modal的controller传入的参数
                        return data;//用于传递数据
                }
            }
        })
    } 
});
//业务类
app.factory('BusinessService', ['$http', function ($http) {
    var list = function (postData) {
        return $http.post('/Employee/GetAllEmployee', postData);
    }
    return {
        list: function (postData) {
            return list(postData);
        }
    }
}]);
app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
app.controller('modalCtrl', function($scope, $modalInstance, data) {
    $scope.data= data;
    //在这里处理要进行的操作   
    $scope.ok = function() {
        $modalInstance.close();
    };
    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    }
});
    
