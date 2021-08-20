const socket = io.connect('http://127.0.0.1:5000');

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];

var currentUser = $('#user-data').data(); // due to the way sessions work with socketio it is neccessary to send the current user from js to socketio

var challenger;

window.addEventListener('load', () => {
    console.log("reached here") // debug
    socket.emit('join', {'user_joined': currentUser})
});

document.getElementById('user-selection').addEventListener('click', () => {
    console.log("wowowowo")
    const formData = new FormData(document.querySelector('form'))
    data = [];
    for (var [key, value] of formData.entries()) { 
        console.log(key, value);
        data.push(value);
      }
    console.log(data)
    socket.emit('sendAction', {'form_data': data, 'user_sent': currentUser})
});

socket.on('broadcast choice', data =>{
    console.log(data, "yeye")
    if (challenger == null){
        var challenger = data.challenger
    }

    modal.style.display = "block";
});

document.getElementById('user-response-rock').addEventListener('click', () => {
    console.log(1, challenger)
    socket.emit('sendResponse', {'challenger': challenger})
    console.log('debug to test if socket.emit ends the function :)')
});

document.getElementById('user-response-paper').addEventListener('click', () => {
    console.log(2)
});

document.getElementById('user-response-scissors').addEventListener('click', () => {
    console.log(3)
});