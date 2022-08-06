function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.12, lng: -96.81 },
    zoom: 5
  });

  const marker = new google.maps.Marker({
    map: map
  });

  const xinput = document.getElementById("xinput");
  const yinput = document.getElementById("yinput");

  map.addListener("click", (e) => {
    map.panTo(e.latLng);
    marker.setPosition(e.latLng);
    xinput.value = e.latLng.lat();
    yinput.value = e.latLng.lng();
  })
}

window.initMap = initMap;