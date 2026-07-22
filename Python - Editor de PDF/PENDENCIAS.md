# Pendências

Lista de problemas identificados no código, organizados dos mais leves aos mais graves.

---

## 🔵 Leves — Padrão de escrita e estilo

### Type hints em comentário, não na sintaxe

**Onde:** Arquivo todo (ex: `defineNomeDisponivel`, `removerTransparencia`, etc.)

Os tipos são documentados como comentários `# (str) -> (str)` em vez de anotações modernas. O ideal seria usar a sintaxe nativa do Python:

```python
def defineNomeDisponivel(nome: str) -> str:
```

### Nomenclatura inconsistente

**Onde:** `mesclarPdf` (temp_pdf), `imagemParaPdf` (nomeBase, arquivoSaida)

A maior parte do código usa `camelCase` em português (`arquivoSaida`, `defineNomeDisponivel`), mas `temp_pdf` está em `snake_case`. Manter um padrão único evita estranheza.

### `nome = "Nada"` — variável morta

**Onde:** `imagemParaPdf:138`

A variável é inicializada com uma string artificial e sobrescrita nas linhas seguintes sem nunca ter sido lida. Pode ser removida.

### Comentário de tipo errado na chamada de `imagemParaPdf`

**Onde:** `mesclarPdf:111`

```python
)  # (int, str, str, str[]) -> (bool)
```

A assinatura real de `imagemParaPdf` é `(str, str | None, int | None) -> (bool)`. O comentário está incorreto.

### Comentário de tipo errado na definição de `imagemParaPdf`

**Onde:** `imagemParaPdf:136`

```python
):  # (int, str, str=None, int=None) -> (bool)
```

O primeiro parâmetro `arquivoImagem` é `str`, não `int`.

### Erro de digitação no prompt

**Onde:** `__main__:193`

```
"do arquivos" → "dos arquivos"
```

### Comentários óbvios

**Onde:** `extrairPdf:70`, `extrairPdf:75`, `imagemParaPdf:137`, etc.

```python
# Verifica o limite de páginas    # redundante — o if já diz isso
# Adiciona as páginas ao novo PDF  # redundante — o for já diz isso
```

Comentários devem explicar **o porquê**, não **o quê**.

### Número mágico 595

**Onde:** `calculaLargura:46`, `__main__:210`

595 é a largura A4 em pontos (210 mm × 72 / 25,4). Deveria ser uma constante nomeada:

```python
LARGURA_A4_PT = 595
```

### `conversao` guarda largura, não "conversão"

**Onde:** `__main__:208-210`

```python
conversao = None
if tipoDeConversao == 2:
    conversao = 595
```

A variável armazena uma largura, não o tipo de conversão. `largura` seria mais claro.

### `adicional` é nome pouco descritivo

**Onde:** `__main__:188`

```python
adicional = 0 if i == 1 else 1
```

`offset` ou `deslocamento` comunicaria melhor a intenção.

---

## 🟡 Moderados — Lógica confusa e possíveis efeitos colaterais

### `largura` reatribuída no meio do loop de mesclagem

**Onde:** `mesclarPdf:96` e `mesclarPdf:118`

A variável começa como largura de referência para redimensionar imagens (`calculaLargura`), mas é reescrita quando um PDF é encontrado:

```python
largura = calculaLargura(arquivosEntrada)  # referência inicial
# ...
    if extensao in [".png", ...]:  # imagem
        imagemParaPdf(arquivo, temp_pdf, largura)  # usa referência
    else:  # PDF
        largura = leitor.pages[-1].mediabox.width  # reatribui
```

A lógica funciona, mas é confusa e não documentada.

### `calculaLargura` vs `mesclarPdf` — inconsistência na página usada

**Onde:** `calculaLargura:45` vs `mesclarPdf:118`

- `calculaLargura` usa `pages[0]` (primeira página)
- `mesclarPdf` usa `pages[-1]` (última página)

Se um PDF tiver páginas com larguras diferentes (ex: mix retrato/paisagem), o resultado pode divergir.

### `redimensionaPdf` modifica in-place e retorna

**Onde:** `redimensionaPdf:50-57`

A função altera o objeto recebido (`pagina.scale_to(...)`) e também o retorna. Isso gera ambiguityade: quem chama pode não saber se precisa reatribuir ou não.

### `removerTransparencia` refaz `.convert("RGBA")` desnecessariamente

**Onde:** `removerTransparencia:34`

A imagem já vem em RGBA (convertida em `imagemParaPdf:146`), mas a função refaz `img.convert("RGBA")`. É redundante e custa processamento extra.

### Salva imagem como PDF, depois reabre para redimensionar

**Onde:** `imagemParaPdf:148-155`

O fluxo atual:
1. Salva a imagem como PDF (`imagem.save(nome, "PDF")`)
2. Reabre o PDF gerado (`PdfReader(nome)`)
3. Redimensiona a página e sobrescreve

Mais eficiente seria redimensionar a imagem **antes** de salvar como PDF, economizando I/O e processamento.

### `except Exception` captura `KeyboardInterrupt`

**Onde:** Todas as funções com `try/except`

Se o usuário pressionar Ctrl+C durante uma operação, `KeyboardInterrupt` é capturado como "Erro: ...", e o programa não encerra. O correto seria:

