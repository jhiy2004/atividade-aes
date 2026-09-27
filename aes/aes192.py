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

KEY_SIZE = 24

def fix_key_size(key: str) -> list[list[int]]:
    """Ajusta o tamanho de uma chave para 24 bytes e a organiza em uma matriz
    4x6.

    A string de entrada é convertida para bytes em UTF-8. Se o tamanho for
    menor que 24 bytes, ela é preenchida à direita com bytes nulos (b'\\x00').
    Se for maior, é truncada nos primeiros 24 bytes. Os bytes resultantes são
    dispostos em uma matriz de 4 linhas e 6 colunas na ordem de coluna principal
    (column-major order).

    Args:
        key (str): A chave original em formato de texto.

    Returns:
        list[list[int]]: Uma lista com 4 sublistas de 6 inteiros cada, onde
        cada inteiro representa o valor de um byte (0 a 255).

    Example:
        >>> fix_key_size("minha_chave")
        [
            [109, 97, 101, 0, 0, 0],
            [105, 95, 44, 0, 0, 0],
            [110, 99, 0, 0, 0, 0],
            [104, 104, 0, 0, 0, 0],
        ]
    """
    key_bytes = key.encode("utf-8")

    if len(key_bytes) < KEY_SIZE:
        fixed_key = key_bytes.ljust(
            KEY_SIZE,
            b"\x00"
        )
    else:
        fixed_key = key_bytes[:KEY_SIZE]

    key_block = [
        [0 for _ in range(6)]
        for _ in range(4)
    ]

    for i in range(KEY_SIZE):
        row = i % 4
        col = i // 4

        key_block[row][col] = fixed_key[i]

    return key_block


def expand_key(key_block: list[list[int]]) -> list[list[list[int]]]:
    """Expande o bloco de chave inicial de 24 bytes em 13 chaves de rodada
    (round keys) de 16 bytes (matrizes 4x4), seguindo o algoritmo de Key
    Schedule (estilo AES-192).

    Args:
        key_block (list[list[int]]): Matriz 4x6 com os bytes da chave inicial.

    Returns:
        list[list[list[int]]]: Lista contendo 13 matrizes 4x4, onde cada matriz
        é uma chave de rodada para o algoritmo de cifragem.

    Note:
        Requer as funções auxiliares `rot_word`, `sub_word`, `xor_words` e o
        vetor de constantes `RCON` definidos no escopo.
    """

    words = []

    # 6 words iniciais
    for col in range(6):

        word = [
            key_block[0][col],
            key_block[1][col],
            key_block[2][col],
            key_block[3][col]
        ]

        words.append(word)

    # Expansão para 52 words
    for i in range(6, 52):
        temp = words[i - 1][:]

        if i % 6 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= RCON[i // 6]

        words.append(
            xor_words(
                words[i - 6],
                temp
            )
        )

    # 13 round keys
    round_keys = []
    for round_number in range(13):
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


def aes192_encrypt(msg: str, key: str) -> list[list[list[int]]]:
    """Criptografa uma mensagem de texto utilizando o algoritmo AES-192.

    A função divide a mensagem em blocos de 16 bytes, ajusta a chave para 192
    bits (24 bytes) e realiza o processo de cifragem em 13 etapas de rodada
    (1 pré-rodada + 11 rodadas padrão + 1 rodada final).

    Args:
        msg (str): A mensagem em texto claro a ser criptografada.
        key (str): A chave de criptografia.

    Returns:
        list[list[list[int]]]: Lista de blocos cifrados, onde cada bloco é uma
        matriz 4x4 de inteiros (bytes).

    Note:
        Requer as funções auxiliares `generate_msg_block`, `fix_key_size`,
        `expand_key`, `add_round_key`, `aes_round`, `sub_bytes` e `shift_rows`
        definidas no escopo.
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

        for round_number in range(1, 12):
            block = aes_round(
                block,
                round_keys[round_number]
            )

        # Última rodada
        sub_bytes(block)
        block = shift_rows(block)

        add_round_key(
            block,
            round_keys[12]
        )

        encrypted_blocks.append(block)
    return encrypted_blocks


def aes192_decrypt(
    encrypted_blocks: list[list[list[int]]], key: str
) -> list[list[list[int]]]:
    """Descriptografa blocos de dados previamente cifrados com AES-192.

    A função reverte o processo de cifragem aplicando as operações inversas do
    AES-192 na ordem oposta, iterando sobre as 13 chaves de rodada da última
    (Round 12) até a primeira (Round 0).

    Args:
        encrypted_blocks (list[list[list[int]]]): Lista de blocos cifrados,
            onde cada bloco é uma matriz 4x4 de inteiros (bytes).
        key (str): A chave de descriptografia original.

    Returns:
        list[list[list[int]]]: Lista de blocos descriptografados, onde cada
        bloco é uma matriz 4x4 de inteiros (bytes).

    Note:
        Requer as funções auxiliares `fix_key_size`, `expand_key`,
        `add_round_key`, `inv_shift_rows`, `inv_sub_bytes` e
        `inv_mix_columns` definidas no escopo.
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
            round_keys[12]
        )

        block = inv_shift_rows(block)
        inv_sub_bytes(block)

        for round_number in range(11, 0, -1):
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