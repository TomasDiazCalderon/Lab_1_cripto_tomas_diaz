import sys

def cesar_cipher(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cipher_text = ""
    text = text.lower()  # Convertir todo a minúsculas
    
    for char in text:
        if char in alphabet:
            new_index = (alphabet.index(char) + shift) % 26
            cipher_text += alphabet[new_index]
        else:
            cipher_text += char  # Mantener espacios y otros caracteres
    
    return cipher_text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py \"texto en minúsculas\" desplazamiento")
        sys.exit(1)
    
    text = sys.argv[1]
    try:
        shift = int(sys.argv[2])
    except ValueError:
        print("El desplazamiento debe ser un número entero.")
        sys.exit(1)
    
    encrypted_text = cesar_cipher(text, shift)
    print(encrypted_text)
