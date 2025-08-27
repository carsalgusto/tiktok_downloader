#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import os
import re
import json
from urllib.parse import quote, urlparse

def download_tiktok_content_alternative(url, content_type='video'):
    """
    Baixa conteúdo do TikTok usando métodos alternativos
    
    Args:
        url (str): URL do vídeo do TikTok
        content_type (str): 'video' ou 'audio'
    """
    
    try:
        print(f"🔄 Processando URL do TikTok...")
        
        # Primeiro método: Tentar obter dados através de scraping
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Fazer requisição para obter a página
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Procurar por dados JSON na página
        html_content = response.text
        
        # Método 1: Procurar por dados JSON no HTML
        json_patterns = [
            r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',
            r'window\.__INITIAL_STATE__\s*=\s*(.*?);</script>',
            r'"videoData":\s*(\{.*?\})',
        ]
        
        video_data = None
        for pattern in json_patterns:
            match = re.search(pattern, html_content, re.DOTALL)
            if match:
                try:
                    json_data = json.loads(match.group(1))
                    # Tentar encontrar dados do vídeo em diferentes estruturas
                    if 'VideoPage' in json_data:
                        video_data = json_data['VideoPage']
                    elif 'videoData' in json_data:
                        video_data = json_data['videoData']
                    elif 'ItemModule' in json_data:
                        video_data = next(iter(json_data['ItemModule'].values()), None)
                    
                    if video_data:
                        break
                except json.JSONDecodeError:
                    continue
        
        if not video_data:
            # Método 2: Tentar API alternativa
            print("📡 Tentando API alternativa...")
            alt_api_url = f"https://tikwm.com/api/?url={quote(url)}"
            api_response = requests.get(alt_api_url, headers=headers, timeout=30)
            
            if api_response.status_code == 200:
                try:
                    api_data = api_response.json()
                    if api_data.get('data'):
                        video_data = api_data['data']
                except json.JSONDecodeError:
                    print("⚠️  Resposta da API não é JSON válido")
        
        if not video_data:
            print("❌ Não foi possível obter dados do vídeo.")
            return False
        
        # Extrair URL de download
        download_url = None
        filename = None
        
        if content_type == 'video':
            # Tentar diferentes caminhos para URL do vídeo
            download_url = (
                video_data.get('video', {}).get('downloadAddr') or
                video_data.get('video', {}).get('playAddr') or
                video_data.get('video', {}).get('url') or
                video_data.get('play') or
                video_data.get('hdplay') or
                video_data.get('wmplay') or
                video_data.get('nwmplay')
            )
            # Extrair ID do vídeo para nome do arquivo
            video_id = os.path.basename(urlparse(url).path)
            if not video_id or video_id == '/':
                video_id = str(hash(url))[:8]  # Fallback: usar hash da URL
            filename = f"tiktok_video_{video_id}.mp4"
        else:
            # URL do áudio - tratamento mais robusto
            music_data = video_data.get('music', {})
            if isinstance(music_data, dict):
                download_url = (
                    music_data.get('playUrl') or
                    music_data.get('downloadUrl') or
                    music_data.get('play_url') or
                    video_data.get('musicInfo', {}).get('playUrl')
                )
            # Se não encontrar música, usar a URL do áudio do JSON
            if content_type == 'audio':
                download_url = video_data.get('music')
                if isinstance(download_url, str):
                    download_url = download_url  # URL do áudio
                else:
                    print("⚠️  URL de áudio não encontrada.")
                    return False
            
            # Extrair ID para nome do arquivo
            audio_id = os.path.basename(urlparse(url).path)
            if not audio_id or audio_id == '/':
                audio_id = str(hash(url))[:8]  # Fallback: usar hash da URL
            filename = f"tiktok_audio_{audio_id}.mp3"
        
        if not download_url:
            print("❌ Não foi possível obter o link de download.")
            return False
        
        print(f"⬇️  Baixando {content_type}...")
        
        # Fazer o download do conteúdo
        content_response = requests.get(download_url, headers=headers, stream=True, timeout=60)
        content_response.raise_for_status()
        
        # Criar diretórios se não existirem
        if content_type == 'video':
            os.makedirs('download_video', exist_ok=True)
            filename = os.path.join('download_video', filename)
        else:
            os.makedirs('download_audio', exist_ok=True)
            filename = os.path.join('download_audio', filename)

        # Salvar o arquivo
        with open(filename, 'wb') as f:
            for chunk in content_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"✅ Download concluído: {filename}")
        print(f"📁 Arquivo salvo em: {os.path.abspath(filename)}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal da aplicação CLI com loop contínuo"""
    
    print("🎵 TikTok Downloader - Modo Contínuo")
    print("=" * 50)
    print("Digite 'sair' a qualquer momento para encerrar")
    print("=" * 50)
    
    while True:
        print("\n" + "=" * 50)
        print("🎵 NOVO DOWNLOAD")
        print("=" * 50)
        
        url = input("Cole o link do TikTok (ou 'sair' para encerrar): ").strip()
        
        if url.lower() == 'sair':
            print("\n👋 Encerrando o programa...")
            break
        
        if not url:
            print("❌ Por favor, forneça um link do TikTok.")
            continue
        
        if not url.startswith(('http://', 'https://')):
            print("❌ Link inválido. Certifique-se de que começa com http:// ou https://")
            continue
        
        print("\n📦 Escolha o tipo de download:")
        print("1 - Vídeo (completo)")
        print("2 - Áudio (somente)")
        
        content_type = 'video'
        while True:
            choice = input("Digite 1 para vídeo ou 2 para áudio: ").strip()
            if choice == '1':
                content_type = 'video'
                break
            elif choice == '2':
                content_type = 'audio'
                break
            elif choice.lower() == 'sair':
                print("\n👋 Encerrando o programa...")
                sys.exit(0)
            else:
                print("❌ Opção inválida. Por favor, digite 1 ou 2.")
        
        print(f"\n📱 Processando: {url}")
        print(f"📦 Tipo: {'Vídeo' if content_type == 'video' else 'Áudio'}")
        print("-" * 50)
        
        success = download_tiktok_content_alternative(url, content_type)
        
        if not success:
            print("\n💡 Dica: Alguns vídeos podem ter restrições de download.")
            print("   Tente um vídeo diferente ou verifique se o link está correto.")
        
        print("\n✅ Pronto para o próximo download!")

if __name__ == "__main__":
    main()
