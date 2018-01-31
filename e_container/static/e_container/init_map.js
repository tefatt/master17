// dumps for last routes
var last_markers = [];
var last_directions_display;

function initMap(mun_markers, mun_name, route_index) {
    // Map options center on Sarajevo
    var options = {
        center: {lat: 43.8627, lng: 18.4001},
        zoom: 12
    };

    // New map
    var map = new google.maps.Map(document.getElementById('map'), options);
    var directionsService = new google.maps.DirectionsService;

    if (mun_markers === undefined) {
        var temp = $('#mun_markers').data("mun_markers");
        temp = temp.replace(/'/g, '"');
        mun_markers = JSON.parse(temp);

    }

    if (mun_markers.length === 0) {
        return;
    }

    console.log(mun_markers);

    // Loop through markers and display the selected ones
    var route_to_display = [];
    for (var m in mun_markers) {
        if (mun_markers.hasOwnProperty(m)) {
            if (mun_markers[m].length != 0) {
                if (m === mun_name) route_to_display.push(mun_markers[m][route_index]);
                else route_to_display.push(mun_markers[m][0]);
            }
        }
    }

    municipality_init(route_to_display, directionsService, map);
}

$(document).ready(function () {
    $(".route").click(function () {
        var route_index = this['value'];
        var mun_name = this['parentElement']['previousElementSibling']['id'];
        var mun_markers = document.getElementById('mun_markers').value;
        initMap(mun_markers, mun_name, route_index);
    });
});

function municipality_init(markers, directionsService, map) {
    markers = markers[0];
    for (var x = 0; x < markers.length; x++) {
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

    }
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
    if (directionsDisplay === undefined) return;
    directionsDisplay.setMap(null);
}

$(document).ready(
    (function worker() {
        $.ajax({
            url: 'http://127.0.0.1:8000/services/return_new_routes/',
            type: "get",
            datatype: "json",
            success: function (data) {
                var mun_markers = document.getElementById('mun_markers');
                mun_markers.value = data.mun_markers;
                initMap(eval(data.mun_markers));
                setTimeout(worker, 1200 * 1000);
            },
            complete: function () {
                // Schedule the next request when the current one's complete
            }
        });
    }));


