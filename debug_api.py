#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from urllib.parse import quote

def debug_tikwm_api(url):
    """Debug function to check what the tikwm API returns"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    api_url = f"https://tikwm.com/api/?url={quote(url)}"
    print(f"🔍 Testing API URL: {api_url}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type')}")
        
        # Try to parse as JSON
        try:
            data = response.json()
            print("✅ JSON response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Check if we have video data
            if data.get('data'):
                video_data = data['data']
                print("\n📹 Video data structure:")
                if isinstance(video_data, dict):
                    print("Keys in video data:", list(video_data.keys()))
                    
                    # Check for music data
                    if 'music' in video_data:
                        music_data = video_data['music']
                        print("🎵 Music data:", music_data)
                        if isinstance(music_data, dict):
                            print("Music keys:", list(music_data.keys()))
                
        except json.JSONDecodeError:
            print("❌ Response is not valid JSON")
            print(f"Response text: {response.text[:500]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    url = "https://vm.tiktok.com/ZMAYsoorR/"
    debug_tikwm_api(url)
