import os
import random
import time
import cloudscraper

def carregar_proxies():
    """Lê a variável de ambiente PROXIES_LIST e retorna uma lista limpa."""
    raw_proxies = os.getenv("PROXIES_LIST", "")
    
    if not raw_proxies:
        print("⚠️ AVISO: A variável 'PROXIES_LIST' não foi encontrada ou está vazia.")
        return []
    
    proxies = []
    for line in raw_proxies.splitlines():
        p = line.strip()
        if "://" in p:
            p = p.split("://")[-1]
        if p:
            proxies.append(p)
            
    return proxies

def executar_acesso_com_proxy(scraper, url_alvo, proxy):
    """Faz a visita no guns.lol simulando um navegador real via proxy."""
    config_proxy = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

    try:
        # timeout de 6 segundos para dar tempo de carregar a proteção do site
        response = scraper.get(url_alvo, proxies=config_proxy, timeout=6)
        
        # Se retornar status 200, significa que a página abriu e a view/visita contou!
        if response.status_code == 200:
            return True
        else:
            print(f"⚠️ Status {response.status_code} recebido.")
    except Exception:
        pass
        
    return False

def main():
    # URL do perfil no guns.lol
    URL_ALVO = "https://guns.lol/gwymbleidd"
    
    proxies = carregar_proxies()
    
    if not proxies:
        print("❌ Nenhuma proxy encontrada. Encerrando.")
        return

    print(f"🔄 Total de {len(proxies)} proxies carregadas.")
    random.shuffle(proxies)
    
    # Cria o scraper que imita um navegador de verdade (Bypassa Cloudflare)
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    sucessos = 0

    for ip_porta in proxies:
        print(f"🌐 Acessando {URL_ALVO} via proxy: {ip_porta} ...")
        
        deu_certo = executar_acesso_com_proxy(scraper, URL_ALVO, ip_porta)
        
        if deu_certo:
            sucessos += 1
            print(f"✅ SUCESSO! Visita contabilizada via {ip_porta} | Total no momento: {sucessos}")
            # Aguarda alguns segundos entre acessos bem-sucedidos
            time.sleep(3)
        else:
            print(f"❌ Proxy falhou ou foi bloqueada: {ip_porta}")

    print(f"\n📊 Finalizado! Total de acessos concluídos com sucesso: {sucessos}")

if __name__ == "__main__":
    main()
    
