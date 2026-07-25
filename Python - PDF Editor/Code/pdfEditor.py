# pdfEditor.py
# Desenvolvedor:
#     Kayky Moreira Praxedes

import os
import re
import sys
import tempfile

from PIL import Image
from pypdf import PdfReader, PdfWriter, PageObject

LARGURA_A4_PT = 595
EXTENSOES_IMAGEM_VALIDAS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp", ".gif")


# Extrai um caminho de arquivo de um token, removendo um par de aspas envolventes se existir, sem quebrar o caminho em espaços internos.
# Diferente de shlex.split, preserva espaços que façam parte do nome do arquivo (ex: paths vindos do zenity, sem aspas, ou digitados com aspas).
# Input:  token  (str)
# Output: (str)
def ExtractFilePath(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        token = token[1:-1]
    return token


# Retorna um nome de arquivo disponível adicionando um sufixo (n) incremental se o nome já existir, evitando sobrescrita.
# Input:  name  (str)
# Output: (str)
def DefineAvailableName(name: str) -> str:
    base_name, ext = os.path.splitext(name)
    match = re.search(r"\(\d+\)$", base_name)
    if match:
        base_name = base_name[: match.start()]
    i = 1
    new_name = name
    while os.path.exists(new_name):
        new_name = f"{base_name}({i}){ext}"
        i += 1
    return new_name


# Remove o canal alpha de imagens PNG, preenchendo o fundo com branco.
# Input:  img  (Image)
# Output: (Image)
def RemoveTransparency(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        return background
    return img.convert("RGB")


# Retorna a largura (em pontos) da primeira página do primeiro PDF da lista.
# Se nenhum PDF for encontrado, retorna 595 (largura A4).
# Input:  files  (list[str])
# Output: (int)
def CalculateWidth(files: list[str]) -> int:
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext == ".pdf":
            reader = PdfReader(file)
            return reader.pages[0].mediabox.width
    return LARGURA_A4_PT


# Redimensiona uma página de PDF proporcionalmente a uma largura alvo.
# Modifica a página in-place, não retorna nada.
# Input:  page (PageObject), max_width (int)
# Output: None
def ResizePdfPage(page: PageObject, max_width: int) -> None:
    ratio = max_width / page.mediabox.width
    new_width = ratio * page.mediabox.width
    new_height = ratio * page.mediabox.height
    page.scale_to(new_width, new_height)


# FUNÇÕES DO PROGRAMA

# Extrai um intervalo de páginas de um PDF e salva em um novo arquivo.
# Input:  start_page (int), end_page (int), input_file (str)
# Output: (bool)
def ExtractPdf(start_page: int, end_page: int, input_file: str) -> bool:
    try:
        if not os.path.exists(input_file):
            print("Erro: arquivo não encontrado")
            return False
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}({start_page}-{end_page}).pdf"
        output_file = DefineAvailableName(output_file)
        reader = PdfReader(input_file)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        if start_page < 1 or end_page > total_pages:
            print(f"Erro: O PDF tem {total_pages} páginas")
            return False
        if start_page > end_page:
            print("Erro: página inicial maior que página final")
            return False
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])
        with open(output_file, "wb") as pdf_file:
            writer.write(pdf_file)
        print(f"📁 Arquivo salvo: {output_file}")
        return True
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


# Mescla múltiplos arquivos (PDFs e imagens) em um único PDF.
# Imagens são convertidas para PDF temporariamente antes da mesclagem.
# Input:  input_files  (list[str])
# Output: (bool)
def MergePdf(input_files: list[str]) -> bool:
    try:
        if not input_files:
            print("Erro: nenhum arquivo informado para mesclagem")
            return False
        base_name = os.path.splitext(input_files[0])[0]
        output_file = base_name + "(mesclado).pdf"
        output_file = DefineAvailableName(output_file)
        writer = PdfWriter()
        current_width = CalculateWidth(input_files)
        for file in input_files:
            if not os.path.exists(file):
                print(f"Erro: arquivo não encontrado: {file}")
                return False
            extension = os.path.splitext(file)[1].lower()
            if extension in EXTENSOES_IMAGEM_VALIDAS:
                temp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
                temp_pdf = temp.name
                temp.close()
                try:
                    ImageToPdf(file, temp_pdf, current_width)
                    reader = PdfReader(temp_pdf)
                    writer.add_page(reader.pages[0])
                finally:
                    if os.path.exists(temp_pdf):
                        os.remove(temp_pdf)
            else:
                reader = PdfReader(file)
                current_width = reader.pages[0].mediabox.width
                for page in reader.pages:
                    writer.add_page(page)
        with open(output_file, "wb") as pdf_file:
            writer.write(pdf_file)
        print(f"📁 Arquivo salvo: {output_file}")
        return True
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


