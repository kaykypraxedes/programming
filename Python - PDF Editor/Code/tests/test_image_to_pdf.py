from pathlib import Path

from pypdf import PdfReader

from pdfEditor import ImageToPdf


class TestImageToPdf:
    def test_jpg_para_pdf(self, jpg_image: Path):
        resultado = ImageToPdf(str(jpg_image))
        assert resultado is True
        pdf_path = str(jpg_image.parent / "foto.pdf")
        leitor = PdfReader(pdf_path)
        assert len(leitor.pages) == 1

    def test_png_transparente_fundo_branco(self, png_transparent: Path):
        resultado = ImageToPdf(str(png_transparent))
        assert resultado is True
        pdf_path = str(png_transparent.parent / "transparente.pdf")
        leitor = PdfReader(pdf_path)
        assert len(leitor.pages) == 1

    def test_png_opaca(self, png_opaque: Path):
        resultado = ImageToPdf(str(png_opaque))
        assert resultado is True
        pdf_path = str(png_opaque.parent / "opaca.pdf")
        leitor = PdfReader(pdf_path)
        assert len(leitor.pages) == 1

    def test_com_largura_none_tamanho_original(self, jpg_image: Path):
        resultado = ImageToPdf(str(jpg_image))
        assert resultado is True
        pdf_path = str(jpg_image.parent / "foto.pdf")
        leitor = PdfReader(pdf_path)
        from PIL import Image
        img = Image.open(str(jpg_image))
        assert leitor.pages[0].mediabox.width == img.width
        assert leitor.pages[0].mediabox.height == img.height

    def test_com_largura_595_redimensiona(self, jpg_image: Path):
        resultado = ImageToPdf(str(jpg_image), None, 595)
        assert resultado is True
        pdf_path = str(jpg_image.parent / "foto.pdf")
        leitor = PdfReader(pdf_path)
        assert abs(leitor.pages[0].mediabox.width - 595) < 2

    def test_com_output_file_especifico(self, jpg_image: Path):
        saida = str(jpg_image.parent / "custom.pdf")
        resultado = ImageToPdf(str(jpg_image), saida)
        assert resultado is True
        leitor = PdfReader(saida)
        assert len(leitor.pages) == 1

    def test_arquivo_inexistente(self):
        resultado = ImageToPdf("/tmp/nao_existe.png")
        assert resultado is False

    def test_formato_nao_suportado(self, invalid_file: Path):
        resultado = ImageToPdf(str(invalid_file))
        assert resultado is False

    def test_define_nome_disponivel(self, jpg_image: Path, tmp_path: Path):
        ImageToPdf(str(jpg_image))
        resultado = ImageToPdf(str(jpg_image))
        assert resultado is True
        pdf_path = str(jpg_image.parent / "foto(1).pdf")
        assert Path(pdf_path).exists()
