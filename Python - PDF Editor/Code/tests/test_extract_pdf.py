from pathlib import Path

from pypdf import PdfReader

from pdfEditor import ExtractPdf


class TestExtractPdf:
    def test_extracao_valida_1_3(self, pdf_3_pages: Path, tmp_path: Path):
        destino = tmp_path / "output"
        destino.mkdir()
        original = str(pdf_3_pages)
        esperado = str(pdf_3_pages.parent / "3pages(1-3).pdf")
        resultado = ExtractPdf(1, 3, original)
        assert resultado is True
        leitor = PdfReader(esperado)
        assert len(leitor.pages) == 3

    def test_extracao_1_pagina(self, pdf_3_pages: Path):
        resultado = ExtractPdf(2, 2, str(pdf_3_pages))
        assert resultado is True
        caminho = str(pdf_3_pages.parent / "3pages(2-2).pdf")
        leitor = PdfReader(caminho)
        assert len(leitor.pages) == 1

    def test_pagina_inicial_maior_que_final(self, pdf_3_pages: Path):
        resultado = ExtractPdf(3, 1, str(pdf_3_pages))
        assert resultado is False

    def test_pagina_inicial_menor_que_1(self, pdf_3_pages: Path):
        resultado = ExtractPdf(0, 2, str(pdf_3_pages))
        assert resultado is False

    def test_pagina_final_excede_total(self, pdf_3_pages: Path):
        resultado = ExtractPdf(1, 10, str(pdf_3_pages))
        assert resultado is False

    def test_arquivo_inexistente(self):
        resultado = ExtractPdf(1, 2, "/tmp/nao_existe.pdf")
        assert resultado is False

    def test_primeira_pagina(self, pdf_3_pages: Path):
        resultado = ExtractPdf(1, 1, str(pdf_3_pages))
        assert resultado is True
        caminho = str(pdf_3_pages.parent / "3pages(1-1).pdf")
        leitor = PdfReader(caminho)
        assert len(leitor.pages) == 1

    def test_ultima_pagina(self, pdf_3_pages: Path):
        resultado = ExtractPdf(3, 3, str(pdf_3_pages))
        assert resultado is True
        caminho = str(pdf_3_pages.parent / "3pages(3-3).pdf")
        leitor = PdfReader(caminho)
        assert len(leitor.pages) == 1