# Converte uma imagem (PNG, JPG, BMP, TIFF) para PDF.
# Opcionalmente redimensiona a página para uma largura alvo.
# Input:  image_file (str), output_file (str | None), width (int | None)
# Output: (bool)
def ImageToPdf(
    image_file: str, output_file: str | None = None, width: int | None = None
) -> bool:
    try:
        if not os.path.exists(image_file):
            print("Erro: arquivo não encontrado")
            return False
        valid_extensions = EXTENSOES_IMAGEM_VALIDAS
        if not image_file.lower().endswith(valid_extensions):
            print("Erro: formato de imagem não suportado")
            return False
        if output_file is None:
            name = os.path.splitext(image_file)[0] + ".pdf"
            name = DefineAvailableName(name)
        else:
            name = output_file
        image = Image.open(image_file).convert("RGBA")
        image = RemoveTransparency(image)
        if width is not None:
            original_w, original_h = image.size
            ratio = width / original_w
            new_w = int(original_w * ratio)
            new_h = int(original_h * ratio)
            image = image.resize((new_w, new_h), Image.LANCZOS)
        image.save(name, "PDF")
        if output_file is None:
            print(f"📁 Arquivo salvo: {name}")
        return True
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        option = int(sys.argv[1])
        cli_args = sys.argv[2:]
    else:
        option = None
        cli_args = []

    if option is None:
        while True:
            try:
                option = int(
                    input(
                        "Escolha uma opção (apenas o número):\n"
                        "(1)- Extrair páginas de PDF\n"
                        "(2)- Mesclar PDFs / imagens\n"
                        "(3)- Converter imagem para PDF\n"
                        "(0)- Encerrar a aplicação\n- "
                    )
                )
                break
            except ValueError:
                print("❌ Entrada inválida. Digite apenas o número.")

    match option:
        case 1:
            if cli_args:
                file_path = cli_args[0]
                formatted_text = cli_args[1].replace(" ", "")
            else:
                file_path = ExtractFilePath(
                    input('Insira o path entre aspas ("") do arquivo (com extensão)\n- ')
                )
                formatted_text = input(
                    "Digite as páginas (ex: 1-3-10, 12-15, 1-7-9)\n- "
                ).replace(" ", "")
            ranges = formatted_text.split(",")
            for element in ranges:
                if not element.strip():
                    continue
                pages = list(map(int, element.split("-")))
                for i in range(1, len(pages)):
                    offset = 0 if i == 1 else 1
                    ExtractPdf(pages[i - 1] + offset, pages[i], file_path)
        case 2:
            if cli_args:
                raw_input = cli_args[0]
            else:
                raw_input = input(
                    'Insira os paths entre aspas ("") dos arquivos (com extensão), separados por "|"\n- '
                )
            files = [ExtractFilePath(x) for x in raw_input.split("|")]
            MergePdf(files)
        case 3:
            if cli_args:
                file_path = cli_args[0]
                conversion_type = int(cli_args[1])
            else:
                file_path = ExtractFilePath(
                    input('Insira o path entre aspas ("") do arquivo (com extensão)\n- ')
                )
                while True:
                    try:
                        conversion_type = int(
                            input(
                                "Tipo de conversão:\n"
                                "(1)- Conversão direta\n"
                                "(2)- Imagem redimensionada para largura de folha A4\n- "
                            )
                        )
                        break
                    except ValueError:
                        print("❌ Entrada inválida. Digite apenas o número.")
            width = None
            if conversion_type == 2:
                width = 595
            ImageToPdf(file_path, None, width)
        case 0:
            print("Operação encerrada!")
        case _:
            print("❌ Opção inválida!")
