import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, Label, END
import socket
import threading
import math

class NameEntryApp:
    def __init__(self, window):
        self.root = window
        self.root.title("Nome do Usuário")

        #self.label = Label(window, text="Digite seu nome:")
        #self.label.pack(side='left')

        #self.name_entry = Entry(window)
        #self.name_entry.pack(side='left')

        self.label = Label(window, text="Digite seu nome:")
        self.label.grid(row=0, column=0,padx=10)

        self.name_entry = Entry(window)
        self.name_entry.grid(row=0, column=1,pady=20)

        self.enter_button = Button(window, text="Entrar", command=self.iniciar_chat)
        self.enter_button.grid(row=1,column=1)

        #self.enter_button = Button(window, text="Entrar", command=self.iniciar_chat)
        #self.enter_button.pack(pady=10)

    def iniciar_chat(self):
        nome_usuario = self.name_entry.get()
        if nome_usuario:
            self.root.destroy()  # Fecha a janela de entrada de nome
            chat_root = tk.Tk()
            app = ChatApp(chat_root, nome_usuario)
            chat_root.mainloop()

class ChatApp:
    def __init__(self, root, nome_usuario):
        self.name = nome_usuario
        self.root = root
        self.root.title(f"Chat Online - Bem-vindo, {nome_usuario}")

        self.chat_display = Text(root, wrap='word', state='disabled', height=10, width=50)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.scrollbar = Scrollbar(root, command=self.chat_display.yview)
        self.scrollbar.grid(row=0, column=3, sticky='nsew')
        self.chat_display['yscrollcommand'] = self.scrollbar.set

        self.message_input = Entry(root, width=30)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = Button(root, text="Enviar", command=self.enviar_mensagem)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.clear_button = Button(root, text="Limpar", command=self.limpar_chat)
        self.clear_button.grid(row=1, column=2, padx=10, pady=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 3000))  # Substitua pelo IP e porta do servidor

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
    window = tk.Tk()

    # Calculando a posição central da tela
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 200) // 2
    window.geometry(f'300x127+{x}+{y}')

    entry_app = NameEntryApp(window)
    window.mainloop()
