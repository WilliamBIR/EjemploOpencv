from tkinter import *
from tkinter import ttk 
import time                     #Para las pausas
import cv2 #Para camara y vision artificial
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as GPIO



import keras
from keras.models import load_model
print('leyendo modelo')
modelorabano= load_model('rabano.h5')
modelozanahoria=load_model('zanahoria.h5')
modelojitomate=load_model('jitomate.h5')
modelolechuga=load_model('lechuga.h5')
print('modelo leido')


GPIO.setmode(GPIO.BOARD)        
GPIO.setwarnings(False)               

#Declarar pines a utilizar
dirx   = 3                   #Salida direccion x
dirx1  = 7
spx = 5                   #Salida pasos x
diry   = 13
spy = 11
dirz   = 10
spz = 8
#Pra la heramienta de maleza: z=5550,z2=5660 ,x=30, y=3655# enx regresar 15 pasos mas
#Para la herramienta de plantar: x=30 y=2860 z=5550 y=-10
#Para la herramienta riego: x=35 y=2072

#para sembrar plantas z=5100
#la ultima z=

z1=5550
z2=5640
zsemilla=5100
zplantar=7680 #al borde, para enterrar+100
#Para las bombas
bombaagua= 15
bombasemilla= 16
microPausa = 0.004
tiemporegado=3

#Configurar todo como salida por que soy imbecil
GPIO.setup(dirx,GPIO.OUT)
GPIO.setup(dirx1,GPIO.OUT)
GPIO.setup(spx,GPIO.OUT)
GPIO.setup(diry,GPIO.OUT)
GPIO.setup(spy,GPIO.OUT)
GPIO.setup(dirz,GPIO.OUT)
GPIO.setup(spz,GPIO.OUT)
GPIO.setup(bombaagua,GPIO.OUT)
GPIO.setup(bombasemilla,GPIO.OUT)


window = Tk()
window.title("Super Driver")
window.geometry('900x950')
color="sienna4"
colormargen="grey27"
window.configure(background=color)


##Funciones del robot
def regadoautomatico():
    print('iniciando regado')
    posactx=posicionx(0)
    posacty=posiciony(0)
    #Mover al robot sobre la herramienta, cambiar valores de acuerdo a lo calculado
    print('posicionando sobre herramienta')
    movimientoxy(posactx,posacty,'30\n','2072\n')
    #Bajar el robot en z para tomar la herramienta
    movimientoz(0,z1)
    #sacar el robot en x para sacar la herramienta
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','2072\n')
    #ELevar el robot
    print('cogiendo regadora')
    movimientoz(z1,0)
    #Mover el robot a la posicion a regar
    print('herramienta regadora lista')
    for i in range(1,43):
        actual=str(i)+'\n'
        posactx=posicionx(0)
        posdeseadax=posicionx(i)
        posacty=posiciony(0)
        posdeseaday=posiciony(i)
        movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
        #Activar la bomba
        print('Regando casilla: ',int(posdeseadax),int(posdeseaday))
        GPIO.output(bombaagua,True)
        time.sleep(tiemporegado)
        GPIO.output(bombaagua,False)
    print('terminado de regar')
    #Regresar Herramienta
    #Posicionar a y distancia
    posactx=posicionx(0)
    posacty=posiciony(0)
    print('regresando herramienta')
    movimientoxy(posactx,posacty,'600\n','2072\n')
    #Bajar el robot
    movimientoz(0,z2)
    #Dejamos la herramienta en el blablabla
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'20\n','2072\n')
    #Subimos el robot par quitar la herramienta
    movimientoz(z2,0)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')

