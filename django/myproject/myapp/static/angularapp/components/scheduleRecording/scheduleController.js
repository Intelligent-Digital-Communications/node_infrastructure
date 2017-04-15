'use strict';

angular.module('myApp.scheduleRecordingController', ['ngRoute'])

.controller('scheduleController', ['$scope', '$http', '$filter', 'fileUpload', function($scope, $http, $filter, fileUpload, rfsns){

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
    // Default values
    // var d = new Date();
    // $scope.recordings[0].time = d.getHours() + ":" + d.getMinutes();
    // $scope.recordings[0].date = $filter("date")(d, 'yyyy-MM-dd');
    // $scope.recordings[0].gain = 55;
    // $scope.recordings[0].frequency= '2.4E+9';
    //
    // $scope.session.startearly = 60;
    // $scope.session.logpath = 'log.txt';
    // $scope.session.samplerate = '25e6';
    var setDefaults = function() {
        var d = new Date();
        // Default values
        $scope.recordings[0].time = d.getHours() + ":" + d.getMinutes();
        $scope.recordings[0].date = $filter("date")(d, 'yyyy-MM-dd');
        $scope.recordings[0].gain = 55;
        $scope.recordings[0].frequency= '2.4E+9';

        $scope.session.startearly = 60;
        $scope.session.logpath = 'log.txt';
        $scope.session.samplerate = '25e6';
    }

    setDefaults();


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
        setDefaults();
    };

    var parseDate = function(date) {
        var arr = date.split("-");
        var newStr = arr[1] + "/" + arr[2] + "/" + arr[0];
        return newStr;
    }

    // Don' need this anymore. Backend handles it
    /*var convertSciNotation = function(num) {
        num = num.replace(/\s+/, "");
        if (num.includes("e")) {
            var temp = num.split("e");
            num = temp[0] * (10 ** temp[1]);
        } else if (num.includes("E+")) {
            var temp = num.split("E+");
            num = temp[0] * (10 ** temp[1]);
        } else if (num.includes("E")) {
            var temp = num.split("E");
            num = temp[0] * (10 ** temp[1]);
        }
        return num;
    }*/


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
