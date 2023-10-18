import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css';

const App = () => {
  const initialPosition = [62, 15];
  const initialZoom = 5.4; 
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/markers");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        console.log("Fetched data:", data); 
        setMarkers(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  return (
    <MapContainer
      center={initialPosition}
      zoom={initialZoom}
      style={{ minHeight: "100vh", minWidth: "100vw" }}
    >
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

{markers.map((marker, index) => (
  marker.Latitude && marker.Longitude ? (
    <Marker
      key={index}
      position={[marker.Latitude, marker.Longitude]}
    >
      <Popup>
        {marker["Type of news"]} <br /> {marker["Location"]} <br /> {marker["Date"]}
      </Popup>
    </Marker>
  ) : null
))}


    </MapContainer>
  );
};

export default App;
