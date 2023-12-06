var sender_id = Date.now();
console.log(sender_id);

document.querySelector("#sender-id").textContent = sender_id;
const videoElement = document.getElementById("video-stream");

function CreateWebsocket(){
    console.log("button clicked");
    var receiver_id = document.getElementById("receiver-id").value;
    const socket = new WebSocket(`ws://127.0.0.1:8000/video-feed/${sender_id}/${receiver_id}`);
    console.log("socket established");
    socket.onmessage = (event) => {
        console.log("Message Received")
    // Set the received frame as the source of the image element
        videoElement.src = URL.createObjectURL(new Blob([event.data], { type: 'image/png' }));                  
    };
}