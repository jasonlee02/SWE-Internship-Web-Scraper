function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.12, lng: -96.81 },
    zoom: 5
  });

  const marker = new google.maps.Marker({
    map: map
  });

  const location = document.getElementById("location");

  const geocoder = new google.maps.Geocoder();

  map.addListener("click", (e) => {
    map.panTo(e.latLng);
    marker.setPosition(e.latLng);
    geocoder.geocode({
      location: e.latLng,
    }, (results, status) => {
      if(status === 'OK') {
          if(results && results.length) {
              var filtered_array = results.filter(result => result.types.includes("locality")); 
              var addressResult = filtered_array.length ? filtered_array[0]: results[0];

              if(addressResult.address_components) {
                  addressResult.address_components.forEach((component) => {
                      if(component.types.includes('locality')) {
                          location.value = component.long_name;
                      }
                  });
              }
          }
      }
  })
})
}
window.initMap = initMap;