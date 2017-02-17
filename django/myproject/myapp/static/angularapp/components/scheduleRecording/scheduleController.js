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
    $scope.recordings = [{}];

    $scope.reset = function() {

        for(var i = 0; i < $scope.recordings.length; i++) {

            $scope.recordings[i].starttime = $scope.recordings[i].date + " " + $scope.recordings[i].time;
            $scope.recordings[i].recordpath = "/opt/test/epoch" + i + ".sc16";
            delete $scope.recordings[i].date;
            delete $scope.recordings[i].time;
            delete $scope.recordings[i].name;
        }
        $scope.newObject = {"recordings" : $scope.recordings, "name": "test", "startingpath": "/opt/test", "logpath": "/opt/test", "rfsnids": [0]}
        console.log($scope.newObject);
        fileUpload.uploadForm($scope.newObject);
    };

    $scope.addTo = function(array, template) {
    array.push(template);
  };

}]);