```python
except Exception as e:
    ...
except KeyboardInterrupt:
    print("\nOperação cancelada.")
    return False
```

Ou não capturar `KeyboardInterrupt`.

### Nenhuma validação de existência do arquivo de entrada

**Onde:** `extrairPdf`, `mesclarPdf`, `imagemParaPdf`

Todas as funções confiam que o path informado existe. Se o arquivo não existir:
- `PdfReader` → `FileNotFoundError`
- `Image.open` → `FileNotFoundError`

Ambos viram "❌ Erro: [Errno 2] No such file or directory", que não é amigável para usuário final. Validação com `os.path.exists()` e mensagem em português seria mais adequado.

### Nenhuma proteção contra extensão não-imagem na conversão

**Onde:** `imagemParaPdf:146`

Se o usuário passar um `.txt` ou outro formato não suportado, `Image.open` lança exceção pouco clara. Uma verificação prévia da extensão com fallback amigável evitaria frustração.

---

## 🔴 Graves — Bugs e comportamento inesperado

### Validação ausente: `paginaInicial > paginaFinal` em `extrairPdf`

**Onde:** `extrairPdf:72`

```python
if paginaInicial < 1 or paginaFinal > totalPaginas:
    print(f"Erro: O PDF tem {totalPaginas} páginas")
    return False
```

Não há verificação de que `paginaInicial <= paginaFinal`. Se o usuário digitar `5-3`, o `range(4, 3)` gera zero iterações e um PDF vazio é criado e salvo sem erro.

É necessário adicionar:

```python
if paginaInicial > paginaFinal:
    print("Erro: página inicial maior que página final")
    return False
```

### `int(input(...))` sem tratamento de exceção na CLI

**Onde:** `__main__:166` e `__main__:201`

```python
opcao = int(input(...))           # linha 166
tipoDeConversao = int(input(...))  # linha 201
```

Se o usuário digitar um valor não numérico, `ValueError` propaga e quebra o programa abruptamente. O correto seria envolver em `try/except` ou usar validação com `str.isdigit()`.

### Input vazio na extração pode crashar

**Onde:** `__main__:184-186`

```python
conjuntos = textoFormatado.split(",")
for elemento in conjuntos:
    paginas = list(map(int, elemento.split("-")))
```

Entrada como `"1-3, , 5"` produz `["1-3", "", " 5"]`. A string vazia `""` ao fazer `"".split("-")` retorna `[""]`, e `int("")` lança `ValueError`. Esse erro não é tratado porque a chamada de `extrairPdf` dentro do `for` está **fora** do `try` dela própria.

### Colisão de `_temp.pdf` com mesmo nome base

**Onde:** `mesclarPdf:108-109`

```python
nomeBase = os.path.splitext(arquivo)[0]
temp_pdf = nomeBase + "_temp.pdf"
```

Se dois arquivos de diretórios diferentes têm o mesmo nome base (ex: `/home/foto.png` e `/tmp/foto.png`), ambos geram `foto_temp.pdf`. O segundo sobrescreve o primeiro sem aviso, e a primeira imagem é perdida no PDF mesclado.

Solução: incluir diretório no nome ou usar `tempfile.NamedTemporaryFile`.

### `temp_pdf` não é limpo em caso de erro

**Onde:** `mesclarPdf:109-123`

Se `PdfReader(temp_pdf)` ou `escritor.add_page(...)` lançar uma exceção entre a criação do `temp_pdf` (linha 109) e sua remoção (linha 122-123), `os.remove` nunca executa. O ideal seria:

```python
try:
    ...
finally:
    if temp_pdf and os.path.exists(temp_pdf):
        os.remove(temp_pdf)
```

Ou usar `tempfile.NamedTemporaryFile` com gerenciador de contexto.

### `nomeBase` sobrescrita dentro do loop

**Onde:** `mesclarPdf:91` e `mesclarPdf:108`

```python
nomeBase = os.path.splitext(arquivosEntrada[0])[0]   # linha 91 — salva o base do output
# ...
for arquivo in arquivosEntrada:
    nomeBase = os.path.splitext(arquivo)[0]           # linha 108 — REESCREVE!
```

O `nomeBase` original (usado para nomear o arquivo mesclado de saída) é perdido dentro do loop. Felizmente o nome de saída já foi computado antes, mas a reatribuição é um bug em potencial se o código for modificado no futuro.

### `imagemParaPdf` não passa por `defineNomeDisponivel` quando `arquivoSaida` é fornecido

**Onde:** `imagemParaPdf:143-144`

```python
if arquivoSaida is None:
    nome = defineNomeDisponivel(nome)
else:
    nome = arquivoSaida  # sem verificação!
```

No caso da mesclagem, `arquivoSaida` é o `_temp.pdf`. Se um `_temp.pdf` já existir (execução anterior interrompida), ele é sobrescrito sem aviso.

### Lista vazia em `mesclarPdf` crasha

**Onde:** `mesclarPdf:91`

```python
nomeBase = os.path.splitext(arquivosEntrada[0])[0]
```

Se `arquivosEntrada` for uma lista vazia, `[0]` lança `IndexError`. A CLI permite isso se o usuário enviar apenas `"|"` separado.
