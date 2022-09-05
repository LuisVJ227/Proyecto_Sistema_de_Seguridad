from tkinter import *
import time 
import serial
import smtplib
from email.message import EmailMessage
import threading

Arduino = serial.Serial('COM5', 9600)
time.sleep(0.5)


def EnviarCorreo():
	#Declaro el correo y contraseña
    Emisor = "luisalbertodejesusv883@gmail.com"
    Contrasena = "qfurqdaeaamepcer"
    Receptor = "t1013600621@unitru.edu.pe"

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

cont = 0

def llamar_sistema():
    global cont
    while True:
        time.sleep(1)
        val = Arduino.readline()
        val = val.decode()
        #Para ver los datos que arroja
        a = int(val)
        print(a)
        if (a == 0):
            cont =+1
            if (cont <= 1):
                EnviarCorreo()
                print('ALERTA')
        elif (a == 1):
            cont = 0

def encender():
    Arduino.write('a'.encode())
    time.sleep(0.1)

def apagar():
    Arduino.write('b'.encode())
    time.sleep(0.1)


def cerrarInterfaz():
    Arduino.close()
    control.destroy()


threading.Thread(target=llamar_sistema).start()

control = Tk()

control.geometry("500x200")
control.title('control de sistema')


boton_1 = Label(control,  bg = 'green')
boton_1.place(x=20,y=50)

boton_2 = Label(control, bg = 'red')
boton_2.place(x=250,y=50)

boton_3 = Label(control, bg = 'red')
boton_3.place(x=400,y=150)

#boton de encender
encender_c = Button(boton_1, text = "ACTIVAR", bg = "white", fg = "black", font = ("ARIAL", 20), command = lambda:encender())
encender_c.pack()

#boton de apagar
apagar_c = Button(boton_2, text = "APAGAR", bg = "white", fg = "black", font = ("ARIAL", 20), command = lambda:apagar())
apagar_c.pack()

#boton de cerrar
cerrar_c = Button(boton_3, text = "CERRAR", bg = "white", fg = "black", font = ("ARIAL", 10), command = lambda:cerrarInterfaz())
cerrar_c.pack()


control.mainloop()