def plantar():
    print('iniciando plantado')
    posactx=posicionx(0)
    posacty=posiciony(0)
    print('oposicionando sobre herramienta')
    #Mover al robot sobre la herramienta, cambiar valores de acuerdo a lo calculado
    movimientoxy(posactx,posacty,'30\n','2860\n')
    #Bajar el robot en z para tomar la herramienta
    movimientoz(0,z1)
    #sacar el robot en x para sacar la herramienta
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','2860\n')
    #ELevar el robot
    print('herramienta lista')
    movimientoz(z1,0)
    aplantar=Plantas.get()
    #seleccionar semilla
    if aplantar=='Lechuga':
        deseadax='0\n'
        deseaday='2455\n'#-95, 4650 en z,35 #Z MAX PARA PLANTAR: 7250
    elif aplantar=="Zanahoria":
        deseadax='0\n'
        deseaday='2585\n' # -95, 65
    elif aplantar=="Rabano":
       deseadax='0\n'
       deseaday='3275\n'
    elif aplantar=="Jitomate":
        deseadax='0\n'
        deseaday='3395\n'
    print('cogiendo semilla')
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,deseadax,deseaday)
    #Bajar robot para tomar semilla
    movimientoz(0,zsemilla)
    #ENcender bomba para tomar semillas
    GPIO.output(bombasemilla,True)
    time.sleep(2)
    #SUbir robot
    movimientoz(zsemilla,0)
    #Mover el robot a la posicion a plantar
    print('herramienta plantadora lista')
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    #Bajar para plantar
    movimientoz(0,zplantar)
    time.sleep(1)
    GPIO.output(bombasemilla,False)
    time.sleep(1)
    movimientoz(zplantar,0)
    print('terminado de plantar')
    #Regresar Herramienta
    #Posicionar a y distancia
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','2860\n')
    #Bajar el robot
    movimientoz(0,z2)
    #Dejamos la herramienta en el blablabla
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'20\n','2860\n')
    #Subimos el robot par quitar la herramienta
    movimientoz(z2,0)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')


def regar():
    print('iniciando regado')
    posactx=posicionx(0)
    posacty=posiciony(0)
    #Mover al robot sobre la herramienta, cambiar valores de acuerdo a lo calculado
    movimientoxy(posactx,posacty,'30\n','2072\n')
    #Bajar el robot en z para tomar la herramienta
    movimientoz(0,z1)
    #sacar el robot en x para sacar la herramienta
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','2072\n')
    #ELevar el robot
    movimientoz(z1,0)
    #Mover el robot a la posicion a regar
    print('herramienta regadora lista')
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    #Activar la bomba
    GPIO.output(bombaagua,True)
    time.sleep(tiemporegado)
    GPIO.output(bombaagua,False)
    print('terminado de regar')
    #Regresar Herramienta
    #Posicionar a y distancia
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','2072\n')
    #Bajar el robot
    movimientoz(0,z2)
    #Dejamos la herramienta en el blablabla
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'20\n','2072\n')
    #Subimos el robot par quitar la herramienta
    movimientoz(z2,0)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')
    
    
def monitorear():
    print('iniciando monitoreo')
    #Prueba de la herramienta    
    posactx=posicionx(0)
    posacty=posiciony(0)
    #Mover al robot sobre la herramienta, cambiar valores de acuerdo a lo calculado
    movimientoxy(posactx,posacty,'30\n','3655\n')
    #Bajar el robot en z para tomar la herramienta
    movimientoz(0,z1)
    #sacar el robot en x para sacar la herramienta
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','3655\n')
    #ELevar el robot
    print('herramienta lista')
    movimientoz(z1,0)
    #Mover el robot a la posicion a observar
    posactx=posicionx(0)
    posdeseadax=posicionx(selected.get())
    posacty=posiciony(0)
    posdeseaday=posiciony(selected.get())
    movimientoxy(posactx,posacty,posdeseadax,posdeseaday)
    visionartificial()
    #SI la vision artificial da un resultado positivo, aqui poner el if y la secuencia de cambio de herramienta, calculos de distancia y movimiento del robot para la eliminacion
    #regresar la herramienta
    #Posicionar a y distancia
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'600\n','3655\n')
    #Bajar el robot
    movimientoz(0,z2)
    #Dejamos la herramienta en el blablabla
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'20\n','3655\n')
    #Subimos el robot par quitar la herramienta
    movimientoz(z2,0)
    print('herramienta desacoplada')
    #Regresamos a 0,0,0
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    print('estando en 0,0')
    

