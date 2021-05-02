'''Datos de correo para notificacon de errores de coneccion o de problemas con carga en la nube.
en fromaddr, se debe escribir un correo del cual se van a enviar sus mensaje, en Pasword, la clave de este correo.
En to addr se debe escribir el destinatario.'''

fromaddr = "XXX@universidadean.edu.co"
password = "XXXXX"
toaddr = "XXX@universidadean.edu.co"

''' Datos guardados en CSV
Ingrese la ubicaion donde desea guardar el archivo con data .csv '''
archivoCSV = "XXXX"

''' Datos en la nube ThingSpeak
Cree una cuenta en thingspeak, cree un canal con los Temperatura, Humedad, PMT25, Eco2 y TVOC.
Deben ser creados en ese orden.
Ingrese el key del canal creado.'''
ThingspeakKey = "XXXX"

''' Determinar el tiempo entre cada una de las pruebas'''
tiempoEntrePruebas = 30