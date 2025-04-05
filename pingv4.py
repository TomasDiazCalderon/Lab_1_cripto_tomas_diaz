import sys
import time
import random
from scapy.all import IP, ICMP, send

def generar_payload_ping_real(caracter):
    relleno = bytearray()
    for i in range(55):  # 56 - 1 (dejamos el primer byte para el carácter)
        relleno.append(0x61 + (i % 26))  # Relleno estilo ping: a-z ciclando
    return caracter.encode('utf-8') + relleno

def enviar_por_icmp(destino, mensaje):
    identificacion_icmp = random.randint(0, 65535)
    
    for i, caracter in enumerate(mensaje):
        timestamp = int(time.time())
        payload = generar_payload_ping_real(caracter)

        paquete = IP(dst=destino, id=i) / ICMP(type=8, id=identificacion_icmp, seq=i) / payload

        print(f"[{timestamp}] Enviando carácter '{caracter}' (seq={i}, IP_ID={i}, ICMP_ID={identificacion_icmp})")
        send(paquete, verbose=False)
        time.sleep(0.2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 ping4v.py \"<texto_cifrado>\"")
        sys.exit(1)

    texto = sys.argv[1]
    destino = "172.217.192.103"  # Cambia esta IP si necesitas

    print(f"Texto a enviar: {texto}")
    enviar_por_icmp(destino, texto)
