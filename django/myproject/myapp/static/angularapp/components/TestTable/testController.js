'use strict';

angular.module('myApp.testController', ['ngRoute'])

.controller('testController', ['$scope', '$http', function($scope, $http){
    $http({
            method: 'GET',
            url: '/myapp/rfsns'
        }).success(function (result) {
        $scope.rfsnList = result;
    });
}]);
