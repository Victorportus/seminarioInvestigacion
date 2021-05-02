import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import adafruit_dht
import time
import sys
import board
import smtplib
import adafruit_tsl2561
import busio
import config_public
import csv
import os
import requests
import urllib

class LectorSensores():
    def __init__(self):
        while True:
            Interruptor.prender(21)
            
            try:
                dic = Sensor().getData()
                print(dic)
                Loader(dic)
            except:
                pass

            
            Interruptor.apagar(21)
            time.sleep(config_public.tiempoEntrePruebas*60)
        
    def correo(mensaje):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(config_public.fromaddr, config_public.password)
            mensaje = mensaje
            server.sendmail(config_public.fromaddr, config_public.toaddr,mensaje)
            server.quit()
        except:
            pass
        
    def connectDht(self):
        GPIO.setmode(GPIO.BCM)
        dht = adafruit_dht.DHT22(board.D4)
        
        
class Sensor():
    def __init__(self):
        dht, tsl = self.connect()
        try: 
            self.unirDic(dht, tsl)
        except:
            pass
                
    def connect(self):
        try:
            dht = DHT22(board.D17)
            tsl = Tsl()
            return dht, tsl
        except:
            Interruptor.apagar(21)
            LectorSensores.correo("Verifica la conexion de los sensores")
        
    
    def unirDic(self, dht, tsl):
        dic1 = dht.dic()
        dic2 = tsl.dic()
        dic1.update(dic2)
        self.setData(dic1)
    
    def getData(self):
        return self.data
    def setData(self,p):
        self.data = p
        
        
class Loader():
    def __init__(self, d):
        Csv(d)
        try:
            Loader.pruebaInternet()
            Thingspeak(d)
        except (requests.ConnectionError, requests.Timeout):
            Interruptor.prender(20)

        
    def pruebaInternet():
        request = requests.get("http://www.google.com", timeout=5)
        
        
        
class Csv():    
    def __init__(self, d):
        self.header()
        self.prepCsv(d)
                
    def prepCsv(self, d):        
        data = (time.strftime("%m/%d/%y"), time.strftime("%H:%M"), d['temperatura'], d['humedad'], d['lux'])
        f = open(config_public.archivoCSV, 'a')
        writer = csv.writer(f)
        writer.writerow(data)
        f.close()        
        
    def header(self):
        header = ["Date","Time","Temperature","Humidity","Lux"]
        f = open(config_public.archivoCSV, 'a')
        writer = csv.writer(f)
        if os.stat(config_public.archivoCSV).st_size == 0:
            writer.writerow(header)
        f.close()
        
class Thingspeak():

    def __init__(self, d):
        self.loadLux(d)
        time.sleep(15.0)
        self.loadTemp(d)
        time.sleep(15.0)
        self.loadHumi(d)
        
    def loadTemp(self, d):
        loadTemp = "https://api.thingspeak.com/update?api_key="+config_public.ThingspeakKey+"&field2="
        f = urllib.request.urlopen(loadTemp + str(d['temperatura']))
        f.read()
        f.close()
        
    def loadHumi(self, d):
        loadHumi = "https://api.thingspeak.com/update?api_key="+config_public.ThingspeakKey+"&field3="
        f = urllib.request.urlopen(loadHumi + str(d['humedad']))
        f.read()
        f.close()
        
    def loadLux(self, d):
        loadLux = "https://api.thingspeak.com/update?api_key="+config_public.ThingspeakKey+"&field1="
        f = urllib.request.urlopen(loadLux + str(d['lux']))
        f.read()
        f.close()
        
   

        
class DHT22(object):
    def __init__(self, pin):
        sensor = self.connect(pin)
        self.read(sensor)
        
    def connect(self, pin):
        GPIO.setmode(GPIO.BCM)
        dht = adafruit_dht.DHT22(pin)
        return dht
    
    def read(self, dht):
        i = 0
        while i < 2:
            try:
                self.setTemp(dht.temperature)
                self.setHumi(dht.humidity)
                dht.exit()
                break
            except RuntimeError as error:
                i += 1
                time.sleep(2.0)
                continue
        if i >= 2:
            dht.exit()
            LectorSensores.correo("No se puede leer sensor DHT22")
            sys.exit()
        
        
    def dic(self):
        dic = {'temperatura' : self.getTemp(), 'humedad' : self.getHumi()}
        return dic
        
    def setHumi(self, p):
        self.humi = p
    def getHumi(self):
        return self.humi
    
    def setTemp(self, p):
        self.temp = p
    def getTemp(self):
        return self.temp
    
    
class Tsl(object):
    def __init__(self):
        try:
            tsl = self.connect()
        except:
            LectorSensores.correo("No se puede leer sensor TSL")
        
    def connect(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        tsl = adafruit_tsl2561.TSL2561(i2c)
        self.setLux(tsl.lux)
        return tsl

        
    def dic(self):
        dic = {'lux' : self.getLux()}
        return dic
        
    def setLux(self, p):
        p = round(p)
        self.lux = p
    def getLux(self):
        return self.lux
        
    
    
    
    
    
class Interruptor(object):
    
    def __init__(self):
        self.prender()
        self.apagar()
        
    def prender(p):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.HIGH)
        GPIO.output(p, GPIO.HIGH)
    
    def apagar(p):
        GPIO.output(p, GPIO.LOW)

Interruptor.prender(20)
Interruptor.apagar(20)

if __name__ == "__main__":
    lectorSensores = LectorSensores()
