const socket = io.connect('http://127.0.0.1:5000');

document.querySelector('#join').addEventListener('click', () => {
    const id = +window.location.href.split('\/').pop()
    socket.emit('join', { 
        id
    })    
});

document.getElementById('send-action').addEventListener('click', () => {
    console.log("reached here") // debug
    const choice = "rock"
    socket.emit('sendAction', {'choice': choice})
});