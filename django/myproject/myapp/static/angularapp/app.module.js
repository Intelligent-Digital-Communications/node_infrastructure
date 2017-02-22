'use strict';

angular.module('myApp', [
	'ngRoute',
	'myApp.scheduleRecordingController',
	'myApp.scheduleRecordingDirective',
	'myApp.scheduleRecordingService',
    'myApp.recordingTableController'
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
            when('/route2', {
                templateUrl: static_url + 'angularapp/html/test2.html',
                controller: 'RouteController2'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);
