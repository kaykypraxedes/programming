/* tempo.h */
#ifndef TEMPO_H
#define TEMPO_H
#include <string>
#include <chrono>
// Simplificação de nome para facilitar operações de conversão
using MICRO = std::chrono::duration<unsigned long long int, std::micro>;
// Struct para armazenar o tempo de uma operação ajustado para a escala
struct TEMPO{
    int minutos{}, resto{};
    std::string escala{};
};
// Apenas retorna uma string formatada, sem modificar nenhum dado global
std::string ajustaEscala(unsigned long long int);
#endif
