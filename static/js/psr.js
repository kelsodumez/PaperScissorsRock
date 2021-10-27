const socket = io.connect('http://127.0.0.1:5000');

var response_modal = document.getElementById("responseModal");
var result_modal = document.getElementById("resultModal")
var span = document.getElementsByClassName("close")[0];  
var currentUser = $('#user-data').data(); // due to the way sessions work with socketio it is neccessary to send the current user from js to socketio
let challenger;
let challenged;
let gameinfo;

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
        // console.log('reached here')
        console.log(data[1], ' 123')
        challenger = data[1]
    }
    challenged = data[2]
    gameinfo = data[3]
    console.log(challenged, 'aaaa')
    // console.log(challenger)
    result_modal.style.display = 'none';
    response_modal.style.display = "block";
    // console.log(challenger.user)

    console.log('dees')
    document.getElementById("name").innerHTML = challenger.user;
});

document.getElementById('user-response-rock').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'rock', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = "none";
});

document.getElementById('user-response-paper').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'paper', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = "none";
});

document.getElementById('user-response-scissors').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'scissors', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = "none";
});

socket.on('broadcast-result', function(data) {
    if (data == "win") {
        document.getElementById("result").innerHTML = "Win";  
    }
    else if (data == "loss") {
        document.getElementById("result").innerHTML = "Lose"; 
    }
    else if (data == "tie") {
        document.getElementById("result").innerHTML = "Tie";
    }
    result_modal.style.display = "block";   
});

document.querySelectorAll("#close").forEach(element => element.addEventListener("click", () => {
    response_modal.style.display = "none";
    result_modal.style.display = "none";
}));