#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from urllib.parse import urlparse

def test_tiktok_url(url):
    """
    Testa se uma URL do TikTok é válida e acessível
    """
    print(f"🔍 Testando URL: {url}")
    print("-" * 50)
    
    # Verificar formato da URL
    if not url.startswith(('http://', 'https://')):
        print("❌ Formato inválido. Deve começar com http:// ou https://")
        return False
    
    parsed_url = urlparse(url)
    if not any(domain in parsed_url.netloc for domain in ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']):
        print("❌ Domínio não reconhecido como TikTok")
        print("   Domínios válidos: tiktok.com, vm.tiktok.com, vt.tiktok.com")
        return False
    
    # Testar conexão com a URL
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        print("🔄 Conectando com o TikTok...")
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        print(f"📊 Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ URL válida e acessível!")
            return True
        elif response.status_code == 404:
            print("❌ Vídeo não encontrado (404)")
            print("   Verifique se o link está correto e o vídeo ainda existe")
            return False
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal"""
    
    print("🎵 TikTok URL Validator")
    print("=" * 50)
    print("Testa se uma URL do TikTok é válida e acessível")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Cole a URL do TikTok para testar: ").strip()
    
    if not url:
        print("❌ Por favor, forneça uma URL")
        sys.exit(1)
    
    print()
    is_valid = test_tiktok_url(url)
    
    print("\n" + "=" * 50)
    if is_valid:
        print("🎉 URL válida! Você pode usar esta URL com os downloaders.")
        print("\n💡 Comandos para testar:")
        print(f"   Downloader original: python tiktok_downloader.py \"{url}\"")
        print(f"   Downloader alternativo: python tiktok_downloader_alternative.py \"{url}\"")
    else:
        print("❌ URL inválida ou inacessível.")
        print("\n💡 Dicas:")
        print("   - Use URLs reais de vídeos do TikTok")
        print("   - Verifique se o vídeo ainda está disponível")
        print("   - Teste a URL no seu navegador primeiro")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
