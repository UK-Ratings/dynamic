// Function to get user location
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    var fixedlatitude = position.coords.latitude.toFixed(4);
    var fixedlongitude = position.coords.longitude.toFixed(4);

    var latElement = document.createElement("input");
    latElement.setAttribute("type", "hidden");
    latElement.setAttribute("name", "mylat");
    latElement.setAttribute("value", fixedlatitude);

    var longElement = document.createElement("input");
    longElement.setAttribute("type", "hidden");
    longElement.setAttribute("name", "mylong");
    longElement.setAttribute("value", fixedlongitude);

    var form = document.getElementById("optionsForm");
    form.appendChild(latElement);
    form.appendChild(longElement);

    // Display latitude and longitude
    document.getElementById("lat").innerText = fixedlatitude;
    document.getElementById("long").innerText = fixedlongitude;
}

function showError(error) {
    var latElement = document.createElement("input");
    latElement.setAttribute("type", "hidden");
    latElement.setAttribute("name", "mylat");
    latElement.setAttribute("value", -999);

    var longElement = document.createElement("input");
    longElement.setAttribute("type", "hidden");
    longElement.setAttribute("name", "mylong");
    longElement.setAttribute("value", -999);

    var form = document.getElementById("optionsForm");
    form.appendChild(latElement);
    form.appendChild(longElement);

    // Display default values
    document.getElementById("lat").innerText = -1;
    document.getElementById("long").innerText = -1;

    console.error("Geolocation error: ", error);
}

// Call getUserLocation when the page loads
window.onload = getUserLocation;