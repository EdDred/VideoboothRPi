from gevent import monkey
monkey.patch_all()

from flask import Flask,flash,render_template,request,redirect,url_for
from backend_videobooth import Videobooth
import time
##### Commented for TESTPURPOSES
# Lib for GPIO
from gpiozero import Button as btn
from flask_socketio import SocketIO,emit,send
app = Flask(__name__)
app.secret_key = 'random string'
# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode='gevent')
# import eventlet
# eventlet.monkey_patch()
# import webbrowser

# GEVENT to support Websockets
import gevent
import os

version = 'v14_2'

#v14_1
#issues with css in full screenbrowser on android. chrome browser is ok
#v14_0
# fixed files function

#v13_9
# fixed sorting of files to show latest file
# be aware of date and time settings!!! also YEAR!!


#v13_8
# Optimize timers

#v13_6
# redesign view page with colums class

#v13_5 15-5-2019

# v13_4 12-05-2019
# fixed last file issue, get file from SD instead of UBS card
# remove ts from sdcard to save room
# reduced some timers

#### v13_2
#### Webpage buttonpress changed to only 1 time, until done

#### V13_1
#### based on approved version v12_1
#### added /files route for listing and downloading files


# directory where recordings will be put
target_dir = "/home/pi/Videobooth/static/video/Recordings/"
# link to be used in flask to get images files
# Directory: "/static/video/Recordings/"  needs to be used as a linked folder to /mnt/data/Recordings where the recordings are available
# flask needs to adress these files via /static directory
flaskimagedir = "/static/video/Recordings/"
videotimer = 20

def buttonmoviepressed():
    print("The Movie button is pressed")
    socketio.emit('message', 'Video', broadcast=True, namespace="/")
    videobooth.video_record_start()

    # Time sleep determins the recording time
    time.sleep(videotimer)
    videobooth.video_record_stop()
    # time.sleep(5)
    return redirect(url_for('recordvideo'))


def buttonphotopressed():
    print("The Photo button is pressed")
    socketio.emit('message', 'Foto', broadcast=True, namespace="/")
    videobooth.take_photo()
    print("Photo is taken")
    return redirect(url_for('viewphoto'))

def getvideofile():
    time.sleep(2)
    print("Get video file in targetdir " + target_dir)
    lastfile,path,name = videobooth.lastfile(target_dir,'mp4')
    webpath = flaskimagedir + name
    print('Video lastfile = ' + lastfile)
    return webpath

def getphotofile():
    print("Get photo file in targetdir " + target_dir)
    lastfile,path,name = videobooth.lastfile(target_dir,'jpg')
    webpath = flaskimagedir + name
    print('Photo lastfile = ' + lastfile)
    return webpath

@app.route("/", methods=['GET','POST'])
def home():
    if 'Videoopnemen' in request.form:
        # return redirect(url_for('recordvideo'))
        videobooth.video_record_start()
        # # Time sleep to be moved if recordvideo page will be used
        time.sleep(videotimer)
        videobooth.video_record_stop()
        # Delay needed to handle video convert and move
        # time.sleep(5)
        webpath = getvideofile()
        return render_template('view.html', data=webpath)

    elif 'Videoafspelen' in request.form:
        webpath = getvideofile()
        return render_template('view.html', data=webpath)
    # Added to try to play the ts file directly

    elif 'Fotomaken' in request.form:
        videobooth.take_photo()
        webpath = getphotofile()
        return render_template('viewfoto.html', data=webpath)

    elif 'Fotokijken' in request.form:
        webpath = getphotofile()
        return render_template('viewfoto.html', data=webpath)
    else:
        pass # unknown
    return render_template('entry.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/files')
def make_tree():
    path = "static/video/Recordings/"
    tree = dict(name=path, children=[])
#    try: lst = os.listdir(path)
    try: lst = sorted(os.listdir(path),reverse=True)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            # if os.path.isdir(fn):
            #     tree['children'].append(make_tree(fn))
            # else:
            tree['children'].append(dict(name=fn))
    # print(tree)
    return render_template('fileslist.html' , data=tree)

@app.route("/counter", methods=['GET', 'POST'])
def counter():
    return render_template('counter.html')

@app.route("/entry", methods=['GET', 'POST'])
def entry():
    return render_template('entry.html')


# Route to view video file
@app.route("/view" , methods=['GET', 'POST'])
def view():
# testing timer 12-05-2019
    time.sleep(5)
    print("Play video in browser")
    webpath = getvideofile()
    return render_template('view.html', data=webpath)

# Route to view Photo file
@app.route("/viewfoto" , methods=['GET', 'POST'])
def viewphoto():
    print("Show Photo in browser")
    webpath = getphotofile()
    return render_template('viewfoto.html', data=webpath)

# NOT USED YET: Route is intented for an in between page if needed
@app.route("/takephoto")
def takephotobutton():
    print("Take photo button")
    # videobooth.take_photo()
    # return render_template('takefoto.html')

# NOT USED YET: Route is intented for an in between page if needed
@app.route("/recordvideo", methods=['GET','POST'])
def recordvideo():
    # emit('message', 'Video maken', broadcast=True)

    videobooth.video_record_start()
#     lastfile,path,name = videobooth.lastfile(target_dir,'mp4')
#     webpath = flaskimagedir+name
    return render_template('recordvideo.html')

# NOT USED YET: Route is intended as seperate page to stop recording to support seperate in between page
@app.route("/stoprecord", methods=['GET','POST'])
def stoprecordvideo():
    videobooth.video_record_stop()
    lastfile,path,name = videobooth.lastfile(target_dir,'mp4')
    webpath = flaskimagedir+name
    print("Sleep timer in stop record video 5 seconds")
    time.sleep(5)
    return render_template('view.html', data=webpath)
#

@socketio.on('message')
def test_message(message):
    print("message : " + message)
    # emit('my response', message, broadcast=True)
    # if message == "Hi server, how are you?":
    #     print("Yes we hebben wat ontvangen")
    #     socketio.emit('message', 'Foto maken', broadcast=True, namespace= "/")
    #
    # else:
    #     print("we hebben iets anders ontvangen")

@socketio.on('connect')
def test_connect():
    print("connected")
    # emit('message', 'The client has connected', broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    videobooth = Videobooth()
    print(app.instance_path)
    button_movie = btn(20)
    button_photo = btn(21)
    button_movie.when_pressed = buttonmoviepressed
    button_photo.when_pressed = buttonphotopressed
    print("VKW Videobooth App Version " + version + " on port 5007 intended VKW weekend, option to record video and take a photo")
    #app.run(host='0.0.0.0', port=5002, debug=True)
    # socketio.run(app,host='0.0.0.0', port=5002, debug=True)
    socketio.run(app,host='0.0.0.0', port=5007)
