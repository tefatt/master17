function initMap(markers) {

    if (markers === undefined) return;

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
        var node = document.createElement("option");
        node.id = x;
        node.value = x;
        node.innerHTML = "Route " + (x + 1).toString();
        document.getElementById("route-selector").appendChild(node);
    }
    document.getElementById('route-selector').value = "0";


    var onChangeHandler = function () {
        x = document.getElementById("route-selector").selectedIndex;
        var route = markers[x];
        var waypoints = [];
        removeMarkers(last_markers);
        removeDirectionsDisplay(last_directions_display);
        for (var i = 0; i < route.length; i++) {
            // Add marker
            if (i == 0 || i == route.length - 1) continue;
            last_markers.push(addMarker(map, route[i]));
            var coords = route[i].coords;
            waypoints.push({stopover: false, location: new google.maps.LatLng(coords.lat, coords.lng)});
        }
        last_directions_display = calculateRoute(map, directionsService, route[0].coords, route[route.length - 1].coords, waypoints);
    };
    // initial route display
    var last_markers = [];
    var last_directions_display;
    onChangeHandler();
    document.getElementById('route-selector').addEventListener('change', onChangeHandler);
}

function addMarker(map, props) {
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

        marker.addListener('mouseover', function () {
            infoWindow.open(map, marker);
        });
        marker.addListener('mouseout', function () {
            infoWindow.close(map, marker);
        });
    }
    return marker;
}

function removeMarkers(markers) {
    for (var i = 0; i < markers.length; i++)
        markers[i].setMap(null);
}

function calculateRoute(map, directionsService, start, end, waypoints) {
    start = new google.maps.LatLng(start.lat, start.lng);
    end = new google.maps.LatLng(end.lat, end.lng);

    var request = {
        origin: start,
        destination: end,
        waypoints: waypoints,
        provideRouteAlternatives: false,
        // unitSystem: UnitSystem.METRIC,
        travelMode: 'DRIVING'
    };
    var directionsDisplay = new google.maps.DirectionsRenderer({});
    directionsDisplay.setMap(map);
    directionsService.route(request, function (result, status) {
        if (status == 'OK') {
            directionsDisplay.setDirections(result);
        }
        else {
            window.alert('Directions request failed due to ' + status);
        }
    });
    return directionsDisplay;
}

function removeDirectionsDisplay(directionsDisplay) {
    if (directionsDisplay===undefined) return;
    directionsDisplay.setMap(null);
}

$(document).ready(
    (function worker() {
        $.ajax({
            url: 'http://127.0.0.1:8000/services/return_new_routes/',
            type: "get",
            datatype: "json",
            success: function (data) {
                initMap(eval(data.markers));
                setTimeout(worker, 1200 * 1000);
            },
            complete: function () {
                // Schedule the next request when the current one's complete
            }
        });
    }())
);

