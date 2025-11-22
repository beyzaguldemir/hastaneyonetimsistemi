#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cypress Test Video'ya Ses Ekleme Script'i
Bu script Cypress test dosyasını parse eder, subtitle oluşturur,
TTS ile ses üretir ve FFmpeg ile video+ses birleştirir.
"""

import re
import os
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict

# ============================================================================
# 1. CYPRESS TEST DOSYASINI PARSE ET
# ============================================================================

def parse_cypress_test(cypress_file: str) -> List[Dict]:
    """Cypress test dosyasını parse edip adımları çıkarır"""
    with open(cypress_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    steps = []
    current_time = 0
    
    # Test bloklarını bul (it('...', () => { ... }))
    # Daha güvenli parsing: it('...', () => { ile başlayan blokları bul
    test_pattern = r"it\('([^']+)',\s*\(\)\s*=>\s*\{"
    test_matches = list(re.finditer(test_pattern, content))
    
    test_blocks = []
    for i, match in enumerate(test_matches):
        start_pos = match.end()
        # Bir sonraki test'in başlangıcını bul veya dosya sonuna kadar
        if i + 1 < len(test_matches):
            end_pos = test_matches[i + 1].start()
        else:
            end_pos = len(content)
        
        test_name = match.group(1)
        test_body = content[start_pos:end_pos]
        # Kapanış parantezini bul
        brace_count = 1
        body_end = 0
        for j, char in enumerate(test_body):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    body_end = j
                    break
        
        if body_end > 0:
            test_body = test_body[:body_end]
            test_blocks.append((test_name, test_body))
    
    for test_name, test_body in test_blocks:
        # Test başlığı
        steps.append({
            'time': current_time,
            'duration': 2,
            'text': f"Test: {test_name}",
            'type': 'test_title'
        })
        current_time += 2
        
        # Yorumları bul ve çevir
        comments = re.findall(r'//\s*(.+)', test_body)
        for comment in comments:
            # İngilizce yorumları Türkçe'ye çevir
            turkish_comment = translate_comment(comment)
            steps.append({
                'time': current_time,
                'duration': 3,
                'text': turkish_comment,
                'type': 'action'
            })
            current_time += 3
        
        # Cypress komutlarını bul ve açıkla
        cy_commands = re.findall(r'cy\.([^(]+)\(([^)]*)\)', test_body)
        for command, params in cy_commands:
            if command.strip() in ['visit', 'get', 'type', 'click', 'contains', 'should']:
                explanation = explain_cypress_command(command.strip(), params)
                if explanation:
                    steps.append({
                        'time': current_time,
                        'duration': 2,
                        'text': explanation,
                        'type': 'action'
                    })
                    current_time += 2
        
        # Testler arası boşluk
        current_time += 1
    
    return steps

def translate_comment(comment: str) -> str:
    """İngilizce yorumları Türkçe'ye çevir"""
    translations = {
        'Verify we\'re on the login page': 'Giriş sayfasında olduğumuzu doğruluyoruz',
        'Fill in login form': 'Giriş formunu dolduruyoruz',
        'Submit login form': 'Giriş formunu gönderiyoruz',
        'Wait for redirect to dashboard': 'Dashboard\'a yönlendirmeyi bekliyoruz',
        'Login first': 'Önce giriş yapıyoruz',
        'Wait for dashboard to load': 'Dashboard\'ın yüklenmesini bekliyoruz',
        'Navigate to Patients page': 'Hastalar sayfasına gidiyoruz',
        'Navigate to Departments page': 'Departmanlar sayfasına gidiyoruz',
        'Click on "Yeni Hasta" button': '"Yeni Hasta" butonuna tıklıyoruz',
        'Click on "Yeni Departman" button': '"Yeni Departman" butonuna tıklıyoruz',
        'Fill in patient form': 'Hasta formunu dolduruyoruz',
        'Fill in department form': 'Departman formunu dolduruyoruz',
        'Submit the form': 'Formu gönderiyoruz',
        'Wait for modal to close and patient to be added': 'Modal\'ın kapanmasını ve hastanın eklenmesini bekliyoruz',
        'Wait for modal to close and department to be added': 'Modal\'ın kapanmasını ve departmanın eklenmesini bekliyoruz',
    }
    
    # Tam eşleşme varsa çevir
    if comment in translations:
        return translations[comment]
    
    # Kısmi eşleşme kontrolü
    for eng, tur in translations.items():
        if eng.lower() in comment.lower():
            return tur
    
    return comment

