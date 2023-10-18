import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer,Marker,Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

const App = () => {                 //declares a functional component named app 
  const position = [62, 15];
  const [markers, setMarkers] = useState ([]);

  useEffect (() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/markers");
        if(!response.ok) {
          throw new Error("Failed to fetch data"); 
        }
        const data = await response.json();
        setMarkers(data);
      } catch (error) {
        console.error(error)
      }
    };

  }, []);

  return (
    <MapContainer
      center={position}
      zoom={5.4}
      scrollWheelZoom={true}
      style={{ minHeight: "100vh", minWidth: "100vw" }}
    >
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {markers.map((marker, index) => (
        <Marker key={index} position={[marker.lat, marker.lon]}>
          <Popup>
            {marker["Tyoe of crime"]} <br /> {marker["Location"]} <br /> {marker["Date"]}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default App;