from .aes_base import (
    generate_msg_block,
    rot_word,
    sub_word,
    xor_words,
    add_round_key,
    sub_bytes,
    shift_rows,
    aes_round, 
    inv_sub_bytes,
    inv_shift_rows,
    inv_mix_columns,
    RCON
)

KEY_SIZE = 16

def fix_key_size(key: str) -> list[list[int]]:
    """
    Ajusta o tamanho de uma string para corresponder a um tamanho de chave fixo (KEY_SIZE)
    e a converte em uma matriz 4x4 de bytes, típica do algoritmo de criptografia AES.

    A função converte a chave para bytes, ajusta seu tamanho (preenchendo com zeros ou 
    truncando) e organiza os bytes resultantes em uma matriz 4x4 em ordem de coluna 
    (column-major order).

    Args:
        key (str): A string original que será processada como chave.

    Returns:
        list[list[int]]: Uma matriz 4x4 onde cada elemento é um valor inteiro (0-255) 
        representando os bytes da chave.
        
    Notes:
        - Requer que uma constante global `KEY_SIZE` esteja definida (geralmente 16 
          para uma matriz 4x4).
        - Se a chave for menor que KEY_SIZE, recebe padding de bytes nulos (b"\\x00").
        - Se a chave for maior que KEY_SIZE, é truncada.
    """
    key_bytes = key.encode("utf-8")

    if len(key_bytes) < KEY_SIZE:
        fixed_key = key_bytes.ljust(KEY_SIZE, b"\x00")
    else:
        fixed_key = key_bytes[:KEY_SIZE]

    key_block = [
        [0 for _ in range(4)]
        for _ in range(4)
    ]

    for i in range(KEY_SIZE):
        row = i % 4
        col = i // 4
        key_block[row][col] = fixed_key[i]

    return key_block


def expand_key(key_block: list[list[int]]):
    """
    Expande a chave inicial de 128 bits do AES (Advanced Encryption Standard) em 11 
    chaves de rodada (round keys) distintas.

    A função implementa o algoritmo de Key Schedule do AES-128. Ela pega a matriz de 
    estado inicial 4x4, extrai suas colunas como as 4 "palavras" (words) iniciais, e 
    então aplica uma série de transformações matemáticas (rotação, substituição S-Box e 
    XOR com constantes de rodada) para gerar um total de 44 palavras de 32 bits. Por 
    fim, agrupa essas 44 palavras de volta em 11 matrizes 4x4.

    Args:
        key_block (list[list[int]]): Uma matriz 4x4 contendo os bytes da chave original.
                                     Normalmente gerada pela função `fix_key_size`.

    Returns:
        list[list[list[int]]]: Uma lista contendo 11 matrizes 4x4. A primeira matriz 
        (índice 0) é a própria chave inicial. As 10 matrizes seguintes são as chaves 
        utilizadas em cada uma das 10 rodadas de criptografia do AES-128.
        
    Notes:
        - Requer que as funções auxiliares `rot_word`, `sub_word` e `xor_words` estejam 
          definidas, assim como a constante `RCON` (Round Constants).
    """
    words = [
        [
            key_block[0][0],
            key_block[1][0],
            key_block[2][0],
            key_block[3][0]
        ],
        [
            key_block[0][1],
            key_block[1][1],
            key_block[2][1],
            key_block[3][1]
        ],
        [
            key_block[0][2],
            key_block[1][2],
            key_block[2][2],
            key_block[3][2]
        ],
        [
            key_block[0][3],
            key_block[1][3],
            key_block[2][3],
            key_block[3][3]
        ]
    ]

    for i in range(4, 44):
        temp = words[i - 1][:]

        if i % 4 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= RCON[i // 4]

        words.append(
            xor_words(
                words[i - 4],
                temp
            )
        )

    round_keys = []

    for round_number in range(11):
        key = [
            [0] * 4
            for _ in range(4)
        ]

        for col in range(4):
            word = words[
                round_number * 4 + col
            ]

            for row in range(4):
                key[row][col] = word[row]

        round_keys.append(key)
    return round_keys

def aes128_encrypt(msg: str, key: str):
    """
    Realiza a criptografia AES-128 (Advanced Encryption Standard) de uma mensagem de texto.

    A função divide a mensagem em blocos de 16 bytes, prepara e expande a chave de
    criptografia em 11 subchaves (round keys) e processa cada bloco através da sequência
    padrão de 10 rodadas do algoritmo AES (Rodada Inicial, 9 Rodadas Principais e Rodada Final).

    Args:
        msg (str): A mensagem em texto plano que será criptografada.
        key (str): A chave utilizada para criptografia.

    Returns:
        list[list[list[int]]]: Uma lista onde cada elemento é uma matriz 4x4 (bloco)
        contendo os bytes cifrados da mensagem.

    Notes:
        - Funciona no modo ECB (Electronic Codebook), criptografando cada bloco de 
          forma independente.
        - Requer as funções auxiliares `generate_msg_block`, `fix_key_size`, `expand_key`,
          `add_round_key`, `aes_round`, `sub_bytes` e `shift_rows`.
    """
    blocks = generate_msg_block(msg)
    key_block = fix_key_size(key)
    round_keys = expand_key(key_block)
    encrypted_blocks = []

    for block in blocks:
        add_round_key(
            block,
            round_keys[0]
        )

        for round_number in range(1, 10):
            block = aes_round(
                block,
                round_keys[round_number]
            )

        sub_bytes(block)
        block = shift_rows(block)

        add_round_key(
            block,
            round_keys[10]
        )

        encrypted_blocks.append(block)

    return encrypted_blocks

# Descriptografar
def aes128_decrypt(encrypted_blocks: list[list[list[int]]], key: str):
    """
    Realiza a descriptografia de blocos cifrados usando o algoritmo AES-128.

    A função reverte a sequência de transformações efetuadas na criptografia. 
    Ela expande a chave de entrada, copia cada bloco cifrado para evitar mutação 
    do parâmetro original e aplica as operações inversas (InvShiftRows, InvSubBytes 
    e InvMixColumns) e AddRoundKey na ordem inversa das subchaves (da 10ª até a inicial).

    Args:
        encrypted_blocks (list[list[list[int]]]): Lista de matrizes 4x4 contendo os bytes
                                                   cifrados a serem descriptografados.
        key (str): A chave em texto original usada na criptografia.

    Returns:
        list[list[list[int]]]: Uma lista de matrizes 4x4 contendo os bytes descriptografados
        do texto plano original.

    Notes:
        - Requer as funções de preparação `fix_key_size` e `expand_key`.
        - Requer as operações inversas do AES: `inv_shift_rows`, `inv_sub_bytes`,
          `inv_mix_columns` e `add_round_key`.
    """
    key_block = fix_key_size(key)
    round_keys = expand_key(key_block)

    decrypted_blocks = []
    for encrypted_block in encrypted_blocks:
        block = [
            row[:]
            for row in encrypted_block
        ]

        add_round_key(
            block,
            round_keys[10]
        )

        block = inv_shift_rows(block)
        inv_sub_bytes(block)

        for round_number in range(9, 0, -1):
            add_round_key(
                block,
                round_keys[round_number]
            )

            block = inv_mix_columns(block)
            block = inv_shift_rows(block)
            inv_sub_bytes(block)

        add_round_key(
            block,
            round_keys[0]
        )

        decrypted_blocks.append(block)

    return decrypted_blocks