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

KEY_SIZE = 32

def fix_key_size(key: str) -> list[list[int]]:
    """Ajusta o tamanho de uma chave para 32 bytes e a organiza em uma matriz 4x8.

    A função realiza a normalização do tamanho de uma string de chave fornecida:
    1. Converte a string de entrada para bytes usando codificação UTF-8.
    2. Garante que o array de bytes tenha exatamente 32 bytes:
       - Se menor que 32 bytes, aplica preenchimento à direita com bytes nulos (0x00).
       - Se maior que 32 bytes, trunca a sequência nos primeiros 32 bytes.
    3. Mapeia os 32 bytes para uma matriz 4x8 (4 linhas por 8 colunas) preenchida
       coluna por coluna (ordem column-major).

    Args:
        key (str): A chave em formato texto a ser ajustada e formatada.

    Returns:
        list[list[int]]: Uma matriz bidimensional de dimensões 4x8 contendo os
        valores inteiros dos bytes (0 a 255).

    Example:
        >>> matriz = fix_key_size("chave_exemplo")
        >>> len(matriz)
        4
        >>> len(matriz[0])
        8
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
        [0 for _ in range(8)]
        for _ in range(4)
    ]

    for i in range(KEY_SIZE):
        row = i % 4
        col = i // 4

        key_block[row][col] = fixed_key[i]

    return key_block


def expand_key(key_block: list[list[int]]) -> list[list[list[int]]]:
    """Gera as chaves de rodada (Round Keys) para AES-256 via Key Schedule.

    Expande o bloco de chave de 256 bits (matriz 4x8) em 60 palavras (words)
    de 4 bytes cada. Em seguida, agrupa essas palavras em 15 chaves de rodada
    (matrizes 4x4) usadas nas etapas do algoritmo de criptografia.

    Args:
        key_block (list[list[int]]): Matriz 4x8 representando a chave inicial
            normalizada de 32 bytes (256 bits).

    Returns:
        list[list[list[int]]]: Uma lista com 15 matrizes de dimensão 4x4,
        onde cada matriz é uma Round Key individual.

    Funções externas necessárias no escopo:
        - rot_word(word): Aplica rotação circular à esquerda de 1 byte.
        - sub_word(word): Aplica a caixa de substituição (S-Box) a cada byte.
        - xor_words(w1, w2): Executa a operação XOR byte a byte entre duas palavras.
        - RCON (list): Tabela de constantes de rodada (Round Constants).
    """
    words = []

    for col in range(8):
        word = [
            key_block[0][col],
            key_block[1][col],
            key_block[2][col],
            key_block[3][col]
        ]

        words.append(word)

    # Expansão para 60 words
    for i in range(8, 60):
        temp = words[i - 1][:]

        if i % 8 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)

            temp[0] ^= RCON[i // 8]

        elif i % 8 == 4:
            temp = sub_word(temp)

        words.append(
            xor_words(
                words[i - 8],
                temp
            )
        )

    # 15 round keys
    round_keys = []
    for round_number in range(15):

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


def aes256_encrypt(msg: str, key: str) -> list[list[list[int]]]:
    """Criptografa uma mensagem usando o padrão AES-256.

    A função processa a mensagem dividindo-a em blocos de 16 bytes (matrizes 4x4),
    ajusta a chave para 256 bits, expande-a em 15 chaves de rodada (Round Keys)
    e executa o ciclo completo de criptografia do AES-256 para cada bloco:
    1. Rodada Inicial (Round 0): Inicia com a operação AddRoundKey.
    2. Rodadas Principais (Rounds 1 a 13): Executa a função `aes_round` (SubBytes,
       ShiftRows, MixColumns e AddRoundKey).
    3. Rodada Final (Round 14): Executa SubBytes, ShiftRows e AddRoundKey
       (omitindo a etapa MixColumns).

    Args:
        msg (str): A mensagem em texto claro a ser criptografada.
        key (str): A chave de criptografia a ser ajustada para 32 bytes (256 bits).

    Returns:
        list[list[list[int]]]: Uma lista de blocos criptografados, onde cada bloco
        é uma matriz de dimensão 4x4 contendo os bytes cifrados.

    Funções externas necessárias no escopo:
        - generate_msg_block(msg): Prepara e divide a mensagem em matrizes 4x4.
        - fix_key_size(key): Normaliza a chave para uma matriz 4x8 de 32 bytes.
        - expand_key(key_block): Gera as 15 Round Keys do AES-256.
        - add_round_key(block, round_key): Aplica XOR do bloco com a chave de rodada.
        - aes_round(block, round_key): Aplica uma rodada completa com MixColumns.
        - sub_bytes(block): Substitui os bytes do bloco usando a S-Box.
        - shift_rows(block): Realiza o deslocamento cíclico das linhas do bloco.
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

        for round_number in range(1, 14):
            block = aes_round(
                block,
                round_keys[round_number]
            )

        sub_bytes(block)
        block = shift_rows(block)

        add_round_key(
            block,
            round_keys[14]
        )

        encrypted_blocks.append(block)

    return encrypted_blocks


def aes256_decrypt(
    encrypted_blocks: list[list[list[int]]], key: str
) -> list[list[list[int]]]:
    """Descriptografa blocos de texto cifrado usando o algoritmo AES-256.

    A função executa o fluxo inverso da criptografia AES-256 em cada bloco de 16 bytes
    (matriz 4x4), aplicando as chaves de rodada na ordem reversa (da rodada 14 até a 0):
    1. Rodada Inversa Inicial: Inicia com a aplicação do AddRoundKey (chave 14),
       seguido por InvShiftRows e InvSubBytes.
    2. Rodadas Inversas Intermediárias (13 a 1): Executa a ordem AddRoundKey,
       InvMixColumns, InvShiftRows e InvSubBytes.
    3. Rodada Inversa Final (Rodada 0): Aplica o AddRoundKey final com a primeira chave
       (chave 0) para recuperar o bloco em texto claro.

    Args:
        encrypted_blocks (list[list[list[int]]]): Lista de matrizes 4x4 contendo
            os bytes cifrados de cada bloco.
        key (str): A mesma chave de texto utilizada na etapa de criptografia.

    Returns:
        list[list[list[int]]]: Lista de matrizes 4x4 contendo os bytes descriptografados
        (texto claro original em formato de blocos).

    Funções externas necessárias no escopo:
        - fix_key_size(key): Normaliza a chave para a matriz 4x8 de 32 bytes.
        - expand_key(key_block): Gera as 15 Round Keys do AES-256.
        - add_round_key(block, round_key): Executa XOR entre o bloco e a chave da rodada.
        - inv_shift_rows(block): Reverte o deslocamento das linhas da matriz.
        - inv_sub_bytes(block): Substitui os bytes usando a tabela S-Box inversa.
        - inv_mix_columns(block): Reverte a transformação de colunas via multiplicadores Galois.
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
            round_keys[14]
        )

        block = inv_shift_rows(block)
        inv_sub_bytes(block)

        for round_number in range(13, 0, -1):
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