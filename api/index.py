#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import tempfile
import threading
from urllib.parse import quote

# Adicionar o diretório atual ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tiktok_downloader_alternative import download_tiktok_content_alternative

app = Flask(__name__)

# Configurar CORS para permitir requisições do frontend
CORS(app)

@app.route('/')
def index():
    """Servir a página HTML principal"""
    return send_file('../index.html')

@app.route('/download', methods=['POST'])
def download():
    """Endpoint para processar downloads"""
    try:
        data = request.get_json()
        url = data.get('url')
        content_type = data.get('contentType', 'video')
        
        if not url:
            return jsonify({
                'success': False,
                'message': 'URL não fornecida'
            }), 400
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4' if content_type == 'video' else '.mp3') as temp_file:
            temp_filename = temp_file.name
        
        # Modificar temporariamente a função para usar o arquivo temporário
        def download_to_temp():
            # Substituir a função de salvamento para usar o arquivo temporário
            import tiktok_downloader_alternative
            original_save = None
            
            def custom_save(content_response, filename, headers):
                nonlocal temp_filename
                with open(temp_filename, 'wb') as f:
                    for chunk in content_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return temp_filename
            
            # Monkey patch temporário
            original_save = tiktok_downloader_alternative.download_tiktok_content_alternative
            def patched_download(*args, **kwargs):
                result = original_save(*args, **kwargs)
                return result
            
            tiktok_downloader_alternative.download_tiktok_content_alternative = patched_download
            
            # Executar download
            success = original_save(url, content_type)
            return success
        
        # Executar em thread para não bloquear
        success = download_to_temp()
        
        if success and os.path.exists(temp_filename):
            # Gerar nome do arquivo baseado na URL
            from urllib.parse import urlparse
            import hashlib
            
            parsed_url = urlparse(url)
            file_id = parsed_url.path.split('/')[-1] or hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"tiktok_{content_type}_{file_id}.{'mp4' if content_type == 'video' else 'mp3'}"
            
            return jsonify({
                'success': True,
                'filename': filename,
                'downloadUrl': f'/download_file?path={quote(temp_filename)}&filename={quote(filename)}'
            })
        else:
            # Limpar arquivo temporário se existir
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            
            return jsonify({
                'success': False,
                'message': 'Falha no download do conteúdo'
            }), 500
            
    except Exception as e:
        # Limpar arquivo temporário se existir
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.unlink(temp_filename)
        
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/download_file')
def download_file():
    """Endpoint para servir o arquivo baixado"""
    try:
        file_path = request.args.get('path')
        filename = request.args.get('filename', 'tiktok_download.mp4')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Servir o arquivo
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
        # Configurar headers para download
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        # Limpar arquivo temporário após o download
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handler para o Vercel
def handler(request):
    from flask import Response
    with app.app_context():
        response = app.full_dispatch_request()
        return Response(response=response.get_data(),
                       status=response.status_code,
                       headers=dict(response.headers))

# Para desenvolvimento local
if __name__ == '__main__':
    print("🚀 Servidor TikTok Downloader iniciando...")
    print("📱 Acesse: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar o servidor")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
