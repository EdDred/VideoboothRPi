
var socket = io.connect('http://' + document.domain + ':' + location.port);

var videotime = 18
var buttonpress = 0
console.log(videotime)



document.getElementsByName("Videoopnemen")[0].addEventListener("click",
function(){
   buttonpressed('video');
   console.log('Video button');
  });

function buttonpressed(type) {
 if (type == 'video' & buttonpress == 0)
 {
   console.log('button doet iets');
    videomessage();
    buttonpress = 1;
}
else if (type == 'photo' & buttonpress == 0)
{
 console.log('button doet iets');
 fotomessage(5);
 buttonpress = 1;
}
else {
    buttonpress = 1;
    console.log('button doet niets');
    console.log(buttonpress);
  }

}


  function videomessage(){
    var x = setInterval(function() {
    var seconds = videotime;
    console.log(videotime);
    document.getElementById("demo").innerHTML ="De opname loopt nog <br>" + seconds + "<br> seconden ";
    if (videotime < 0) {
       clearInterval(x);
       document.getElementById("demo").innerHTML = "Momentje, je video wordt zo getoond";
       console.log("Wacht 10 seconden")
       window.setTimeout(function(){
         window.location.href = "/view"
       }
       , 10000);
    }
    videotime = videotime -1;
    }, 1000);
  };

  function fotomessage(fototijd){
     fototijd = 5
     console.log(fototijd)
     socket.emit('message', 'Hi server, how are you?');
     var x = setInterval(function() {
     var seconds = fototijd;
     console.log(fototijd);
     document.getElementById("demo").innerHTML ="Je foto wordt gemaakt over <br> " + seconds + "<br> seconden ";
     if (fototijd < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "Momentje, je foto wordt zo getoond";
        console.log("Wacht 10 seconden")
        window.setTimeout(function(){
          window.location.href = "/viewfoto"
        }
        , 5000);
    }
     fototijd = fototijd -1;
    }, 1000);

   };



document.getElementsByName("Fotomaken")[0].addEventListener("click",
function(){
  buttonpressed('photo');
  console.log('Photo Button pressed');
  //fotomessage(5);
});

  socket.on('connect', function(data) {
       console.log('connected1');
       document.getElementById("demo").innerHTML ="Connected ";

  });

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
