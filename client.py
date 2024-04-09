import tkinter as tk
#from tkinter import Scrollbar, Text, Entry, Button, Label, END
import ttkbootstrap as ttk
import socket
import threading
import math

class NameEntryApp:
    def __init__(self, window):
        self.root = window
        self.root.title("Nome do Usuário")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('TButton', font=('Arial', 10))

        self.box = tk.Frame(window)

        self.label = ttk.Label(self.box, text="Digite seu nome:")
        self.name_entry = ttk.Entry(self.box)
        self.enter_button = ttk.Button(window, text="Confirmar", command=self.iniciar_chat)

        self.box.pack(pady = 15)
        self.label.pack(side = 'left', padx = 5)
        self.name_entry.pack(side = 'right')
        self.enter_button.pack()


    def iniciar_chat(self):
        nome_usuario = self.name_entry.get()
        if nome_usuario:
            self.root.withdraw()  # Esconde a janela de entrada de nome
            chat_root = tk.Toplevel()  # Usar Toplevel em vez de Window
            app = ChatApp(chat_root, nome_usuario)            

class ChatApp:
    def __init__(self, root, nome_usuario):
        self.name = nome_usuario
        self.root = root
        self.root.title(f"Chat Online - Bem-vindo, {nome_usuario}")

        #self.style = ttk.Style()
        #self.style.configure('TText', font=('Arial', 10))
        #self.style.configure('TButton', font=('Arial', 10))
        #self.style.configure('TEntry', font=('Arial', 10))  

        self.chat_display = ttk.Text(root, wrap='word', state='disabled', height=10, width=50)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.scrollbar = ttk.Scrollbar(root, command=self.chat_display.yview)
        self.scrollbar.grid(row=0, column=3, sticky='nsew')
        self.chat_display['yscrollcommand'] = self.scrollbar.set

        self.message_input = ttk.Entry(root, width=30)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = ttk.Button(root, text="Enviar", command=self.enviar_mensagem)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.clear_button = ttk.Button(root, text="Limpar", command=self.limpar_chat)
        self.clear_button.grid(row=1, column=2, padx=10, pady=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 3000))

        threading.Thread(target=self.receber_mensagens).start()


    def enviar_mensagem(self):
        ''' Abaixo tem 3 parametros: 
            I. a mensagem em si; 
            II. o delimitador de paraemtro (para separar no recebimento de mensagem, qual é cada parametro);
            III. o nome do cliente.'''
        mensagem = f"{self.message_input.get()} {format(math.pi, '.10f')} {self.name}"
        if mensagem:
            self.socket.send(mensagem.encode())
            self.message_input.delete(0, tk.END)

    def receber_mensagens(self):
        while True:
            try:
                mensagem = self.socket.recv(1024).decode()
                mensagem = mensagem.split(f" {format(math.pi, '.10f')} ")
                if mensagem[0]:
                    nome = mensagem[1]
                    
                    self.chat_display.configure(state='normal')
                    self.chat_display.insert(tk.END, f'{nome}: {mensagem[0]}\n')
                    self.chat_display.configure(state='disabled')
            except ConnectionError:
                break

    def limpar_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.configure(state='disabled')


if __name__ == '__main__':
    window = ttk.Window()

    # Calculando a posição central da tela
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    window.geometry(f'300x127+{x}+{y}')

    entry_app = NameEntryApp(window)
    window.mainloop()
