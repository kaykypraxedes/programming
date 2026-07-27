import os

from PIL import Image
from pypdf import PdfReader

from PdfEditor import (
    LARGURA_A4_PT,
    CalculateWidth,
    DefineAvailableName,
    RemoveTransparency,
    ResizePdfPage,
)


class TestDefineAvailableName:
    def test_nome_original_quando_nao_existe(self, tmp_path):
        caminho = str(tmp_path / "novo.pdf")
        resultado = DefineAvailableName(caminho)
        assert resultado == caminho

    def test_incrementa_quando_existe(self, tmp_path):
        caminho = str(tmp_path / "relatorio.pdf")
        open(caminho, "w").close()
        resultado = DefineAvailableName(caminho)
        assert resultado == str(tmp_path / "relatorio(1).pdf")
        open(resultado, "w").close()
        resultado2 = DefineAvailableName(caminho)
        assert resultado2 == str(tmp_path / "relatorio(2).pdf")

    def test_pula_arquivo_inexistente(self, tmp_path):
        caminho = str(tmp_path / "dados(10).pdf")
        resultado = DefineAvailableName(caminho)
        assert resultado == caminho

    def test_respeita_extensao(self, tmp_path):
        png = str(tmp_path / "foto.png")
        pdf = str(tmp_path / "foto.pdf")
        open(png, "w").close()
        resultado = DefineAvailableName(png)
        assert resultado == str(tmp_path / "foto(1).png")
        open(pdf, "w").close()
        resultado2 = DefineAvailableName(pdf)
        assert resultado2 == str(tmp_path / "foto(1).pdf")


class TestRemoveTransparency:
    def test_png_alpha_vira_rgb(self, png_transparent):
        img = Image.open(png_transparent).convert("RGBA")
        assert img.mode == "RGBA"
        resultado = RemoveTransparency(img)
        assert resultado.mode == "RGB"

    def test_fundo_branco_em_alpha(self, png_transparent):
        img = Image.open(png_transparent).convert("RGBA")
        resultado = RemoveTransparency(img)
        pixel = resultado.getpixel((0, 0))
        assert pixel == (255, 255, 255)

    def test_jpg_sem_alpha_permanece_rgb(self, jpg_image):
        img = Image.open(jpg_image).convert("RGB")
        resultado = RemoveTransparency(img)
        assert resultado.mode == "RGB"

    def test_imagem_opaca_inalterada(self, png_opaque):
        img = Image.open(png_opaque).convert("RGBA")
        resultado = RemoveTransparency(img)
        assert resultado.mode == "RGB"
        pixel_original = Image.open(png_opaque).getpixel((0, 0))
        pixel_resultado = resultado.getpixel((0, 0))
        assert pixel_resultado == pixel_original


class TestCalculateWidth:
    def test_com_pdf_retorna_largura(self, pdf_3_pages, jpg_image):
        largura = CalculateWidth([str(jpg_image), str(pdf_3_pages)])
        leitor = PdfReader(str(pdf_3_pages))
        assert largura == leitor.pages[0].mediabox.width

    def test_sem_pdf_retorna_a4(self, jpg_image):
        largura = CalculateWidth([str(jpg_image)])
        assert largura == LARGURA_A4_PT

    def test_lista_vazia_retorna_a4(self):
        largura = CalculateWidth([])
        assert largura == LARGURA_A4_PT

    def test_ignora_nao_pdf(self, png_transparent, pdf_3_pages):
        largura = CalculateWidth([str(png_transparent), str(pdf_3_pages)])
        leitor = PdfReader(str(pdf_3_pages))
        assert largura == leitor.pages[0].mediabox.width


class TestResizePdfPage:
    def test_retorna_none(self, pdf_3_pages):
        leitor = PdfReader(str(pdf_3_pages))
        pagina = leitor.pages[0]
        resultado = ResizePdfPage(pagina, 400)
        assert resultado is None

    def test_redimensiona_largura(self, pdf_3_pages):
        leitor = PdfReader(str(pdf_3_pages))
        pagina = leitor.pages[0]
        ResizePdfPage(pagina, 400)
        assert pagina.mediabox.width == 400

    def test_mantem_proporcao(self, pdf_3_pages):
        leitor = PdfReader(str(pdf_3_pages))
        pagina = leitor.pages[0]
        proporcao_original = pagina.mediabox.height / pagina.mediabox.width
        ResizePdfPage(pagina, 100)
        proporcao_nova = pagina.mediabox.height / pagina.mediabox.width
        assert abs(proporcao_original - proporcao_nova) < 0.01
