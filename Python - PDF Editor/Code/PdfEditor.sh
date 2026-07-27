#!/bin/bash

source /opt/anaconda3/etc/profile.d/conda.sh
conda activate

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/PdfEditor.py"
LAST_DIR="$HOME/"

while true; do
    opcao=$(exec -a PdfEditor zenity --list \
        --title="Ferramentas PDF" \
        --text="Escolha uma opção:" \
        --column="Opção" \
        "Extrair páginas de PDF" \
        "Mesclar PDFs / imagens" \
        "Converter imagem para PDF" 2>/dev/null) || break

    case "$opcao" in
        "Extrair páginas de PDF")
            arquivo=$(exec -a PdfEditor zenity --file-selection \
                --title="Extrair páginas de PDF" \
                --filename="$LAST_DIR/" 2>/dev/null) || continue
            LAST_DIR="$(dirname "$arquivo")"

            paginas=$(exec -a PdfEditor zenity --entry \
                --title="Extrair páginas de PDF" \
                --text="Digite as páginas (ex: 1-3-10, 12-15, 1-7-9)" 2>/dev/null) || continue

            saida=$(python "$SCRIPT" 1 "$arquivo" "$paginas" 2>&1)
            ;;

        "Mesclar PDFs / imagens")
            paths=()
            while true; do
                if [ ${#paths[@]} -eq 0 ]; then
                    titulo="Selecione um arquivo (Cancelar para terminar)"
                else
                    titulo=""
                    for arq in "${paths[@]}"; do
                        titulo+=" $(basename "$arq")"
                    done
                    arquivo_base="${paths[-1]}"
                fi

                path=$(exec -a PdfEditor zenity --file-selection \
                    --title="$titulo" \
                    --filename="${arquivo_base:-$LAST_DIR/}" 2>/dev/null) || break

                paths+=("$path")
                LAST_DIR="$(dirname "$path")"
            done

            [ ${#paths[@]} -eq 0 ] && continue

            lista=$(printf "%s|" "${paths[@]}")
            lista=${lista%|}

            saida=$(python "$SCRIPT" 2 "$lista" 2>&1)
            ;;

        "Converter imagem para PDF")
            imagem=$(exec -a PdfEditor zenity --file-selection \
                --title="Converter imagem para PDF" \
                --filename="$LAST_DIR/" 2>/dev/null) || continue
            LAST_DIR="$(dirname "$imagem")"

            tipo=$(exec -a PdfEditor zenity --list \
                --title="Tipo de conversão" \
                --column="Opção" \
                "Conversão direta" \
                "Imagem com largura de A4" 2>/dev/null) || continue

            [ "$tipo" = "Conversão direta" ] && tipoConversao=1 || tipoConversao=2

            saida=$(python "$SCRIPT" 3 "$imagem" "$tipoConversao" 2>&1)
            ;;
    esac

    if [ -n "$saida" ]; then
        (exec -a PdfEditor zenity --info \
            --title="PDF Editor" \
            --width=400 \
            --text="$saida") 2>/dev/null
    fi
done

conda deactivate
