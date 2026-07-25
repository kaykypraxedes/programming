#!/bin/sh
# run_all.sh — executa todos os testbenchs e exibe o resumo

cd "$(dirname "$0")/.." || exit 1

if [ ! -f airport_manager ]; then
    echo "ERRO: binario 'airport_manager' nao encontrado. Execute 'make' primeiro."
    exit 1
fi

passed=0
failed=0
total=0

for tb in testbenchs/tb_*; do
    [ -x "$tb" ] || continue
    [ "$(basename "$tb")" = "run_all.sh" ] || [ "$(basename "$tb")" = "helpers.sh" ] && continue

    name=$(basename "$tb")
    total=$((total + 1))

    if sh "$tb" >/dev/null 2>&1; then
        echo "  PASS: $name"
        passed=$((passed + 1))
    else
        echo "  FAIL: $name"
        failed=$((failed + 1))
    fi
done

echo ""
echo "  ----------------------------------"
echo "  Total: $total | Passou: $passed | Falhou: $failed"
echo "  ----------------------------------"

[ "$failed" -eq 0 ]
