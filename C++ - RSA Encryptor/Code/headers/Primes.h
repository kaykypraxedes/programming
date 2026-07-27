/* Primes.h */
#ifndef PRIMES_H
#define PRIMES_H
#include <vector>
#include <cmath>
#include "Time.h"
// Outros métodos tem de ter acesso à lista de primos
std::vector<unsigned long long int> getPrimos();
// Modifica o vetor primos e retorna o tempo que demorou
unsigned long long int calculaPrimos(const unsigned long long int &);
// Modifica o vetor primos e retorna o primo
unsigned long long int primoMin(const unsigned long long int &);
void clearPrimos();
#endif
