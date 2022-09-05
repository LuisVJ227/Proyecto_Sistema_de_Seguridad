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

    Registro = "ALGUIEN ABRIO LA PUERTA EL "+ Fecha + " A LA HORA " + Hora + " CUIDADO !!!"

    #Agregar al registro

    lista1.insert(END,(Registro))

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

control.geometry("700x500")
control.title('control de sistema')

titulo1 = Frame()
titulo1.config(bg = "gray", width = "700", height = "80")
titulo1.place(x = 0, y = 0)

lbltitulo = Label(titulo1, text = "SISTEMA DE SEGURIDAD",bg = "gray", fg = "black",font =("Arial Rounded MT Bold", 25))
lbltitulo.place(x = 155, y = 20)

botones = Frame()
botones.config(bg = "black", width = "700", height = "120")
botones.place(x = 0, y = 80)

registro = Frame()
registro.config(bg = "blue", width = "700", height = "300")
registro.place(x=0, y= 200)

lista1 = Listbox(registro, bg = "white", width = "80", height = "15")
lista1.place(x = 115, y = 10)


#boton de encender
encender_c = Button(botones, text = "ACTIVAR", bg = "green", fg = "black", font = ("ARIAL", 20), command = lambda:encender())
encender_c.place(x = 100, y = 20)

#boton de apagar
apagar_c = Button(botones, text = "APAGAR", bg = "red", fg = "black", font = ("ARIAL", 20), command = lambda: apagar())
apagar_c.place(x = 490, y = 20)

#boton de cerrar
cerrar_c = Button(registro, text = "CERRAR", bg = "black", fg = "white", font = ("ARIAL", 10), command = lambda: cerrarInterfaz())
cerrar_c.place(x = 620, y = 270)

control.mainloop()