def explain_cypress_command(command: str, params: str) -> str:
    """Cypress komutlarını Türkçe açıklamaya çevir"""
    explanations = {
        'visit': 'Sayfayı ziyaret ediyoruz',
        'get': 'Element seçiyoruz',
        'type': 'Metin yazıyoruz',
        'click': 'Tıklıyoruz',
        'contains': 'İçeriği kontrol ediyoruz',
        'should': 'Doğrulama yapıyoruz',
    }
    
    if command in explanations:
        return explanations[command]
    return None

# ============================================================================
# 2. SRT SUBTITLE DOSYASI OLUŞTUR
# ============================================================================

def format_time(seconds: float) -> str:
    """Saniyeyi SRT formatına çevir (00:00:00,000)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt_subtitle(steps: List[Dict], output_file: str, scale_factor: float = 1.0):
    """SRT formatında subtitle dosyası oluşturur
    
    Args:
        steps: Adım listesi
        output_file: Çıktı dosyası
        scale_factor: Zaman ölçeklendirme faktörü (varsayılan: 1.0)
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, step in enumerate(steps):
            start_time = step['time'] * scale_factor
            end_time = (step['time'] + step['duration']) * scale_factor
            
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{step['text']}\n\n")
    
    if scale_factor != 1.0:
        print(f"✅ SRT subtitle oluşturuldu (ölçeklendirildi x{scale_factor:.2f}): {output_file}")
    else:
        print(f"✅ SRT subtitle oluşturuldu: {output_file}")

# ============================================================================
# 3. TEXT-TO-SPEECH (TTS) İŞLEMLERİ
# ============================================================================

def text_to_speech_elevenlabs(text: str, output_audio: str, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bool:
    """Eleven Labs API ile ses oluşturur"""
    try:
        import requests
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open(output_audio, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Ses oluşturuldu: {text[:50]}...")
            return True
        else:
            print(f"  ❌ Hata ({response.status_code}): {response.text[:100]}")
            return False
            
    except ImportError:
        print("❌ 'requests' kütüphanesi yüklü değil. 'pip install requests' çalıştırın.")
        return False
    except Exception as e:
        print(f"❌ TTS hatası: {str(e)}")
        return False

def text_to_speech_google(text: str, output_audio: str, api_key: str = None) -> bool:
    """Google Cloud TTS ile ses oluşturur (alternatif)"""
    try:
        from google.cloud import texttospeech
        
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="tr-TR",
            name="tr-TR-Wavenet-D"
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_audio, 'wb') as f:
            f.write(response.audio_content)
        
        print(f"  ✅ Ses oluşturuldu: {text[:50]}...")
        return True
        
    except ImportError:
        print("❌ Google Cloud TTS kütüphanesi yüklü değil.")
        return False
    except Exception as e:
        print(f"❌ TTS hatası: {str(e)}")
        return False

def text_to_speech_edge(text: str, output_audio: str, voice: str = "tr-TR-EmelNeural") -> bool:
    """Microsoft Edge TTS ile ses oluşturur (ÜCRETSİZ, API key gerekmez)"""
    try:
        import edge_tts
        import asyncio
        
        async def generate_speech():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_audio)
        
        asyncio.run(generate_speech())
        print(f"  ✅ Ses oluşturuldu: {text[:50]}...")
        return True
        
    except ImportError:
        print("❌ 'edge-tts' kütüphanesi yüklü değil. 'pip install edge-tts' çalıştırın.")
        return False
    except Exception as e:
        print(f"❌ TTS hatası: {str(e)}")
        return False

