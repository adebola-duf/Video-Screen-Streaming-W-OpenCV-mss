// This line creates a new WebSocket object and establishes a connection to the WebSocket endpoint provided by your FastAPI server. 
// The URL ws://127.0.0.1:8000/video_feed corresponds to the WebSocket endpoint you defined in your FastAPI application.
const socket = new WebSocket("ws://127.0.0.1:8000/video-feed");
// using a relative url
const host = window.location.hostname;
const port = window.location.port || (window.location.protocol === 'https:' ? 443 : 80);
// Construct the WebSocket URL
// const socket = new WebSocket(`ws://${host}:${port}/video-feed`);
const videoElement = document.getElementById("video-stream");
console.log(host, port)
socket.onmessage = (event) => {
    // Set the received frame as the source of the image element
    videoElement.src = URL.createObjectURL(new Blob([event.data], { type: 'image/jpeg' }));
};
               
                