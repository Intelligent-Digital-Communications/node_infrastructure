'use strict';

angular.module('myApp.scheduleRecordingService', ['ngRoute'])

.service('fileUpload', ['$http', function ($http) {
	return {
	    uploadFileToUrl: function(file, uploadUrl){
	        var fd = new FormData();
	        fd.append('docfile', file);
	        $http.post(uploadUrl, fd, {
	            transformRequest: angular.identity,
	            headers: {'Content-Type': undefined}
	        })
	        .success(function(){
	            alert("Success");
	        })
	        .error(function(){
	            alert("Uploading file failed");
	        });
	    },

        uploadForm: function(object) {
        	$http.post("/myapp/schedule_form/", object)
        	.success(function() {
                alert("Success");
            }).error(function(){
                alert("Failed");
            });
        }
	}
}]);
