'use strict';

angular.module('myApp', [
	'ngRoute',
	'myApp.scheduleRecordingController',
	'myApp.scheduleRecordingDirective',
	'myApp.scheduleRecordingService',
    'myApp.recordingTableController',
	'myApp.rfsnListController'
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
            when('/rfsns', {
                templateUrl: static_url + 'angularapp/components/rfsnList/rfsnListView.html',
                controller: 'rfsnListController'
            }).
            otherwise({
                redirectTo: '/rfsns'
            });
    }]);
