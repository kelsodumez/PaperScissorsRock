const socket = io.connect('http://127.0.0.1:5000');


var response_modal = document.getElementById('responseModal');
var result_modal = document.getElementById('resultModal')
var span = document.getElementsByClassName('close')[0];  
var currentUser = $('#user-data').data(); // due to the way sessions work with socketio it is neccessary to send the current user from js to socketio
let challenger;
let challenged;
let gameinfo;


window.addEventListener('load', () => {
    socket.emit('join', {'user_joined': currentUser})
});

window.addEventListener('beforeunload', () => {
    socket.emit('disconnect')
});

document.getElementById('user-selection').addEventListener('click', () => {
    const formData = new FormData(document.querySelector('form'))
    form = [];
    for (var [key, value] of formData.entries()) { 
            form.push(value);
      }
    socket.emit('sendAction', {'form_data': form, 'user_sent': currentUser})
});


socket.on('broadcast-choice', function(data) {
    if (challenger == undefined){
        challenger = data[1]
    }
    challenged = data[2]
    gameinfo = data[3]
    result_modal.style.display = 'none';
    response_modal.style.display = 'block';
    document.getElementById('name').innerHTML = challenger.user;
});


document.getElementById('user-response-rock').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'rock', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = 'none';
});


document.getElementById('user-response-paper').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'paper', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = 'none';
});

document.getElementById('user-response-scissors').addEventListener('click', () => {
    socket.emit('sendResponse', {'challenger': challenger, 'move': 'scissors', 'challenged': challenged, 'game_info': gameinfo})
    response_modal.style.display = 'none';
});


socket.on('broadcast-result', function(data) {
    if (data == 'win') {
        document.getElementById('result').innerHTML = 'Win';  
    }
    else if (data == 'loss') {
        document.getElementById('result').innerHTML = 'Lose'; 
    }
    else if (data == 'tie') {
        document.getElementById('result').innerHTML = 'Tie';
    }
    else if (data == 'error'){
        document.getElementById('result').innerHTML = 'User not available, make sure they are logged in and on play page'
    }
    result_modal.style.display = 'block';   
});


document.querySelectorAll('#close').forEach(element => element.addEventListener('click', () => {
    response_modal.style.display = 'none';
    result_modal.style.display = 'none';
}));