import sys, time, sched, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import Thread, Event


commands = ["Read", "Write", "Take a Walk"]

class Commands(Thread): 

    def sleepyTime(self, delay=4):
        self.timer.enter(delay,1,self.startCountdown,())
        self.timer.run()

    def startCountdown(self):
        self.time = 10
        self.startCommandTime.set()
        self.form.show()


    def setCountdownText(self):
        self.form.timetext.setText(str(self.time))

    def run(self):
        while True:
            self.startCommandTime.wait()
            print self.time
            self.setCountdownText()
            time.sleep(1)
            if self.time != 0:
                self.time -= 1
            else:
                self.form.hide()
                self.setCountdownText()
                self.startCommandTime.clear()
                self.sleepyTime()



    def __init__(self, commandDelayTime = 10):
        Thread.__init__(self)
        self.time = self.tot_time = commandDelayTime
        self.timer = sched.scheduler(time.time, time.sleep)

        self.form = Form()
        self.form.show()

        self.startCommandTime = Event()
        self.startCommandTime.set()
        self.restart = False
        self.setDaemon(True)
        self.sleepyTime()

    def main(self):
        
        self.start()



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
#           timetext.show()
#           layout.show()
        self.setWindowFlags(Qt.SplashScreen)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()

    def setTimeText(self, message):
        self.timetext.setText("<font size=200>"+str(message)+"</font>")

    def setCommandText(self, message):
        self.commandtext.setText("<font size=300>"+str(message)+"</font>")

def getCommand():
    return random.choice(commands)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timing = Commands()
    timing.main()
    app.exec_()


