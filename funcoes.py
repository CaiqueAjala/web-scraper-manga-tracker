import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import os
import requests

def enviar_msg_telegram(texto):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url_base = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={texto}"
    try:
        requests.get(url_base)
    except:
        print("Erro ao enviar mensagem para o Telegram.")

def rastrear_capitulo():
    options = uc.ChromeOptions()
    # Parte do código que não consegui passar pelo cloudflare
    # options.add_argument('--headless')
    
    driver = None 

    try:
        print("Abrindo navegador")
        driver = uc.Chrome(options=options, version_main=145) 
        
        url = "https://sakuramangas.org/obras/grand-blue-dreaming/"
        driver.get(url)
        
        print("Aguardando o Cloudflare")
        # 30 segundos para te dar tempo de clicar se o robô não passar sozinho
        time.sleep(30) 

        # Tenta rolar para carregar a lista
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2) 

        html = driver.page_source
        site_html = BeautifulSoup(html, "html.parser")
        
        elemento = site_html.find("a", class_="a-scan title-text")

        if elemento:
            texto_cap = elemento.get_text(strip=True)
            capitulo_atual = texto_cap.split()[-1]
            print(f"✅ SUCESSO! Encontrei o capítulo: {capitulo_atual}")
            
            arquivo_historico = "ultimo_capitulo.txt"
            if not os.path.exists(arquivo_historico):
                with open(arquivo_historico, "w") as f:
                    f.write(capitulo_atual)
                print(f"Memória criada: {capitulo_atual}")
            else:
                with open(arquivo_historico, "r") as f:
                    ultimo_salvo = f.read().strip()
                
                if float(capitulo_atual) > float(ultimo_salvo):
                    enviar_msg_telegram(f"🔥 NOVO CAPÍTULO: {capitulo_atual} de Grand Blue!")
                    with open(arquivo_historico, "w") as f:
                        f.write(capitulo_atual)
                else:
                    enviar_msg_telegram(f"Olá, ainda não foi lançado um novo capítulo")
        else:
            driver.save_screenshot("erro_visao_robo.png")
            print("❌ Não achei o capítulo. Verifique o arquivo 'erro_visao_robo.png'")

    except Exception as e:
        print(f"⚠️ Erro técnico: {e}")

    finally:
        if driver:
            driver.quit()