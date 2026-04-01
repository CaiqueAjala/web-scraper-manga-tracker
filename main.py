""""
Objetivo: Um script que me avise caso um novo capítulo
de um mangá foi lançado
"""


from funcoes import rastrear_capitulo
import time
from dotenv import load_dotenv

dias_de_espera = 1
# Transformando dias em segundos: 24h * 60min * 60seg
segundos = dias_de_espera * 24 * 60 * 60 

print("Rastreador de Mangás iniciado...")

while True:
    print(f"[{time.strftime('%H:%M:%S')}] Verificando site...")
    
    # chamando a função principal 
    rastrear_capitulo()
    
    print(f"Aguardando {dias_de_espera} dia(s) para a próxima verificação...")
    time.sleep(segundos)
