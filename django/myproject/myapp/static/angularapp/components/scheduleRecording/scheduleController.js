'use strict';

angular.module('myApp.scheduleRecordingController', ['ngRoute'])

.controller('scheduleController', ['$scope', '$http', 'fileUpload', function($scope, $http, fileUpload, rfsns){

    $scope.rfsns = {};

    $http({
            method: 'GET',
            url: '/myapp/rfsns'
        }).success(function (result) {
        $scope.rfsnList = result;
    });

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
    $scope.offset = {};
    $scope.length = $scope.recordings.length;

    $scope.submitForm = function() {
        var ids = [];
        Object.keys($scope.rfsns).forEach(function(key){
            ids.push(key);
        });

        for(var i = 0; i < $scope.recordings.length; i++) {
            var date = parseDate($scope.recordings[i].date);
            $scope.recordings[i].starttime = date + " " + $scope.recordings[i].time;
            $scope.recordings[i].recordpath = $scope.session.startingpath + "epoch" + i + ".sc16";
            $scope.recordings[i].frequency = $scope.recordings[i].frequency * 1000000;
            delete $scope.recordings[i].date;
            delete $scope.recordings[i].time;
        }

        $scope.session = {
            "recordings" : $scope.recordings,
            "name": $scope.session.name,
            "startingpath": $scope.session.startingpath,
            "startearly": $scope.session.startearly,
            "logpath": $scope.session.logpath ,
            "samplerate": $scope.session.samplerate,
            "rfsnids": ids
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

    $scope.addTo = function() {
        $scope.recordings.push({
            'frequency': $scope.recordings[0].frequency,
            'gain': $scope.recordings[0].gain,
            'date' : $scope.recordings[0].date,
            'length' : $scope.recordings[0].length,
            'time' : $scope.recordings[0].time
            
        });
  };

}]);
