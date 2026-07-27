# Editor de PDF

Editor de PDF via terminal em Python, com suporte a extração de páginas, mesclagem de múltiplos arquivos (PDFs e imagens) e conversão de imagens para PDF, utilizando `pypdf` e `Pillow`.

**Desenvolvedor:** Kayky Moreira Praxedes

---

## Funcionalidades

- **Extrair páginas de PDF** — Seleciona um intervalo (ou múltiplos intervalos) de páginas de um PDF e salva em novo arquivo. Suporta extrações encadeadas no mesmo comando (ex: `1-3-10, 12-15`).
- **Mesclar PDFs e imagens** — Combina múltiplos arquivos PDF e imagens (PNG, JPG, BMP, TIFF, WEBP, GIF) em um único PDF, na ordem fornecida. Imagens são redimensionadas proporcionalmente à largura do último PDF processado.
- **Converter imagem para PDF** — Converte uma imagem para PDF, com opção de redimensionar para a largura de uma folha A4 (595 pt) mantendo a proporção original.

### Helpers

Funções auxiliares de uso geral:

- `DefineAvailableName(nome)` — Evita sobrescrita de arquivos: se o nome já existir, adiciona um sufixo `(n)` incremental.
- `RemoveTransparency(img)` — Converte imagens PNG (ou outros formatos com canal alpha) para RGB, preenchendo o fundo com branco.
- `CalculateWidth(arquivos)` — Retorna a largura (em pontos) da primeira página do primeiro PDF da lista. Se nenhum PDF for encontrado, retorna 595 (largura A4).
- `ResizePdfPage(pagina, larguraMax)` — Redimensiona uma página de PDF proporcionalmente a uma largura alvo. Modifica o objeto in-place (retorna `None`).

### Operações principais

#### `ExtractPdf(paginaInicial, paginaFinal, arquivoEntrada)`
Extrai um intervalo de páginas de um PDF para um novo arquivo. O nome do arquivo de saída segue o padrão `original(inicio-fim).pdf`.
1. Valida se os índices estão dentro do número total de páginas.
2. Copia as páginas do intervalo para um `PdfWriter`.
3. Salva o novo arquivo com nome disponível (evita sobrescrita).

#### `MergePdf(arquivosEntrada)`
Mescla uma lista de PDFs e imagens em um único arquivo. Imagens são convertidas para PDF automaticamente antes da mesclagem.
1. Determina a largura de referência inicial com `CalculateWidth`.
2. Para cada arquivo:
   - Se for imagem: converte para PDF temporário com `ImageToPdf`, redimensionando para a largura de referência.
   - Se for PDF: copia todas as páginas e atualiza a largura de referência para a última página.
3. Remove os PDFs temporários criados.
4. Salva o arquivo mesclado como `primeiroArquivo(mesclado).pdf`.

#### `ImageToPdf(arquivoImagem, arquivoSaida=None, largura=None)`
Converte uma imagem para PDF. Aceita PNG, JPG, BMP, TIFF, WEBP e GIF.
1. Abre a imagem e remove transparência (fundo branco).
2. Se `largura` for fornecida, redimensiona a imagem antes de salvar (evita I/O extra).
3. Salva como PDF.
4. Se `arquivoSaida` não for fornecido, o nome é derivado do arquivo original com extensão `.pdf` e verificação de disponibilidade.

**Casos especiais:**
- PNGs com transparência recebem fundo branco automático.
- Quando chamada internamente por `MergePdf`, o nome do arquivo não passa por `DefineAvailableName` (o temporário usa `tempfile.NamedTemporaryFile`).

---

## Testes

Testes automatizados são escritos com `pytest` e estão localizados no diretório `tests/`. Execute com:

```bash
pytest
```

---

## Uso / Configuração

### Requisitos

- **pypdf** e **Pillow**:
  ```bash
  pip install pypdf pillow
  ```
- **Zenity** (necessário apenas para o lançador GUI):
  ```bash
  # Debian/Ubuntu
  sudo apt install zenity
  ```
- **Conda** — o script `PdfEditor.sh` espera uma instalação do Anaconda em `/opt/anaconda3/` e ativa o ambiente base automaticamente.

### Executar

**Terminal (diretamente):**
```bash
python PdfEditor.py
```

**GUI (via script com diálogos de arquivo):**
```bash
bash PdfEditor.sh
```

### Exemplos de uso

**Extrair páginas 2 a 5 e depois 7 a 10:**
```
1
"/caminho/para/documento.pdf"
2-5, 7-10
```

**Mesclar dois PDFs e uma imagem:**
```
2
"/caminho/para/a.pdf"|"/caminho/para/b.pdf"|"/caminho/para/foto.png"
```

**Converter imagem para PDF (direta):**
```
3
"/caminho/para/foto.png"
1
```
