import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import sys, time, sched, random, argparse

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from threading import Thread, Event


commands = ["Jerk Off!", "Buy Some Shit", "Jerk Off!"]

class Commands(QThread): 

       def __init__(self, mytime):
            QThread.__init__(self)
            self.time = int(mytime)

       def __del__(self):
           self.wait()

       def run(self):
            while True:
                self.emit(SIGNAL('update(QString)'),  str(self.time))
                time.sleep(1)
                if self.time != 0:
                    self.time -= 1
                else:
                    self.emit(SIGNAL('timefinished'))
                    self.terminate()

class Form(QDialog):
   
    def __init__(self, parent=None):
        print "initialized"
        super(Form, self).__init__(parent)

        self.commandtext = QLabel("<font size=200>"+getCommand()+"</font>")
        self.timetext = QLabel("Time")
        layout = QVBoxLayout()
        layout.addWidget(self.commandtext)
        layout.addWidget(self.timetext)
        self.commandtext.setAlignment(Qt.AlignCenter)
        self.timetext.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setWindowFlags(Qt.SplashScreen)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def setTimeText(self, time):
        p1 = int(time) / 60 
        p2 = int(time) % 60 
        if p2 < 10: p2 = "0" + str(p2)
        self.timetext.setText("<font size=200>"+str(p1)+":"+str(p2)+"</font>")

    def setCommandText(self, message):
        self.commandtext.setText("<font size=300>"+str(message)+"</font>")

    def sleepyTime(self, delay=4):
        print "sleeping"
        self.hide()
        time.sleep(float(delayTime))
        self.startCountdown()

    def startCountdown(self):
        self.timing = Commands(showTime)
        self.timing.start()
        self.setCommandText(getCommand())
        self.timetext.connect(self.timing, SIGNAL("update(QString)"), self.setTimeText)
        self.connect(self.timing, SIGNAL('timefinished'), self.sleepyTime)
        self.show()
        self.showFullScreen()


def getCommand():
    return random.choice(commands)
def toMinutes(num):
    return num*60

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='pass some integers')
    argparser.add_argument('ints', metavar='N', type=int, nargs=2, help="input two numbers, first is the delay time, second is show time")
    args = argparser.parse_args()

    delayTime = toMinutes(args.ints[0])
    showTime = toMinutes(args.ints[1])
    app = QApplication(sys.argv)
    form = Form()   
    form.sleepyTime()
    app.exec_()


