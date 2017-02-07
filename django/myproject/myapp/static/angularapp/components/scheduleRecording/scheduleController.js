'use strict';

angular.module('myApp.scheduleRecordingController', ['ngRoute'])

.controller('scheduleController', ['$scope', 'fileUpload', function($scope, fileUpload){
    $scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = "/myapp/upload_file/";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };

    $scope.recording = {};
    $scope.reset = function() {
        //$scope.user = angular.copy($scope.master);
        console.log($scope.recording);
    };

}]);
