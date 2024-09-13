var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('message', function(msg) {
    var chat = document.getElementById('chat');
    var message = document.createElement('p');
    message.textContent = msg;
    chat.appendChild(message);
});

document.getElementById('send').onclick = function() {
    var msg = document.getElementById('message').value;
    socket.send(msg);
    document.getElementById('message').value = '';
}
