app.controller('bulkimportCtrl', function($scope,$http,$filter) {
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
      //分类接口
      $scope.typeList=function(){
          $http({
              method: 'POST',
              url: zsurl+'/xiaogan/import_file_type',
          headers:{'Content-type':'application/x-www-form-urlencoded'}
          }).success(function (response) {
              console.log(response);
              $scope.moldSum=response.import_file_type;
              $scope.pitch=response.import_file_type[0];
          }).error(function(r){
              layer.msg("加载错误："+r);
          });
      };
      $scope.typeList();
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
      //分类点击选中事件
      $(".lk_border_box").click(function(){
          $(".lk_down_box").toggle();
          cancelBubble();
      });
      $(".lk_down_box").delegate(".parameter","click",function(){
          var p_name=$(this).text();
          $(".lk_border_box input").val(p_name);
          setTimeout(function(){
              $(".lk_down_box").toggle();
          },100);
          cancelBubble();
      });
      $("body").click(function(){
          $(".lk_down_box").hide();
      });
      //选择文件
      var FileExt="";
      var fileName="";
      var strFileName="";
      var state="ok";
      $("#file").change(function(){
          //获取文件名
          var file = $("#file").val();
              fileName = getFileName(file);
          function getFileName(o){
              var pos=o.lastIndexOf("\\");
              return o.substring(pos+1);  
          }
          strFileName=file.replace(/^.+?\\([^\\]+?)(\.[^\.\\]*?)?$/gi,"$1");
          FileExt=file.replace(/.+\./,"");
          $("#nameList").html("<li>"+fileName+"</li>");
      });
      //点击提交按钮
      var recordNub=0;
      $("#upload-button").click(function(){
          if(state=="ok"){
              var patt1=strFileName;
              if(patt1==""){
                  layer.msg("请先选择文件!");
                  return false;
              }else{
                  if(FileExt=="xls" || FileExt=="xlsx"){
                      //假的进度条
                      var matnNub=parseInt(Math.random()*70);
                      $(".planBar").show();
                      var l=0;
                      function time(){
                          if(l<matnNub){
                              l=l+1;
                              $(".progress-bar").css({"width":l+"%"});
                              setTimeout(function(){
                                  $(".progress-bar").html(l+"%");
                              },25);
                          }else{
                              recordNub=l;
                              clearInterval(dsTime);
                              $scope.tijiaoButton();
                          }
                      }
                      var dsTime=setInterval(time,50);
                  }else{
                      layer.msg("格式错误,上传格式只支持xls,xlsx");
                      return false;
                  }
              }
          }else{
              layer.msg("请等待上一个文件上传结束!");
              return false;
          }
      });
      //提交按钮
      $scope.tijiaoButton=function(){
          state="no";
          var formData = new FormData($( "#uploadForm" )[0]);  
          $.ajax({  
              url: zsurl+'/xiaogan/FileImport',
              type: 'POST',  
              data: formData,  
              async: false,  
              cache: false,  
              contentType: false,  
              processData: false,
              success: function (response) {  
                  console.log(response);
                  state="ok";
                  switch(response){
                      case 1:
                          function time02(){
                              if(recordNub<100){
                                  recordNub=recordNub+1;
                                  $(".progress-bar").css({"width":recordNub+"%"});
                                  setTimeout(function(){
                                      $(".progress-bar").html(recordNub+"%");
                                  },25);
                              }else{
                                  clearInterval(dsTime02);
                                  setTimeout(function(){
                                      layer.msg("提交成功!");
                                      $(".planBar").hide();
                                      window.location.reload();
                                  },1000);
                              }
                          }
                          var dsTime02=setInterval(time02,50);
                      break;
                      default:
                          layer.msg("提交失败!");
                          $(".planBar").hide();
                          window.location.reload();
                      break;
                  }
              },  
              error: function (r) {  
                  layer.msg("加载错误："+r);
                  window.location.reload();
              }  
          });  
      }
      //table表格(接口)
      var sumShuJv=0;
      function loadList(PageIndex){
        $.ajax({
          url: zsurl+'/xiaogan/showimport',
          type : "POST",
          dataType: "json",
          async: false, 
          data : {PageIndex : PageIndex},
          success : function(response){
            $scope.columnText=response.title_name;
            $scope.importList=response.page_resultList;
            $scope.pageCount=response.pageCount;
            $scope.rowCount=response.rowCount;
            sumShuJv=$scope.rowCount;
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
                  }
              }
          });
      }
      $(function () {
          loadData(1);
          loadpage();
      });
      //table表格删除单条记录(接口)
      $scope.loadList1=function(deliteId){
          $http({
              method: 'POST',
              url: zsurl+'/xiaogan/show_delete',
              data: $.param({
                  file_id : deliteId
              }),
          headers:{'Content-type':'application/x-www-form-urlencoded'}
          }).success(function (response) {
              console.log(response);
              $(function () {
                loadData(1);
                loadpage();
              });
          }).error(function(r){
              layer.msg("加载错误："+r);
          });
      }
      //table表格删除单条记录按钮
      $scope.delete=function(item){
          console.log(item[0]);
          if(window.confirm('你确定要删除记录吗？')){
              $scope.loadList1(item[0]);
              return true;
          }else{
              return false;
          }
      };
    }
});
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});