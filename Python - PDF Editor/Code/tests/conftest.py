import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter


@pytest.fixture
def pdf_3_pages(tmp_path: Path) -> Path:
    path = tmp_path / "3pages.pdf"
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(200, 300)
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture
def pdf_2_pages_different_widths(tmp_path: Path) -> Path:
    path = tmp_path / "mixed.pdf"
    writer = PdfWriter()
    writer.add_blank_page(400, 300)
    writer.add_blank_page(200, 300)
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture
def pdf_empty(tmp_path: Path) -> Path:
    path = tmp_path / "empty.pdf"
    writer = PdfWriter()
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture
def jpg_image(tmp_path: Path) -> Path:
    path = tmp_path / "foto.jpg"
    img = Image.new("RGB", (100, 200), (255, 0, 0))
    img.save(path)
    return path


@pytest.fixture
def png_transparent(tmp_path: Path) -> Path:
    path = tmp_path / "transparente.png"
    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    for x in range(10, 40):
        for y in range(10, 40):
            img.putpixel((x, y), (0, 255, 0, 255))
    img.save(path)
    return path


@pytest.fixture
def png_opaque(tmp_path: Path) -> Path:
    path = tmp_path / "opaca.png"
    img = Image.new("RGB", (80, 60), (0, 0, 255))
    img.save(path)
    return path


@pytest.fixture
def bmp_image(tmp_path: Path) -> Path:
    path = tmp_path / "bitmap.bmp"
    img = Image.new("RGB", (30, 40), (128, 128, 128))
    img.save(path)
    return path


@pytest.fixture
def tiff_image(tmp_path: Path) -> Path:
    path = tmp_path / "image.tiff"
    img = Image.new("RGB", (60, 90), (0, 255, 255))
    img.save(path)
    return path


@pytest.fixture
def invalid_file(tmp_path: Path) -> Path:
    path = tmp_path / "not_an_image.txt"
    path.write_text("não é uma imagem")
    return path


@pytest.fixture
def nonexistent_file() -> str:
    return "/tmp/nao_existe_12345.pdf"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    return tmp_path / "output"
