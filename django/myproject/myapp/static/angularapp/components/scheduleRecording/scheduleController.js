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
    $scope.session = {};

    $scope.submitForm = function() {

        for(var i = 0; i < $scope.recordings.length; i++) {
            var date = parseDate($scope.recordings[i].date);
            $scope.recordings[i].starttime = date + " " + $scope.recordings[i].time;
            $scope.recordings[i].recordpath = "/opt/test/epoch" + i + ".sc16";
            $scope.recordings[i].frequency = $scope.recordings[i].frequency * 1000000;
            delete $scope.recordings[i].date;
            delete $scope.recordings[i].time;
        }

        $scope.session = {
            "recordings" : $scope.recordings,
            "name": $scope.session.name, 
            "startingpath": $scope.session.startingpath, 
            "logpath": $scope.session.logpath , 
            "rfsnids": [0]
        }
        console.log($scope.session);
        fileUpload.uploadForm($scope.session);
        $scope.recording = {};
        $scope.recordings = [{}];
        $scope.session = {};
    };

    var parseDate = function(date) {
        var arr = date.split("-");
        var newStr = arr[1] + "/" + arr[2] + "/" + arr[0];
        return newStr; 
    }

    $scope.addTo = function(array, template) {
    array.push(template);
  };

}]);
