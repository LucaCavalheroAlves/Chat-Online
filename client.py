import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import threading
import socket
import os
import math

class NameEntryApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Nome do Usuário")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('TButton', font=('Arial', 10))

        self.box = tk.Frame(window)

        self.label = ttk.Label(self.box, text="Digite seu nome:")
        self.name_entry = ttk.Entry(self.box)
        self.enter_button = ttk.Button(window, text="Confirmar", command=self.iniciar_chat)

        self.box.pack(pady=15)
        self.label.pack(side='left', padx=5)
        self.name_entry.pack(side='right')
        self.enter_button.pack()

    def iniciar_chat(self):
        nome_usuario = self.name_entry.get()
        if nome_usuario:
            self.window.withdraw()
            chat_window = tk.Toplevel()
            chat_window.geometry(f'800x500+200+200')
            app = ChatApp(chat_window, nome_usuario)

class ChatApp:
    def __init__(self, window, nome_usuario):
        self.name = nome_usuario
        self.window = window
        self.window.title(f"Chat Online - {self.name}")

        self.chat_box = tk.Frame(self.window)
        self.input = tk.Frame(self.window)

        self.chat_display = tk.Text(self.chat_box, wrap='word', state='disabled', height=10, width=120)
        self.chat_display.pack(side='left', padx=10)
        self.scrollbar = ttk.Scrollbar(self.chat_box, command=self.chat_display.yview)
        self.scrollbar.pack(side='right', padx=10, fill='y')
        self.message_input = ttk.Entry(self.input, width=30)
        self.message_input.pack(side='left', padx=10)
        self.send_button = ttk.Button(self.input, text="Enviar", command=self.enviar_mensagem)
        self.send_button.pack(side='left', padx=8)

        self.send_file_button = ttk.Button(self.input, text="Enviar Arquivo", command=self.enviar_arquivo)
        self.send_file_button.pack(side='left', padx=8)

        self.chat_box.pack(fill='x', padx=10, pady=10)
        self.input.pack(fill='x', padx=10, pady=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 3000))

        threading.Thread(target=self.receber_mensagens).start()

    def enviar_mensagem(self):
        mensagem = f"{self.message_input.get()} {format(math.pi, '.10f')} {self.name}"
        if mensagem:
            self.socket.send(mensagem.encode())
            self.message_input.delete(0, tk.END)

    def enviar_arquivo(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'rb') as file:
                file_data = file.read()
                file_name = os.path.basename(filename)
                message = f"Arquivo: {file_name} {file_data.hex()} {self.name()}"
                self.socket.send(message.encode())

    def receber_mensagens(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                decoded_data = data.decode()
                if decoded_data.startswith("Arquivo:"):
                    parts = decoded_data.split(" ")
                    file_name = parts[1]
                    file_data = bytes.fromhex(parts[2])
                    sender_name = parts[3]
                    self.salvar_arquivo(file_name, file_data)
                    self.exibir_mensagem(f"Arquivo recebido: {file_name} de {sender_name}")
                else:
                    self.exibir_mensagem(decoded_data)
            except ConnectionError:
                break

    def salvar_arquivo(self, file_name, file_data):
        with open(file_name, "wb") as file:
            file.write(file_data)

    def exibir_mensagem(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state='disabled')
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        self.chat_display.yview_moveto(1.0)

if __name__ == '__main__':
    Start_window = tk.Tk()
    Start_window.title("Chat Online")

    screen_width = Start_window.winfo_screenwidth()
    screen_height = Start_window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    Start_window.geometry(f'300x127+{x}+{y}')

    entry_app = NameEntryApp(Start_window)
    Start_window.mainloop()
import base64
import os
from Lib import CriptografiaRSA as rsa

from tkinter import scrolledtext, messagebox, filedialog
import tkinter as tk
import ttkbootstrap as ttk
import socket
import threading
import math
import time

#Passo 1: Coloque o nome
#Passo 2: Coloque o ipv4 do server, aparece no terminal do server.py
#Passo 3: Selecione a opção de cima, a de baixo ainda não foi programada
#Passo 4: Coloque uma porta desejada, acho que entre #1025 a 49152 não da erro, mas talvez devemos pesquisar isso
#Passo 5: Colocaria a senha, porém ainda não tem funcionalidade para ela

#comando = 'Crie', Delete e crie, Crie-Toplevel
run = []

def Tratar_janela_erro(window_antiga,dimensoes,qtd_label,text_l,font_l,pady_l):
    window_antiga.withdraw()
    window_erro = Gerenciar_Janela('Crie',{'dimensoes' : dimensoes, 'alinhamento_tela': 'centralizado'},"Aviso")
    for i in range(qtd_label):
        ttk.Label(window_erro,text=f'{text_l[i]}',font=font_l[i],background='white').pack(pady=pady_l[i])
    window_erro.protocol("WM_DELETE_WINDOW", lambda:(
    window_antiga.deiconify(),
    window_erro.destroy() ))


def Gerenciar_Janela(comando,config_janela,titulo,window_reserva=None):
    def Destroir_widgets():
        for widget in window.winfo_children():
            widget.destroy()
        return

    def Janela_title_geometry(janela_personalizada,config_janela):
        x,y = 0,0
        if config_janela['alinhamento_tela'] == 'centralizado':
            # Calculando a posição central da tela
            screen_width = janela_personalizada.winfo_screenwidth()
            screen_height = janela_personalizada.winfo_screenheight()
            x = (screen_width - 400) // 2
            y = (screen_height - 200) // 2

        janela_personalizada.geometry(f"{config_janela['dimensoes']}+{x}+{y}")
        janela_personalizada.title(titulo)

        return janela_personalizada
    

    if comando == 'Crie' and len(run) == 0:
        global window
        window = ttk.Window()
        run.append(window)
    elif comando == 'Delete e crie':
        Destroir_widgets()
    elif comando == 'Crie' and len(run) >= 1:
        window_reserva = ttk.Window()  
        window_reserva = Janela_title_geometry(window_reserva,config_janela)
        run.append(window_reserva)
        return window_reserva

    if comando == 'Crie' or comando == 'Delete e crie':
        window = Janela_title_geometry(window,config_janela) 
        return window        

    if comando == 'Crie-Toplevel':
        #global window_Toplevel  #Acho que da para tirar isso
        window_Toplevel = ttk.Toplevel()    # Usar Toplevel em vez de Window, evita msg de erro (Cria uma janela mais independente, pelo que entendi) 
        window.withdraw()                   # usa witdraw em vez de destroy, evita msg de erro (isso faz a tela não aparecer para o usuario em vez de destroila)
       
        window_Toplevel = Janela_title_geometry(window_Toplevel,config_janela)  
        return window_Toplevel
 

def Tratar_input(string,id,window_antiga,pode_numero,pode_char_esp,pode_char_alfa,limite_max_char,limite_min_char):
    validação = True
    validação_numero = validação_char_esp = validação_char_alfa = validação_max_limite = validação_min_limite = validação_vazia  = ''

    string = string.strip()
    if string == '':
        validação = False
        validação_vazia = 'Erro'
    if (pode_numero == False) and (any(char.isdigit() for char in string)):
        validação = False
        validação_numero = 'Erro'

    if (pode_char_esp == False) and (any(not char.isalnum() and not char.isspace() and not char == '.' for char in string)):
        validação = False
        validação_char_esp = 'Erro'
        
    if (pode_char_alfa == False) and (any(char.isalpha() for char in string)):    
        validação = False
        validação_char_alfa = 'Erro'
        
    if (limite_max_char != False) and (limite_max_char < len(string)):
        validação = False
        validação_max_limite = 'Erro'

    if (limite_min_char != False) and (limite_min_char > len(string)):
        validação = False
        validação_min_limite = 'Erro'

    if validação == False:
        window_antiga.withdraw() 
        window_erro = Gerenciar_Janela('Crie',{'dimensoes' : '300x127', 'alinhamento_tela': 'centralizado'},"Aviso")
        ttk.Label(window_erro,text='Aviso!!',font=('Arial',13, 'bold'),background='white').pack(pady=(5))
        if validação_numero == 'Erro':
            ttk.Label(window_erro,text='- Números não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_esp == 'Erro':
            ttk.Label(window_erro,text='- Caracteres especiais não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_char_alfa == 'Erro':
            ttk.Label(window_erro,text='- Caracteres do alfabeto não são permitidos!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_max_limite == 'Erro':     
            ttk.Label(window_erro,text=f'- É necessário que o(a) {id} contenha até {limite_max_char} caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_min_limite == 'Erro':
            ttk.Label(window_erro, text=f'- É necessário que o(a) {id} tenha no minimo {limite_min_char} de caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        if validação_vazia == 'Erro':
            ttk.Label(window_erro,text=f'- É necessário que o(a) {id} contenha até {limite_max_char} caracteres!',font=('Arial',10,'bold'),wraplength=300,background='white').pack()
        window_erro.protocol("WM_DELETE_WINDOW", lambda:(
            window_antiga.deiconify(),
            window_erro.destroy() )) # Adiciona um evento ao fechar a janela
        return string, False
    return string, True


def Chat_App(nmr_porta,senha,qtd_pessoas,window_antiga,pedido):
    def Fechar_janela_chat():
        chat_window.destroy() #Isso aqui destroy a chat_window apenas na primeira thread
        msg_close = "Protocolo_close"
        Enviar_mensagem(msg_close) #Avisa ao server, que o client desconectou
        Thread_receber.join()
        time.sleep(1) #Coloquei isso para resolver um bug em que era enviado a msg ao server que fechou a conexão, porém a msg nem chegava ao server, e a linha cliente_socket.close(), já fechava o socket antes da msg chegar no server 
        cliente_socket.close() #Cliente se desconecta de fato

    def Enviar_mensagem(msg=None, arquivo=False, nome_arquivo=None, conteudo_base64=None):
        if msg == "Protocolo_close":
            cliente_socket.send(msg.encode())
            return
        mensagem = f"{message_input.get()} {format(math.pi, '.10f')} {name}"
        if mensagem:
            cifra = rsa.cifrar(mensagem,28837,40301)
            cliente_socket.send(cifra.encode())
            message_input.delete(0, tk.END)
            
    def selecionar_arquivo():
        arquivo = filedialog.askopenfilename()
        if arquivo:
            nome_arquivo_label.config(text=f"Arquivo selecionado: {arquivo}")
            enviar_botao.config(state=tk.NORMAL, command=lambda: enviar_arquivo(arquivo))
    
     
    def enviar_arquivo(arquivo):
        with open(arquivo, "rb") as f:
            conteudo = f.read()
            conteudo_base64 = base64.b64encode(conteudo).decode()
            mensagem = f"Arquivo:{arquivo}:{conteudo_base64}"
            cliente_socket.send(mensagem.encode())
         
        
    def baixar_arquivo(nome_arquivo, conteudo_base64):
        conteudo_decodificado = base64.b64decode(conteudo_base64)
        with open(nome_arquivo, 'wb') as arquivo_salvo:
            arquivo_salvo.write(conteudo_decodificado)
        print(f'O arquivo {nome_arquivo} foi salvo com sucesso!')

    def Receber_mensagens():
        rodar = True
        while rodar:
            try:
                mensagem = cliente_socket.recv(1000000).decode()
                msg_decifrada = rsa.decifrar(mensagem, 40301, 12973)
                msg_decifrada = msg_decifrada.split(f" {format(math.pi, '.10f')} ")
                if msg_decifrada[0]:
                    if chat_window.winfo_exists():
                        nome = msg_decifrada[1]
                        chat_display.configure(state='normal')

                        if nome == name:
                            chat_display.insert(tk.END, f'{msg_decifrada[0]}\n', 'right')
                        else:
                            if msg_decifrada[0].startswith("Arquivo: "):
                                partes = msg_decifrada[0].split(": ")
                                nome_arquivo = partes[1]
                                conteudo_base64 = partes[2]
                                botao_baixar_arquivo = tk.Button(chat_display, text=f'Baixar {nome_arquivo}', command=lambda: baixar_arquivo(nome_arquivo, conteudo_base64))
                                chat_display.window_create(tk.END, window=botao_baixar_arquivo)
                                chat_display.insert(tk.END, '\n')
                            else:
                                chat_display.insert(tk.END, f'{nome}: {msg_decifrada[0]}\n', 'left')
                        Scroll_to_bottom()
                        chat_display.configure(state='disabled')
                    else:
                        rodar = False
                else:
                    rodar = False
            except ConnectionError:
                break

    def Limpar_chat():
        chat_display.configure(state='normal')
        chat_display.delete(1.0, tk.END)
        chat_display.configure(state='disabled')
        
    def Scroll_to_bottom():
        """Rola o chat para baixo."""
        chat_display.yview_moveto(1.0)

    nmr_porta, validação_a = Tratar_input(nmr_porta,'porta',window_antiga,True,False,False,5,4)
    if validação_a == True:
        senha, validação_b = Tratar_input(senha,'senha',window_antiga,True,True,True,8,3)
        if validação_b == True:
            #Abaixo a gente manda para o server, a mensagem contendo os 3 parametros abaixo, para o chat criar um novo chat lá com base nessas info
            message = f'{nmr_porta}+{senha}+{qtd_pessoas}+{pedido}'
            connection.send(message.encode())

            escutando = True
            connection.settimeout(4) #Escuta por no maximo 4s se conseguiu fazer conexão com o server
            while escutando: #Isso aqui é para ver se o servidor aceita mais uma conexão no chat, ou se já esta cheio ou se a senha está errada
                try:
                    confirmacao = connection.recv(1024).decode()
                    if confirmacao == 'Autorizado':
                        escutando = False
                        conexao_validacao = True
                        break
                    elif confirmacao == 'Recusado, Grupo nao existe':
                        escutando = False
                        conexao_validacao = False
                        Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão não existe!']
                                           , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                        Inicio()
                        return
                    elif confirmacao == 'Recusado, Grupo esta cheio':
                        escutando = False
                        conexao_validacao = False
                        Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão está cheio!']
                                           , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                        Inicio()
                        return
                    elif confirmacao == 'Recusado, Grupo já criado':
                        escutando = False
                        conexao_validacao = False
                        Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- O grupo em questão já foi criado!']
                                           , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                        Inicio()
                        return
                    elif confirmacao == 'Recusado, senha está errada!':
                        escutando = False
                        conexao_validacao = False
                        Tratar_janela_erro(window_antiga, '400x127', 2, ['Aviso!!','- A senha está incorreta!']
                                           , [('Arial',13, 'bold'),('Arial',11)] , [(5),(0)])
                        return
                except (ConnectionError,ConnectionRefusedError, TimeoutError, OSError, BlockingIOError, socket.error, socket.timeout) as a:
                        print(f'Erro: {a}') #Pode apagar isso antes de entregar a aps
                        escutando = False
                        conexao_validacao = False
                        return
            connection.settimeout(None) #Desfaz o escuta até no max 4s    

            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((ip_server, int(nmr_porta)))
              
            
            if conexao_validacao == True:
                chat_window = Gerenciar_Janela('Crie-Toplevel',
                                            {'dimensoes': '800x500','alinhamento_tela': 'nenhum' },
                                            f'Chat Online - {name} e #cliente que conecta junto')#colocar nome de quem conectou junto

                chat_box = tk.Frame(chat_window)
                input = tk.Frame(chat_window)

                chat_display = ttk.Text(chat_box,wrap='word',state='disabled',height=10,width=120)
                chat_display.pack(side = 'left',padx=10)
                # Configuração de tags para alinhamento
                chat_display.tag_configure('right', justify='right')
                chat_display.tag_configure('left', justify='left')

                scrollbar = ttk.Scrollbar(chat_box, command=chat_display.yview)
                scrollbar.pack(side='right', padx=10, fill='y')  # fill='y' para preencher a altura disponível

                message_input = ttk.Entry(input, width=30)
                message_input.pack(side='left',padx=10)

                send_button = ttk.Button(input, text="Enviar", command=Enviar_mensagem)
                send_button.pack(side='left',padx=8)

                clear_button = ttk.Button(input, text="Limpar", command=Limpar_chat)
                clear_button.pack(side='left',padx=7)
                
                selecionar_botao = tk.Button(input, text="Selecionar Arquivo", command=selecionar_arquivo)
                selecionar_botao.pack()

                nome_arquivo_label = tk.Label(input, text="")
                nome_arquivo_label.pack()

                enviar_botao = tk.Button(input, text="Enviar Arquivo", state=tk.DISABLED)
                enviar_botao.pack()
                                              
                chat_box.pack(fill='x', padx=10, pady=10)
                input.pack(fill='x', padx=10, pady=10) 
                Thread_receber = threading.Thread(target=Receber_mensagens)
                Thread_receber.start()
                chat_window.protocol("WM_DELETE_WINDOW", lambda: Fechar_janela_chat())
            else:
                cliente_socket.close()



def config_chat(box,qtd_pessoas,dimensoes,diplomacia):
    window = Gerenciar_Janela('Delete e crie',
                     {'dimensoes' : dimensoes, 'alinhamento_tela': 'centralizado'}, #Alterar largura
                     'Configuração - Chat')
    box = tk.Frame(window)
    box.pack()    
    box2 = tk.Frame(box)
    box2.pack()
    box3 = tk.Frame(box)
    box3.pack()


    label_porta = ttk.Label(box2,text=f'{diplomacia} uma porta de rede: ')
    label_porta.pack(pady=(10,5))

    input_porta = ttk.Entry(box2)
    input_porta.pack()
    
    label_senha = ttk.Label(box3,text=f'{diplomacia} a senha da rede:')
    label_senha.pack(pady=(10,5))

    input_senha = ttk.Entry(box3)
    input_senha.pack()

    if qtd_pessoas == 'cliente escolhe':
        label_qtd = ttk.Label(box3,text='Quantidade maxima de pessoas: ')
        label_qtd.pack(pady=(10,5))

        input_qtd_pessoa = ttk.Entry(box3)
        input_qtd_pessoa.pack()
        confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),int(input_qtd_pessoa.get()),window,'criar grupo'))
        input_qtd_pessoa.bind("<Return>", lambda event: confirm_button.invoke())
    elif qtd_pessoas == 'host ja escolheu':
        confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),False,window,'entrar grupo'))
    else: 
        confirm_button = ttk.Button(box,text='Confirmar', command=lambda: Chat_App(input_porta.get(),input_senha.get(),2,window,'entrar direct'))

    input_porta.focus_set()  # Define o foco para o Entry do nome do usuário
    input_senha.bind("<Return>", lambda event: confirm_button.invoke())
    confirm_button.pack(pady=(15))

  
