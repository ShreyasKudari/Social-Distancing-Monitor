function initMap(){
    var options = {
        zoom:8,
        center:{lat:32.7767,lng:-96.7970}
    }

    var map = new google.maps.Map(document.getElementById('map'), options);
    
    /*
    var marker = new google.maps.Marker({
        position:{lat:32.7767,lng:-96.7970},
        map:map,
        // icon:''
    });

    var infoWindow = new google.maps.InfoWindow({
        content: '<h1>Dallas TX</h1>'
    });

    marker.addListener('click', function(){
        infoWindow.open(map, marker);
    })*/

    var markers = [
        {
            coords:{lat:32.7767,lng:-96.7970},
            icon: {
                url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
            },
            content: '<h1 style="color=black;">Location</h1>'
        },
        {
            coords:{lat:32.7555,lng:-97.3308},
            icon: {
                url: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
            },
            content: '<p style="color=black;">60% of people wear masks at this location</p>'
        },
        {
            coords:{lat:32.7357,lng:-97.1081},
            icon: {
                url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            },
            content: '<p style="color=black;">95% of people wear masks at this location</p>'
        }
    ];

    for(var i = 0; i < markers.length; i++){
        addMarker(markers[i]);
    }

    // var markers = locations.map(function(location, i) {
    //     return new google.maps.Marker({
    //         position: location,
    //         label: labels[i % labels.length]
    //     });
    // });

    // var locations = [
    //     {lat: -31.563910, lng: 147.154312},
    //     {lat: -33.718234, lng: 150.363181},
    //     {lat: -33.727111, lng: 150.371124},
    //     {lat: -33.848588, lng: 151.209834},
    //     {lat: -33.851702, lng: 151.216968},
    //     {lat: -34.671264, lng: 150.863657},
    //     {lat: -35.304724, lng: 148.662905},
    //     {lat: -36.817685, lng: 175.699196},
    //     {lat: -36.828611, lng: 175.790222},
    //     {lat: -37.750000, lng: 145.116667},
    //     {lat: -37.759859, lng: 145.128708},
    //     {lat: -37.765015, lng: 145.133858},
    //     {lat: -37.770104, lng: 145.143299},
    //     {lat: -37.773700, lng: 145.145187},
    //     {lat: -37.774785, lng: 145.137978},
    //     {lat: -37.819616, lng: 144.968119},
    //     {lat: -38.330766, lng: 144.695692},
    //     {lat: -39.927193, lng: 175.053218},
    //     {lat: -41.330162, lng: 174.865694},
    //     {lat: -42.734358, lng: 147.439506},
    //     {lat: -42.734358, lng: 147.501315},
    //     {lat: -42.735258, lng: 147.438000},
    //     {lat: -43.999792, lng: 170.463352}
    // ]    

    function addMarker(props){
        var marker = new google.maps.Marker({
            //position:coords,
            position:props.coords,
            map:map,
            // icon:''
        });

        // checking for custom icon
        if(props.icon){
            marker.setIcon(props.icon);
        }

        // checking for content
        if(props.content){
            var infoWindow = new google.maps.InfoWindow({
                content:props.content
            });

            marker.addListener('click', function(){
                infoWindow.open(map, marker);
            })
        }

        
    }

    // var markerCluster = new google.map.MarkerCluster(map, markers, {imagePath:'images/'});


    var infoWindow = new google.maps.InfoWindow;
    // Include geolocation of user
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            map.setCenter(pos);
        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
    }

}
