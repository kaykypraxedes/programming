# helpers.sh — funções compartilhadas pelos testbenchs
# Uso: . "$(dirname "$0")/helpers.sh"

AEROPORTO="$(dirname "$0")/../airport_manager"
RESULT=""

set_input() {
    RESULT=$(printf "$1" | "$AEROPORTO" 2>&1)
}

assert_contains() {
    if echo "$RESULT" | grep -q "$1"; then
        return 0
    fi
    echo "  FALHA: esperava encontrar \"$1\""
    echo "  --- primeiras linhas da saída ---"
    echo "$RESULT" | head -10
    return 1
}

assert_not_contains() {
    if ! echo "$RESULT" | grep -q "$1"; then
        return 0
    fi
    echo "  FALHA: não esperava encontrar \"$1\""
    echo "  --- primeiras linhas da saída ---"
    echo "$RESULT" | head -10
    return 1
}