def create_audio_files(steps: List[Dict], output_dir: str, tts_provider: str = "edge", api_key: str = None) -> List[str]:
    """Tüm adımlar için ses dosyaları oluşturur"""
    audio_files = []
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📢 {len(steps)} adım için ses dosyaları oluşturuluyor...")
    
    for i, step in enumerate(steps):
        audio_file = os.path.join(output_dir, f"audio_{i:03d}.mp3")
        
        if tts_provider == "elevenlabs":
            success = text_to_speech_elevenlabs(step['text'], audio_file, api_key)
        elif tts_provider == "google":
            success = text_to_speech_google(step['text'], audio_file, api_key)
        elif tts_provider == "edge":
            success = text_to_speech_edge(step['text'], audio_file)
        else:
            print(f"❌ Bilinmeyen TTS provider: {tts_provider}")
            success = False
        
        if success:
            audio_files.append(audio_file)
        else:
            print(f"  ⚠️ Adım {i+1} için ses oluşturulamadı, atlanıyor...")
    
    return audio_files

# ============================================================================
# 4. FFMPEG İŞLEMLERİ
# ============================================================================

def check_ffmpeg() -> bool:
    """FFmpeg'in kurulu olup olmadığını kontrol eder"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def get_video_duration(video_file: str) -> float:
    """Video dosyasının süresini saniye cinsinden döndürür"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', video_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
        return None
    except Exception as e:
        print(f"⚠️ Video süresi öğrenilemedi: {str(e)}")
        return None

