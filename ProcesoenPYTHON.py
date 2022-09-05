import time
import smtplib
import serial
from tkinter import *
from email.message import EmailMessage

Puerto = serial.Serial("COM5",9600)

def EnviarCorreo():
	#Declaro el correo y contraseña
    Emisor = "luisalbertodejesusv883@gmail.com"
    Contrasena = "qfurqdaeaamepcer"
    Receptor = "t1513600321@unitru.edu.pe"

    print("Iniciando envio")
    #Obteniendo la fecha y hora actual 
    Fecha = time.strftime("%d/%m/%y")
    Hora = time.strftime("%H:%M:%S")

    #Titulo del correo
    Asunto = "ALERTA DE SEGURIDAD"

    #Creando el mensaje que se quiere mandar
    Mensaje = "Alguien abrio la puerta el "+ Fecha + " a la hora " + Hora

    #Aspectos de mensaje
    em = EmailMessage()
    em["From"] = Emisor
    em["To"] = Receptor
    em["Subject"] = Asunto
    em.set_content(Mensaje)

    #Preparando el envio
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(Emisor, Contrasena)
        smtp.sendmail(Emisor, Receptor, em.as_string())

def cerrarInterfaz():
    Puerto.close()
    control.destroy()

def encenderSIST():
    Puerto.write('a'.encode())
    time(1)
    while True:
        while(Puerto.inWaiting()==0):
            pass
            Dato = Puerto.readline()
            #Para ver los datos que arroja
            #print(Dato)
            a = Dato.splitlines()
            b = str(a[0])
            c = b.replace("b","")
            d = c.replace("'","")
            e = int(d)
            print (e)

            if (e == 0):
                EnviarCorreo()
                print('ALERTA')
                time.sleep(0.5)
            time.sleep(0.1)
   
def apagarSIST():
    Puerto.write('b'.encode())
    time(1)

control = Tk()

control.geometry("500x200")
control.title('control de sistema')

titleFrame = Frame()
titleFrame.config(bg = "yellow", width = "500", height = "80")
titleFrame.place(x=0, y=0)
#titulo
lbltitulo = Label(titleFrame, text = "ENCENDIDO Y APAGADO DE SISTEMA", bg = "yellow", font =("ARIAL", 15))
lbltitulo.place(x=70, y=20)

botonesFrame = Frame()
botonesFrame.config(bg = "orange", width = "500", height = "120")
botonesFrame.place(x=0, y=80)

#boton de encender
encender = Button(botonesFrame, text = "ACTIVAR", bg = "green", fg = "white", font = ("ARIAL", 12),command = encenderSIST)
encender.place(x=100, y=40)

#boton de apagar
apagar = Button(botonesFrame, text = "APAGAR", bg = "red", fg = "white", font = ("ARIAL", 12),command = apagarSIST)
apagar.place(x=300, y=40)

#boton de Cerrar sistema
cerrar= Button(botonesFrame, text = ("Salir"),font = ("ARIAL", 14), command = cerrarInterfaz)
cerrar.place(x=440, y=80)

control.mainloop()