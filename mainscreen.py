import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import sys, time, sched, random, argparse

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from threading import Thread, Event

pcommands = ["Read", "Write", "Draw","Rap","Meditate"]
dcommands = ["Jerk Off!", "Buy Some Shit", "Jerk Off!", "Get some money", "Score some coke!", "Watch Porn!"]

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

class CommandWindow(QDialog):
   
    def __init__(self, parent=None):
        super(CommandWindow, self).__init__(parent)
        self.commandtext = QLabel("Command")
        self.timetext = QLabel("Time")
        layout = QVBoxLayout()
        layout.addWidget(self.commandtext)
        layout.addWidget(self.timetext)
        self.commandtext.setAlignment(Qt.AlignCenter)
        self.timetext.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setLayout(layout)
        self.setWindowFlags(Qt.SplashScreen)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.timetext.setStyleSheet('font-size: 200px; color: black;')
        self.commandtext.setStyleSheet('font-size: 100px; color: black')

    def setTimeText(self, time):
        p1,p2 = divmod(int(time), 60)
        if p2 < 10: p2 = "0" + str(p2)
        self.timetext.setText(str(p1)+":"+str(p2))

    def setCommandText(self, message):
        self.commandtext.setText(str(message))

    def sleepyTime(self):
        print "sleeping"
        self.hide()
        time.sleep(float(delayTime))
        self.startCountdown()

    def startCountdown(self):
        self.timing = Commands(showTime)
        self.timing.start()
        self.setCommandText(getCommand())
        self.setTimeText(showTime)
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
    argparser.add_argument('-dt','--delaytime', metavar='N', type=int, default=25, help="input delay time")
    argparser.add_argument('-st','--showtime', metavar='N', type=int, default=5, help="input show time")
    argparser.add_argument('-dys', '--dystopian', action='store_true')
    args = argparser.parse_args()
    if(args.dystopian):
        print 'using dystopian commands'
        commands = dcommands
    else: 
        commands = pcommands
    delayTime = toMinutes(args.delaytime)
    showTime = toMinutes(args.showtime)

    app = QApplication(sys.argv)
    window = CommandWindow()   
    window.sleepyTime()
    app.exec_()


