var app=angular.module("myApp",["ui.router"]);
app.config(function($stateProvider , $urlRouterProvider){
    $urlRouterProvider.otherwise('/index');
    $stateProvider
    .state('/' , {
        url : "/index",
        templateUrl:'templates/index.html',
        controller : 'indexCtrl'
    })
    .state('index' , {
        url : "/index",
        templateUrl:'templates/index.html',
        controller : 'indexCtrl'
    })
    .state('abnormal' , {
        url : "/abnormal",
        templateUrl:'templates/abnormal.html',
        controller : 'abnormalCtrl'
    })
    .state('particulars' , {
        url : "/particulars",
        templateUrl:'templates/particulars.html',
        controller : 'particularsCtrl'
    })
    .state('entering' , {
        url : "/entering",
        templateUrl:'templates/entering.html',
        controller : 'enteringCtrl'
    })
     .state('entering.enteringone',{
        url:"/enteringone",
        templateUrl:'templates/enteringone.html',
        controller:'enteringoneCtrl'
    })
    .state('entering.enteringdetail',{
        url:"/enteringdetail",
        templateUrl:'templates/enteringdetail.html',
        controller:'enteringdetailCtrl'
    })
    .state('entering.enteringindividually',{
        url:"/enteringindividually",
        templateUrl:'templates/enteringindividually.html',
        controller:'enteringindividuallyCtrl'
    })
    .state('entering.enteringbulkimport',{
        url:"/enteringbulkimport",
        templateUrl:'templates/enteringbulkimport.html',
        controller:'enteringbulkimportCtrl'
    })
    .state('entering.enteringbatch',{
        url:"/enteringbatch",
        templateUrl:'templates/enteringbatch.html',
        controller:'enteringbatchCtrl'
    })
    .state('computermanage',{
        url:"/computermanage",
        templateUrl:'templates/computermanage.html',
        controller:'computermanageCtrl'
    })
    .state('equipment',{
        url:"/equipment",
        templateUrl:'templates/equipment.html',
        controller:'equipmentCtrl'
    })
    .state('equipment.equipmentone',{
        url:"/equipmentone",
        templateUrl:'templates/equipmentone.html',
        controller:'equipmentoneCtrl'
    })
    .state('equipment.basecontrast',{
        url:"/basecontrast",
        templateUrl:'templates/basecontrast.html',
        controller:'basecontrastCtrl'
    })
    .state('equipment.equipmentdetail',{
        url:"/equipmentdetail",
        templateUrl:'templates/equipmentdetail.html',
        controller:'equipmentdetailCtrl'
    })
    .state('equipment.linechart',{
        url:"/linechart",
        templateUrl:'templates/linechart.html',
        controller:'linechartCtrl'
    })
    .state('equipment.bulkimport',{
        url:"/bulkimport",
        templateUrl:'templates/bulkimport.html',
        controller:'bulkimportCtrl'
    })
    .state('entering.enteringbatchdetail',{
        url:"/enteringbatchdetail",
        templateUrl:'templates/enteringbatchdetail.html',
        controller:'enteringbatchdetailCtrl'
    })
    .state('insectSite',{
        url:"/insectSite",
        templateUrl:'templates/insectSite.html',
        controller:'insectSiteCtrl'
    })
    .state('meterReading',{
        url:"/meterReading",
        templateUrl:'templates/meterReading.html',
        controller:'meterReadingCtrl'
    })
    .state('equipmentresourcepower',{  //开关电源
        url:"/equipmentresourcepower",
        templateUrl:'templates/equipmentresourcepower.html',
        controller:'equipmentresourcepowerCtrl'
    })
    .state('equipmentresourceaccumulator',{  //蓄电池
        url:"/equipmentresourceaccumulator",
        templateUrl:'templates/equipmentresourceaccumulator.html',
        controller:'equipmentresourceaccumulatorCtrl'
    })
    .state('equipmentresourceconditioner',{   //空调
        url:"/equipmentresourceconditioner",
        templateUrl:'templates/equipmentresourceconditioner.html',
        controller:'equipmentresourceconditionerCtrl'
    })
    .state('equipmentresourceacdistribution',{ //交流配电箱
        url:"/equipmentresourceacdistribution",
        templateUrl:'templates/equipmentresourceacdistribution.html',
        controller:'equipmentresourceacdistributionCtrl'
    })
    .state('equipmentresourceout',{  //拉远站（交转直）
        url:"/equipmentresourceout",
        templateUrl:'templates/equipmentresourceout.html',
        controller:'equipmentresourceoutCtrl'
    })
    .state('equipmentresourcedirec',{//直流远供局端
        url:"/equipmentresourcedirec",
        templateUrl:'templates/equipmentresourcedirec.html',
        controller:'equipmentresourcedirecCtrl'
    })
    .state('equipmentresourceintegration',{ //一体化机柜
        url:"/equipmentresourceintegration",
        templateUrl:'templates/equipmentresourceintegration.html',
        controller:'equipmentresourceintegrationCtrl'
    })
    .state('equipmentresourceteansformer',{ //变压器
        url:"/equipmentresourceteansformer",
        templateUrl:'templates/equipmentresourceteansformer.html',
        controller:'equipmentresourceteansformerCtrl'
    })
    .state('equipmentresourceemergency',{ //应急油机
        url:"/equipmentresourceemergency",
        templateUrl:'templates/equipmentresourceemergency.html',
        controller:'equipmentresourceemergencyCtrl'
    }).state('resourceInventory',{ //资源清查
        url:"/resourceInventory",
        templateUrl:'templates/resourceInventory.html',
        controller:'resourceInventoryCtrl'
    }).state('tower',{ //铁塔
        url:"/tower",
        templateUrl:'templates/tower.html',
        controller:'towerCtrl'
    }).state('professionalCleaning',{ //专业清理统计表
        url:"/professionalCleaning",
        templateUrl:'templates/professionalCleaning.html',
        controller:'professionalCleaningCtrl'
    })
    
    
    
})
app.run(['$rootScope', '$window', '$location', '$log', function ($rootScope, $window, $location, $log) {
    var locationChangeStartOff = $rootScope.$on('$locationChangeStart', locationChangeStart);
    var isSecond = false;
    function locationChangeStart(event, newUrl, currentUrl) {
        if($location.path()=="/entering"){
            $location.path("entering/enteringone"); 
        }else if($location.path()=="/computermanage"){
            $location.path("computermanage/enteringone");
        }
    }
}]);