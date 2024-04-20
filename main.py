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

# Criar janela principal
root = tk.Tk()
root.title("Registro de Ponto")
root.geometry("400x300")  # Aumentar o tamanho da janela

# Frame para inserir código do usuário e senha
frame_login = tk.Frame(root)

label_usuario = tk.Label(frame_login, text="Usuário:")
label_usuario.grid(row=0, column=0, padx=5, pady=5)
entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1, padx=5, pady=5)

label_senha = tk.Label(frame_login, text="Senha:")
label_senha.grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(frame_login, show="*")
entry_senha.grid(row=1, column=1, padx=5, pady=5)

def autenticar_usuario():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    # Verifica se o usuário e a senha correspondem ao admin
    if usuario == "admin" and senha == "admin123":
        messagebox.showinfo("Login", "Bem-vindo, admin!")
        login_sucesso(usuario)
    # Verifica se o usuário e a senha correspondem ao funcionario
    elif usuario == "funcionario" and senha == "funcionario123":
        messagebox.showinfo("Login", "Bem-vindo, funcionário!")
        login_sucesso(usuario)
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")

def login_sucesso(usuario):
    frame_login.pack_forget()  # Esconde o frame de login
    if usuario == "admin":
        criar_interface_admin()
    elif usuario == "funcionario":
        criar_interface_funcionario()

def criar_interface_admin():
    # Frame para administrar funcionários
    frame_admin = tk.Frame(root)

    label_admin = tk.Label(frame_admin, text="Você está no modo admin!")
    label_admin.pack()

    # Implemente as funcionalidades do usuário "admin" aqui
    # Por exemplo, botões para criar/editar/definir nome e código de funcionários

    frame_admin.pack()

def criar_interface_funcionario():
    # Frame para registrar entrada/saída
    frame_registrar = tk.Frame(root)

    label_bem_vindo = tk.Label(frame_registrar, text="Bem-vindo!")
    label_bem_vindo.pack(pady=10)

    label_codigo = tk.Label(frame_registrar, text="Digite o código do funcionário:")
    label_codigo.pack()

    entry_codigo = tk.Entry(frame_registrar)
    entry_codigo.pack(pady=5)

    # Função para registrar ponto
    def registrar_ponto(codigo_funcionario, tipo_ponto):
        data = datetime.today().date()
        hora = datetime.today().strftime("%H:%M:%S")
        try:
            cursor.execute("INSERT INTO RegistrosPonto (codigo_funcionario, tipo_ponto, data, hora) VALUES (%s, %s, %s, %s)", (codigo_funcionario, tipo_ponto, data, hora))
            conn.commit()
            messagebox.showinfo("Registro de Ponto", "Horário registrado com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao registrar ponto: {err}")

    button_entrada_manha = tk.Button(frame_registrar, text="Registrar Entrada Manhã", command=lambda: registrar_ponto(entry_codigo.get(), "entrada_manha"))
    button_entrada_manha.pack(pady=5)

    button_saida_manha = tk.Button(frame_registrar, text="Registrar Saída Manhã", command=lambda: registrar_ponto(entry_codigo.get(), "saida_manha"))
    button_saida_manha.pack(pady=5)

    button_entrada_tarde = tk.Button(frame_registrar, text="Registrar Entrada Tarde", command=lambda: registrar_ponto(entry_codigo.get(), "entrada_tarde"))
    button_entrada_tarde.pack(pady=5)

    button_saida_tarde = tk.Button(frame_registrar, text="Registrar Saída Tarde", command=lambda: registrar_ponto(entry_codigo.get(), "saida_tarde"))
    button_saida_tarde.pack(pady=5)

    frame_registrar.pack()

button_login = tk.Button(frame_login, text="Login", command=autenticar_usuario)
button_login.grid(row=2, columnspan=2, padx=5, pady=5)

# Iniciar loop principal
frame_login.pack(padx=20, pady=20)
root.mainloop()
