import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime, time
import unicodedata

# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bacana',
            database='relogio_ponto'
        )
        if conn.is_connected():
            print('Conexão ao banco de dados bem-sucedida.')
            # Adicionando commit aqui
            conn.commit()
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

# Função para remover acentos e caracteres especiais
def remover_acentos(texto):
    # Usando NFKD para decompor e filtrando apenas caracteres ASCII
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


# Função para editar registro de ponto
def editar_registro():
    # Criar uma janela para entrada de código e tipo de ponto
    def abrir_janela_edicao():
        codigo_funcionario = simpledialog.askinteger("Editar Registro", "Digite o código do funcionário:")
        if codigo_funcionario:
            tipo_ponto = simpledialog.askstring("Editar Registro", "Digite o tipo de ponto (Ex: Entrada Manhã):")
            if tipo_ponto:
                editar_ponto(codigo_funcionario, tipo_ponto)

    # Função para editar o registro de ponto
    def editar_ponto(codigo_funcionario, tipo_ponto):
        try:
            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Funcionarios WHERE codigo = %s", (codigo_funcionario,))
                nome_funcionario = cursor.fetchone()
                if nome_funcionario:
                    cursor.execute("SELECT data_hora FROM RegistrosPonto WHERE codigo_funcionario = %s AND tipo_ponto = %s", (codigo_funcionario, tipo_ponto))
                    registro = cursor.fetchone()
                    if registro:
                        novo_horario = simpledialog.askstring("Editar Registro", "Digite o novo horário (AAAA-MM-DD HH:MM:SS):")
                        if novo_horario:
                            cursor.execute("UPDATE RegistrosPonto SET data_hora = %s WHERE codigo_funcionario = %s AND tipo_ponto = %s", (novo_horario, codigo_funcionario, tipo_ponto))
                            conn.commit()
                            messagebox.showinfo("Sucesso", f"Registro de ponto atualizado com sucesso para {nome_funcionario[0]}.")
                    else:
                        messagebox.showerror("Erro", f"Registro de ponto não encontrado para {nome_funcionario[0]} e tipo de ponto {tipo_ponto}.")
                else:
                    messagebox.showerror("Erro", "Código de funcionário não encontrado.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao editar registro de ponto: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    # Chamar a função para abrir a janela de edição
    abrir_janela_edicao()

# Função para excluir registro de ponto
def excluir_registro():
    # Criar uma janela para entrada de código, tipo de ponto e data
    def abrir_janela_exclusao():
        codigo_funcionario = simpledialog.askinteger("Excluir Registro", "Digite o código do funcionário:")
        if codigo_funcionario:
            tipo_ponto = simpledialog.askstring("Excluir Registro", "Digite o tipo de ponto (Ex: Entrada Manhã):")
            if tipo_ponto:
                data = simpledialog.askstring("Excluir Registro", "Digite a data (AAAA-MM-DD):")
                if data:
                    excluir_ponto(codigo_funcionario, tipo_ponto, data)

    # Função para excluir o registro de ponto
    def excluir_ponto(codigo_funcionario, tipo_ponto, data):
        try:
            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Funcionarios WHERE codigo = %s", (codigo_funcionario,))
                nome_funcionario = cursor.fetchone()
                if nome_funcionario:
                    cursor.execute("SELECT data_hora FROM RegistrosPonto WHERE codigo_funcionario = %s AND tipo_ponto = %s AND DATE(data_hora) = %s", (codigo_funcionario, tipo_ponto, data))
                    registro = cursor.fetchone()
                    if registro:
                        confirmacao = messagebox.askokcancel("Confirmação", f"Você deseja excluir o registro de ponto para {nome_funcionario[0]} e tipo de ponto {tipo_ponto} na data {data}?")
                        if confirmacao:
                            cursor.execute("DELETE FROM RegistrosPonto WHERE codigo_funcionario = %s AND tipo_ponto = %s AND DATE(data_hora) = %s", (codigo_funcionario, tipo_ponto, data))
                            conn.commit()
                            messagebox.showinfo("Sucesso", f"Registro de ponto excluído com sucesso para {nome_funcionario[0]}.")
                    else:
                        messagebox.showerror("Erro", f"Registro de ponto não encontrado para {nome_funcionario[0]}, tipo de ponto {tipo_ponto} e data {data}.")
                else:
                    messagebox.showerror("Erro", "Código de funcionário não encontrado.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao excluir registro de ponto: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    # Chamar a função para abrir a janela de exclusão
    abrir_janela_exclusao()

    # Chamar a função para abrir a janela de exclusão
    abrir_janela_exclusao()

# Função para registrar ponto
def registrar_ponto(tipo_ponto):
    # Criar uma janela para entrada de código de funcionário
    def abrir_janela_registro():
        codigo_funcionario = simpledialog.askinteger("Registrar Ponto", "Digite o código do funcionário:")
        if codigo_funcionario:
            verificar_registro(codigo_funcionario, tipo_ponto)

    # Função para verificar o registro de ponto
    def verificar_registro(codigo_funcionario, tipo_ponto):
        try:
            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome FROM Funcionarios WHERE codigo = %s", (codigo_funcionario,))
                nome_funcionario = cursor.fetchone()
                if nome_funcionario:
                    # Verificar se o funcionário já registrou entrada manhã
                    if tipo_ponto == "Saída Manhã":
                        cursor.execute("SELECT tipo_ponto FROM RegistrosPonto WHERE codigo_funcionario = %s AND tipo_ponto = 'Entrada Manhã'", (codigo_funcionario,))
                        entrada_manha = cursor.fetchone()
                        if not entrada_manha:
                            messagebox.showerror("Erro", "Você não registrou entrada pela manhã.")
                            return
                    # Verificar se o funcionário já registrou entrada tarde
                    if tipo_ponto == "Saída Tarde":
                        cursor.execute("SELECT tipo_ponto FROM RegistrosPonto WHERE codigo_funcionario = %s AND tipo_ponto IN ('Entrada Manhã', 'Entrada Tarde')", (codigo_funcionario,))
                        entrada_tarde = cursor.fetchone()
                        if not entrada_tarde:
                            messagebox.showerror("Erro", "Você não registrou entrada.")
                            return
                    # Pop-up de confirmação
                    confirmacao = messagebox.askokcancel("Confirmação", f"Você deseja registrar um ponto de {tipo_ponto} para {nome_funcionario[0]}?")
                    if confirmacao:
                        # Registrar o ponto
                        cursor.execute("INSERT INTO RegistrosPonto (codigo_funcionario, tipo_ponto, data_hora) VALUES (%s, %s, NOW())", (codigo_funcionario, tipo_ponto))
                        conn.commit()
                        messagebox.showinfo("Sucesso", f"Ponto {tipo_ponto} registrado com sucesso para {nome_funcionario[0]}.")
                else:
                    messagebox.showerror("Erro", "Código de funcionário não encontrado.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar ponto: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

    # Chamar a função para abrir a janela de registro
    abrir_janela_registro()

# Função para fazer login
def fazer_login():
    # Cria uma janela de login
    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x200")

    # Função para verificar o login
    def verificar_login():
        if entry_login.get() == "admin" and entry_senha.get() == "admin":
            gerar_relatorio()
            login_window.destroy()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    # Labels e Entry para inserir o login e senha
    label_login = tk.Label(login_window, text="Login:")
    label_login.pack(pady=10)
    entry_login = tk.Entry(login_window)
    entry_login.pack()

    label_senha = tk.Label(login_window, text="Senha:")
    label_senha.pack(pady=10)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.pack()

    # Botão para fazer login
    button_login = tk.Button(login_window, text="Login", command=verificar_login)
    button_login.pack(pady=20)

# Função para gerar relatório
def gerar_relatorio():
    # Pop-up de confirmação
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja gerar o relatório?"):
        try:
            conn = conectar_bd()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT f.codigo, f.nome, DATE_FORMAT(rp.data_hora, '%d/%m/%Y %H:%i:%s'), rp.tipo_ponto FROM Funcionarios f INNER JOIN RegistrosPonto rp ON f.codigo = rp.codigo_funcionario ORDER BY f.codigo, rp.data_hora")
                relatorio = cursor.fetchall()

                # Criar arquivo Excel
                wb = Workbook()
                for linha in relatorio:
                    codigo_funcionario, nome_funcionario, data_hora, tipo_ponto = linha
                    nome_planilha = remover_acentos(nome_funcionario)
                    if nome_planilha not in wb.sheetnames:
                        ws = wb.create_sheet(title=nome_planilha)
                        ws.append(["Código", "Nome", "Data/Hora", "Tipo de Ponto"])
                    ws.append([codigo_funcionario, nome_funcionario, data_hora, tipo_ponto])
                wb.remove(wb["Sheet"])  # Remover a planilha padrão criada automaticamente
                wb.save("relatorio_ponto.xlsx")

                # Limpar apenas os dados de registros do banco de dados
                cursor.execute("DELETE FROM RegistrosPonto")
                conn.commit()

                messagebox.showinfo("Relatório", "Relatório gerado com sucesso.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()

# Função principal para criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Registro de Ponto")

    # Centralizar a janela na tela
    largura_janela = 600
    altura_janela = 400
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x_pos = largura_tela // 2 - largura_janela // 2
    y_pos = altura_tela // 2 - altura_janela // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    # Titulo centralizado na parte superior da janela
    label_titulo = tk.Label(root, text="Registro de Ponto", font=("Helvetica", 16))
    label_titulo.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Quadrado para registros de horários
    frame_registros = tk.Frame(root, borderwidth=2, relief="groove")
    frame_registros.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

    button_entrada_manha = tk.Button(frame_registros, text="Registrar Entrada Manhã", command=lambda: registrar_ponto("Entrada Manhã"))
    button_entrada_manha.grid(row=0, column=0, padx=10, pady=5)

    button_saida_manha = tk.Button(frame_registros, text="Registrar Saída Manhã", command=lambda: registrar_ponto("Saída Manhã"))
    button_saida_manha.grid(row=1, column=0, padx=10, pady=5)

    button_entrada_tarde = tk.Button(frame_registros, text="Registrar Entrada Tarde", command=lambda: registrar_ponto("Entrada Tarde"))
    button_entrada_tarde.grid(row=2, column=0, padx=10, pady=5)

    button_saida_tarde = tk.Button(frame_registros, text="Registrar Saída Tarde", command=lambda: registrar_ponto("Saída Tarde"))
    button_saida_tarde.grid(row=3, column=0, padx=10, pady=5)

    # Quadrado para excluir/editar registros
    frame_edicao = tk.Frame(root, borderwidth=2, relief="groove")
    frame_edicao.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    button_editar_registro = tk.Button(frame_edicao, text="Editar Registro", command=editar_registro)
    button_editar_registro.grid(row=0, column=0, padx=10, pady=5)

    button_excluir_registro = tk.Button(frame_edicao, text="Excluir Registro", command=excluir_registro)
    button_excluir_registro.grid(row=1, column=0, padx=10, pady=5)

    # Quadrado para gerar relatório
    frame_relatorio = tk.Frame(root, borderwidth=2, relief="groove")
    frame_relatorio.place(relx=0.85, rely=0.3, anchor=tk.CENTER)

    button_relatorio = tk.Button(frame_relatorio, text="Gerar Relatório", command=fazer_login)
    button_relatorio.grid(row=0, column=0, padx=10, pady=10)

    root.mainloop()

# Chamando a função principal para criar a interface gráfica
criar_interface()