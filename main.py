import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from processadores import Processadores
from pdf_generator import gerar_pdf


class AppFinanceiro:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Financeiro")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f2f5")

        # Container Centralizador
        self.content = tk.Frame(root, bg="#f0f2f5")
        self.content.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(self.content, text="Analista de Extratos", font=("Segoe UI", 20, "bold"), bg="#f0f2f5").pack(pady=10)

        # Input Centralizado
        tk.Label(self.content, text="Arquivo selecionado:", bg="#f0f2f5").pack(anchor="w")
        self.entry_path = tk.Entry(self.content, font=("Segoe UI", 11), width=45, bd=1, relief="solid")
        self.entry_path.pack(pady=5, ipady=5)

        tk.Button(self.content, text="Escolher Arquivo", command=self.selecionar).pack(pady=10)

        # Botões de Bancos
        self.criar_botao("NUBANK (CSV)", "#8A05BE", lambda: self.executar("NUBANK"))
        self.criar_botao("BANCO INTER (CSV)", "#FF7A00", lambda: self.executar("INTER"))
        self.criar_botao("PICPAY (XLS/XLSX)", "#21C25E", lambda: self.executar("PICPAY"))

    def criar_botao(self, texto, cor, comando):
        btn = tk.Button(self.content, text=texto, command=comando, bg=cor, fg="white",
                        font=("Segoe UI", 10, "bold"), width=30, height=2, relief="flat", cursor="hand2")
        btn.pack(pady=5)

    def selecionar(self):
        p = filedialog.askopenfilename()
        if p:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, p)

    def executar(self, banco):
        path = self.entry_path.get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("Erro", "Selecione o arquivo!")
            return

        funcs = {"NUBANK": Processadores.nubank, "INTER": Processadores.inter, "PICPAY": Processadores.picpay}
        dados = funcs[banco](path)

        if dados:
            out = os.path.join(os.path.dirname(path), f"Relatorio_{banco}.pdf")
            gerar_pdf(dados, out)
            messagebox.showinfo("Sucesso", f"PDF gerado!\nSalvo em: {out}")


if __name__ == "__main__":
    root = tk.Tk()
    AppFinanceiro(root)
    root.mainloop()