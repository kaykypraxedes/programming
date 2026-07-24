# PDF Editor

Terminal-based PDF editor in Python, supporting page extraction, merging of multiple files (PDFs and images), and image-to-PDF conversion, using `pypdf` and `Pillow`.

**Developer:** Kayky Moreira Praxedes

---

## Features

- **Extract PDF pages** — Selects a range (or multiple ranges) of pages from a PDF and saves to a new file. Supports chained extractions in the same command (e.g., `1-3-10, 12-15`).
- **Merge PDFs and images** — Combines multiple PDF files and images (PNG, JPG, BMP, TIFF) into a single PDF, in the given order. Images are proportionally resized to the width of the last processed PDF.
- **Convert image to PDF** — Converts an image to PDF, with an option to resize it to A4 width (595 pt) while maintaining the original aspect ratio.

### Helpers

General-purpose helper functions:

- `defineNomeDisponivel(name)` — Prevents file overwriting: if the name already exists, adds an incremental `(n)` suffix.
- `removerTransparencia(img)` — Converts PNG images (or other formats with an alpha channel) to RGB, filling the background with white.
- `calculaLargura(files)` — Returns the width (in points) of the first page of the first PDF in the list. If no PDF is found, returns 595 (A4 width).
- `redimensionaPdf(page, maxWidth)` — Resizes a PDF page proportionally to a target width. Modifies the object in-place.

### Main Operations

#### `extrairPdf(startPage, endPage, inputFile)`
Extracts a range of pages from a PDF to a new file. The output filename follows the pattern `original(start-end).pdf`.
1. Validates that the indices are within the total number of pages.
2. Copies the pages in the range to a `PdfWriter`.
3. Saves the new file with an available name (prevents overwriting).

#### `mesclarPdf(inputFiles)`
Merges a list of PDFs and images into a single file. Images are automatically converted to PDF before merging.
1. Determines the initial reference width with `calculaLargura`.
2. For each file:
   - If it is an image: converts to a temporary PDF with `imagemParaPdf`, resizing to the reference width.
   - If it is a PDF: copies all pages and updates the reference width to the last page.
3. Removes the temporary PDFs created.
4. Saves the merged file as `firstFile(merged).pdf`.

#### `imagemParaPdf(imageFile, outputFile=None, width=None)`
Converts an image to PDF. Accepts PNG, JPG, BMP, and TIFF.
1. Opens the image, removes transparency (white background), and saves as PDF.
2. If `width` is provided, resizes the page to that width (maintaining aspect ratio).
3. If `outputFile` is not provided, the name is derived from the original file with `.pdf` extension and availability check.

**Special cases:**
- PNGs with transparency automatically receive a white background.
- When called internally by `mesclarPdf`, the filename does not go through `defineNomeDisponivel` (the temporary uses a fixed name).

---

## Safety / Limitations / Robustness

- **No overwrite confirmation** — Only the `defineNomeDisponivel` helper prevents overwriting, and it is not applied in all paths (e.g., temporary files during merging).
- **Python ≥ 3.10 required** — Due to the use of `match/case`.
- **Generic error handling** — All exceptions are caught as `Exception` and displayed as a simple message. There is no logging or distinction between user error and internal error.
- **Fragile input handling** — The CLI converts `input()` to `int` without validation; non-numeric input breaks the program.
- **Educational/utility project** — Suitable for personal use and learning, not recommended for production environments without the fixes noted in `PENDENCIAS.md`.

---

## Tests

The project does not have an automated test suite. Validation is done manually by running the script.

---

## Usage / Setup

### Requirements

```bash
pip install pypdf pillow
```

### Run

```bash
python pdfEditor.py
```

### Usage Examples

**Extract pages 2 to 5 and then 7 to 10:**
```
1
"/path/to/document.pdf"
2-5, 7-10
```

**Merge two PDFs and an image:**
```
2
"/path/to/a.pdf"|"/path/to/b.pdf"|"/path/to/photo.png"
```

**Convert image to PDF (direct):**
```
3
"/path/to/photo.png"
1
```
