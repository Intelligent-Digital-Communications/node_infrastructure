'use strict';

angular.module('myApp.recordingTableController', ['ngRoute'])

.
config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.controller('recordingController', function($scope, $http){
    //$http.get("/myapp/recording_list/").then(function(response) {$scope.recordings = response.data.records;});
    $http({
            method: 'GET',
            url: '/myapp/recording_list'
        }).success(function (result) {
        $scope.recordings = result;
    });
})
