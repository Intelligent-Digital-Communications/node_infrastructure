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
	            alert("There was an error scheduling. Contact someone on the SysOps team");
	        });
	    },

        uploadForm: function(object) {
        	$http.post("/myapp/schedule_form/", object)
        	.success(function() {
                alert("Success");
            }).error(function(){
	            alert("There was an error scheduling. Contact someone on the SysOps team");
	        });
        }
	}
}]);
