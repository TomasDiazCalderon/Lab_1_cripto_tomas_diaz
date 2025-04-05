import sys
from scapy.all import rdpcap, ICMP
from termcolor import colored

def extraer_mensaje(pcap_file):
    paquetes = rdpcap(pcap_file)
    mensaje_cifrado = []

    for paquete in paquetes:
        if paquete.haslayer(ICMP) and paquete[ICMP].type == 8:  # Solo Echo Request
            data = bytes(paquete[ICMP].payload)
            if len(data) > 0:
                mensaje_cifrado.append(chr(data[0]))  # Extraer el primer byte (el carácter útil)

    return "".join(mensaje_cifrado)

def cesar_descifrar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - desplazamiento) % 26 + base)
        else:
            resultado += char
    return resultado

def evaluar_probabilidad(texto):
    # Verifica cuántas palabras comunes en español aparecen
    palabras_comunes = ["el", "la", "de", "que", "en", "y", "a", "los", "un", "con"]
    texto_minusculas = texto.lower()
    return sum(1 for palabra in palabras_comunes if palabra in texto_minusculas)

def probar_todos_los_desplazamientos(mensaje):
    mejores_resultados = []
    print("\nIntentando descifrar el mensaje...\n")
    
    for i in range(26):
        mensaje_descifrado = cesar_descifrar(mensaje, i)
        score = evaluar_probabilidad(mensaje_descifrado)
        mejores_resultados.append((mensaje_descifrado, score, i))
    
    # Encontrar el desplazamiento más probable
    mejor_resultado = max(mejores_resultados, key=lambda x: x[1])

    for texto, score, desplazamiento in mejores_resultados:
        if texto == mejor_resultado[0]:  # Si es el mejor resultado, ponerlo en verde
            print(colored(f"Desplazamiento {desplazamiento}: {texto}", "green"))
        else:
            print(f"Desplazamiento {desplazamiento}: {texto}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 readv2.py <archivo.pcapng>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    mensaje = extraer_mensaje(pcap_file)
    
    print(f"\nMensaje capturado: {mensaje}")
    probar_todos_los_desplazamientos(mensaje)
