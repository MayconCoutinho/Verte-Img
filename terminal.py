import os
from PIL import Image
import math

class ImageConverter:
    def __init__(self, diretorio_base):
        self.diretorio_base = diretorio_base
        self.extensoes_a_converter = [".jpg", ".jpeg", ".png"]
        self.arquivos_a_converter = []

    def listar_arquivos_a_converter(self):
        self.arquivos_a_converter = []

        for diretorio_pai, _, arquivos in os.walk(self.diretorio_base):
            for arquivo in arquivos:
                nome_arquivo, extensao = os.path.splitext(arquivo)
                extensao = extensao.lower()
                if extensao in self.extensoes_a_converter:
                    self.arquivos_a_converter.append(os.path.join(diretorio_pai, arquivo))

    def converter_arquivos(self):
        if not self.arquivos_a_converter:
            print("Nenhum arquivo para converter encontrado.")
            return

        total_tamanho_inicial = 0
        total_tamanho_final = 0

        print("Iniciando conversão...")

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

            print(f"Convertido: {arquivo} -> {novo_caminho}")

        diferenca_tamanho = total_tamanho_inicial - total_tamanho_final
        porcentagem_melhoria = math.ceil((diferenca_tamanho / total_tamanho_inicial) * 100)

        print(f"Conversão concluída. Total de {len(self.arquivos_a_converter)} arquivos convertidos.")
        print(f"Tamanho inicial: {self.format_size(total_tamanho_inicial)}")
        print(f"Tamanho final: {self.format_size(total_tamanho_final)}")
        print(f"Diferença: {self.format_size(diferenca_tamanho)} ({porcentagem_melhoria}% de melhoria)")

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
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    conversor = ImageConverter(diretorio_base)
    conversor.listar_arquivos_a_converter()
    conversor.converter_arquivos()
