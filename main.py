import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from openpyxl import Workbook

# Conectar ao banco de dados MySQL
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='bacana',
        database='relogio_ponto'
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")
    exit()

# Função para autenticar o usuário
def autenticar_usuario(username, password):
    if username == "admin" and password == "admin123":
        return "admin"
    elif username == "funcionario" and password == "func123":
        return "funcionario"
    else:
        return None

# Função para limpar os campos de entrada
def limpar_campos():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# Função para exibir a janela principal
def exibir_janela_principal(tipo_usuario):
    # Ocultar a janela de login
    frame_login.pack_forget()

    # Criar a janela principal
    root.title("Registro de Ponto")
    root.geometry("400x300")  # Aumentar o tamanho da janela

    if tipo_usuario == "admin":
        # Lógica para o usuário admin
        print("Usuário admin logado.")
    elif tipo_usuario == "funcionario":
        # Lógica para o usuário funcionário
        print("Usuário funcionário logado.")
    else:
        print("Tipo de usuário inválido.")

# Função para processar o login
def processar_login():
    username = entry_username.get()
    password = entry_password.get()
    tipo_usuario = autenticar_usuario(username, password)
    if tipo_usuario:
        exibir_janela_principal(tipo_usuario)
        limpar_campos()
    else:
        messagebox.showerror("Login Inválido", "Nome de usuário ou senha incorretos.")

# Criar janela de login
root = tk.Tk()
root.title("Login")
root.geometry("300x150")

frame_login = tk.Frame(root)

label_username = tk.Label(frame_login, text="Usuário:")
label_username.grid(row=0, column=0, padx=5, pady=5)

entry_username = tk.Entry(frame_login)
entry_username.grid(row=0, column=1, padx=5, pady=5)

label_password = tk.Label(frame_login, text="Senha:")
label_password.grid(row=1, column=0, padx=5, pady=5)

entry_password = tk.Entry(frame_login, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

button_login = tk.Button(frame_login, text="Login", command=processar_login)
button_login.grid(row=2, columnspan=2, pady=10)

frame_login.pack(padx=50, pady=50)

# Iniciar loop principal
root.mainloop()
