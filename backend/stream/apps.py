from django.apps import AppConfig
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponseServerError
from rest_framework.response import Response
import cv2
import time
import threading
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from firebase_admin import storage


class StreamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stream'

    def ready(self):

        print("hello i started")
        self.video = cv2.VideoCapture(0)    #   <------ change this to IP at which esp32 camera is connected at 
                                            #   currently works for webcam in this configuration
        self.video.set(3, 640)
        self.video.set(4, 480)
        (self.grabbed, self.frame) = self.video.read()
        t1 = threading.Thread(target=self.update)
        t1.setDaemon(True)
        t1.start()
    def update(self):
        import multiprocessing as mp
        last_face = 0
        passed_time = 0
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        bucket = storage.bucket()
        self.t=mp.Process(target=self.upload, daemon=True)
        while True:
            (self.grabbed, self.frame) = self.video.read()
            time.sleep(1/30)
            _, jpeg = cv2.imencode('.jpg', self.frame)
            global gbl
            gbl = jpeg.tobytes()
            self.frame2 = self.frame
            # Below line is used to flip an image around y- axis
            self.frame2 = cv2.flip(self.frame2, 1)
            gray = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20)
            )
            now = datetime.now()
            self.dt_string = now.strftime("%d%m%Y%H%M%S")
            self.dt_string += ('.jpg')
            self.dt_string = str(self.dt_string)
            if abs(last_face-len(faces)) > 0 and (passed_time > 60):
                passed_time = 0
                mp.Process(target=self.upload, daemon=True).start()
            passed_time += 1



    
    def notify(self, img_url):
        from firebase_admin import messaging
        registration_token = 'cq55f9cz5eT2vE19bbsd8w:APA91bF5hozGqvrzIsjqDuJIuor2wbeBJIbzzrhA-48zpXutm1ll0UyyloaynVYeuu3hbjKV1Wk3449XKZXRIHXCSQaJUFATktbx6J_qf_P1cWOByyXM1YrzAoyJ19xALkoAM_P3170M'
        msg = messaging.Message(notification=messaging.Notification(
            title="hello", body="ahaha", image=None),
            token=registration_token)
        x = messaging.send(msg)
        print(img_url)
        print(x)

    def upload(self):
        from api.models import Snap
        from firebase_admin import storage
        fname = self.dt_string
        frame = self.frame2
        bucket = storage.bucket()
        cv2.imwrite(fname, frame)
        blob = bucket.blob(fname)
        blob.upload_from_filename(fname)
        # to make public access from the URL
        blob.make_public()
        snap = Snap(img_url=blob.public_url)
        snap.save()
        self.notify(blob.public_url,)


def gen():
    while True:
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + gbl + b'\r\n\r\n')


@gzip.gzip_page
def index(request):
    try:
        return StreamingHttpResponse(gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("aborted")
