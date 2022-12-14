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
from PIL import Image, ImageTk


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
    port_antigo = []
    port_select_antiga = ''
    portAtual = 'Nenhuma'
    while True:
        #Nomeia o arquivo CSV a ser criado
        filename = 'CSVFile_Month_%d_Day_%d_Time_%.2d-%.2d.csv'%(x.month,x.day,x.hour,x.minute)
        try:
            #Pega todas as ports disponiveis e adiciona, como uma lista, no Combobox para selecionar
            ports = serial.tools.list_ports.comports()

            portList = ['Nenhuma']

            for n in ports:
                portList.append(str(n))

            #Se uma port aparecer muda a lista de ports
            if portList != port_antigo:
                port_antigo = portList
                posta_conect = ttk.Combobox(master,values=port_antigo,font=("jost",25))
                posta_conect.place(width= int(1800*(225/screen_width)), height= int(1850*(40/screen_height)), x = screen_width/19.45, y = screen_height/1.281)
                posta_conect.set('Nenhuma')

            #Pega a porta atual e compara com a ultima port conectada, se forem diferentes entra na nova
            port_select_antiga = posta_conect.get()
            if port_select_antiga != portAtual:
                port_select_antiga = portAtual
                portAtual = posta_conect.get()

            #Da init na port selecionada
            serialInst = serial.Serial()
            serialInst.baudrate = 9600
            serialInst.port = portAtual[:5]
            serialInst.open()
            time.sleep(1)
            while True:

                #Fica verificando a adição de ports no computador
                portAtualizar = ['Nenhuma']
                for n in ports:
                    portAtualizar.append(str(n))

                #Se alguma port for adicionada irá mudar a lista de ports
                if portAtualizar != port_antigo:
                    port_antigo = portAtualizar
                    posta_conect = ttk.Combobox(master,values=port_antigo,font=("jost",25))
                    posta_conect.place(width= int(1800*(225/screen_width)), height= int(1850*(40/screen_height)), x = screen_width/19.45, y = screen_height/1.281)
                    posta_conect.set('Nenhuma')
                
                #Pega a lista da port selecionada e se for diferente da antiga da um break
                portUsando = posta_conect.get()
                if port_select_antiga != portUsando:
                    break
                
                #Espera para começar a leitura do monitor serial da port
                if serialInst.in_waiting:
                    packet = serialInst.readline()
                    line = packet.decode('utf')
                    lista = line.split(',')
                    if lista[0] == 'tempo_hh:mm:ss':
                        pass
                    else:
                        print(lista)
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
                        # if "1" in lista[3]:
                        #     botao = PhotoImage(file="botaoVerde.png")
                        #     tempoCorBotao = 6
                        # elif tempoCorBotao == 0:
                        #     botao = PhotoImage(file="botaoVermelho.png")
                        #     tempoCorBotao = 0
                        # else:
                        #     botao = PhotoImage(file="botaoVerde.png")
                        #     tempoCorBotao -=1
                        # botao = botao.subsample(1,1)

                        figural = Label(image= botao, bg= "#071f40")
                        figural.place(width= int(1750*(145/screen_width)), height= int(1750*(80/screen_height)), x = screen_width/45, y = screen_height/5.51)
                        master.update_idletasks()

                        #Edição/Criação dos dados armazenados no arquivo CSV
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

#Pegar informações da tela
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

#Nome da Aplicação + Tamanho dela
master.title('Velocímetro Eco')
master.geometry((str(int(900*(screen_width/1200)))+'x'+str(int(900*(screen_height/1000)))))
master.resizable(width= 1, height= 1)

#Coloca a imagem
img = Image.open('VELOCÍMETRO ECO.png')
img_resized = img.resize((int(900*(screen_width/1200)),int(900*(screen_height/1000))),Image.ANTIALIAS)
img_final = ImageTk.PhotoImage(img_resized)
lab_img = Label(master, image= img_final)
lab_img.pack()

#Colocando as variáveis no Tkinter + setar valores iniciais
velocidade = Label(master,textvariable=velo,font=("jost",45))
velocidade.place(width= int(1750*(303/screen_width)), height= int(1750*(155/screen_height)), x = screen_width/8.16, y = screen_height/3.7)


velocidade_media = Label(master,textvariable=velo_medio,font=("jost",40))
velocidade_media.place(width= int(1750*(257/screen_width)), height= int(1750*(136/screen_height)), x = screen_width/3.19, y = screen_height/1.71)


distancia = Label(master,textvariable=dist,font=("jost",45))
distancia.place(width= int(1750*(303/screen_width)), height= int(1750*(155/screen_height)), x = screen_width/2.06, y = screen_height/3.7)


maior_velocidade = Label(master,textvariable=maior_velo,font=("jost",25))
maior_velocidade.place(width= int(1750*(168/screen_width)), height= int(1750*(40/screen_height)), x = screen_width/1.639, y = screen_height/1.5073)


menor_velocidade = Label(master,textvariable=menor_velo,font=("jost",25))
menor_velocidade.place(width= int(1750*(168/screen_width)), height= int(1750*(40/screen_height)), x = screen_width/1.931, y = screen_height/1.247)


listas_portas = ['Nenhuma']
posta_conect = ttk.Combobox(master,values=listas_portas,font=("jost",25))
posta_conect.place(width= int(1800*(225/screen_width)), height= int(1850*(40/screen_height)), x = screen_width/19.45, y = screen_height/1.281)


botao = PhotoImage(file="botaoVermelho.png")
botao = botao.subsample(1,1)
figural = Label(image= botao, bg= "#071f40")
figural.place(width= int(1750*(145/screen_width)), height= int(1750*(80/screen_height)), x = screen_width/45, y = screen_height/5.51)


maior_velo.set('0.000')
menor_velo.set('0.000')
velo_medio.set('0.000')
velo.set('0.000') 
dist.set('0.000')
porta.set('Nenhuma')
posta_conect.set('Nenhuma')


#Não deixar o full screen
master.resizable(0, 0)

#Threding da função + o Init do Tkinter
threading.Thread(target= open_serial).start()
master.mainloop()