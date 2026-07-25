# RSA Encryptor

Educational implementation of the RSA algorithm in C++, with utilities for prime number generation and factorization.

**Developer:** Kayky Moreira Praxedes

---

## Features

- **Number factorization** — Decomposes a value into its prime factors, displaying processing time and the count of primes computed.
- **Smallest n-digit prime calculation** — Finds the smallest prime number with a specific number of digits using Legendre's conjecture.
- **RSA encryption/decryption** — Key generation (public and private), message encoding and decoding.

---

## Project Structure

```
Code/
├── main.cpp           # Main interface (interactive menu)
├── cripto.cpp/.h      # RSA implementation
├── fatora.cpp/.h      # Prime factor decomposition
├── primos.cpp/.h      # Prime generation (Sieve of Eratosthenes)
└── tempo.cpp/.h       # Time formatting (us → ms → s → min)
```

---

## Modules

### primos

Generates prime numbers up to a limit using the **Sieve of Eratosthenes**. The `calculaPrimos()` function builds the sieve up to `sqrt(n) + 1` and stores the primes in a vector. `primoMin()` uses Legendre's conjecture to find the smallest prime above `10^(n-1)`.

### fatora

Receives a vector of primes from the `primos` module and performs successive divisions to obtain the prime factor decomposition. Returns a formatted string (e.g., `"84 = 2^2 * 3 * 7"`).

### cripto

Implements RSA with the following operations:

- **Modular multiplication** (`modMul`) — Prevents `unsigned long long` overflow with conditional subtractions.
- **Modular exponentiation** (`modPow`) — Binary algorithm for `b^e mod n`.
- **Modular inverse** (`modInverse`) — Extended Euclidean algorithm.
- **Encoding** — Converts the message to ASCII numbers, divides into blocks smaller than `n`, and applies `C(b) = b^e mod n`.
- **Decoding** — Receives the encoded blocks, applies `D(a) = a^d mod n`, and converts back to text.

### tempo

Converts microseconds to milliseconds, seconds, or minutes + seconds for friendly display.

---

## Security and Limitations

The Sieve of Eratosthenes implemented in this project can only factor numbers whose largest prime factor is within the feasible memory limit (~4 GB for `sqrt(2^64)`, or 2³² bits). For a real RSA number (typically 2048 bits or more), its square root would already be 1024 bits — making the sieve completely unfeasible. This project illustrates precisely that naive algorithms, even when optimized, cannot break RSA in practice, serving only as an educational demonstration of the algorithm's mathematical workings.
