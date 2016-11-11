'use strict';

angular.module('myApp.recordingTableController', ['ngRoute'])

.
config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})

.controller('recordingController', function($scope, $http){
    /*$http.get("/myapp/schedule_session/").then(function(response) {$scope.names = response.data.records;});*/
    $scope.names = [ 
	    {"timedate":"10/27/2016 13:42","filename":"epoch0.sc16", 
	    "freq":"2412000000", "length":"5", "specrec":"45", "gain":"55", "ids":"[1,2,3]"},
	    {"timedate":"10/27/2016 13:47","filename":"epoch1.sc16",
	    "freq":"2412000000", "length":"5", "specrec":"45", "gain":"55", "ids":"[1,2,3]"}
    ];
})