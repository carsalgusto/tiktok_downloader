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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tiktok_downloader_alternative import download_tiktok_content_alternative

app = Flask(__name__)
CORS(app)

# Remover a parte do favicon

@app.route('/')
def index():
    """Servir a página HTML principal"""
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    """Endpoint para processar downloads"""
    try:
        print("Recebendo requisição de download...")
        data = request.get_json()
        url = data.get('url')
        content_type = data.get('contentType', 'video')
        
        if not url:
            print("URL não fornecida.")
            return jsonify({
                'success': False,
                'message': 'URL não fornecida'
            }), 400

        print(f"URL recebida: {url}, Tipo de conteúdo: {content_type}, Dados recebidos: {data}")

        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4' if content_type == 'video' else '.mp3') as temp_file:
            temp_filename = temp_file.name
        
        # Modificar temporariamente a função para usar o arquivo temporário
        def download_to_temp():
            import tiktok_downloader_alternative
            original_save = None
            
            def custom_save(content_response, filename, headers):
                nonlocal temp_filename
                with open(temp_filename, 'wb') as f:
                    for chunk in content_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return temp_filename
            
            original_save = tiktok_downloader_alternative.download_tiktok_content_alternative
            def patched_download(*args, **kwargs):
                result = original_save(*args, **kwargs)
                return result
            
            tiktok_downloader_alternative.download_tiktok_content_alternative = patched_download
            
            success = original_save(url, content_type)
            return success
        
        success = download_to_temp()
        
        if success and os.path.exists(temp_filename):
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
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            
            print("Falha no download do conteúdo.")
            return jsonify({
                'success': False,
                'message': 'Falha no download do conteúdo'
            }), 500
            
    except Exception as e:
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.unlink(temp_filename)
        
        print(f"Erro interno: {str(e)}")
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
        
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        print(f"Erro ao servir o arquivo: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Servidor TikTok Downloader iniciando...")
    print("📱 Acesse: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar o servidor")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
