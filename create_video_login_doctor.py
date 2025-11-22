#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login ve Doktor Ekleme Test Video'ya Ses Ekleme Script'i
Bu script sadece login ve doctor ekleme testi için özelleştirilmiştir.
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
    
    # Test başlığı
    test_match = re.search(r"it\('([^']+)'", content)
    if test_match:
        test_name = test_match.group(1)
        steps.append({
            'time': current_time,
            'duration': 2,
            'text': f"Test: {test_name}",
            'type': 'test_title'
        })
        current_time += 2
    
    # Yorumları bul ve çevir
    comments = re.findall(r'//\s*(.+)', content)
    for comment in comments:
        turkish_comment = translate_comment(comment)
        steps.append({
            'time': current_time,
            'duration': 3,
            'text': turkish_comment,
            'type': 'action'
        })
        current_time += 3
    
    # Cypress komutlarını bul ve açıkla
    cy_commands = re.findall(r'cy\.([^(]+)\(([^)]*)\)', content)
    for command, params in cy_commands:
        if command.strip() in ['visit', 'get', 'type', 'click', 'contains', 'should', 'wait', 'select']:
            explanation = explain_cypress_command(command.strip(), params)
            if explanation:
                steps.append({
                    'time': current_time,
                    'duration': 2,
                    'text': explanation,
                    'type': 'action'
                })
                current_time += 2
    
    return steps

def translate_comment(comment: str) -> str:
    """İngilizce yorumları Türkçe'ye çevir"""
    translations = {
        'Step 1: Visit the application': 'Adım 1: Uygulamayı ziyaret ediyoruz',
        'Step 2: Verify we\'re on the login page': 'Adım 2: Giriş sayfasında olduğumuzu doğruluyoruz',
        'Step 3: Fill in login form': 'Adım 3: Giriş formunu dolduruyoruz',
        'Step 4: Submit login form': 'Adım 4: Giriş formunu gönderiyoruz',
        'Step 5: Wait for redirect to dashboard': 'Adım 5: Dashboard\'a yönlendirmeyi bekliyoruz',
        'Step 6: Navigate to Doctors page': 'Adım 6: Doktorlar sayfasına gidiyoruz',
        'Step 7: Click on "Yeni Doktor" button': 'Adım 7: "Yeni Doktor" butonuna tıklıyoruz',
        'Step 8: Fill in doctor form': 'Adım 8: Doktor formunu dolduruyoruz',
        'Step 9: Select department': 'Adım 9: Departman seçiyoruz',
        'Step 10: Submit the form': 'Adım 10: Formu gönderiyoruz',
        'Step 11: Wait for modal to close and doctor to be added': 'Adım 11: Modal\'ın kapanmasını ve doktorun eklenmesini bekliyoruz',
    }
    
    if comment in translations:
        return translations[comment]
    
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
        'wait': 'Bekliyoruz',
        'select': 'Seçim yapıyoruz',
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
    """SRT formatında subtitle dosyası oluşturur"""
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
        
        if tts_provider == "edge":
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
        current_duration = get_video_duration(audio_file)
        if not current_duration or current_duration <= 0:
            return False
        
        scale_factor = current_duration / target_duration
        
        if scale_factor > 2.0:
            atempo_filters = []
            remaining_scale = scale_factor
            while remaining_scale > 2.0:
                atempo_filters.append("atempo=2.0")
                remaining_scale /= 2.0
            if remaining_scale > 1.0:
                atempo_filters.append(f"atempo={remaining_scale:.2f}")
            filter_complex = ",".join(atempo_filters)
        elif scale_factor < 0.5:
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

def merge_audio_files(audio_files: List[str], output_file: str):
    """FFmpeg ile ses dosyalarını birleştirir"""
    if not audio_files:
        print("❌ Birleştirilecek ses dosyası yok!")
        return False
    
    concat_file = "concat_list.txt"
    with open(concat_file, 'w', encoding='utf-8') as f:
        for audio in audio_files:
            audio_path = audio.replace('\\', '/')
            f.write(f"file '{audio_path}'\n")
    
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-c', 'copy',
        output_file,
        '-y'
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

