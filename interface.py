import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image
import math

class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.extensoes_a_converter = [".jpg", ".jpeg", ".png"]
        self.arquivos_a_converter = []
        
        self.root.title("Conversor de Imagens")
        
        # Configuração de estilo
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.label = Label(self.root, text="Selecione um diretório para converter imagens", font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(pady=10)
        
        self.selecionar_botao = Button(self.root, text="Selecionar Diretório", command=self.selecionar_diretorio, font=("Arial", 12))
        self.selecionar_botao.pack(pady=10)
        
        self.converter_botao = Button(self.root, text="Converter", command=self.converter_arquivos, font=("Arial", 12), bg="#009933", fg="white")
        self.converter_botao.pack(pady=10)
        
        self.info_text = ScrolledText(self.root, width=50, height=10, font=("Arial", 12), wrap=WORD)
        self.info_text.pack(pady=10)

        # Definir as tags de estilo para as cores
        self.info_text.tag_configure("vermelho", foreground="red")
        self.info_text.tag_configure("verde", foreground="green")
        self.info_text.tag_configure("azul", foreground="blue")

    def selecionar_diretorio(self):
        diretorio = filedialog.askdirectory(title="Selecione o diretório base")
        if diretorio:
            self.diretorio_base = diretorio
            self.label.config(text=f"Diretório selecionado: {self.diretorio_base}")
    
    def listar_arquivos_a_converter(self):
        self.arquivos_a_converter = []
        
        for diretorio_pai, _, arquivos in os.walk(self.diretorio_base):
            for arquivo in arquivos:
                nome_arquivo, extensao = os.path.splitext(arquivo)
                extensao = extensao.lower()
                if extensao in self.extensoes_a_converter:
                    self.arquivos_a_converter.append(os.path.join(diretorio_pai, arquivo))
    
    def converter_arquivos(self):
        if not hasattr(self, 'diretorio_base'):
            messagebox.showerror("Erro", "Selecione um diretório primeiro.")
            return
        
        self.listar_arquivos_a_converter()
        
        if not self.arquivos_a_converter:
            messagebox.showinfo("Info", "Nenhum arquivo para converter encontrado.")
            return

        mensagem_confirmacao = f"Você deseja converter {len(self.arquivos_a_converter)} arquivos?"
        if not messagebox.askyesno("Confirmação", mensagem_confirmacao):
            return

        total_tamanho_inicial = 0
        total_tamanho_final = 0

        self.info_text.delete(1.0, END)  # Limpar o texto anterior
        self.info_text.insert(END, "Iniciando conversão...\n")
        self.info_text.update()
        
        for arquivo in self.arquivos_a_converter:
            imagem = Image.open(arquivo)
            tamanho_inicial = os.path.getsize(arquivo)
            total_tamanho_inicial += tamanho_inicial

            novo_nome_arquivo = os.path.splitext(arquivo)[0] + ".webp"
            novo_caminho = os.path.join(os.path.dirname(arquivo), novo_nome_arquivo)
            imagem.save(novo_caminho, "WEBP")
            os.remove(arquivo)

            tamanho_final = os.path.getsize(novo_caminho)
            total_tamanho_final += tamanho_final

            self.info_text.insert(END, f"Convertido: {arquivo} -> {novo_caminho}\n")
            self.info_text.see("end")  # Rolar para a parte inferior
            self.info_text.update()
        
        diferenca_tamanho = total_tamanho_inicial - total_tamanho_final
        porcentagem_melhoria = math.ceil((diferenca_tamanho / total_tamanho_inicial) * 100)

        self.info_text.insert(END, "Conversão concluída. Total de ")
        self.info_text.insert(END, f"{len(self.arquivos_a_converter)}", "verde")
        self.info_text.insert(END, " arquivos convertidos.\n")
        self.info_text.insert(END, "Tamanho inicial: ", "vermelho")
        self.info_text.insert(END, f"{self.format_size(total_tamanho_inicial)}\n")
        self.info_text.insert(END, "Tamanho final: ", "verde")
        self.info_text.insert(END, f"{self.format_size(total_tamanho_final)}\n")
        self.info_text.insert(END, "Diferença: ", "azul")
        self.info_text.insert(END, f"{self.format_size(diferenca_tamanho)} ({porcentagem_melhoria}% de melhoria)\n")
        
        messagebox.showinfo("Conversão Concluída", f"{len(self.arquivos_a_converter)} arquivos convertidos e arquivos originais excluídos com sucesso.")

    def format_size(self, size):
        # Função para formatar o tamanho em bytes para um formato legível
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.2f} GB"

if __name__ == '__main__':
    root = Tk()
    app = ImageConverter(root)
    root.mainloop()
