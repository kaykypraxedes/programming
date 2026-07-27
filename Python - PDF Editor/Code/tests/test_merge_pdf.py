from pathlib import Path

from pypdf import PdfReader

from PdfEditor import MergePdf


class TestMergePdf:
    def test_2_pdfs(self, pdf_3_pages: Path, pdf_2_pages_different_widths: Path):
        resultado = MergePdf([str(pdf_3_pages), str(pdf_2_pages_different_widths)])
        assert resultado is True
        saida = str(pdf_3_pages.parent / "3pages(mesclado).pdf")
        leitor = PdfReader(saida)
        assert len(leitor.pages) == 5

    def test_pdf_e_imagem(self, pdf_3_pages: Path, jpg_image: Path):
        resultado = MergePdf([str(pdf_3_pages), str(jpg_image)])
        assert resultado is True
        saida = str(pdf_3_pages.parent / "3pages(mesclado).pdf")
        leitor = PdfReader(saida)
        assert len(leitor.pages) == 4

    def test_2_imagens(self, jpg_image: Path, png_transparent: Path):
        resultado = MergePdf([str(jpg_image), str(png_transparent)])
        assert resultado is True
        saida = str(jpg_image.parent / "foto(mesclado).pdf")
        leitor = PdfReader(saida)
        assert len(leitor.pages) == 2

    def test_lista_vazia(self):
        resultado = MergePdf([])
        assert resultado is False

    def test_arquivo_inexistente_na_lista(self, pdf_3_pages: Path):
        resultado = MergePdf([str(pdf_3_pages), "/tmp/nao_existe.pdf"])
        assert resultado is False

    def test_imagem_redimensionada(self, jpg_image: Path, pdf_3_pages: Path):
        resultado = MergePdf([str(pdf_3_pages), str(jpg_image)])
        assert resultado is True
        saida = str(pdf_3_pages.parent / "3pages(mesclado).pdf")
        leitor = PdfReader(saida)
        leitor_ref = PdfReader(str(pdf_3_pages))
        assert leitor.pages[3].mediabox.width == leitor_ref.pages[0].mediabox.width

    def test_pdf_apos_imagem_atualiza_largura(
        self, jpg_image: Path, pdf_3_pages: Path
    ):
        resultado = MergePdf([str(jpg_image), str(pdf_3_pages)])
        assert resultado is True
        saida = str(jpg_image.parent / "foto(mesclado).pdf")
        leitor = PdfReader(saida)
        leitor_ref = PdfReader(str(pdf_3_pages))
        largura_imagem = leitor.pages[0].mediabox.width
        largura_pdf = leitor.pages[1].mediabox.width
        assert largura_pdf == leitor_ref.pages[0].mediabox.width

    def test_tipos_de_imagem(
        self,
        jpg_image: Path,
        png_transparent: Path,
        bmp_image: Path,
        tiff_image: Path,
    ):
        resultado = MergePdf(
            [
                str(jpg_image),
                str(png_transparent),
                str(bmp_image),
                str(tiff_image),
            ]
        )
        assert resultado is True

    def test_saida_e_pdf_valido(self, jpg_image: Path, pdf_3_pages: Path):
        resultado = MergePdf([str(jpg_image), str(pdf_3_pages)])
        assert resultado is True
        saida = str(jpg_image.parent / "foto(mesclado).pdf")
        PdfReader(saida)
