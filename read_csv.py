import csv
from turtle import bgcolor
import serial
from tkinter import *
import time
import threading
import os
import datetime
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
from tkinter import ttk


# Função que puxa os dados do CSV
def open_csv():
    with open('combustao_exemplo.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        v_m = 0.000
        v_menor = []
        deltaT = 0
        x = datetime.datetime.now()
        filename = 'CSVFile_Month_%d_Day_%d_Time_%.2d-%.2d.csv'%(x.month,x.day,x.hour,x.minute)

        for n in csv_reader:
            if n[0] == 'tempo_hh:mm:ss':
                pass
            else:
                if deltaT == 0:
                    sZero = float(n[2])
                try:
                    v_media = (float(n[2])-sZero)/deltaT
                except:
                    v_media = '0.0'
                if v_m < float(n[1]):
                    maior_velo.set(str('{:.3f}'.format(float(n[1])))) 
                    v_m = float(n[1]) 
                if len(v_menor) == 5:
                    menor_velo.set(str('{:.3f}'.format(float(min(v_menor))))) 
                    v_menor = []
                v_menor.append(float(n[1]))
                velo.set(str('{:.3f}'.format(float(n[1]))))
                velo_medio.set(str('{:.3f}'.format(float(v_media))))
                dist.set(str('{:.3f}'.format(float(n[2]))))
                master.update_idletasks()
                if float(str('{:.3f}'.format(float(n[2])))) >= 0.003:
                    deltaT += 1/3600
                    if not os.path.exists(f'CSVs\{filename}'):
                        csv_guardar = ['tempo_hh:mm:ss','velocidade_Instantanea_kmh','velocidade_Media_kmh','distancia_km']
                    else:
                        x = datetime.datetime.now()
                        hora = '%.2d:%.2d:%.2d'%(x.hour,x.minute,x.second)
                        csv_guardar = [hora,n[1],v_media,n[2]]
                    with open(f'CSVs\{filename}', 'a', newline='') as csvfile:
                        csvwrite = csv.writer(csvfile)
                        csvwrite.writerow(csv_guardar)
                #print(n[0])
                time.sleep(0.01)

# Função que puxa os dados do Port Serial que seria igual a um CSV
def open_serial():
    v_m = 0.000
    deltaT = 0
    v_menor = []
    tempoCorBotao = 0
    x = datetime.datetime.now()
    while True:
        filename = 'CSVFile_Month_%d_Day_%d_Time_%.2d-%.2d.csv'%(x.month,x.day,x.hour,x.minute)
        try:
            #Tenta encontrar a Port que apresenta um Arduino conectado via USB-SERIAL
            ports = serial.tools.list_ports.comports()

            portList = []

            portAtual = 'Nenhuma'

            for n in ports:
                portList.append(str(n))

            for n in portList:
                if 'USB-SERIAL' in n:
                    portAtual = n

            serialInst = serial.Serial()
            serialInst.baudrate = 9600
            serialInst.port = portAtual[:5]
            if portAtual == 'Nenhuma':
                porta.set(portAtual)
            else:
                porta.set(portAtual[:5])
            serialInst.open()
            time.sleep(1)
            while True:
                if serialInst.in_waiting:
                    packet = serialInst.readline()
                    line = packet.decode('utf')
                    lista = line.split(',')
                    if lista[0] == 'tempo_hh:mm:ss':
                        pass
                    else:
                        print(lista[0])
                        if deltaT == 0:
                            sZero = float(lista[2])


                        try:
                            v_media = (float(lista[2])-sZero)/deltaT
                        except:
                            v_media = '0.0'
                        if v_m < float(lista[1]):
                            maior_velo.set(str('{:.3f}'.format(float(lista[1])))) 
                            v_m = float(lista[1]) 
                        if len(v_menor) == 5:
                            menor_velo.set(str('{:.3f}'.format(float(min(v_menor))))) 
                            v_menor = []
                        v_menor.append(float(lista[1]))
                        velo.set(str('{:.3f}'.format(float(lista[1]))))
                        velo_medio.set(str('{:.3f}'.format(float(v_media))))
                        dist.set(str('{:.3f}'.format(float(lista[2]))))
                        #Cria o Botão do OK, se receber 1 fica verde por 6 segundos
                        if "1" in lista[3]:
                            botao = PhotoImage(file="botaoVerde.png")
                            tempoCorBotao = 6
                        elif tempoCorBotao == 0:
                            botao = PhotoImage(file="botaoVermelho.png")
                            tempoCorBotao = 0
                        else:
                            botao = PhotoImage(file="botaoVerde.png")
                            tempoCorBotao -=1
                        botao = botao.subsample(1,1)
                        figural = Label(image= botao, bg= "#071f40")
                        figural.place(width= 140, height= 140, x = 44, y = 199) 
                        master.update_idletasks()
                        if float(str('{:.3f}'.format(float(lista[2])))) >= 0.003:
                            deltaT += 1/3600
                            if not os.path.exists(f'CSVs\{filename}'):
                                csv_guardar = ['tempo_hh:mm:ss','velocidade_Instantanea_kmh','velocidade_Media_kmh','distancia_km']
                            else:
                                x = datetime.datetime.now()
                                hora = '%.2d:%.2d:%.2d'%(x.hour,x.minute,x.second)
                                csv_guardar = [hora,lista[1],v_media,lista[2][:-2]]
                            with open(f'CSVs\{filename}', 'a', newline='') as csvfile:
                                csvwrite = csv.writer(csvfile)
                                csvwrite.writerow(csv_guardar)
        except:
            pass

#Iniciar o Tkinter
master = Tk()

#Variáveis
velo = StringVar()
velo_medio = StringVar()
dist = StringVar()
maior_velo = StringVar()
menor_velo = StringVar()
porta = StringVar()


#Nome da Aplicação + Tamanho dela
master.title('Velocímetro Eco')
master.geometry('1500x1000+190+10')
master.resizable(width= 1, height= 1)

#Coloca a imagem
img = PhotoImage(file= 'VELOCÍMETRO ECO.png')
lab_img = Label(master, image= img)
lab_img.pack()

#Colocando as variáveis no Tkinter + setar valores iniciais
velocidade = Label(master,textvariable=velo,font=("jost",45))
velocidade.place(width= 291, height= 260, x = 243, y = 300)


velocidade_media = Label(master,textvariable=velo_medio,font=("jost",40))
velocidade_media.place(width= 248, height= 218, x = 626, y = 652)


distancia = Label(master,textvariable=dist,font=("jost",45))
distancia.place(width= 291, height= 260, x = 970, y = 300)
maior_velocidade = Label(master,textvariable=maior_velo,font=("jost",25))
maior_velocidade.place(width= 164, height= 72, x = 1218, y = 731)


menor_velocidade = Label(master,textvariable=menor_velo,font=("jost",25))
menor_velocidade.place(width= 164, height= 72, x = 1033, y = 886)



posta_conect = Label(master,textvariable=porta,font=("jost",25))
posta_conect.place(width= 219, height= 72, x = 102, y = 869)


botao = PhotoImage(file="botaoVermelho.png")
botao = botao.subsample(1,1)
figural = Label(image= botao, bg= "#071f40")
figural.place(width= 140, height= 140, x = 44, y = 199) 

maior_velo.set('0.000')
menor_velo.set('0.000')
velo_medio.set('0.000')
velo.set('0.000') 
dist.set('0.000')
porta.set('Nenhuma')

#Não deixar o full screen
master.resizable(0, 0)

#Threding da função + o Init do Tkinter
threading.Thread(target= open_serial).start()
master.mainloop()