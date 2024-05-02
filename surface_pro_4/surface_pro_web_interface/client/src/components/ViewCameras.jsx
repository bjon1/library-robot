
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const ViewCameras = () => {
    const [objectDetectionData, setObjectDetectionData] = useState(null);

    useEffect(() => {
        /*
        console.log("test");
        const socket = io('http://127.0.0.1:5332/');

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('frame_data', (data) => {
            console.log(JSON.parse(data).frame)
            setObjectDetectionData(JSON.parse(data).frame);
        });

        return () => {
            socket.disconnect();
        };
        */

    }, []);

    return (
        <div className="ViewCameras">
            <img 
                className="ViewCameras__video-stream"
                src="/stream" alt="Video Stream"/>
        </div>
    );
}
export default ViewCameras;
