/* Crypto.h */
#ifndef CRYPTO_H
#define CRYPTO_H
#include <string>
#include <vector>
bool testaChaves(unsigned long long int &, unsigned long long int &, unsigned long long int &);
std::string getChaves(unsigned long long int &, unsigned long long int &, unsigned long long int &);
std::string codificacao(const std::string &, unsigned long long int &, unsigned long long int &);
std::string decodificacao(const std::string &, unsigned long long int &, unsigned long long int &);
#endif
