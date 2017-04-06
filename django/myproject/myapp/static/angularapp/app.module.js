'use strict';

angular.module('myApp', [
	'ngRoute',
	'myApp.scheduleRecordingController',
	'myApp.scheduleRecordingDirective',
	'myApp.scheduleRecordingService',
    'myApp.recordingTableController',
	'myApp.testController'
]).
config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
}).
config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/schedule', {
                templateUrl: static_url + 'angularapp/components/scheduleRecording/scheduleView.html',
                controller: 'scheduleController'
            }).
            when('/viewRecordings', {
                templateUrl: static_url + 'angularapp/components/recordingTable/recordingView.html',
                controller: 'recordingController'
            }).
            when('/RFSNS', {
                templateUrl: static_url + 'angularapp/components/TestTable/TestView.html',
                controller: 'testController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);
