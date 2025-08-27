#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import os
from urllib.parse import quote

def download_tiktok_content(url, content_type='video'):
    """
    Baixa conteúdo do TikTok usando a API do Tiklydown
    
    Args:
        url (str): URL do vídeo do TikTok
        content_type (str): 'video' ou 'audio'
    """
    # URL da API (mesma usada no código JavaScript original)
    api_url = f"https://api.tiklydown.eu.org/api/download?url={quote(url)}&key=tk_f154223be6b6af9f3d5ae5de0e344e46ad769e723e5b638ebe344574f296569c"
    
    try:
        print(f"🔄 Conectando com a API...")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data and data.get('video') and data['video'].get('noWatermark'):
            if content_type == 'video':
                download_url = data['video']['noWatermark']
                filename = f"tiktok_video_{os.path.basename(url)}.mp4"
            else:
                download_url = data.get('music')
                filename = f"tiktok_audio_{os.path.basename(url)}.mp3"
            
            if not download_url:
                print("❌ Não foi possível obter o link de download.")
                return False
            
            print(f"⬇️  Baixando {content_type}...")
            
            # Fazer o download do conteúdo
            content_response = requests.get(download_url, stream=True, timeout=60)
            content_response.raise_for_status()
            
            # Salvar o arquivo
            with open(filename, 'wb') as f:
                for chunk in content_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ Download concluído: {filename}")
            print(f"📁 Arquivo salvo em: {os.path.abspath(filename)}")
            return True
            
        else:
            print("❌ Erro ao processar o vídeo. Verifique o link.")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal da aplicação CLI"""
    
    print("🎵 TikTok Downloader - CLI")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        # Modo com argumentos de linha de comando
        url = sys.argv[1]
        content_type = 'video'
        if len(sys.argv) > 2:
            content_type = sys.argv[2].lower()
    else:
        # Modo interativo
        url = input("Cole o link do TikTok: ").strip()
        print("\nEscolha o tipo de download:")
        print("1 - Vídeo (sem marca d'água)")
        print("2 - Áudio")
        choice = input("Digite 1 ou 2: ").strip()
        
        content_type = 'audio' if choice == '2' else 'video'
    
    if not url:
        print("❌ Por favor, forneça um link do TikTok.")
        sys.exit(1)
    
    if not url.startswith(('http://', 'https://')):
        print("❌ Link inválido. Certifique-se de que começa com http:// ou https://")
        sys.exit(1)
    
    print(f"\n📱 Processando: {url}")
    print(f"📦 Tipo: {'Vídeo' if content_type == 'video' else 'Áudio'}")
    print("-" * 40)
    
    success = download_tiktok_content(url, content_type)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
