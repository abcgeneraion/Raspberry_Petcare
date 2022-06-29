import cv2
from base_camera import BaseCamera
import imutils
import time
class Camera(BaseCamera):
    video_source = 0
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        # 使用camera.set(propId, value)设置视频的一些参数信息
        camera.set(3, 640)
        camera.set(4, 480)
        camera.set(1, 10.0)
        # avg = None
        # def nothing(x):
        #     pass
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            # read current frame
            _, img = camera.read()
            img = imutils.resize(img,height=200,width=300)
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # if avg is None:
            #     avg = gray.copy().astype("float")
            #     continue

            yield cv2.imencode('.jpg', img)[1].tobytes()
