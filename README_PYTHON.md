# TikTok Downloader - Versão Python

Esta é uma versão em Python do downloader de TikTok, convertida do código JavaScript original.

## Como usar

### 1. Instalar Python (se ainda não tiver)
- Baixe do site oficial: https://www.python.org/downloads/
- Durante a instalação, marque "Add Python to PATH"

### 2. Instalar a biblioteca requests
Abra o terminal/CMD e execute:
```
pip install requests
```

### 3. Executar o downloader

**Modo interativo:**
```
python tiktok_downloader.py
```

**Modo com argumentos:**
```
python tiktok_downloader.py "https://vm.tiktok.com/SEU_LINK_AQUI/" [video|audio]
```

Exemplos:
```
# Download de vídeo
python tiktok_downloader.py "https://vm.tiktok.com/ZMAYB9dDA/"

# Download de áudio
python tiktok_downloader.py "https://vm.tiktok.com/ZMAYB9dDA/" audio
```

## Funcionalidades

- ✅ Download de vídeos do TikTok sem marca d'água
- ✅ Download de áudio separado
- ✅ Interface de linha de comando simples
- ✅ Suporte a argumentos e modo interativo

## Arquivos baixados

Os arquivos são salvos no mesmo diretório com os nomes:
- `tiktok_video_[ID].mp4` para vídeos
- `tiktok_audio_[ID].mp3` para áudios

## Dependências

- Python 3.6+
- Biblioteca `requests`

## Notas

- A aplicação usa a mesma API do código JavaScript original
- Alguns vídeos podem ter restrições de download
- O serviço da API pode estar temporariamente indisponível

## Solução de problemas

Se encontrar erros de "pip não reconhecido":
1. Verifique se o Python foi instalado corretamente
2. Certifique-se de que a opção "Add Python to PATH" foi marcada durante a instalação
3. Reinicie o terminal após a instalação do Python
