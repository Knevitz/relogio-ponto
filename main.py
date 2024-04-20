import tkinter as tk
from tkinter import messagebox, simpledialog
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

# Função para editar funcionários
def editar_funcionarios():
    # Solicitar o nome do funcionário a ser editado
    nome_funcionario = simpledialog.askstring("Editar Funcionários", "Digite o nome do funcionário:")
    if nome_funcionario:
        novo_nome = simpledialog.askstring("Editar Funcionários", f"Digite o novo nome para '{nome_funcionario}':")
        if novo_nome:
            try:
                cursor.execute("UPDATE Funcionarios SET nome = %s WHERE nome = %s", (novo_nome, nome_funcionario))
                conn.commit()
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao atualizar funcionário: {err}")

# Função para editar código de funcionários
def editar_codigo_funcionario():
    # Solicitar o nome do funcionário para o qual o código será editado
    nome_funcionario = simpledialog.askstring("Editar Código de Funcionário", "Digite o nome do funcionário:")
    if nome_funcionario:
        novo_codigo = simpledialog.askinteger("Editar Código de Funcionário", "Digite o novo código:")
        if novo_codigo is not None:
            try:
                cursor.execute("UPDATE Funcionarios SET codigo = %s WHERE nome = %s", (novo_codigo, nome_funcionario))
                conn.commit()
                messagebox.showinfo("Sucesso", "Código de funcionário atualizado com sucesso!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao atualizar código de funcionário: {err}")

# Função para gerar relatório
def gerar_relatorio():
    try:
        cursor.execute("SELECT codigo, nome FROM Funcionarios")
        funcionarios = cursor.fetchall()
        wb = Workbook()
        for funcionario in funcionarios:
            codigo_funcionario, nome_funcionario = funcionario
            cursor.execute("SELECT DATE_FORMAT(data, '%d/%m/%y'), hora, tipo_ponto FROM RegistrosPonto WHERE codigo_funcionario = %s", (codigo_funcionario,))
            registros = cursor.fetchall()
            ws = wb.create_sheet(title=nome_funcionario)  # Criar planilha para o funcionário
            ws.append(["Data", "Hora", "Tipo de Ponto"])
            for registro in registros:
                ws.append(registro)
        wb.remove(wb["Sheet"])  # Remover a planilha padrão criada automaticamente
        wb.save("relatorio_ponto.xlsx")
        messagebox.showinfo("Relatório Gerado", "Relatório gerado com sucesso!")
        limpar_registros()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro ao Gerar Relatório", f"Erro ao gerar relatório: {err}")

# Função para limpar os registros do banco de dados
def limpar_registros():
    try:
        cursor.execute("DELETE FROM RegistrosPonto")
        conn.commit()
        messagebox.showinfo("Limpeza de Registros", "Registros apagados com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro ao Limpar Registros", f"Erro ao limpar registros: {err}")

# Função para fazer login
def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    try:
        cursor.execute("SELECT tipo FROM Usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
        tipo_usuario = cursor.fetchone()
        if tipo_usuario:
            if tipo_usuario[0] == 'admin':
                exibir_interface_admin()
            elif tipo_usuario[0] == 'funcionario':
                exibir_interface_funcionario()
        else:
            messagebox.showerror("Login Inválido", "Usuário ou senha incorretos!")
    except mysql.connector.Error as err:
        print(f"Erro ao fazer login: {err}")

def exibir_interface_admin():
    frame_login.pack_forget()
    button_logout.pack()
    button_relatorio.pack()
    button_editar_funcionarios.pack()
    button_editar_codigo.pack()

def exibir_interface_funcionario():
    frame_login.pack_forget()
    button_logout.pack()
    frame_registrar.pack()

def logout():
    button_logout.pack_forget()
    button_relatorio.pack_forget()
    button_editar_funcionarios.pack_forget()
    button_editar_codigo.pack_forget()
    frame_registrar.pack_forget()
    frame_login.pack()

# Criar janela principal
root = tk.Tk()
root.title("Registro de Ponto")
root.geometry("400x300")  # Aumentar o tamanho da janela

# Frame para inserir código do funcionário e mostrar mensagem de boas-vindas
frame_login = tk.Frame(root)

label_usuario = tk.Label(frame_login, text="Usuário:")
label_usuario.pack()

entry_usuario = tk.Entry(frame_login)
entry_usuario.pack(pady=5)

label_senha = tk.Label(frame_login, text="Senha:")
label_senha.pack()

entry_senha = tk.Entry(frame_login, show="*")  # A senha será mostrada como asteriscos
entry_senha.pack(pady=5)

button_verificar = tk.Button(frame_login, text="Entrar", command=fazer_login)
button_verificar.pack(pady=5)

# Botão para logout
button_logout = tk.Button(root, text="Logout", command=logout)

# Botão para editar funcionários
button_editar_funcionarios = tk.Button(root, text="Editar Funcionários", command=editar_funcionarios)

# Botão para editar código de funcionários
button_editar_codigo = tk.Button(root, text="Editar Código de Funcionário", command=editar_codigo_funcionario)

# Frame para registrar entrada/saída
frame_registrar = tk.Frame(root)

button_entrada_manha = tk.Button(frame_registrar, text="Registrar Entrada Manhã")
button_entrada_manha.pack(pady=5)

button_saida_manha = tk.Button(frame_registrar, text="Registrar Saída Manhã")
button_saida_manha.pack(pady=5)

button_entrada_tarde = tk.Button(frame_registrar, text="Registrar Entrada Tarde")
button_entrada_tarde.pack(pady=5)

button_saida_tarde = tk.Button(frame_registrar, text="Registrar Saída Tarde")
button_saida_tarde.pack(pady=5)

button_relatorio = tk.Button(root, text="Gerar Relatório", command=gerar_relatorio)

# Iniciar loop principal
frame_login.pack(padx=20, pady=20)
root.mainloop()