def merge_video_audio(video_file: str, audio_file: str, output_file: str, subtitle_file: str = None):
    """FFmpeg ile video ve sesi birleştirir, isteğe bağlı subtitle ekler"""
    if not os.path.exists(video_file):
        print(f"❌ Video dosyası bulunamadı: {video_file}")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Ses dosyası bulunamadı: {audio_file}")
        return False
    
    cmd = ['ffmpeg', '-i', video_file, '-i', audio_file]
    
    if subtitle_file and os.path.exists(subtitle_file):
        subtitle_path = subtitle_file.replace('\\', '/').replace(':', '\\:')
        cmd.extend(['-vf', f"subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000'"])
    
    cmd.extend([
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
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
    print("🎬 Login ve Doktor Ekleme Test Video'ya Ses Ekleme Script'i")
    print("=" * 60)
    
    # Dosya yolları
    cypress_file = "frontend/cypress/e2e/login-and-doctor.cy.js"
    video_file = "test_videos/login-and-doctor.cy.js.mp4"
    srt_file = "subtitles_login_doctor.srt"
    temp_audio_dir = "temp_audio_login_doctor"
    merged_audio = "merged_audio_login_doctor.mp3"
    final_video = "login-and-doctor-with-audio.mp4"
    
    # 1. FFmpeg kontrolü
    print("\n1️⃣ FFmpeg kontrol ediliyor...")
    if not check_ffmpeg():
        print("❌ FFmpeg bulunamadı! Lütfen FFmpeg'i kurun.")
        return
    print("✅ FFmpeg bulundu")
    
    # 2. Cypress test dosyasını parse et
    print("\n2️⃣ Cypress test dosyası parse ediliyor...")
    if not os.path.exists(cypress_file):
        print(f"❌ Cypress test dosyası bulunamadı: {cypress_file}")
        return
    
    steps = parse_cypress_test(cypress_file)
    print(f"✅ {len(steps)} adım bulundu")
    
    # 2.5. Video süresini öğren
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
    
    # 3. SRT subtitle oluştur
    print("\n3️⃣ SRT subtitle dosyası oluşturuluyor...")
    create_srt_subtitle(steps, srt_file, scale_factor=subtitle_scale_factor)
    
    # 4. TTS Provider seçimi
    print("\n4️⃣ TTS Provider kontrol ediliyor...")
    tts_provider = os.getenv("TTS_PROVIDER", "edge").lower()
    print("✅ Ücretsiz Microsoft Edge TTS kullanılıyor (API key gerekmez)")
    
    # 5. Ses dosyalarını oluştur
    audio_files = []
    print(f"\n5️⃣ Ses dosyaları oluşturuluyor ({tts_provider})...")
    audio_files = create_audio_files(steps, temp_audio_dir, tts_provider, None)
    
    if audio_files:
        # Ses dosyalarını birleştir
        print("\n6️⃣ Ses dosyaları birleştiriliyor...")
        merge_audio_files(audio_files, merged_audio)
        
        # 6.5. Ses'i video süresine göre ölçeklendir
        if os.path.exists(merged_audio):
            audio_duration = get_video_duration(merged_audio)
            
            if audio_duration and original_video_duration > 0:
                print(f"\n6.5️⃣ Ses süresi: {audio_duration:.2f} saniye")
                print(f"   Video süresi: {original_video_duration:.2f} saniye")
                print(f"   Ses video süresine göre ölçeklendiriliyor (senkronizasyon için)...")
                
                scaled_audio = "merged_audio_scaled_login_doctor.mp3"
                if scale_audio_to_duration(merged_audio, original_video_duration, scaled_audio):
                    merged_audio = scaled_audio
                    print(f"✅ Ses {original_video_duration:.2f} saniyeye ölçeklendirildi (video ile senkronize)")
                else:
                    print("⚠️ Ses ölçeklendirme başarısız")
                
                print(f"✅ Video orijinal hızında kalacak ({original_video_duration:.2f} saniye)")
    else:
        print("⚠️ Hiç ses dosyası oluşturulamadı!")
    
    # 7. Video ve sesi birleştir
    print("\n7️⃣ Video ve ses birleştiriliyor...")
    if not os.path.exists(video_file):
        print(f"⚠️ Video dosyası bulunamadı: {video_file}")
        return
    
    if os.path.exists(merged_audio):
        merge_video_audio(video_file, merged_audio, final_video, srt_file)
    else:
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
    
    for temp_file in ["merged_audio_scaled_login_doctor.mp3"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
    
    print("\n" + "=" * 60)
    print("✅ İşlem tamamlandı!")
    print(f"📹 Final video: {final_video}")
    print(f"📝 Subtitle: {srt_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()

