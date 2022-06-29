import schedule
import time
import RPi.GPIO as GPIO
from steer import Steer
from Hx711 import Hx711
import app
datas = []



def job(qulity):
    gear = Steer()
    s = Hx711().start()
    gear.open()
    time.sleep(1)
    #s<qulity-20中-20是为了更好的减少误差
    while(s<qulity-20):
        print(s)
        time.sleep(0.5)
        s = Hx711().start()
    gear.close()
    GPIO.cleanup()


class worker:
    def __init__(self):
        schedule.clear()
        self.datas = app.getdata()
        for data in self.datas:
            schedule.every().day.at(str(data.time)).do(job, data.qulity)







if __name__ == '__main__':

    while True:
        worker()
        time.sleep(3)
        schedule.run_pending()
