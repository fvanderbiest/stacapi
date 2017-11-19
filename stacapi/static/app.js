var app = angular.module('myApp', []);

//~ var direction = 1;
//~ var stopid = 2200918;
//~ var logicalstopid = 132949;

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{-');
  $interpolateProvider.endSymbol('-}');
}]);



app.controller('myCtrl', function($scope, $http) {

    $scope.etas = [];
    $scope.directions = [];
    
    var STOPS = [];
    
    var refresh = function(lineid, stopid, direction) {
        $http.get([
            "/realtime",
            lineid,
            stopid,
            direction].join("/")
        ).then(function(r){
            $scope.etas = r.data.nextbuses;
        }, function(r){
            $scope.error = "Echec à récupérer les informations !";
        });
    };
    
    // Chargement des données initiales lignes et stops:
    $http.get("/lines").then(function(r){
        $scope.lines = r.data.lines;
        // pick the first one:
        $scope.line = r.data.lines[0];
        //$scope.lineChanged();
        
        $scope.directions = [{
            id: 1, name: $scope.line.direction1
        }, {
            id: 2, name: $scope.line.direction2
        }];
        $scope.direction = $scope.directions[0];
        
        $http.get("/stops").then(function(rs){
            STOPS = rs.data.stops;
            // pick the first one matching the chosen line:
            //~ var stop = STOPS[0], i = 0;
            //~ while (stop.line_id != r.data.lines[0].id) {
                //~ i += 1;
                //~ stop = STOPS[i];
            //~ }
            var stops = [], stop;
            for (i = 0; i < STOPS.length; i++) {
                if (STOPS[i].line_id == $scope.line.id) {
                    stops.push(STOPS[i]);
                    stop = STOPS[i];
                }
            }
            $scope.stops = stops;
            $scope.stop = stop;
            
            refresh($scope.line.id, $scope.stop.id, $scope.direction.id)
        }, function(r){
            $scope.error = "Echec à récupérer les informations de stops";
        });
        
    }, function(r){
        $scope.error = "Echec à récupérer les informations de ligne";
    });

    
    $scope.lineChanged = function(){
        // raffraichir / filter la liste des stops
        // raffraichir la liste des directions
        var stops = [];
        for (i = 0; i < STOPS.length; i++) {
            if (STOPS[i].line_id == $scope.line.id) {
                stops.push(STOPS[i]);
            }
        }
        $scope.stops = stops;
        $scope.stop = stops[0];
        
        $scope.directions = [{
            id: 1, name: $scope.line.direction1
        }, {
            id: 2, name: $scope.line.direction2
        }];
        $scope.direction = $scope.directions[0];
        
        // relancer au besoin requete sur realtime
        
        //if ($scope.stop && $scope.direction) {
        refresh($scope.line.id, $scope.stop.id, $scope.direction.id)
        //}
    }
    

    $scope.stopChanged = function(){
        // raffraichir / filter la liste des lignes à partir de ce point
        // raffraichir la liste des directions à partir de ce point 
        
        // relancer au besoin requete sur realtime
        refresh($scope.line.id, $scope.stop.id, $scope.direction.id)
    }

    $scope.directionChanged = function(){
        refresh($scope.line.id, $scope.stop.id, $scope.direction.id)
    }
});