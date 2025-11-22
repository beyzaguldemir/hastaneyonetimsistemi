#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sade Login ve Doktor Ekleme Test Video'ya Ses Ekleme Script'i
Daha sade ve anlaşılır ses anlatımı için özelleştirilmiştir.
"""

import re
import os
import subprocess
from pathlib import Path
from typing import List, Dict

# ============================================================================
# 1. CYPRESS TEST DOSYASINI PARSE ET - SADE VERSİYON
# ============================================================================

def parse_cypress_test_simple(cypress_file: str) -> List[Dict]:
    """Cypress test dosyasını parse edip sade adımları çıkarır"""
    with open(cypress_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    steps = []
    current_time = 0
    
    # Sade adımlar - sadece önemli işlemler
    step_descriptions = [
        ("Giriş yapılıyor", 3),
        ("E-posta adresi giriliyor", 2),
        ("Şifre giriliyor", 2),
        ("Giriş butonuna tıklanıyor", 3),
        ("Dashboard sayfasına yönlendiriliyor", 3),
        ("Doktorlar sayfasına gidiliyor", 3),
        ("Yeni doktor butonuna tıklanıyor", 2),
        ("Doktor adı giriliyor", 2),
        ("Doktor e-posta adresi giriliyor", 2),
        ("Doktor telefon numarası giriliyor", 2),
        ("Doktor uzmanlık alanı giriliyor", 2),
        ("Departman seçiliyor", 2),
        ("Form gönderiliyor", 4),
        ("Doktor başarıyla eklendi", 3),
    ]
    
    for description, duration in step_descriptions:
        steps.append({
            'time': current_time,
            'duration': duration,
            'text': description,
            'type': 'action'
        })
        current_time += duration
    
    return steps

# ============================================================================
# 2. SRT SUBTITLE DOSYASI OLUŞTUR
# ============================================================================

def format_time(seconds: float) -> str:
    """Saniyeyi SRT formatına çevir"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_srt_subtitle(steps: List[Dict], output_file: str, scale_factor: float = 1.0):
    """SRT formatında sade subtitle dosyası oluşturur"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, step in enumerate(steps):
            start_time = step['time'] * scale_factor
            end_time = (step['time'] + step['duration']) * scale_factor
            
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{step['text']}\n\n")
    
    print(f"✅ SRT subtitle oluşturuldu: {output_file}")

# ============================================================================
# 3. TEXT-TO-SPEECH (TTS)
# ============================================================================

def text_to_speech_edge(text: str, output_audio: str, voice: str = "tr-TR-EmelNeural") -> bool:
    """Microsoft Edge TTS ile ses oluşturur"""
    try:
        import edge_tts
        import asyncio
        
        async def generate_speech():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_audio)
        
        asyncio.run(generate_speech())
        print(f"  ✅ Ses: {text}")
        return True
        
    except Exception as e:
        print(f"❌ TTS hatası: {str(e)}")
        return False

def create_audio_files(steps: List[Dict], output_dir: str) -> List[str]:
    """Ses dosyaları oluşturur"""
    audio_files = []
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📢 {len(steps)} adım için ses dosyaları oluşturuluyor...")
    
    for i, step in enumerate(steps):
        audio_file = os.path.join(output_dir, f"audio_{i:03d}.mp3")
        if text_to_speech_edge(step['text'], audio_file):
            audio_files.append(audio_file)
    
    return audio_files

# ============================================================================
# 4. FFMPEG İŞLEMLERİ
# ============================================================================

def check_ffmpeg() -> bool:
    """FFmpeg kontrolü"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def get_video_duration(video_file: str) -> float:
    """Video süresini öğren"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', video_file],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
        return None
    except:
        return None

def scale_audio_to_duration(audio_file: str, target_duration: float, output_file: str) -> bool:
    """Ses dosyasını hedef süreye göre ölçeklendirir"""
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
            'ffmpeg', '-i', audio_file, '-filter:a', filter_complex,
            '-y', output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ Ses ölçeklendirildi: {current_duration:.2f}s -> {target_duration:.2f}s")
            return True
        return False
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return False

def merge_audio_files(audio_files: List[str], output_file: str) -> bool:
    """Ses dosyalarını birleştirir"""
    if not audio_files:
        return False
    
    concat_file = "concat_list.txt"
    with open(concat_file, 'w', encoding='utf-8') as f:
        for audio in audio_files:
            audio_path = audio.replace('\\', '/')
            f.write(f"file '{audio_path}'\n")
    
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file,
        '-c', 'copy', output_file, '-y'
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        os.remove(concat_file)
        print(f"✅ Ses dosyaları birleştirildi")
        return True
    except:
        if os.path.exists(concat_file):
            os.remove(concat_file)
        return False

def merge_video_audio(video_file: str, audio_file: str, output_file: str, subtitle_file: str = None):
    """Video ve sesi birleştirir"""
    if not os.path.exists(video_file) or not os.path.exists(audio_file):
        return False
    
    cmd = ['ffmpeg', '-i', video_file, '-i', audio_file]
    
    if subtitle_file and os.path.exists(subtitle_file):
        subtitle_path = subtitle_file.replace('\\', '/').replace(':', '\\:')
        cmd.extend(['-vf', f"subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000'"])
    
    cmd.extend([
        '-c:v', 'libx264', '-c:a', 'aac',
        '-map', '0:v:0', '-map', '1:a:0',
        '-shortest', output_file, '-y'
    ])
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Final video oluşturuldu: {output_file}")
        return True
    except:
        return False

# ============================================================================
# 5. ANA FONKSİYON
# ============================================================================

def main():
    print("=" * 60)
    print("🎬 Sade Login ve Doktor Ekleme Video'ya Ses Ekleme")
    print("=" * 60)
    
    cypress_file = "frontend/cypress/e2e/login-doctor-simple.cy.js"
    video_file = "test_videos/login-doctor-simple.cy.js.mp4"
    srt_file = "subtitles_simple.srt"
    temp_audio_dir = "temp_audio_simple"
    merged_audio = "merged_audio_simple.mp3"
    final_video = "login-doctor-simple-with-audio.mp4"
    
    # 1. FFmpeg kontrolü
    print("\n1️⃣ FFmpeg kontrol ediliyor...")
    if not check_ffmpeg():
        print("❌ FFmpeg bulunamadı!")
        return
    print("✅ FFmpeg bulundu")
    
    # 2. Sade adımları oluştur
    print("\n2️⃣ Sade adımlar oluşturuluyor...")
    steps = parse_cypress_test_simple(cypress_file)
    print(f"✅ {len(steps)} sade adım oluşturuldu")
    
    # 3. Video süresini öğren
    print("\n3️⃣ Video süresi kontrol ediliyor...")
    video_duration = get_video_duration(video_file)
    if not video_duration:
        print(f"⚠️ Video dosyası bulunamadı: {video_file}")
        print("   Önce test'i çalıştırın: cd frontend && npm run cypress:run -- --spec 'cypress/e2e/login-doctor-simple.cy.js'")
        return
    
    print(f"📹 Video süresi: {video_duration:.2f} saniye")
    
    # 4. Ses dosyalarını oluştur (39 saniye hedef)
    target_audio_duration = 39.0
    print(f"\n4️⃣ {target_audio_duration:.0f} saniyelik ses oluşturuluyor...")
    audio_files = create_audio_files(steps, temp_audio_dir)
    
    if audio_files:
        merge_audio_files(audio_files, merged_audio)
        
        # Ses'i 39 saniyeye ölçeklendir
        if os.path.exists(merged_audio):
            audio_duration = get_video_duration(merged_audio)
            if audio_duration:
                print(f"📢 Ses süresi: {audio_duration:.2f} saniye")
                scaled_audio = "merged_audio_scaled_simple.mp3"
                if scale_audio_to_duration(merged_audio, target_audio_duration, scaled_audio):
                    merged_audio = scaled_audio
                    print(f"✅ Ses {target_audio_duration:.0f} saniyeye ölçeklendirildi")
    
    # 5. Subtitle oluştur (video zamanlamasına göre)
    if steps and video_duration:
        total_step_duration = steps[-1]['time'] + steps[-1]['duration']
        if total_step_duration > 0:
            subtitle_scale = video_duration / total_step_duration
        else:
            subtitle_scale = 1.0
    else:
        subtitle_scale = 1.0
    
    print(f"\n5️⃣ Subtitle oluşturuluyor...")
    create_srt_subtitle(steps, srt_file, scale_factor=subtitle_scale)
    
    # 6. Video ve sesi birleştir
    print(f"\n6️⃣ Video ve ses birleştiriliyor...")
    if os.path.exists(merged_audio):
        merge_video_audio(video_file, merged_audio, final_video, srt_file)
    else:
        print("⚠️ Ses dosyası yok")
    
    # 7. Temizlik
    print(f"\n7️⃣ Temizlik yapılıyor...")
    if os.path.exists(temp_audio_dir):
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                os.remove(audio_file)
        try:
            os.rmdir(temp_audio_dir)
        except:
            pass
    
    for temp_file in ["merged_audio_scaled_simple.mp3", "concat_list.txt"]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
    
    print("\n" + "=" * 60)
    print("✅ İşlem tamamlandı!")
    print(f"📹 Final video: {final_video}")
    print("=" * 60)

if __name__ == "__main__":
    main()

