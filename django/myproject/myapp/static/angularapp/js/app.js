var myApp = angular.module("myApp", ['ngRoute']);
myApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})
myApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/route1', {
                templateUrl: static_url + 'angularapp/html/test1.html',
                controller: 'RouteController1'
            }).
            when('/route2', {
                templateUrl: static_url + 'angularapp/html/test2.html',
                controller: 'RouteController2'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);

myApp.controller("RouteController1", function($scope) {
    $scope.test="Angular working for test1"
});
myApp.controller("RouteController2", function($scope) {
    $scope.test="Angular working for test2"
});


myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('docfile', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
            alert("Success");
        })
        .error(function(){
            alert("Uploading file failed");
        });
    }
}]);

myApp.controller('myCtrl', ['$scope', 'fileUpload', function($scope, fileUpload){
    
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = "/myapp/upload_file/";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
    
}]);
