
var socket = io.connect('http://' + document.domain + ':' + location.port);

var videotime = 18
var buttonpress = 0





  socket.on('message', function(data) {
       console.log('iets')
       console.log(data);
       if (data == 'Foto') {
       // document.getElementById("demo").innerHTML ="ButtonPress Foto";
       fotomessage()
     }
       if (data == 'Video') {
         // document.getElementById("demo").innerHTML ="ButtonPress Video";
         videomessage()
       }
  });
