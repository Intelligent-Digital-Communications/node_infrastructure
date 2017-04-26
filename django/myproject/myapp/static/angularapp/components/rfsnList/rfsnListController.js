'use strict';

angular.module('myApp.rfsnListController', ['ngRoute'])

.controller('rfsnListController', ['$scope', '$http', function($scope, $http){
    $http({
            method: 'GET',
            url: '/myapp/rfsns'
        }).success(function (result) {
        $scope.rfsnList = result;
    });
}]);