def movimientoxy(x0,y0,xf,yf):
    print('movimiento en x y')
    print(x0,' ',xf)
    print(y0,' ',yf)
    movimientox=(int(xf)-int(x0))
    movimientoy=(int(yf)-int(y0))
    print(movimientox," ",movimientoy)
    #movimiento robot
    if movimientox>0:
        GPIO.output(dirx,1)
        GPIO.output(dirx1,0)
    else:
        GPIO.output(dirx,0)
        GPIO.output(dirx1,1)
    if movimientoy<0:
        GPIO.output(diry,0)
    else:
        GPIO.output(diry,1)
        
    if abs(movimientox)>=abs(movimientoy):
        print('x>=y')
        for i in range(0,abs(movimientox)):
            GPIO.output(spx, True)
            if abs(movimientoy)>i:
                GPIO.output(spy, True)
                #print(movimientoy)
                #print(i)
            time.sleep(microPausa)
            GPIO.output(spx, False)
            GPIO.output(spy, False)
            #print(movimientox)
            time.sleep(microPausa)
        time.sleep(microPausa)
    else:
        print('x<y')
        for i in range(0,abs(movimientoy)):
            GPIO.output(spy, True)
            if abs(movimientox)>i:
                GPIO.output(spx, True)
                #print(i)
                #print(movimientox)
            time.sleep(microPausa)
            GPIO.output(spx, False)
            GPIO.output(spy, False)
            #print(movimientoy)
            time.sleep(microPausa)
        time.sleep(microPausa)
    #Actualizacion posiciones
    f=open('posicionesx','r')
    aux=f.readlines()
    aux[0]=xf
    f.close()
    #print(aux)
    f=open('posicionesx','w')
    for i in range(0,44):
        f.write(aux[i])
        #print(aux[i])
    f.close()
    aux=[]
    f=open('posicionesy','r')
    aux=f.readlines()
    aux[0]=yf
    f.close()
    #print(aux)
    f=open('posicionesy','w')
    for i in range(0,44):
        f.write(aux[i])
        #print(aux[i])
    f.close()
    print('terminando x y')

def movimientoz(z0,zf):
    print('movimiento z')
    movimientoz=(zf-z0)
    if movimientoz>0:
        GPIO.output(dirz,0)
    else:
        GPIO.output(dirz,1)
    for i in range(0,abs(movimientoz)):
        GPIO.output(spz, True)
        time.sleep(microPausa)
        GPIO.output(spz, False)
        time.sleep(microPausa)
        print(i)
    time.sleep(microPausa)
    print('terminando z')

def posiciony(posy):
    f=open('posicionesy','r')
    aux=f.readlines()
    posacty=aux[posy]
    f.close()
    return posacty

def posicionx(posx):
    f=open('posicionesx','r')
    aux=f.readlines()
    posactx=aux[posx]
    f.close()
    return posactx

