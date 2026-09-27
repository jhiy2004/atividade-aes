from aes.aes128 import aes128_encrypt, aes128_decrypt
from aes.aes192 import aes192_encrypt, aes192_decrypt
from aes.aes256 import aes256_encrypt, aes256_decrypt

from typing import Tuple

def change_bit_text(text_bytes_repr, last_bit) -> str:
    option = -1

    while option < 0 or option > last_bit:
        option = int(input(
            f"Escolha uma posição de bit no seguinte range [0, {last_bit}]: "
        ))

    value = int.from_bytes(text_bytes_repr, byteorder="big")

    value ^= (1 << option)

    return value.to_bytes(len(text_bytes_repr), byteorder="big").decode("utf-8")

def encrypt_decrypt_aes(aes: str, msg: str, key: str) -> Tuple[str, str]:
    if aes == "AES-128":
        encrypted_blocks = aes128_encrypt(msg, key)
        encrypted_msg = get_str_from_blocks(encrypted_blocks)

        decrypted_blocks = aes128_decrypt(encrypted_blocks, key)
        decrypted_msg = get_utf8_from_blocks(decrypted_blocks)
    elif aes == "AES-192":
        encrypted_blocks = aes192_encrypt(msg, key)
        encrypted_msg = get_str_from_blocks(encrypted_blocks)

        decrypted_blocks = aes192_decrypt(encrypted_blocks, key)
        decrypted_msg = get_utf8_from_blocks(decrypted_blocks)
    elif aes == "AES-256":
        encrypted_blocks = aes256_encrypt(msg, key)
        encrypted_msg = get_str_from_blocks(encrypted_blocks)

        decrypted_blocks = aes256_decrypt(encrypted_blocks, key)
        decrypted_msg = get_utf8_from_blocks(decrypted_blocks)
    else:
        raise ValueError("Invalid AES type")

    return (encrypted_msg, decrypted_msg)

def run_aes(option):
    if option < 1 or option > 3:
        print("Opção inválida")
        return

    msg = input("Digite a mensagem a ser cifrada: ")
    key = input("Digite a mensagem a ser cifrada: ")

    if option == 1:
        chosen_aes = "AES-128"
    elif option == 2:
        chosen_aes = "AES-192"
    else:
        chosen_aes = "AES-256"

    encrypted_msg, decrypted_msg = encrypt_decrypt_aes(chosen_aes, msg, key)

    print(f"Mensagem cifrada: {encrypted_msg}")
    print(f"Mensagem decifrada: {decrypted_msg}")

    msg_bytes_repr = msg.encode(encoding="utf-8")
    key_bytes_repr = key.encode(encoding="utf-8")

    msg_last_bit = len(msg_bytes_repr) * 8 - 1
    key_last_bit = len(key_bytes_repr) * 8 - 1

    option = -1
    while (option < 0 or option > 2):
        print(f"1 - Mensagem ({msg})")
        print(f"2 - Chave ({key})")
        print("0 - Sair")
        option = int(input("Escolha qual texto deseja alterar um bit: "))


    if option == 0:
        return

    if option == 1:
        altered_msg = change_bit_text(msg_bytes_repr, msg_last_bit)
        print(f"Nova mensagem: {altered_msg}")

        encrypted_msg, decrypted_msg = encrypt_decrypt_aes(chosen_aes, altered_msg, key)
    else:
        altered_key = change_bit_text(key_bytes_repr, key_last_bit)
        print(f"Nova chave: {altered_key}")

        encrypted_msg, decrypted_msg = encrypt_decrypt_aes(chosen_aes, msg, altered_key)

    print(f"Mensagem cifrada: {encrypted_msg}")
    print(f"Mensagem decifrada: {decrypted_msg}")

def get_str_from_blocks(blocks):
    msg = []
    for block in blocks:
        for i in range(4):
            for j in range(4):
                msg.append(f"{block[j][i]:02x}")

    return "".join(msg)

def get_utf8_from_blocks(blocks):
    data = bytearray()

    for block in blocks:
        for col in range(4):
            for row in range(4):
                data.append(block[row][col])

    return bytes(data).decode("utf-8").rstrip("\x00")

def main():
    option = -1
    while (option < 0 or option > 3):
        print("1 - AES 128")
        print("2 - AES 192")
        print("3 - AES 256")
        print("0 - Sair")
        option = int(input("Escolha qual algoritmo AES deseja usar: "))


    if option == 0:
        print("Saindo...")
        return
    
    run_aes(option)


if __name__ == "__main__":
    main()