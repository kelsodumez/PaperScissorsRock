const socket = io.connect('http://127.0.0.1:5000');

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];  
var currentUser = $('#user-data').data(); // due to the way sessions work with socketio it is neccessary to send the current user from js to socketio
let challenger;

window.addEventListener('load', () => {
    console.log("reached here") // debug
    socket.emit('join', {'user_joined': currentUser})
});

document.getElementById('user-selection').addEventListener('click', () => {
    console.log("wowowowo")
    const formData = new FormData(document.querySelector('form'))
    form = [];
    for (var [key, value] of formData.entries()) { 
        console.log(key, value);
            form.push(value);
      }
    console.log(form)
    socket.emit('sendAction', {'form_data': form, 'user_sent': currentUser})
});

socket.on('broadcast-choice', function(data) {
    console.log(data, "yeye")
    console.log(challenger, data[1] )
    if (challenger == undefined){
        console.log('reached here')
        console.log(data[1])
        challenger = data[1]
    }
    console.log(challenger)
    modal.style.display = "block";
});

document.getElementById('user-response-rock').addEventListener('click', () => {
    console.log(1, challenger)
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'rock'})
    modal.style.display = "none";
});

document.getElementById('user-response-paper').addEventListener('click', () => {
    console.log(2, challenger)
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'paper'})
    modal.style.display = "none";
});

document.getElementById('user-response-scissors').addEventListener('click', () => {
    console.log(3, challenger)
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'scissors'})
    modal.style.display = "none";
});