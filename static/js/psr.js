const socket = io.connect('http://127.0.0.1:5000');

var response_modal = document.getElementById("responseModal");
var result_modal = document.getElementById("resultModal")
var span = document.getElementsByClassName("close")[0];  
var currentUser = $('#user-data').data(); // due to the way sessions work with socketio it is neccessary to send the current user from js to socketio
let challenger;
let challegend;

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
    // console.log(data, "yeye")
    console.log(challenger, data[1] )
    if (challenger == undefined){
        // console.log('reached here')
        console.log(data[1])
        challenger = data[1]
    }
    // console.log(challenger)
    response_modal.style.display = "block";
    // console.log(challenger.user)
    challenged = data[2]

    document.getElementById("name").innerHTML = challenger.user;
});

document.getElementById('user-response-rock').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'rock', 'challegend': challegend})
    response_modal.style.display = "none";
});

document.getElementById('user-response-paper').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'paper', 'challegend': challegend})
    response_modal.style.display = "none";
});

document.getElementById('user-response-scissors').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'scissors', 'challegend': challegend})
    response_modal.style.display = "none";
});

socket.on('broadcast-result', function(data) {
    if (data == "win") {
        document.getElementById("result").innerHTML = "Win";
        result_modal.style.display = "block";   
    }
    else if (data == "loss") {
        document.getElementById("result").innerHTML = "Lose";
        result_modal.style.display = "block";   
    }
    result_modal.style.display = "block";   
    console.log("result_modal")
});