#!/usr/bin/env python3
"""
Scraper avançado usando Playwright para Site Rastreio
Consegue extrair dados que são carregados via JavaScript
"""

import asyncio
from playwright.async_api import async_playwright
import json
from typing import Dict, Optional, Any

async def scrape_with_playwright(codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
    """
    Faz scraping do Site Rastreio usando Playwright
    Aguarda o carregamento JavaScript antes de extrair dados
    """
    
    url = f"https://www.siterastreio.com.br/{codigo_rastreamento}"
    
    async with async_playwright() as p:
        # Usa Chromium (mais rápido que Firefox)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print(f"[*] Acessando: {url}")
            
            # Aguarda o carregamento da página com timeout reduzido
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            except:
                # Se falhar, continua mesmo assim
                print("[!] Timeout aguardando página, continuando...")
            
            # Aguarda pelo menos 3 segundos para dados carregarem
            await page.wait_for_timeout(3000)
            
            print("[+] Página carregada, extraindo dados...")
            
            # Tenta extrair dados da estrutura visível
            data = await page.evaluate("""() => {
                const result = {
                    codigo: '',
                    product: '',
                    status: '',
                    location: '',
                    date: '',
                    delivery_date: '',
                    service: '',
                    events: []
                };
                
                // Extrai código do título ou do campo de código
                const titleEl = document.querySelector('h1');
                if (titleEl) {
                    result.codigo = titleEl.textContent.trim();
                }
                
                // Procura por informações estruturadas
                const sections = document.querySelectorAll('section, div[class*="card"], div[class*="tracking"]');
                
                sections.forEach(section => {
                    const text = section.textContent;
                    
                    // Procura por padrões de data
                    const dateMatch = text.match(/\\d{1,2}\\/\\d{1,2}\\/\\d{4}\\s+\\d{1,2}:\\d{2}/);
                    if (dateMatch && !result.date) {
                        result.date = dateMatch[0];
                    }
                    
                    // Procura por status
                    if (text.includes('entregue') || text.includes('Entregue')) {
                        result.status = 'Entregue';
                    } else if (text.includes('trânsito') || text.includes('Trânsito')) {
                        result.status = 'Em Trânsito';
                    } else if (text.includes('postado') || text.includes('Postado')) {
                        result.status = 'Postado';
                    }
                    
                    // Procura por localização (padrão: CIDADE/UF)
                    const locMatch = text.match(/([A-ZÁÉÍÓÚ][A-Za-záéíóúãõç\\s]+)\\/([A-Z]{2})/);
                    if (locMatch && !result.location) {
                        result.location = locMatch[0];
                    }
                    
                    // Procura por tipo de serviço
                    if (text.includes('PAC') || text.includes('Pac')) {
                        result.service = 'PAC';
                    } else if (text.includes('SEDEX') || text.includes('Sedex')) {
                        result.service = 'SEDEX';
                    }
                });
                
                return result;
            }""")
            
            await browser.close()
            return data
            
        except Exception as e:
            print(f"[ERROR] Erro durante scraping: {e}")
            await browser.close()
            return None

def scrape_sync(codigo_rastreamento: str) -> Optional[Dict[str, Any]]:
    """Versão síncrona do scraper"""
    return asyncio.run(scrape_with_playwright(codigo_rastreamento))

if __name__ == "__main__":
    import sys
    
    codigo = sys.argv[1] if len(sys.argv) > 1 else "AM947285279BR"
    
    print(f"[*] Iniciando scraping para: {codigo}")
    print("-" * 50)
    
    resultado = scrape_sync(codigo)
    
    if resultado:
        print(f"\n[+] Dados extraidos:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print("[-] Falha ao extrair dados")
