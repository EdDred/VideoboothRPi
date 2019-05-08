import os
import time
import glob
from subprocess import Popen
from datetime import datetime

# v06 changed target_dir to /mnt/data/Recordings
# v061 added -o local to play video function

#
class Videobooth:
    def __init__(self):
        # pass
        # Directory of PICAM Recordings https://github.com/iizukanao/picam
        self.dir = "/home/pi/picam/rec/archive/"
        self.photodir = "/home/pi/picam/archive/"
        self.target_dir = "/mnt/data/Recordings/"
        self.typefile = ""


    def video_record_start(self):
        os.system('echo \'text=Vader Kind Weekend 2019\' > /home/pi/picam/hooks/subtitle' )
        os.system('touch /home/pi/picam/hooks/start_record')
        print("Recording started")

    def video_record_stop(self):
        # Recording time moved to javascript.
        os.system('touch /home/pi/picam/hooks/stop_record')
        print("Recording stopped")
        time.sleep(5) # Delay is needed before the file is available in OS
        latest_file,path,latestfilename = self.lastfile(self.dir,'ts')
        self.convert_to_mp4(latest_file)
        time.sleep(5) # Delay is needed before the file is available in OS
        latest_file,path,latestfilename  = self.lastfile(self.dir,'mp4')
        print('mp4 latest file = '+ latest_file)
        os.system('mv ' +  latest_file + " " + self.target_dir )
        print("Target dir to move to is: " + self.target_dir)

    def take_photo(self):
        #Stop the picam service to get access to the camera
        os.system('sudo service picam stop')
        self.filename1 = "VKW_Foto_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        print(self.filename1)
        time.sleep(1)
        os.system('raspistill -o '+ self.photodir + self.filename1)
        #D elay is needed to restart the picam service correct
        time.sleep(1)
        # Restart the Picam Service
        os.system('sudo service picam restart')
        # Delay to get the service running
        time.sleep(2)
        self.latest_file,self.path,self.latestfilename  = self.lastfile(self.photodir,'jpg')
        os.system('mv ' +  self.latest_file + " " + self.target_dir )
        print("Photo taken")



    def convert_to_mp4(self,lastfile):
        print("start Convert to MP4 van: " + lastfile + ' naar : ' + os.path.splitext(lastfile)[0])
        os.system(' ffmpeg -i ' + lastfile + ' -c:v copy -c:a copy -bsf:a aac_adtstoasc ' + os.path.splitext(lastfile)[0]+'.mp4')
        time.sleep(2) # Delay is needed before the file is available in OS
        print("Conversion from ts to mp4 done")

    def playvideo(self,latestfile):
        print("Start backend play video: " + latestfile)
        omxc = Popen(['omxplayer', '-o' , 'local', latestfile])
        player = True

    def lastfile(self,dirtosearch,typefile):
        print("Target Dir (from backend):" + dirtosearch + " type of file to search " + typefile)
        # for testing on windows machine use:
        # list_of_files = glob.glob("*." + typefile)

        # FOR USE ON RASPBERRY PI:
        list_of_files = glob.glob(dirtosearch + '*.' + typefile)
        # print("List of files = " + str(list_of_files))
        latest_file = max(list_of_files, key=os.path.getctime)
        path, latestfilename = os.path.split(latest_file)
        print("Backend latest_file = " + latest_file)
        return latest_file,path,latestfilename

    def showphoto(self,latestfile):
        # print("Show photo")
        # print("latestfile = "+ latestfile)
        # frontend_videobooth.create_widgets()
        # frontend_videobooth.create_image()
        # create_image(latestfile)
        return latestfile
