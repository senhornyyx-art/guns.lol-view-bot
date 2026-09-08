import os
import random
import time
import requests

def carregar_proxies():
    """Lê a variável de ambiente PROXIES_LIST e retorna uma lista limpa."""
    raw_proxies = os.getenv("PROXIES_LIST", "")
    
    if not raw_proxies:
        print("⚠️ AVISO: A variável 'PROXIES_LIST' não foi encontrada ou está vazia.")
        return []
    
    # Limpa quebras de linha, espaços e remove prefixos como http:// ou socks5://
    proxies = []
    for line in raw_proxies.splitlines():
        p = line.strip()
        if "://" in p:
            p = p.split("://")[-1]
        if p:
            proxies.append(p)
            
    return proxies

def executar_requisicao_com_proxy(url_alvo, proxy):
    """
    Tenta fazer a requisição usando um proxy específico.
    Retorna a resposta se der certo, ou None se falhar.
    """
    config_proxy = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    # Headers para simular um navegador comum e evitar bloqueios fáceis
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # timeout=4 evita que o bot fique travado esperando por proxies mortas
        response = requests.get(url_alvo, proxies=config_proxy, headers=headers, timeout=4)
        if response.status_code == 200:
            return response
    except requests.exceptions.RequestException:
        # Pega qualquer erro de rede/timeout/conexão recusada
        pass
        
    return None

def main():
    # URL do alvo (Altere para a URL real que o seu bot precisa acessar)
    URL_ALVO = "https://httpbin.org/ip"
    
    proxies = carregar_proxies()
    
    if not proxies:
        print("❌ Nenhuma proxy carregada. Encerrando execução.")
        return

    print(f"🔄 Total de {len(proxies)} proxies carregadas da variável de ambiente.")
    
    # Embaralha a lista para não usar sempre na mesma ordem
    random.shuffle(proxies)
    
    sucessos = 0

    for ip_porta in proxies:
        print(f"🌐 Testando proxy: {ip_porta} ...")
        
        resposta = executar_requisicao_com_proxy(URL_ALVO, ip_porta)
        
        if resposta:
            print(f"✅ SUCESSO! Proxy funcionou: {ip_porta}")
            print(f"📄 Resposta: {resposta.text.strip()}")
            sucessos += 1
            
            # INSIRA AQUI O CÓDIGO DO SEU BOT QUE PROCESSA OS DADOS QUE DEU CERTO
            # ...
            
            # Dá uma pequena pausa entre requisições bem-sucedidas
            time.sleep(2)
        else:
            print(f"❌ Falhou ou expirou: {ip_porta}")

    print(f"\n📊 Execução finalizada! Total de contabilizações com sucesso: {sucessos}")

if __name__ == "__main__":
    main()
        
