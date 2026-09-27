# Implementação do Algoritmo AES em Python

Este projeto consiste em uma implementação didática e funcional do algoritmo de criptografia simétrica **AES (Advanced Encryption Standard)** em suas três variações de tamanho de chave: **AES-128**, **AES-192** e **AES-256**.

Além das funções de cifragem e decifragem, a aplicação conta com uma interface em linha de comando (CLI) interativa que permite testar os algoritmos e observar o **efeito avalanche** através da alteração pontual de bits da mensagem ou da chave.

---

## 📁 Estrutura do Projeto

```text
.
├── main.py
└── aes/
    ├── aes_base.py
    ├── aes128.py
    ├── aes192.py
    └── aes256.py
```

### Detalhamento dos Módulos

* **`aes/aes_base.py`**:
  Contém as operações primitivas e reutilizáveis do AES que são comuns a todas as variações de tamanho de chave, tais como:
  * Tabelas de substituição (`S-Box` e `Inverse S-Box`).
  * Funções de transformação de bloco: `SubBytes`, `ShiftRows`, `MixColumns` (e suas respectivas operações inversas).
  * Função `AddRoundKey`.
  * Constantes de rodada (`RCON`).
  * Funções utilitárias de manipulação de blocos e matrizes $4 \times 4$.

* **`aes/aes128.py`**, **`aes/aes192.py`** e **`aes/aes256.py`**:
  Contêm as implementações específicas para cada variação do padrão:
  * **Ajuste e validação do tamanho da chave** ($16$, $24$ ou $32$ bytes).
  * **Expansão de chave (*Key Schedule*)** adequada ao tamanho e número de palavras (*words*) necessárias.
  * **Fluxo de rodadas (*Rounds*)**: $10$ rodadas no AES-128, $12$ rodadas no AES-192 e $14$ rodadas no AES-256.

* **`main.py`**:
  Interface CLI interativa responsável por receber as entradas do usuário, invocar as funções de criptografia correspondentes e demonstrar a sensibilidade do algoritmo a pequenas alterações de dados (efeito avalanche).

---

## 🚀 Como Executar

### Pré-requisitos

* Python 3.10 ou superior.

### Executando a Aplicação

No terminal, execute o arquivo principal:

```bash
python main.py
```

---

## 🛠️ Funcionalidades da CLI

1. **Escolha da Variante AES**:
   O usuário escolhe entre **AES-128**, **AES-192** ou **AES-256**.

2. **Entrada de Dados**:
   O sistema solicita a **mensagem em texto claro** e a **chave de criptografia**.

3. **Cifragem e Decifragem**:
   A mensagem é cifrada e exibida em formato Hexadecimal. Em seguida, é executada a decifragem para validar a recuperação do texto original em UTF-8.

4. **Teste de Efeito Avalanche (Inversão de Bit)**:
   A CLI permite selecionar **1 bit** específico na mensagem ou na chave para inverter seu valor via operação `XOR` (`1 << bit_position`). Após a alteração, o processo de criptografia é reexecutado para demonstrar como uma mudança mínima afeta drasticamente o texto cifrado gerado.

---

## 📊 Comparativo Técnico dos Algoritmos

| Algoritmo | Tamanho da Chave | Tamanho do Bloco | Rodadas (*Rounds*) | Chave Expandida (Palavras de 32-bit) |
| :--- | :--- | :--- | :--- | :--- |
| **AES-128** | 128 bits (16 bytes) | 128 bits (16 bytes) | 10 | 44 *words* |
| **AES-192** | 192 bits (24 bytes) | 128 bits (16 bytes) | 12 | 52 *words* |
| **AES-256** | 256 bits (32 bytes) | 128 bits (16 bytes) | 14 | 60 *words* |