def Inicio(): #Programar se o usuario clicar em criar grupo
    window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x150', 'alinhamento_tela' : 'centralizado'},'Escolha de chat')
    box = tk.Frame(window)
    box.pack()

    direct_chat_button = ttk.Button(box, text='Conexão Direta', width = 15, command= lambda:config_chat(box,2,'300x200','Insira'))
    create_chat_button = ttk.Button(box, text='Criar um Grupo', width = 15, command= lambda:config_chat(box,'cliente escolhe','300x250','Escolha'))
    conect_chat_button = ttk.Button(box, text='Unir-se a Grupo', width = 15, command= lambda: config_chat(box,'host ja escolheu','300x200','Insira'))

    direct_chat_button.pack(pady=(20,0))
    create_chat_button.pack(pady=10)
    conect_chat_button.pack(padx=20)

def Conectar_ao_servidor(name_entry,window_antiga):
    def Teste_conexão(): #Adicionar tela de loading
        global ip_server
        ip_server, validação = Tratar_input(input_ip_servidor.get(),'ipv4',window,True,False,False,15,7)
        if validação == True:
            try:
                global connection
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #Adicionar tela de loading aqui antes de tentar conexão, atualmente o app trava se colocar invalido
                connection.connect((ip_server, 3000))

                Inicio()
            except (ConnectionRefusedError, TimeoutError, OSError) as e: #Tela de erro ao conectar ao ip do server
                #Tratar_janela_erro(window_antiga,dimensoes,qtd_label,text_l,font_l,pady_l):
                Tratar_janela_erro(window,'400x127',3,['Aviso!!','- Não foi possivel estabelecer a conexão com o servidor!','- Verifique se o ipv4 do servidor foi digitado corretamente!'],
                                   [('Arial',13, 'bold'),('Arial',11),('Arial',11)],
                                   [(5),(0),(0)])
            return
    
    global name #Levar essa verificação para outro lugar
    name, validação = Tratar_input(name_entry,'nome',window_antiga,False,False,True,16,False)
    if validação == True:
        window = Gerenciar_Janela('Delete e crie',{'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},'Conecte ao Servidor')

        box = tk.Frame(window)
        box.pack()

        label_servidor = ttk.Label(box, text='Insira o ipv4 do servidor abaixo:')
        label_servidor.pack(pady=5)

        input_ip_servidor = ttk.Entry(box)
        input_ip_servidor.pack()

        button_servidor = ttk.Button(box, text='Confirmar',command= lambda:Teste_conexão())
        button_servidor.pack(pady=10)

        input_ip_servidor.focus_set()  # Define o foco para o Entry do nome do usuário
        input_ip_servidor.bind("<Return>", lambda event: button_servidor.invoke())


def Entrada():
    window = Gerenciar_Janela('Crie',
                              {'dimensoes':'300x127', 'alinhamento_tela' : 'centralizado'},
                              "Nome do Usuário")

    style = ttk.Style() 
    style.configure('TButton', font=('Arial', 10)) #ttk.button não aceita alterar font facilmente igual o label

    box = tk.Frame(window)
    box2 = tk.Frame(window)

    label = ttk.Label(box, text="Digite seu nome:",font=('Arial', 10, 'bold'))
    name_entry = ttk.Entry(box)
    enter_button = ttk.Button(box2, text="Confirmar", command=lambda: Conectar_ao_servidor(name_entry.get(),window)) #Programar que o comando 'enter' faça o mesmo que clicar no botao

    box.pack(pady=15)
    box2.pack()
    label.pack(side='left', padx=5)
    name_entry.pack(side='left')
    enter_button.pack()

    name_entry.focus_set()  # Define o foco para o Entry do nome do usuário
    name_entry.bind("<Return>", lambda event: enter_button.invoke())

    window.mainloop()
    window.protocol("WM_DELETE_WINDOW", lambda: window.quit())  # Fechar janela principal sem erro
          

Entrada()

