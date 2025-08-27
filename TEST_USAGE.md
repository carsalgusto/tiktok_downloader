# Como Testar o TikTok Downloader

## URLs Válidas para Teste

Para testar o downloader, você precisa usar URLs reais de vídeos do TikTok. URLs de exemplo como `https://www.tiktok.com/@example/video/1234567890` não funcionam porque não são vídeos reais.

### Como obter URLs válidas:

1. **Abra o TikTok** no seu navegador ou app
2. **Encontre um vídeo** que deseja baixar
3. **Copie o link** compartilhando o vídeo e selecionando "Copiar link"

### Exemplos de formatos de URL válidos:
- `https://www.tiktok.com/@username/video/1234567890123456789`
- `https://vm.tiktok.com/ABCDEFGHI/`
- `https://vt.tiktok.com/XYZ123456/`

## Testando o Downloader

### 1. Primeiro verifique se a URL é válida:
```bash
python -c "import requests; url = 'SUA_URL_AQUI'; print(f'Testando: {url}'); r = requests.head(url, timeout=10, allow_redirects=True); print(f'Status: {r.status_code}')"
```

### 2. Teste com o downloader original (requer API key válida):
```bash
python tiktok_downloader.py "SUA_URL_TIKTOK_AQUI"
```

### 3. Teste com o downloader alternativo:
```bash
python tiktok_downloader_alternative.py "SUA_URL_TIKTOK_AQUI"
```

## Solução de Problemas Comuns

### ❌ Erro 401 (API key required)
- O API key do Tiklydown pode ter expirado
- Entre em contato com @tiklydownapi_bot no Telegram para obter uma nova key
- Atualize a key no arquivo `tiktok_downloader.py`

### ❌ Não foi possível obter dados do vídeo
- Verifique se a URL é válida e acessível
- Alguns vídeos podem ter restrições de download
- Tente um vídeo diferente

### ❌ Erro de conexão
- Verifique sua conexão com a internet
- O serviço pode estar temporariamente indisponível

## Dicas Importantes

1. **Sempre use URLs reais** - URLs de exemplo não funcionam
2. **Teste a URL primeiro** - certifique-se de que a página carrega no navegador
3. **Respeite direitos autorais** - use apenas para conteúdo pessoal
4. **Alguns vídeos são restritos** - nem todos os vídeos podem ser baixados

## API Keys Válidas

Se precisar de uma nova API key para o serviço Tiklydown:
1. Entre em contato com @tiklydownapi_bot no Telegram
2. Siga as instruções para obter uma key válida
3. Atualize a variável `api_url` no arquivo `tiktok_downloader.py`
