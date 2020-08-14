var firebaseConfig = {
    apiKey: "AIzaSyAf58ybK5T7_dZr10b4tum-XAu3aqu1v_Q",
    authDomain: "social-distancing-monito-c9b2c.firebaseapp.com",
    databaseURL: "https://social-distancing-monito-c9b2c.firebaseio.com/",
    projectId: "social-distancing-monito-c9b2c",
    storageBucket: "social-distancing-monito-c9b2c.appspot.com",
    messagingSenderId: "847811129335",
    appId: "1:847811129335:web:505c7263ef941efeaf88f2",
    measurementId: "G-H2DKQT2CK8"
  };
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
//   firebase.analytics();

var ref = firebase.database().ref();

var data;

ref.on('child_added', function(child) {
    console.log('child added:');
    data = child.val();
    addMarker(data);
});
ref.on('child_changed', function(child) {
    console.log('child changed:');
    data = child.val();
    updateMarker(data);
});

var map;

// var markers = [
//     // {
//     //     coords: {lat:32.7767,lng:-96.7970}, //dallas
//     //     index: 25,
//     //     content: '<h1 style="color=black;">Location</h1>'
//     // },
//     {
//         coords:{lat:32.7555,lng:-97.3308}, //fort worth
//         index: 40,
//         content: '<p style="color=black;">60% of people wear masks at this location</p>'
//     },
//     {
//         coords:{lat:32.7357,lng:-97.1081}, //arlington
//         index: 60,
//         content: '<p style="color=black;">95% of people wear masks at this location</p>'
//     },
//     {
//         coords:{lat:33.1507,lng:-96.8236}, //frisco
//         index: 99,
//         content: '<p style="color=black;">95% of people wear masks at this location</p>'
//     }
// ];

var markers = [];
var windows = [];

function initMap(){
    var options = {
        zoom:9,
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



    // for(var i = 0; i < markers.length; i++){
    //     addMarker(markers[i]);
    // }

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
            infoWindow.setContent('<h8 style="color:black">Current Location</h8>');
            infoWindow.open(map);
            map.setCenter(pos);
            windows.push(infoWindow);
        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        handleLocationError(false, infoWindow, map.getCenter());
    }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
    }

    google.maps.event.addListener(map, "click", function(event) {
        for (var i = 0; i < windows.length; i++ ) {
             windows[i].close();
        }
    });


}

function addMarker(props){
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(props.lat, props.lng),
        map:map,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 15,
            fillColor: '#000000',
            fillOpacity: 0.35,
            strokeColor: '#000000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
        },
    });

    updateColor(props, marker);

    // add info window
    var infoWindow = new google.maps.InfoWindow({
        content: `<h8 style="color:black">${props.avgIndex}% mask-wearers in this area</h8>`
    });

    marker.addListener('click', function(){
        infoWindow.open(map, marker);
    })

    windows.push(infoWindow);

    markers.push(marker);
}

function updateMarker(newMarker){
    for (var i=0; i < markers.length; i++) {
        var m = markers[i];
        if (m.getPosition().lat() === newMarker.lat && m.getPosition().lng() === newMarker.lng) {
            updateColor(newMarker, m);
        }
    }

}

function updateColor(newMarker, m){
    var mag = newMarker.avgIndex;
    var cFill;
    var cStroke;
    if(mag < 25){ 
        cFill = "#FF0000"
        cStroke = "#FF0000"
    }
    else if(mag >= 25 && mag < 50){
        cFill = "#FFA500"
        cStroke = "#FFA500"
    }
    else if(mag >= 50 && mag < 75){
        cFill = "#FFFF00"
        cStroke = "#FFFF00"
    }
    else{
        cFill = "#00FF00"
        cStroke = "#00FF00"
    }

    const icon = {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 15,
        fillColor: cFill,
        fillOpacity: 0.35,
        strokeColor: cStroke,
        strokeOpacity: 0.8,
        strokeWeight: 2,
    };

    m.setIcon(icon);
}