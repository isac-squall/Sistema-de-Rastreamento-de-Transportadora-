#!/usr/bin/env python3
"""
Script para analisar a estrutura HTML completa após JavaScript
e melhorar os seletores
"""

import asyncio
from playwright.async_api import async_playwright

async def inspect_page_structure(codigo_rastreamento: str):
    """
    Inspeciona a página após carregamento JavaScript
    para entender melhor a estrutura dos dados
    """
    
    url = f"https://www.siterastreio.com.br/{codigo_rastreamento}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print(f"[*] Acessando: {url}\n")
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            except:
                print("[!] Timeout no carregamento\n")
            
            # Espera o JavaScript executar
            await page.wait_for_timeout(3000)
            
            # Extrai conteudo da página
            html = await page.content()
            
            # Procura por padrões importantes
            print("[+] PROCURANDO POR DADOS NA PÁGINA:\n")
            
            # Procura por datas
            import re
            dates = re.findall(r'\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2})?', html)
            if dates:
                print(f"[*] Datas encontradas: {set(dates)}\n")
            
            # Procura por cidades/estados
            cities = re.findall(r'[A-Z][A-Za-z\s]+/[A-Z]{2}', html)
            if cities:
                print(f"[*] Localizacoes: {set(cities)}\n")
            
            # Tenta extrair via JavaScript puro
            print("[*] Tentando extrair via JavaScript:\n")
            
            info = await page.evaluate("""() => {
                const allText = document.body.innerText;
                return allText.substring(0, 3000);
            }""")
            
            print(info)
            
            await browser.close()
            
        except Exception as e:
            print(f"[ERROR] {e}")
            await browser.close()

if __name__ == "__main__":
    import sys
    codigo = sys.argv[1] if len(sys.argv) > 1 else "AM947285279BR"
    
    asyncio.run(inspect_page_structure(codigo))
