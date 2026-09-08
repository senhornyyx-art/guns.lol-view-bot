import os
import time
import cloudscraper
from colorama import Fore, init

init(autoreset=True)

# 1. Carrega o alvo (URL ou usuário) das variáveis de ambiente ou arquivo
target = os.getenv("TARGET_URL")
if not target:
    try:
        with open("target.txt", "r") as f:
            target = f.read().strip()
    except FileNotFoundError:
        target = ""

if not target:
    print(Fore.RED + "[ERRO] Nenhuma URL/Usuário configurado! Configure a variável TARGET_URL.")
    exit(1)

# Garante que a URL esteja no formato correto
if not target.startswith("http"):
    target = f"https://guns.lol/{target}"

# 2. Carrega as proxies das variáveis de ambiente ou do arquivo proxies.txt
proxies_raw = os.getenv("PROXIES_LIST")

if proxies_raw:
    proxies = [p.strip() for p in proxies_raw.split("\n") if p.strip()]
else:
    try:
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        proxies = []

if not proxies:
    print(Fore.YELLOW + "[AVISO] Nenhuma proxy encontrada. Rodando com IP direto (não recomendado para muitas reqs).")

print(Fore.CYAN + f"=== Bot Iniciado ===")
print(Fore.CYAN + f"Alvo: {target}")
print(Fore.CYAN + f"Total de Proxies carregadas: {len(proxies)}\n")

# 3. Loop principal de envio de visualizações
scraper = cloudscraper.create_scraper()

def send_view(proxy=None):
    proxy_dict = None
    if proxy:
        if not proxy.startswith("http"):
            proxy = f"http://{proxy}"
        proxy_dict = {"http": proxy, "https": proxy}
    
    try:
        response = scraper.get(target, proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            print(Fore.GREEN + f"[SUCESSO] Visualização enviada via {proxy if proxy else 'IP Local'}")
        else:
            print(Fore.YELLOW + f"[FALHA] Código de status: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"[ERRO] Falha ao enviar requisição com a proxy {proxy}: {e}")

# Execução
if proxies:
    for proxy in proxies:
        send_view(proxy)
        time.sleep(1) # Intervalo de 1 segundo entre requisições
else:
    while True:
        send_view()
        time.sleep(2)
                  