def visionartificial():
    camara=cv2.VideoCapture(0)
    print('camara abierta')
    #camara.set(10, 0  ) # brightness     min: 0   , max: 255 , increment:1  
    #camara.set(11, 70   ) # contrast       min: 0   , max: 255 , increment:1     
    #camara.set(12, 60   ) # saturation     min: 0   , max: 255 , increment:1
    #cam.set(13, 13   ) # hue         
    #camara.set(15, -3   ) 
    for n in range(1,60):
        print(n)
        leido, frame  = camara.read()
    if leido == True:
        cv2.imwrite("foto.jpg", frame)
        print("Foto tomada correctamente \n")
        nimage="foto.jpg"
        image=cv2.imread(nimage)
        image=cv2.resize(image,(640,480))
        cv2.imshow('original', image)
        ##Convertir a escala de grises
        image2=image
        image3=image
        gris = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        n=7;
        gaussiana=cv2.GaussianBlur(gris,(n,n),1);
        t,dst=cv2.threshold(gaussiana,100,150,cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        print('filtrando')
        contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # dibujar los contornos
        ##cv2.drawContours(image, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
        i=1
        print('procesando')
        for c in contours:
            #area = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)
            if w >=50 and h>=50:    
                mensaje=f'Objeto {i}'
                aux=cv2.imread(nimage)
                aux=cv2.resize(aux,(640,480))
                crop_img=aux[y:y+h,x:x+w]
                img_ori= crop_img
                img= cv2.resize(img_ori,(150,150),interpolation=cv2.INTER_CUBIC)
                imagen_a_probar=np.reshape(img,(1,150,150,3))
                predictions=modelorabano.predict_classes(imagen_a_probar)
                print('primera neurona')
                #print(predictions)
                print('objeto: ',i)
                if (predictions==0):
                    mensaje=f'{i} Ok'            
                    print('rabano')
                elif(predictions==1):
                    print('segunda neurona')
                    predictions2=modelolechuga.predict_classes(imagen_a_probar)
                    #print(predictions2)
                    if(predictions2==0):
                        mensaje=f'{i} Ok'            
                        print('Lechuga')
                    elif(predictions2==1):
                        print('tercera neurona')
                        predictions3=modelozanahoria.predict_classes(imagen_a_probar)
                        if(predictions3==0):
                            mensaje=f'{i} Ok'            
                            print('zanahoria')
                        elif(predictions3==1):
                            print('cuarta neurona')
                            predictions4=modelojitomate.predict_classes(imagen_a_probar)
                            if(predictions4==0):
                                mensaje=f'{i} Ok'            
                                print('zanahoria')                        
                            elif(predictions4==1):
                                mensaje=f'{i} Maleza'
                                print('maleza')
                (x, y, w, h) = cv2.boundingRect(c)        
                cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image2,mensaje,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                i+=1
        cv2.imwrite('recorte.png',crop_img)
        cv2.imwrite("foto.png", image2)
        print('imagen procesada')
    else:
        print('Error al acceder a la camara')
    camara.release()
    print("ewe")


def btnExit():
    print('saliendo')
    posactx=posicionx(0)
    posacty=posiciony(0)
    movimientoxy(posactx,posacty,'0\n','0\n')
    window.destroy()
    
    
#Organizacion de la interfaz
    
#Organizacion
f1=Frame(window,width=900,height=150,bg=colormargen)
f1.place(x=0,y=0)
f2=Frame(window,width=900,height=250,bg=colormargen)
f2.place(x=0,y=750)
f3=Frame(window,width=150,height=900,bg=colormargen)
f3.place(x=0,y=0)
f4=Frame(window,width=200,height=900,bg=colormargen)
f4.place(x=750,y=0)

f8=Frame(window,width=810,height=130,bg='grey67')
f8.place(x=30,y=800)

logoupiita=PhotoImage(file=r"logoupiita150.png")
f5=Label(window,image=logoupiita,bd=0)
f5.place(x=750,y=0)
logopoli=PhotoImage(file=r"logopoli150.png")
f6=Label(window,image=logopoli,bd=0)
f6.place(x=0,y=0)
f7=Label(window,text="INSTITUTO POLITÉCNICO NACIONAL",bg=colormargen,font=("Arial",15),fg="ghost white")
f7.place(x=270,y=20)
f9=Label(window,text="UNIDAD PROFESIONAL INTERDISCIPLINARIA EN INGENIERÍA Y TECNOLOGÍAS AVANZADAS",bg=colormargen,font=("Arial",10),fg="ghost white")
f9.place(x=160,y=55)
f10=Label(window,text="ROBOT CARTESIANO",bg=colormargen,font=("Arial",30),fg="ghost white")
f10.place(x=240,y=80)    
    


    
Plantar=Button(window,text="Plantar",font=("Arial",20),background="lime green",height=1,width=10,command=plantar);
Monitorear=Button(window,text="Monitorear",font=("Arial",20),background="khaki1",height=1,width=10,command=monitorear);
Regar=Button(window,text="Regar",font=("Arial",20),background="cyan",height=1,width=10,command=regar);
Salir=Button(window,text="Salir",font=("Arial",20),background="Brown3",height=1,width=10,command=btnExit);
Rauto=Button(window,text="R automatico",font=("Arial",20),background="Skyblue2",height=1,width=10,command=regadoautomatico);

ybotones=815
xbotones=40
Monitorear.place(x=xbotones,y=ybotones);
Plantar.place(x=xbotones+160,y=ybotones);
Regar.place(x=xbotones+(160*2),y=ybotones);
Salir.place(x=xbotones+(160*4),y=ybotones);
Rauto.place(x=xbotones+(160*3),y=ybotones);

Plantas=ttk.Combobox(window,font=("Arial",20),background="Brown3",height=30,width=8);
Plantas['values']=("Lechuga","Zanahoria","Rabano","Jitomate");
Plantas.current(1)
Plantas.place(x=200,y=875)


# ybotones=775
# xbotones=140
# Monitorear.place(x=xbotones,y=ybotones);
# Plantar.place(x=xbotones+125,y=ybotones);
# Regar.place(x=xbotones+(125*2),y=ybotones);
# Salir.place(x=xbotones+(125*4),y=ybotones);
# Rauto.place(x=xbotones+(125*3),y=ybotones);

# Plantas=ttk.Combobox(window,font=("Arial",15),background="Brown3",height=30,width=8);
# Plantas['values']=("Lechuga","Zanahoria","Rabano","Jitomate");
# Plantas.current(1)
# Plantas.place(x=270,y=825)



selected=IntVar()
lechuga1=Radiobutton(window,value=1,variable=selected,background=color);
lechuga2=Radiobutton(window,value=2,variable=selected,background=color);
lechuga3=Radiobutton(window,value=3,variable=selected,background=color);
lechuga4=Radiobutton(window,value=4,variable=selected,background=color);
lechuga5=Radiobutton(window,value=5,variable=selected,background=color);

zanahoria1=Radiobutton(window,value=6,variable=selected,background=color);
zanahoria2=Radiobutton(window,value=7,variable=selected,background=color);
zanahoria3=Radiobutton(window,value=8,variable=selected,background=color);
zanahoria4=Radiobutton(window,value=9,variable=selected,background=color);
zanahoria5=Radiobutton(window,value=10,variable=selected,background=color);
zanahoria6=Radiobutton(window,value=11,variable=selected,background=color);
zanahoria7=Radiobutton(window,value=12,variable=selected,background=color);
zanahoria8=Radiobutton(window,value=13,variable=selected,background=color);
zanahoria9=Radiobutton(window,value=14,variable=selected,background=color);
zanahoria10=Radiobutton(window,value=15,variable=selected,background=color);
zanahoria11=Radiobutton(window,value=16,variable=selected,background=color);
zanahoria12=Radiobutton(window,value=17,variable=selected,background=color);
zanahoria13=Radiobutton(window,value=18,variable=selected,background=color);
zanahoria14=Radiobutton(window,value=19,variable=selected,background=color);
zanahoria15=Radiobutton(window,value=20,variable=selected,background=color);
zanahoria16=Radiobutton(window,value=21,variable=selected,background=color);

rabano1=Radiobutton(window,value=22,variable=selected,background=color);
rabano2=Radiobutton(window,value=23,variable=selected,background=color);
rabano3=Radiobutton(window,value=24,variable=selected,background=color);
rabano4=Radiobutton(window,value=25,variable=selected,background=color);
rabano5=Radiobutton(window,value=26,variable=selected,background=color);
rabano6=Radiobutton(window,value=27,variable=selected,background=color);
rabano7=Radiobutton(window,value=28,variable=selected,background=color);
rabano8=Radiobutton(window,value=29,variable=selected,background=color);
rabano9=Radiobutton(window,value=30,variable=selected,background=color);
rabano10=Radiobutton(window,value=31,variable=selected,background=color);
rabano11=Radiobutton(window,value=32,variable=selected,background=color);
rabano12=Radiobutton(window,value=33,variable=selected,background=color);
rabano13=Radiobutton(window,value=34,variable=selected,background=color);
rabano14=Radiobutton(window,value=35,variable=selected,background=color);
rabano15=Radiobutton(window,value=36,variable=selected,background=color);
rabano16=Radiobutton(window,value=37,variable=selected,background=color);

jitomate1=Radiobutton(window,value=38,variable=selected,background=color);
jitomate2=Radiobutton(window,value=39,variable=selected,background=color);
jitomate3=Radiobutton(window,value=40,variable=selected,background=color);
jitomate4=Radiobutton(window,value=41,variable=selected,background=color);
jitomate5=Radiobutton(window,value=42,variable=selected,background=color);



lechuga1.place(x=225,y=225);
lechuga2.place(x=375,y=225);
lechuga3.place(x=300,y=300)
lechuga4.place(x=225,y=375);
lechuga5.place(x=375,y=375);


a=500
b=200
zanahoria1.place(x=a,y=b);
zanahoria2.place(x=a+66,y=b);
zanahoria3.place(x=633,y=b);
zanahoria4.place(x=699,y=b);
b=266
zanahoria5.place(x=500,y=b);
zanahoria6.place(x=566,y=b);
zanahoria7.place(x=633,y=b);
zanahoria8.place(x=700,y=b);
b=333
zanahoria9.place(x=500,y=b);
zanahoria10.place(x=566,y=b);
zanahoria11.place(x=633,y=b);
zanahoria12.place(x=700,y=b);
b=400
zanahoria13.place(x=500,y=b);
zanahoria14.place(x=566,y=b);
zanahoria15.place(x=633,y=b);
zanahoria16.place(x=700,y=b);

b=475;
rabano1.place(x=200,y=b);
rabano2.place(x=266,y=b);
rabano3.place(x=333,y=b);
rabano4.place(x=400,y=b);
b=541;
rabano5.place(x=200,y=b);
rabano6.place(x=266,y=b);
rabano7.place(x=333,y=b);
rabano8.place(x=400,y=b);
b=608;
rabano9.place(x=200,y=b);
rabano10.place(x=266,y=b);
rabano11.place(x=333,y=b);
rabano12.place(x=400,y=b);
b=675;
rabano13.place(x=200,y=b);
rabano14.place(x=266,y=b);
rabano15.place(x=333,y=b);
rabano16.place(x=400,y=b);


jitomate1.place(x=525,y=500)
jitomate2.place(x=675,y=500);
jitomate3.place(x=600,y=575)
jitomate4.place(x=525,y=650);
jitomate5.place(x=675,y=650);



window.mainloop()
