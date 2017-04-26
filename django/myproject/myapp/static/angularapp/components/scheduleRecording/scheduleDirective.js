'use strict';

angular.module('myApp.scheduleRecordingDirective', ['ngRoute'])


.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

angular.module('myApp.scheduleRecordingInputDirective', ['ngRoute'])

.directive('input', function() {
    return {
        restrict: 'E',
        priority: -1,
        link: function(scope, element, attrs) {
            if (attrs.type == 'date' || attrs.type == 'time') {
                $(element).updatePolyfill();
            }
        }
    };
});