def scale_audio_to_duration(audio_file: str, target_duration: float, output_file: str) -> bool:
    """Ses dosyasını hedef süreye göre ölçeklendirir (hızlandırır veya yavaşlatır)"""
    try:
        # Önce mevcut ses süresini öğren
        current_duration = get_video_duration(audio_file)  # ffprobe hem video hem audio için çalışır
        if not current_duration:
            return False
        
        if current_duration <= 0:
            return False
        
        # Ölçek faktörü hesapla
        scale_factor = current_duration / target_duration
        
        # FFmpeg ile ses hızını ayarla (atempo filter)
        # atempo 0.5-2.0 arası değerler alır, daha büyük değerler için birden fazla atempo kullan
        if scale_factor > 2.0:
            # 2.0'dan büyükse birden fazla atempo kullan
            atempo_filters = []
            remaining_scale = scale_factor
            while remaining_scale > 2.0:
                atempo_filters.append("atempo=2.0")
                remaining_scale /= 2.0
            if remaining_scale > 1.0:
                atempo_filters.append(f"atempo={remaining_scale:.2f}")
            filter_complex = ",".join(atempo_filters)
        elif scale_factor < 0.5:
            # 0.5'ten küçükse birden fazla atempo kullan
            atempo_filters = []
            remaining_scale = scale_factor
            while remaining_scale < 0.5:
                atempo_filters.append("atempo=0.5")
                remaining_scale /= 0.5
            if remaining_scale < 1.0:
                atempo_filters.append(f"atempo={remaining_scale:.2f}")
            filter_complex = ",".join(atempo_filters)
        else:
            filter_complex = f"atempo={scale_factor:.2f}"
        
        cmd = [
            'ffmpeg',
            '-i', audio_file,
            '-filter:a', filter_complex,
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Ses ölçeklendirildi: {current_duration:.2f}s -> {target_duration:.2f}s (x{scale_factor:.2f})")
            return True
        else:
            print(f"❌ Ses ölçeklendirme hatası: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Ses ölçeklendirme hatası: {str(e)}")
        return False

def slow_down_video(video_file: str, target_duration: float, output_file: str) -> bool:
    """Video'yu yavaşlatarak hedef süreye uzatır (setpts filter ile)"""
    try:
        # Önce mevcut video süresini öğren
        current_duration = get_video_duration(video_file)
        if not current_duration or current_duration <= 0:
            return False
        
        # Ölçek faktörü hesapla (video ne kadar yavaşlatılacak)
        scale_factor = target_duration / current_duration
        
        if scale_factor <= 0:
            return False
        
        # FFmpeg ile video'yu yavaşlat (setpts filter)
        # setpts=PTS/scale_factor video'yu yavaşlatır
        # Örnek: setpts=PTS/0.5 = 2x yavaşlatır
        setpts_value = 1.0 / scale_factor
        
        # Video filter: setpts ile yavaşlat
        # Audio filter: atempo ile hızlandır (video yavaşladığı için ses de yavaşlar, bunu düzeltmek için)
        # Ama biz sadece video'yu yavaşlatıyoruz, ses ayrı eklenecek
        
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-filter:v', f'setpts=PTS*{scale_factor:.4f}',
            '-an',  # Audio'yu kaldır (ses ayrı eklenecek)
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Video yavaşlatıldı: {current_duration:.2f}s -> {target_duration:.2f}s (x{scale_factor:.2f} yavaş)")
            return True
        else:
            print(f"❌ Video yavaşlatma hatası: {result.stderr[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Video yavaşlatma hatası: {str(e)}")
        return False

def merge_audio_files(audio_files: List[str], output_file: str):
    """FFmpeg ile ses dosyalarını birleştirir"""
    if not audio_files:
        print("❌ Birleştirilecek ses dosyası yok!")
        return False
    
    # Concat listesi oluştur
    concat_file = "concat_list.txt"
    with open(concat_file, 'w', encoding='utf-8') as f:
        for audio in audio_files:
            # Windows path için düzeltme
            audio_path = audio.replace('\\', '/')
            f.write(f"file '{audio_path}'\n")
    
    # FFmpeg ile birleştir
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        output_file,
        '-y'  # Overwrite without asking
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        os.remove(concat_file)
        print(f"✅ Ses dosyaları birleştirildi: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg hatası: {e.stderr}")
        if os.path.exists(concat_file):
            os.remove(concat_file)
        return False

def loop_video_to_duration(video_file: str, target_duration: float, output_file: str) -> bool:
    """Video'yu loop'layarak hedef süreye uzatır"""
    try:
        current_duration = get_video_duration(video_file)
        if not current_duration or current_duration <= 0:
            return False
        
        # Kaç kez loop'lanması gerektiğini hesapla
        loops_needed = int(target_duration / current_duration) + 1
        
        # Concat listesi oluştur
        concat_file = "video_loop_list.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            video_path = video_file.replace('\\', '/')
            for _ in range(loops_needed):
                f.write(f"file '{video_path}'\n")
        
        # FFmpeg ile birleştir
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-t', str(target_duration),  # Hedef süreye kadar kes
            '-c', 'copy',
            output_file,
            '-y'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        os.remove(concat_file)
        
        if result.returncode == 0:
            print(f"✅ Video loop'landı: {current_duration:.2f}s -> {target_duration:.2f}s ({loops_needed} kez)")
            return True
        else:
            print(f"❌ Video loop hatası: {result.stderr[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Video loop hatası: {str(e)}")
        return False

def merge_video_audio(video_file: str, audio_file: str, output_file: str, subtitle_file: str = None):
    """FFmpeg ile video ve sesi birleştirir, isteğe bağlı subtitle ekler"""
    if not os.path.exists(video_file):
        print(f"❌ Video dosyası bulunamadı: {video_file}")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Ses dosyası bulunamadı: {audio_file}")
        return False
    
    cmd = ['ffmpeg', '-i', video_file, '-i', audio_file]
    
    # Subtitle varsa ekle
    if subtitle_file and os.path.exists(subtitle_file):
        # Windows path için düzeltme
        subtitle_path = subtitle_file.replace('\\', '/').replace(':', '\\:')
        cmd.extend(['-vf', f"subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000'"])
    
    cmd.extend([
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',  # Kısa olanın süresine göre kes
        output_file,
        '-y'
    ])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Final video oluşturuldu: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg hatası: {e.stderr}")
        return False

# ============================================================================
# 5. ANA FONKSİYON
# ============================================================================

def main():
    print("=" * 60)
    print("🎬 Cypress Test Video'ya Ses Ekleme Script'i")
    print("=" * 60)
    
    # Dosya yolları
    cypress_file = "frontend/cypress/e2e/hospital-management.cy.js"
    # En yeni video dosyasını bul
    video_dir = Path("test_videos")
    video_files = sorted(video_dir.glob("hospital-management.cy.js*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
    if video_files:
        video_file = str(video_files[0])
        print(f"📹 Kullanılan video: {video_file}")
    else:
        video_file = "test_videos/hospital-management.cy.js.mp4"
    srt_file = "subtitles.srt"
    temp_audio_dir = "temp_audio"
    merged_audio = "merged_audio.mp3"
    final_video = "hospital-management-with-audio.mp4"
    
    # 1. FFmpeg kontrolü
    print("\n1️⃣ FFmpeg kontrol ediliyor...")
    if not check_ffmpeg():
        print("❌ FFmpeg bulunamadı! Lütfen FFmpeg'i kurun.")
        print("   Windows: https://ffmpeg.org/download.html")
        print("   veya: choco install ffmpeg")
        return
    print("✅ FFmpeg bulundu")
    
    # 2. Cypress test dosyasını parse et
    print("\n2️⃣ Cypress test dosyası parse ediliyor...")
    if not os.path.exists(cypress_file):
        print(f"❌ Cypress test dosyası bulunamadı: {cypress_file}")
        return
    
    steps = parse_cypress_test(cypress_file)
    print(f"✅ {len(steps)} adım bulundu")
    
    # 2.5. Video süresini öğren - ses video süresine göre ölçeklendirilecek
    print("\n2.5️⃣ Video süresi kontrol ediliyor...")
    original_video_duration = get_video_duration(video_file)
    if not original_video_duration:
        print("⚠️ Video süresi öğrenilemedi")
        original_video_duration = 0
    
    print(f"📹 Video süresi: {original_video_duration:.2f} saniye")
    print(f"🎯 Ses video süresine göre ölçeklendirilecek (senkronizasyon için)")
    
    # Subtitle zamanlamasını video süresine göre ölçeklendir
    if steps:
        total_subtitle_duration = steps[-1]['time'] + steps[-1]['duration']
        if total_subtitle_duration > 0 and original_video_duration > 0:
            subtitle_scale_factor = original_video_duration / total_subtitle_duration
            print(f"📝 Subtitle ölçek faktörü: {subtitle_scale_factor:.2f}x (video zamanlamasına göre)")
        else:
            subtitle_scale_factor = 1.0
    else:
        subtitle_scale_factor = 1.0
    
    # 3. SRT subtitle oluştur (video zamanlamasına göre ölçeklendirilmiş)
    print("\n3️⃣ SRT subtitle dosyası oluşturuluyor...")
    create_srt_subtitle(steps, srt_file, scale_factor=subtitle_scale_factor)
    
    # 4. TTS Provider seçimi
    print("\n4️⃣ TTS Provider kontrol ediliyor...")
    tts_provider = os.getenv("TTS_PROVIDER", "edge").lower()  # Varsayılan: edge (ücretsiz)
    
    create_audio = True
    api_key = None
    
    if tts_provider == "elevenlabs":
        api_key = os.getenv("ELEVEN_LABS_API_KEY")
        if not api_key:
            print("⚠️ ELEVEN_LABS_API_KEY environment variable bulunamadı!")
            print("   Ücretsiz 'edge' TTS kullanılacak.")
            tts_provider = "edge"
    elif tts_provider == "google":
        api_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not api_key:
            print("⚠️ GOOGLE_APPLICATION_CREDENTIALS bulunamadı!")
            print("   Ücretsiz 'edge' TTS kullanılacak.")
            tts_provider = "edge"
    elif tts_provider == "edge":
        print("✅ Ücretsiz Microsoft Edge TTS kullanılıyor (API key gerekmez)")
    else:
        print(f"⚠️ Bilinmeyen provider: {tts_provider}, 'edge' kullanılacak")
        tts_provider = "edge"
    
    # 5. Ses dosyalarını oluştur
    audio_files = []
    if create_audio:
        print(f"\n5️⃣ Ses dosyaları oluşturuluyor ({tts_provider})...")
        audio_files = create_audio_files(steps, temp_audio_dir, tts_provider, api_key)
        
        if audio_files:
            # Ses dosyalarını birleştir
            print("\n6️⃣ Ses dosyaları birleştiriliyor...")
            merge_audio_files(audio_files, merged_audio)
            
            # 6.5. Ses'i video süresine göre ölçeklendir (video zamanlamasına göre senkronize et)
            if os.path.exists(merged_audio):
                audio_duration = get_video_duration(merged_audio)
                
                if audio_duration and original_video_duration > 0:
                    print(f"\n6.5️⃣ Ses süresi: {audio_duration:.2f} saniye")
                    print(f"   Video süresi: {original_video_duration:.2f} saniye")
                    print(f"   Ses video süresine göre ölçeklendiriliyor (senkronizasyon için)...")
                    
                    # Ses'i video süresine göre ölçeklendir (hızlandır)
                    scaled_audio = "merged_audio_scaled.mp3"
                    if scale_audio_to_duration(merged_audio, original_video_duration, scaled_audio):
                        merged_audio = scaled_audio
                        print(f"✅ Ses {original_video_duration:.2f} saniyeye ölçeklendirildi (video ile senkronize)")
                    else:
                        print("⚠️ Ses ölçeklendirme başarısız")
                    
                    # Video orijinal hızında kalacak (loop yok, yavaşlatma yok)
                    print(f"✅ Video orijinal hızında kalacak ({original_video_duration:.2f} saniye)")
        else:
            print("⚠️ Hiç ses dosyası oluşturulamadı!")
            create_audio = False
    
    # 7. Video ve sesi birleştir
    print("\n7️⃣ Video ve ses birleştiriliyor...")
    if not os.path.exists(video_file):
        print(f"⚠️ Video dosyası bulunamadı: {video_file}")
        print("   Mevcut video dosyaları:")
        video_dir = Path("test_videos")
        if video_dir.exists():
            for vf in video_dir.glob("*.mp4"):
                print(f"     - {vf}")
        return
    
    if create_audio and os.path.exists(merged_audio):
        merge_video_audio(video_file, merged_audio, final_video, srt_file)
    else:
        # Sadece subtitle ekle
        print("⚠️ Ses dosyası yok, sadece subtitle ekleniyor...")
        merge_video_audio(video_file, video_file, final_video, srt_file)
    
    # 8. Temizlik
    print("\n8️⃣ Geçici dosyalar temizleniyor...")
    if os.path.exists(temp_audio_dir):
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        try:
            os.rmdir(temp_audio_dir)
        except:
            pass
    
    # Ölçeklendirilmiş video ve ses dosyalarını sil
    for temp_file in ["video_slowed.mp4", "video_scaled.mp4", "video_looped.mp4", "merged_audio_scaled.mp3"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"✅ Geçici dosya temizlendi: {temp_file}")
            except:
                pass
    
    if os.path.exists(merged_audio):
        # Kullanıcı isterse saklayabilir
        pass
    
    print("\n" + "=" * 60)
    print("✅ İşlem tamamlandı!")
    print(f"📹 Final video: {final_video}")
    print(f"📝 Subtitle: {srt_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()

