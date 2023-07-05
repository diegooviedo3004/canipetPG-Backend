// // mapeo
// let marcadores = [];
// function initAutocomplete() {
//   const map = new google.maps.Map(document.getElementById("map"), {
//     center: { lat: 12.11748259762615, lng: -86.26703253421367 },
//     zoom: 13,
//     mapTypeId: "roadmap",
//     mapId: "578064e81e64e0ba"
//   });

//   //Evente de agregar marcador
//   // This event listener calls addMarker() when the map is clicked.
//   google.maps.event.addListener(map, "click", (event) => {
    
    
//     addMarker(event.latLng, map);
//     //console.log(event.latLng.toLocaleString())
//     if (marcadores.length > 1) {
//       hideMarkers();


//     }
   
 


//   });

//   /*agrega los marcadores*/
//   function addMarker(location, map) {
//     // Add the marker at the clicked location, and add the next-available label
//     // from the array of alphabetical characters.

//     let marker = new google.maps.Marker({
//       position: location,
      
//       // label: labels[labelIndex++ % labels.length],
//       map: map,
//     });
//     marcadores.push(marker);

//     //console.log(marcadores);

//   }


//   // Create the search box and link it to the UI element.
//   const input = document.getElementById("pac-input");
//   const searchBox = new google.maps.places.SearchBox(input);
  

//   // Bias the SearchBox results towards current map's viewport.
//   map.addListener("bounds_changed", () => {
//     searchBox.setBounds(map.getBounds());
//   });

//   let markers = [];

//   // Listen for the event fired when the user selects a prediction and retrieve
//   // more details for that place.
//   searchBox.addListener("places_changed", () => {
//     const places = searchBox.getPlaces();
//     //*marcadores de busqueda*//
//     console.log(places);
   
//     if (places.length == 0) {
//       return;
//     }
// //////
//     // Clear out the old markers.
//     markers.forEach((marker) => {
//       marker.setMap(null);
//     });
//     markers = [];

//     // For each place, get the icon, name and location.
//     const bounds = new google.maps.LatLngBounds();

//     places.forEach((place) => {
//       if (!place.geometry || !place.geometry.location) {
//         console.log("Returned place contains no geometry");
//         return;
//       }

//       const icon = {
//         url: place.icon,
//         size: new google.maps.Size(71, 71),
//         origin: new google.maps.Point(0, 0),
//         anchor: new google.maps.Point(17, 34),
//         scaledSize: new google.maps.Size(25, 25),
//       };

//       // Create a marker for each place.
//       markers.push(
//         new google.maps.Marker({
//           map,
//           icon,
//           title: place.name,
//           position: place.geometry.location,
//         })
//       );
//       if (place.geometry.viewport) {
//         // Only geocodes have viewport.
//         bounds.union(place.geometry.viewport);
//       } else {
//         bounds.extend(place.geometry.location);
//       }
//     });
//     map.fitBounds(bounds);
//   });

//   /*montar marcadores*/
//   function setMapOnAll(map) {

//     //console.log(marcadores); 
//     marcadores[0].setMap(map);
//     marcadores.shift()

//   }

//   // Removes the markers from the map, but keeps them in the array.
//   function hideMarkers() {
//     setMapOnAll(null);
//   }


// }


// window.initAutocomplete = initAutocomplete;

//********//
let map;
let marcadores= [];


function initMap() {
    const bangalore = { lat: 12.382645880308907, lng: -85.51629206686383};
    map = new google.maps.Map(document.getElementById("map"), {
    center: { lat:12.382645880308907, lng: -85.51629206686383 },
    zoom: 17,
  });




  // Add a marker at the center of the map.
  addMarker(bangalore, map);


// Adds a marker to the map.
function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.

  let marker = new google.maps.Marker({
    position: location,
   // label: labels[labelIndex++ % labels.length],
    map: map,
  });
  marcadores.push(marker);

  //console.log(marcadores);

}

//console.log("L" + marcadores.length


// setea el marcador de la posicion 0 y elimina el ultimo elemento de la lista de marcadores
function setMapOnAll(map) {

    //console.log(marcadores);
    marcadores[0].setMap(map);
    marcadores.shift()

  }

  // Removes the markers from the map, but keeps them in the array.
  function hideMarkers() {
    setMapOnAll(null);
  }



}


window.initMap = initMap;