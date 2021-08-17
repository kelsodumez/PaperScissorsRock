const socket = io.connect('http://127.0.0.1:5000');

var modal = document.getElementById("myModal");
var span = document.getElementsByClassName("close")[0];


window.addEventListener('load', () => {
    console.log("reached here") // debug
    socket.emit('join')
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
    socket.emit('sendAction', {'form_data': data})
});

socket.on('broadcast choice', data =>{
    console.log(data, "yeye")
    modal.style.display = "block";
});
