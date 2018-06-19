app.controller('particularsCtrl', function($scope,$http,$filter,$rootScope) {
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
	    $scope.echartsData01=function(dataOn01,dataOn02){
	    	jiLv=dataOn01;
	        $http({
	          	method: 'POST',
	          	url: zsurl+'/xiaogan/sta_details',
	          	data: $.param({  
	                sta_no: dataOn01,
	                err_type: dataOn02          
	            }),
	        headers:{'Content-type':'application/x-www-form-urlencoded'}
	        }).success(function (response) {
	            single01(response.date_list,response.load_list);
	            $scope.baseStation=response.name;
	            $scope.handlingMethod=response.err_type;
	            $scope.hueiTianList();
	            $(".la_index_mask").hide();
	        }).error(function(r){
	            layer.msg("加载错误："+r);
	        });
	    }
	    // 导航栏选中
        $(function(){
        	var dataOn01;
        	var dataOn02;
        	if($rootScope.indexBj01 == undefined||$rootScope.lowBj01 == undefined||$rootScope.hightBj01 == undefined){
        	}else if($rootScope.indexBj01!=""){
        		$(".tableShow01").removeClass("pitchUp");
        		$(".getShoot01").removeClass("quiver");
            	$(".tableShow02").removeClass("pitchUp");
            	$(".getShoot02").removeClass("quiver");
            	dataOn01=$rootScope.indexBj01;
            	dataOn02=$rootScope.indexBj02;
            	$scope.echartsData01(dataOn01,dataOn02);
        	}else if($rootScope.lowBj01!=""){
        		$(".tableShow01").addClass("pitchUp");
        		$(".getShoot01").addClass("quiver");
            	$(".tableShow02").removeClass("pitchUp");
            	$(".getShoot02").removeClass("quiver");
            	dataOn01=$rootScope.lowBj01;
            	dataOn02=$rootScope.lowBj02;
            	$scope.echartsData01(dataOn01,dataOn02);
        	}else if($rootScope.hightBj01!=""){
        		$(".tableShow01").removeClass("pitchUp");
        		$(".getShoot01").removeClass("quiver");
            	$(".tableShow02").addClass("pitchUp");
            	$(".getShoot02").addClass("quiver");
            	dataOn01=$rootScope.hightBj01;
            	dataOn02=$rootScope.hightBj02;
            	$scope.echartsData01(dataOn01,dataOn02);
        	}
            $(".optFor a").each(function(){
                var ts_href=$(this).attr("href"),
                    local_path=location.hash;
                if(ts_href=="#/abnormal"){
                  $(this).parents(".optFor").addClass('pitchOn').siblings().removeClass('pitchOn');
                }else if(local_path=="#/"){
                  $(".optFor").eq(0).addClass('pitchOn').siblings().removeClass('pitchOn');
                }
            });
        });
	    //------------------回填数据模块
	   
	    $(".htButton").click(function(){
	    	$(".formMenu").show();
	    });
	    //隐藏
	    $(".wrong").click(function(){
	    	$(".formMenu").hide();
	    });
	    //增加
	    $(".addButton").click(function(){
	    	$(".inputArea").append("<div class='inputTitleEntity'><div class='designationBorder'><input type='text' placeholder='示例:XG-0001'></div><div class='quantityBorder'><input type='text' placeholder='2018-01-12'></div><div class='rateWorkBorder'><input type='text' onkeyup='if(/\D/.test(this.value)){layer.msg('只能输入数字');this.value='';}' placeholder='25'></div><p class='expurgateBorder'>X</p></div>")
	    });
	    //删除
	    $(".inputArea").delegate(".expurgateBorder","click",function(){
	    	$(this).parents(".inputTitleEntity").remove();
	    })

	    // 提交回填数据
    	$(".tiJaoButton").click(function(){
    		$(".inputTitleEntity").each(function(i){
    			var danGe01=$(this).find("input").eq(0).val();
    			var danGe02=$(this).find("input").eq(1).val();
    			var danGe03=$(this).find("input").eq(2).val();
    			if(i==0){
    			}else{
    				if(danGe01==""&&danGe02==""&&danGe03==""){
						$(this).remove();
					}
				}
    		});
    		var jizhanMing=[];
    		var suLang=[];
    		var gongLv=[];
    		$(".designationBorder").each(function(){
    			var jack01=$(this).find("input").val();
    			if(jack01!=""){
    				jizhanMing.push(jack01);
    			}
    		});
    		$(".quantityBorder").each(function(){
    			var jack02=$(this).find("input").val();
    			if(jack02!=""){
    				suLang.push(jack02);
    			}
    		});
    		$(".rateWorkBorder").each(function(){
    			var jack03=$(this).find("input").val();
    			if(jack03!=""){
    				gongLv.push(jack03);
    			}
    		});
    		//第一层防护
    		if(jizhanMing.length == suLang.length && suLang.length == gongLv.length && jizhanMing.length != 0 && suLang.length != 0 && gongLv.length != 0){
    			//第二层防护
    			var fangHu=[];
    			var cs=0;
    			$(".inputTitleEntity input").each(function(i){
    				cs=i;
	    			var fangZhi=$(this).val();
	    			if(fangZhi != ""){
	    				fangHu.push(fangZhi);
	    			}
	    		});
	    		if(cs == fangHu.length-1){
		    		$http({
			          	method: 'POST',
			          	url: zsurl+'/xiaogan/dev_data_insert',
			          	data: $.param({  
			                sta_name: jiLv,
			                dev_name: jizhanMing.toString(),
			                count: suLang.toString(),
			                power: gongLv.toString()          
			            }),
			        headers:{'Content-type':'application/x-www-form-urlencoded'}
			        }).success(function (response) {
			        	console.log(response);
			            console.log(response.flag);
			            if(response.flag==1){
			            	layer.msg('提交成功!');
			            	$scope.hueiTianList();
			            	$(".designationBorder").find("input").val("");
				            $(".quantityBorder").find("input").val("");
				            $(".rateWorkBorder").find("input").val("");
			            }else{
			            	layer.msg("提交失败!");
			            }
			        }).error(function(r){
			            layer.msg("加载错误："+r);
			            $(".designationBorder").find("input").val("");
			            $(".quantityBorder").find("input").val("");
			            $(".rateWorkBorder").find("input").val("");
			        });
    			}else{
    				layer.msg("输入信息不能为空,请完善!");
    			}
    		}else{
	    		layer.msg("输入信息不能为空,请完善!");
		    }
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
	        	console.log(response);
	            $scope.htList=response.sta_data_list;
	            //遮罩层关闭
      			$(".la_index_mask").hide();
	        }).error(function(r){
	            layer.msg("加载错误："+r);
	        });
    	}
    	//编辑,取消
    	var preserveOne;
    	var preserveTwo;
    	var preserveThree;
    	$(".specific").delegate(".compile","click",function(){
    		preserveOne=$(this).parents(".exhibition").find(".sheBeiName").val();
    		preserveTwo=$(this).parents(".exhibition").find(".sheBeiNub").val();
    		preserveThree=$(this).parents(".exhibition").find(".sheBeiGl").val();
    		$(this).parents(".exhibition").find("input").css({"border":"1px solid #ddd"});
    		$(this).parents(".exhibition").find("input").attr("disabled",false);
    		$(this).hide();
    		$(this).siblings(".expurgate").hide();
    		$(this).siblings(".putIn").show();
    		$(this).siblings(".revocation").show();
    	});
    	$(".specific").delegate(".revocation","click",function(){
    		$(this).parents(".exhibition").find(".sheBeiName").val(preserveOne);
    		$(this).parents(".exhibition").find(".sheBeiNub").val(preserveTwo);
    		$(this).parents(".exhibition").find(".sheBeiGl").val(preserveThree);
    		$(this).parents(".exhibition").find("input").css({"border":"none"});
    		$(this).parents(".exhibition").find("input").attr("disabled",true);
    		$(this).hide();
    		$(this).siblings(".putIn").hide();
    		$(this).siblings(".expurgate").show();
    		$(this).siblings(".compile").show();
    	});
    	//删除
    	$scope.shanChu=function(val){
    		$http({
	          	method: 'POST',
	          	url: zsurl+'/xiaogan/del_device',
	          	data: $.param({  
	                id: val[0]
	            }),
	        	headers:{'Content-type':'application/x-www-form-urlencoded'}
	        }).success(function (response) {
	            console.log(response.flag);
	            if(response.flag==1){
	            	layer.msg("删除成功!");
	            	$scope.hueiTianList();
	            }else{
	            	layer.msg("删除失败!");
	            }
	        }).error(function(r){
	            layer.msg("加载错误："+r);
	        });
    	}
    	//修改提交
    	$(".specific").delegate(".putIn","click",function(){
    		var chanSu01=$(this).parents(".exhibition").find(".idName").val();
    		var chanSu02=$(this).parents(".exhibition").find(".sheBeiName").val();
    		var chanSu03=$(this).parents(".exhibition").find(".sheBeiNub").val();
    		var chanSu04=$(this).parents(".exhibition").find(".sheBeiGl").val();
    		$http({
	          	method: 'POST',
	          	url: zsurl+'/xiaogan/edit_devices',
	          	data: $.param({  
	                id: chanSu01,
	                sta_name: jiLv,
	                dev_name: chanSu02,
	                count: chanSu03,
	                power: chanSu04
	            }),
	        	headers:{'Content-type':'application/x-www-form-urlencoded'}
	        }).success(function (response) {
	            console.log(response.flag);
	            if(response.flag==1){
	            	layer.msg("修改成功!");
	            	$scope.hueiTianList();
	            }else{
	            	layer.msg("修改失败!");
	            }
	        }).error(function(r){
	            layer.msg("加载错误："+r);
	        });
    	});
        //点击查看发生的记录在根作用域上
        $rootScope.condition="off";
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});