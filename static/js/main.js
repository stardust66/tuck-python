var app = angular.module("tuckToGo", ["ngCookies"]);

// Prevent conflicts between Flask templates and angular templates
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller("loginCtrl", ["$cookies", "$scope", "$rootScope", function($cookies, $scope, $rootScope) {
  if ($cookies.get("user_email")) {
    $rootScope.logged_in = true;
    $rootScope.user_name = $cookies.get("user_name");
  }

  $scope.logout = function() {
    $cookies.remove("user_email");
    $cookies.remove("user_name");
    $rootScope.logged_in = false;
    $rootScope.user_name = "";
  }
}]);
