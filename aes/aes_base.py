from typing import Sequence

S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]


INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38,
    0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87,
    0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d,
    0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2,
    0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16,
    0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
    0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a,
    0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02,
    0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea,
    0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85,
    0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89,
    0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20,
    0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31,
    0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d,
    0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0,
    0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26,
    0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]


RCON = [
    0x00,
    0x01,
    0x02,
    0x04,
    0x08,
    0x10,
    0x20,
    0x40,
    0x80,
    0x1B,
    0x36
]


def generate_msg_block(msg: str) -> list[list[list[int]]]:
    """
    Converte uma string em uma lista de blocos de 16 bytes formatados como matrizes 4x4.

    A função codifica a mensagem de entrada em UTF-8 e a divide em blocos de 16 bytes. 
    Cada bloco é convertido em uma matriz de estado 4x4 (comum em algoritmos de 
    criptografia como o AES), preenchida por colunas (column-major order). Se o 
    tamanho da mensagem não for múltiplo de 16, os bytes restantes no último bloco 
    permanecerão como 0 (zero-padding).

    Args:
        msg (str): A mensagem de texto que será convertida em blocos.

    Returns:
        list[list[list[int]]]: Uma lista de blocos. Cada bloco é uma matriz 4x4 
                               (lista de 4 listas contendo 4 inteiros cada), onde 
                               cada inteiro representa o valor em bytes da string.
    """
    msg_bytes = msg.encode("utf-8")
    msg_size = len(msg_bytes)
    blocks_qtd = msg_size // 16

    if msg_size % 16 != 0:
        blocks_qtd += 1

    blocks = [
        [[0, 0, 0, 0] for _ in range(4)]
        for _ in range(blocks_qtd)
    ]

    for i, block in enumerate(blocks):
        for j in range(16):
            idx = 16 * i + j
            if idx < msg_size:
                block[j % 4][j // 4] = msg_bytes[idx]

    return blocks

def rot_word(word):
    """
    RotWord:
    [a, b, c, d]
    
    vira
    [b, c, d, a]
    """

    return word[1:] + word[:1]


def sub_word(word):
    """
    Aplica a S-Box em cada byte da word.
    """

    return [
        S_BOX[b]
        for b in word
    ]


def xor_words(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """
    Realiza a operação bit a bit XOR (OU exclusivo) entre duas sequências de inteiros.

    A função itera simultaneamente sobre as duas sequências de entrada. Para cada 
    par de elementos, aplica o operador XOR (`^`) e retorna uma nova lista com 
    os resultados. É uma operação fundamental em algoritmos de criptografia 
    (como AES e cifras de bloco) e geração de chaves.

    Nota: Se as sequências tiverem tamanhos diferentes, o resultado terá o 
    tamanho da menor sequência, devido ao comportamento da função `zip`.

    Args:
        a (Sequence[int]): A primeira sequência de inteiros (ex: lista ou tupla de bytes/palavras).
        b (Sequence[int]): A segunda sequência de inteiros.

    Returns:
        list[int]: Uma nova lista contendo o resultado do XOR elemento a elemento.
    """
    return [
        x ^ y
        for x, y in zip(a, b)
    ]

def add_round_key(block: list[list[int]], key_block: list[list[int]]) -> None:
    """
    Aplica a chave da rodada atual ao bloco de dados utilizando a operação XOR.

    Esta função representa a etapa 'AddRoundKey' do algoritmo de criptografia AES. 
    Ela combina a matriz de estado (o bloco de dados atual) com uma subchave 
    específica da rodada (key_block). A operação é feita bit a bit (XOR) e 
    modifica o bloco original diretamente (in-place), sem retornar uma nova lista.

    Args:
        block (list[list[int]]): O bloco de dados atual (matriz de estado 4x4) 
                                 que será modificado.
        key_block (list[list[int]]): A chave da rodada atual (matriz 4x4) 
                                     que será combinada com o bloco.

    Returns:
        None: A função modifica o parâmetro `block` diretamente.
    """
    for row in range(4):
        for col in range(4):
            block[row][col] ^= key_block[row][col]


def sub_bytes(block: list[list[int]]) -> None:
    """
    Aplica uma substituição não linear de bytes no bloco de dados utilizando a S-Box.

    Esta função representa a etapa 'SubBytes' do algoritmo de criptografia AES. 
    Cada byte da matriz de estado (block) é substituído por um byte correspondente 
    encontrado em uma tabela de pesquisa global chamada S-Box (Substitution Box). 
    Essa etapa adiciona não linearidade ao algoritmo, o que é fundamental para a 
    segurança contra ataques criptoanalíticos. A modificação é feita in-place.

    Args:
        block (list[list[int]]): O bloco de dados (matriz de estado 4x4) 
                                 cujos bytes serão substituídos.

    Returns:
        None: A função não retorna nada, pois modifica o parâmetro `block` diretamente.
        
    Raises:
        NameError: Se a variável global `S_BOX` não estiver definida no escopo.
        IndexError: Se algum valor dentro do `block` for maior que o tamanho da `S_BOX` (geralmente > 255).
    """
    for row in range(4):
        for col in range(4):
            block[row][col] = S_BOX[
                block[row][col]
            ]


def shift_rows(block: list[list[int]]) -> list[list[int]]:
    """
    Realiza o deslocamento circular à esquerda dos bytes em cada linha do bloco.

    Esta função representa a etapa 'ShiftRows' do algoritmo de criptografia AES. 
    O objetivo desta etapa é espalhar os dados pelo bloco (princípio da difusão), 
    garantindo que as colunas sejam embaralhadas. Cada linha da matriz de estado 
    (block) é deslocada para a esquerda por um número de posições igual ao índice 
    da própria linha (a linha 0 não se move, a linha 1 move 1 casa, etc.).

    Diferente de algumas outras etapas do algoritmo, esta implementação retorna 
    uma nova matriz de estado, preservando a matriz original.

    Args:
        block (list[list[int]]): O bloco de dados atual (matriz de estado 4x4).

    Returns:
        list[list[int]]: Uma nova matriz 4x4 representando o bloco após o 
                         deslocamento das linhas.
    """
    result = [
        row[:]
        for row in block
    ]

    for row in range(4):
        result[row] = (
            block[row][row:]
            +
            block[row][:row]
        )

    return result

def gmul(a: int, b: int) -> int:
    """
    Realiza a multiplicação de dois inteiros no Corpo de Galois (Galois Field) GF(2^8).

    Esta operação é fundamental na etapa 'MixColumns' do algoritmo AES. Na 
    matemática dos Corpos de Galois, a adição é substituída pelo XOR, e a 
    multiplicação é feita deslocando bits e reduzindo o resultado módulo um 
    polinômio irredutível específico do AES (0x1B, que representa x^8 + x^4 + x^3 + x + 1).

    Args:
        a (int): O primeiro operando (um byte de 8 bits).
        b (int): O segundo operando (um byte de 8 bits).

    Returns:
        int: O resultado da multiplicação no campo GF(2^8), garantido como 
             um valor de 8 bits (0 a 255).
    """
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a

        high_bit = a & 0x80
        a = (a << 1) & 0xFF

        if high_bit:
            a ^= 0x1B

        b >>= 1

    return result


def mix_columns(block: list[list[int]]) -> list[list[int]]:
    """
    Realiza a etapa de mistura de colunas do algoritmo AES.

    Esta função representa o passo 'MixColumns', onde cada coluna da matriz de 
    estado (block) é tratada como um polinômio e multiplicada por uma matriz 
    fixa sobre o Corpo de Galois GF(2^8). Juntamente com a etapa 'ShiftRows', 
    o 'MixColumns' é responsável por fornecer a difusão no algoritmo (espalhar 
    a influência dos bits do texto original por todo o bloco).

    Args:
        block (list[list[int]]): O bloco de dados atual (matriz de estado 4x4).

    Returns:
        list[list[int]]: Uma nova matriz 4x4 representando o bloco após a 
                         transformação linear das colunas.
    """
    result = [
        [0] * 4
        for _ in range(4)
    ]

    for col in range(4):

        a0 = block[0][col]
        a1 = block[1][col]
        a2 = block[2][col]
        a3 = block[3][col]

        result[0][col] = (
            gmul(a0, 0x02)
            ^
            gmul(a1, 0x03)
            ^
            a2
            ^
            a3
        )

        result[1][col] = (
            a0
            ^
            gmul(a1, 0x02)
            ^
            gmul(a2, 0x03)
            ^
            a3
        )

        result[2][col] = (
            a0
            ^
            a1
            ^
            gmul(a2, 0x02)
            ^
            gmul(a3, 0x03)
        )

        result[3][col] = (
            gmul(a0, 0x03)
            ^
            a1
            ^
            a2
            ^
            gmul(a3, 0x02)
        )

    return result

def aes_round(
    block: list[list[int]], key_block: list[list[int]]
) -> list[list[int]]:
    """
    Executa uma rodada principal (main round) da cifra de criptografia AES.

    Esta função encadeia as quatro transformações fundamentais do algoritmo 
    AES na ordem exata definida pela especificação. A combinação dessas etapas 
    garante as propriedades de confusão e difusão necessárias para transformar 
    o texto puro em texto cifrado de forma segura.

    Args:
        block (list[list[int]]): O bloco de dados atual (matriz de estado 4x4).
        key_block (list[list[int]]): A subchave da rodada atual (matriz 4x4) 
                                     derivada do processo de expansão de chave.

    Returns:
        list[list[int]]: A nova matriz de estado 4x4 do bloco após o processamento 
                         completo da rodada.
    """
    sub_bytes(block)

    block = shift_rows(block)
    block = mix_columns(block)

    add_round_key(
        block,
        key_block
    )

    return block

def inv_sub_bytes(block: list[list[int]]) -> None:
    """
    Aplica a substituição inversa de bytes no bloco de dados usando a InvS-Box.

    Esta função representa a etapa 'InvSubBytes' do algoritmo de descriptografia AES. 
    Ela reverte a transformação aplicada originalmente pela etapa 'SubBytes', 
    substituindo cada byte da matriz de estado (block) pelo seu valor original 
    recuperado da tabela `INV_S_BOX` (Inverse Substitution Box). A modificação 
    é feita in-place.

    Args:
        block (list[list[int]]): O bloco de dados cifrado (matriz de estado 4x4) 
                                 cujos bytes serão revertidos.

    Returns:
        None: A função modifica o parâmetro `block` diretamente.

    Raises:
        NameError: Se a variável global `INV_S_BOX` não estiver definida no escopo.
        IndexError: Se algum valor no `block` ultrapassar o tamanho da `INV_S_BOX` (geralmente > 255).
    """
    for row in range(4):
        for col in range(4):
            block[row][col] = INV_S_BOX[
                block[row][col]
            ]


def inv_shift_rows(block: list[list[int]]) -> list[list[int]]:
    """
    Realiza o deslocamento circular à direita dos bytes em cada linha do bloco.

    Esta função representa a etapa 'InvShiftRows' do algoritmo de descriptografia AES. 
    Ela reverte a transformação efetuada por 'ShiftRows', deslocando cada linha da 
    matriz de estado (block) para a direita por um número de posições igual ao índice 
    da própria linha (a linha 0 não se move, a linha 1 move 1 casa à direita, a linha 2 
    move 2 casas, etc.).

    Args:
        block (list[list[int]]): O bloco de dados cifrado (matriz de estado 4x4).

    Returns:
        list[list[int]]: Uma nova matriz 4x4 com as posições originais das linhas restauradas.
    """
    result = [
        row[:]
        for row in block
    ]

    for row in range(4):
        result[row] = (
            block[row][-row:]
            +
            block[row][:-row]
        ) if row != 0 else block[row][:]

    return result


def inv_mix_columns(block: list[list[int]]) -> list[list[int]]:
    """
    Realiza a etapa de mistura inversa de colunas na descriptografia do AES.

    Esta função reverte a transformação aplicada por 'mix_columns'. Cada coluna 
    da matriz de estado (block) é multiplicada pela matriz inversa constante de 
    Rijndael sobre o Corpo de Galois GF(2^8). Essaoperação restaura as relações 
    entre os bytes das colunas antes de passarem pela difusão do MixColumns.

    Args:
        block (list[list[int]]): O bloco de dados (matriz de estado 4x4) a ser processado.

    Returns:
        list[list[int]]: Uma nova matriz 4x4 contendo o estado das colunas revertido.
    """
    result = [
        [0] * 4
        for _ in range(4)
    ]

    for col in range(4):

        a0 = block[0][col]
        a1 = block[1][col]
        a2 = block[2][col]
        a3 = block[3][col]

        result[0][col] = (
            gmul(a0, 0x0E)
            ^
            gmul(a1, 0x0B)
            ^
            gmul(a2, 0x0D)
            ^
            gmul(a3, 0x09)
        )

        result[1][col] = (
            gmul(a0, 0x09)
            ^
            gmul(a1, 0x0E)
            ^
            gmul(a2, 0x0B)
            ^
            gmul(a3, 0x0D)
        )

        result[2][col] = (
            gmul(a0, 0x0D)
            ^
            gmul(a1, 0x09)
            ^
            gmul(a2, 0x0E)
            ^
            gmul(a3, 0x0B)
        )

        result[3][col] = (
            gmul(a0, 0x0B)
            ^
            gmul(a1, 0x0D)
            ^
            gmul(a2, 0x09)
            ^
            gmul(a3, 0x0E)
        )

    return result


def aes_inv_round(
    block: list[list[int]], key_block: list[list[int]]
) -> list[list[int]]:
    """
    Executa uma rodada principal de descriptografia (inverse main round) do AES.

    Esta função encadeia as quatro etapas inversas do algoritmo AES na ordem 
    necessária para desfazer o processamento de uma rodada de criptografia. 
    A execução em ordem reversa restaura o estado do bloco de dados para a 
    sua forma anterior.

    Args:
        block (list[list[int]]): O bloco de dados cifrado atual (matriz de estado 4x4).
        key_block (list[list[int]]): A subchave de rodada correspondente (matriz 4x4).

    Returns:
        list[list[int]]: A nova matriz de estado 4x4 contendo o bloco de dados 
                         após a reversão das transformações da rodada.
    """
    block = inv_shift_rows(block)
    inv_sub_bytes(block)

    add_round_key(
        block,
        key_block
    )

    block = inv_mix_columns(block)

    return block