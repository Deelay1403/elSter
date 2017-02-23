from multiprocessing import Process, Queue
from time import sleep
import serial
import gtk
from threading import Thread
import multiprocessing

class interactiveSerial:
    def __init__(self, port):
        print "ROZPOCZETO"
        self.serPort = port
        self.queue = Queue()
        self.objects = {}
        print "inicjacja zakonczona"

    def stopListen(self):
        self.queue.put(['STOP_LISTENING', ''])

    def startListen(self, q, endLineChar = ';'):
        while True:
            try:
                daneOdebrane = q.get_nowait()
                if (daneOdebrane[0] == "STOP_LISTENING"):
                    print "STOP!"
                    break
            except Exception:
                daneOdebrane = "pusto"

            if (daneOdebrane[0] == 'SEND'):
                try:
                    #self.serPort.write(daneOdebrane[1])
                    print "WYSLANO " + daneOdebrane[1]
                except serial.serialutil.SerialException:
                    print 'Blad zapisu'
                    return "ERR01"

            try:
                print "ODBIERAM"
                #lineOfData = self.serPort.read_until(endLineChar)
                lineOfData = "BAT_4_517"
                print lineOfData
                lineOfData = lineOfData.strip("\r\n")
                print lineOfData

                if lineOfData.startswith('BAT_'):  # szuka odpowiedzniej komendy
                    raw = lineOfData.strip('BAT_;\n')  # "oczyszcza" ja
                    print 'komenda ' + raw
                    infoBattery = raw.split('_')
                    batteryObject = self.getObject('battery')
                    print "__________________________________"
                    print batteryObject
                    if (batteryObject != 'ERIS01' and batteryObject != 'ERIS02'):
                        print "TRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRUUUUUUUUUUEEEEEEEEEEEE"
                        print "ID:" + infoBattery[0]
                        print "VAL:" + infoBattery[1]
                        # self.objects['battery'].update(4,699)
                        #testuje



                        self.event.clear()
                        for i in range(1,6):
                            t = Thread(name="log", target=self.updateBattery(i,self.y)).start()
                            self.y = self.y + 100
                        self.event.set()

                        self.event.clear()
                        self.updateBattery(6,600)
                        self.event.set()
                        if(self.dziala == 1):
                            self.event.clear()
                            self.updateBattery(1,700)
                            self.event.set()
                        # p = Process(target=self.updateBattery(3,100), name="Window").start()
                        # if self.x==6:
                        #     break
                        # self.objects["battery"].update(self.x,self.y)
                        # self.objects["battery"].update(ID=2,level=300)
                        # print "OK!"
                        # self.x=self.x+1



                elif lineOfData.startswith('ER_'):
                    raw = lineOfData.strip('ER_;\n')  # "oczyszcza" ja
                    print 'komenda ' + raw
                    infoError = raw.split('_')
                    print "ERROR"
                    print  infoError

            except serial.serialutil.SerialException:
                print 'Blad odczytu'
                return "ERR02"
            pass

            print "co odbieram " + daneOdebrane[0] + " " + daneOdebrane[1]
            sleep(1)
            break

    def updateBattery(self, ID, LVL):
        self.objects['battery'].update(ID, LVL)

    def send(self, whatSend):
        if not self.serPort == 'NO_PORTS':
            self.queue.put(['SEND', whatSend])
        else:
            print('EMULATING')
            #TODO: SIMULATING SCENES
        pass

    def addObject(self, name, object):
        self.objects[name] = object
        # self.updateBattery(4,100)
        #print self.objects

    def getObject(self, name):
        try:
            if (self.objects[name]):
                return self.objects[name]
            else:
                return "ERIS01"
                print "brak obiektu dla " + name
        except KeyError:
            return "ERIS02"
            print "brak obiektu dla " + name
    def jebacTo(self, ID, LVL):
        self.updateBattery(ID, LVL)

    def setup(event,d):
        global unpaused
        unpaused = event
    def start(self, endLineChar = ';'):
        self.dziala = 0
        self.x = 1
        self.y = 150
        print "START!"
        self.event = multiprocessing.Event()
        self.pool = multiprocessing.Pool(1, self.setup, (self.event,))
        self.result = self.pool.map_async(self.startListen(self.queue), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.event.set()
        #p = Thread(target=self.startListen(self.queue),name="kek").start()
        # t = Thread(name="log", target=self.updateBattery(4,300)).start()
        #p = Process(target=self.jebacTo, args=(5,500,)).start()
        #self.jebacTo(4,100)
        print "OKK!"


if __name__ == "__main__":
    popcorn = interactiveSerial('tty/=/1')
    popcorn.start()

    popcorn.addObject('bateria','tak')

    popcorn.getObject('bateria')

    sleep(5)
    popcorn.send("OK!")
    sleep(5)
    popcorn.send("NACHOS!")