var map;

fetch('/hello')
    .then(function (response) {
        console.log('Success!', response);
        //return response.json();
    }).then(function (data) {
        console.log('GET response as JSON: ');
        console.log(data);
    }).catch(function (err) {
        console.warn('Something went wrong.', err);
    });    



//var infoObject = JSON.parse()


var markers = [
    {
        coords: {lat:32.7767,lng:-96.7970}, //dallas
        index: 25,
        content: '<h1 style="color=black;">Location</h1>'
    },
    {
        coords:{lat:32.7555,lng:-97.3308}, //fort worth
        index: 40,
        content: '<p style="color=black;">60% of people wear masks at this location</p>'
    },
    {
        coords:{lat:32.7357,lng:-97.1081}, //arlington
        index: 60,
        content: '<p style="color=black;">95% of people wear masks at this location</p>'
    },
    {
        coords:{lat:33.1507,lng:-96.8236}, //frisco
        index: 99,
        content: '<p style="color=black;">95% of people wear masks at this location</p>'
    }
];

function initMap(){
    var options = {
        zoom:8,
        center:{lat:32.7767,lng:-96.7970}
    }

    map = new google.maps.Map(document.getElementById('map'), options);
    
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



    for(var i = 0; i < markers.length; i++){
        addMarker(markers[i]);
    }

    // var markers = locations.map(function(location, i) {
    //     return new google.maps.Marker({
    //         position: location,
    //         label: labels[i % labels.length]
    //     });
    // });


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

function addMarker(props){
    var cFill;
    var cStroke;
    mag = props.index;
    // red, orange, yellow, green
    if(mag < 25){ 
        cFill = "#FF0000"
        cStroke = "#FF0000"
    }
    else if(mag >= 25 && mag < 50){
        cFill = "#FF6600"
        cStroke = "#FF6600"
    }
    else if(mag >= 50 && mag < 75){
        cFill = "#FFFF00"
        cStroke = "#FFFF00"
    }
    else{
        cFill = "#00FF00"
        cStroke = "#00FF00"
    }

    var marker = new google.maps.Marker({
        position:props.coords,
        map:map,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 25,
            fillColor: cFill,
            fillOpacity: 0.35,
            strokeColor: cStroke,
            strokeOpacity: 0.8,
            strokeWeight: 2
        },
    });

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