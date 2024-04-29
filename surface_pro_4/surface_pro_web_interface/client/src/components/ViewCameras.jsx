import React, { useState, useEffect } from 'react';

const ViewCameras = () => {
    const [objectDetectionData, setObjectDetectionData] = useState(null);

    useEffect(() => {
        // Update ObjectDetectionData with the stream from the server
    }, []);

    return (
        <div>
            {objectDetectionData && <img src={objectDetectionData} alt="Object Detection Data" />}
        </div>
    );
}

export default ViewCameras;