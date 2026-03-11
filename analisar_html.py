#!/usr/bin/env python3
"""
Script para analisar a estrutura HTML do Site Rastreio
e entender melhor como extrair os dados
"""

import requests
from bs4 import BeautifulSoup
import json

def analisar_site_rastreio(codigo):
    """Analisa o HTML da página de rastreamento"""
    
    url = f"https://www.siterastreio.com.br/{codigo}"
    
    print(f"Fetching: {url}")
    print("-" * 80)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        print("-" * 80)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts e styles para análise mais clara
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Procura por elementos que contêm informações de rastreamento
        print("\n🔍 PROCURANDO POR DADOS DE RASTREAMENTO:\n")
        
        # Procura por texto comum em páginas de rastreamento
        patterns = [
            'entregue', 'enviado', 'postado', 'entrega', 'prazo',
            'serviço', 'encomenda', 'destinatário', 'remetente',
            'local', 'data', 'hora', 'produto'
        ]
        
        # Encontra todos os divs, spans e elementos que podem conter dados
        containers = soup.find_all(['div', 'span', 'p', 'article', 'section'])
        
        # Extrai e exibe informações estruturadas
        print("📊 Procurando por estrutura de dados:\n")
        
        # Procura por data/hora
        import re
        data_pattern = r'\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}'
        datas = re.findall(data_pattern, response.text)
        
        if datas:
            print(f"✅ Datas encontradas: {set(datas)}\n")
        
        # Procura por localidades
        locals = re.findall(r'([A-Z\u00C0-\u00DC][A-Z\u00C0-\u00DCa-z\u00E0-\u00FC\s]+)/[A-Z]{2}', response.text)
        if locals:
            print(f"✅ Localidades: {set(locals)}\n")
        
        # Extrai primeira parte do HTML para análise
        print("📄 PRIMEIROS ELEMENTOS HTML RELEVANTES:\n")
        
        for container in containers[:30]:
            text = container.get_text(strip=True)
            if len(text) > 20 and any(pat in text.lower() for pat in patterns):
                print(f"Tag: {container.name} | Classes: {container.get('class', [])}")
                print(f"Texto: {text[:200]}")
                print("-" * 80)
        
        # Tenta encontrar dados estruturados em JSON
        print("\n\n🔎 PROCURANDO POR DADOS EM FORMATO JSON:\n")
        
        json_scripts = soup.find_all('script', type='application/json')
        for i, script in enumerate(json_scripts):
            try:
                data = json.loads(script.string)
                print(f"JSON Script {i+1}:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                print("-" * 80)
            except:
                pass
        
        # Procura por atributos data-* que podem conter informações
        print("\n\n🏷️ PROCURANDO POR ATRIBUTOS DATA-*:\n")
        
        elements_with_data = soup.find_all(attrs={"data-": True})
        for elem in elements_with_data[:10]:
            attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
            if attrs:
                print(f"Elemento: {elem.name} | Atributos: {attrs}")
                print(f"Texto: {elem.get_text(strip=True)[:100]}")
                print("-" * 80)
        
        # Salva o HTML completo para inspeção manual se necessário
        with open('html_completo.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("\n✅ HTML completo salvo em 'html_completo.html'")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao fazer requisição: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Usa o código que o usuário forneceu
    codigo = "AM947285279BR"
    analisar_site_rastreio(codigo)
