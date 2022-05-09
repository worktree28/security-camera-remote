# import cv2
# from datetime import datetime

# import firebase_admin
# from firebase_admin import storage
# from firebase_admin import credentials

# cred = credentials.Certificate("/home/harsh/Downloads/django-notific-firebase-adminsdk-xbiwi-2c98137e61.json")
# default_app = firebase_admin.initialize_app(cred,{
#     'storageBucket': 'django-notific.appspot.com'
# })
# bucket = storage.bucket()

# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# # cap=cv2.VideoCapture("http://192.168.43.214:80/stream")
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
# last_face = 0
# passed_time = 0

# while True:
#     ret, img = cap.read()
#     # Below line is used to flip an image around y- axix
#     img = cv2.flip(img, 1)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.2,
#         minNeighbors=5,
#         minSize=(20, 20)
#     )
#     # print(os.getcwd())
#     now = datetime.now()
#     dt_string = now.strftime("%d%m%Y%H%M%S")
#     dt_string+=('.jpg')
#     dt_string=str(dt_string)
#     #print(dt_string)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = img[y:y+h, x:x+w]
#     # print(os.listdir())
#     if abs(last_face-len(faces)) > 0 and ( passed_time>35  ) :
#         cv2.imwrite(dt_string, img)
#         last_face = len(faces)
#         passed_time=0
#         blob = bucket.blob(dt_string)
#         blob.upload_from_filename(dt_string)

#         # Opt : if you want to make public access from the URL
#         blob.make_public()

#         print("your file url", blob.public_url)
#         #print("Image saved")
#     passed_time+=1
#     cv2.imshow('video', img)
#     k = cv2.waitKey(30)
#     if k == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()
