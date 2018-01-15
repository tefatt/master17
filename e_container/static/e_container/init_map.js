function initMap(markers, path_colors) {

    // if (markers === undefined) {
    //     markers = eval($('#markers').data("markers"));
    // }
    // if (path_colors === undefined) {
    //     path_colors = eval($('#path_colors').data("path_colors"));
    // }
    var directionsService = new google.maps.DirectionsService;

    // Map options center on Sarajevo
    var options = {
        center: {lat: 43.8627, lng: 18.4001},
        zoom: 12
    };

    // New map
    var map = new google.maps.Map(document.getElementById('map'), options);

    // Loop through markers
    for (var x = 0; x < markers.length; x++) {
        var route = markers[x];
        var waypoints = [];
        for (var i = 0; i < route.length; i++) {

            // Add marker
            if (i == 0 || i == route.length - 1) continue;
            addMarker(route[i]);
            var coords = route[i].coords;
            waypoints.push({stopover: false, location: new google.maps.LatLng(coords.lat, coords.lng)});
        }
        calculateRoute(route[0].coords, route[route.length - 1].coords, waypoints, path_colors[x]);
    }

    // Add Marker Function
    function addMarker(props) {
        var marker = new google.maps.Marker({
            position: props.coords,
            map: map
            //icon:props.iconImage
        });

        // Check for custom icon
        if (props.iconImage) {
            // Set icon image
            marker.setIcon(props.iconImage);
        }

        // Check content
        if (props.content) {
            var infoWindow = new google.maps.InfoWindow({
                content: props.content
            });

            marker.addListener('click', function () {
                infoWindow.open(map, marker);
            });
        }
    }

    function calculateRoute(start, end, waypoints, color) {
        start = new google.maps.LatLng(start.lat, start.lng);
        end = new google.maps.LatLng(end.lat, end.lng);

        var request = {
            origin: start,
            destination: end,
            waypoints: waypoints,
            provideRouteAlternatives: true,
            // unitSystem: UnitSystem.METRIC,
            travelMode: 'DRIVING'
        };
        var directionsDisplay = new google.maps.DirectionsRenderer({
            polylineOptions: {strokeColor: color}
        });
        directionsDisplay.setMap(map);

        directionsService.route(request, function (result, status) {
            if (status == 'OK') {
                directionsDisplay.setDirections(result);
            }
        });
    }

}

$(document).ready(
    (function worker() {
        $.ajax({
            url: 'http://localhost:8000/services/return_new_routes/',
            type: "get",
            datatype: "json",
            success: function (data) {
                initMap(eval(data.markers), eval(data.path_colors));
                setTimeout(worker, 1200 * 1000);
            },
            complete: function () {
                // Schedule the next request when the current one's complete
            }
        });
    }())
);
