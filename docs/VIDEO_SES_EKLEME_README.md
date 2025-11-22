# 🎬 Cypress Test Video'ya Ses Ekleme Kılavuzu

Bu script, Cypress test videolarınıza otomatik olarak ses ve subtitle ekler.

## 📋 Gereksinimler

### 1. Python 3.7+
```bash
python --version
```

### 2. FFmpeg
FFmpeg video ve ses işleme için gereklidir.

**Windows Kurulumu:**
- İndir: https://ffmpeg.org/download.html
- veya Chocolatey ile: `choco install ffmpeg`
- veya Scoop ile: `scoop install ffmpeg`

**Kurulumu kontrol et:**
```bash
ffmpeg -version
```

### 3. Python Paketleri
```bash
pip install -r requirements.txt
```

### 4. TTS API Key (Opsiyonel)

#### Eleven Labs (Önerilen)
1. https://elevenlabs.io/ adresinden hesap oluşturun
2. API key alın
3. Environment variable olarak ayarlayın:

**Windows PowerShell:**
```powershell
$env:ELEVEN_LABS_API_KEY="your_api_key_here"
```

**Windows CMD:**
```cmd
set ELEVEN_LABS_API_KEY=your_api_key_here
```

**Kalıcı olarak ayarlamak için:**
```powershell
[System.Environment]::SetEnvironmentVariable('ELEVEN_LABS_API_KEY', 'your_api_key_here', 'User')
```

#### Google Cloud TTS (Alternatif)
1. Google Cloud Console'da proje oluşturun
2. Text-to-Speech API'yi etkinleştirin
3. Service account key oluşturun
4. Environment variable ayarlayın:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

## 🚀 Kullanım

### 1. Cypress Test Video'sunu Oluşturun
Önce Cypress test'inizi çalıştırıp video oluşturun:
```bash
cd frontend
npm run cypress:run
```

Video dosyası `test_videos/hospital-management.cy.js.mp4` konumunda olmalı.

### 2. Script'i Çalıştırın
```bash
python create_video_with_audio.py
```

### 3. Çıktı Dosyaları
- `hospital-management-with-audio.mp4` - Sesli final video
- `subtitles.srt` - Subtitle dosyası
- `merged_audio.mp3` - Birleştirilmiş ses dosyası (opsiyonel)

## ⚙️ Yapılandırma

### TTS Provider Seçimi
Environment variable ile TTS provider seçebilirsiniz:
```powershell
$env:TTS_PROVIDER="elevenlabs"  # veya "google"
```

### Ses Ayarları
Script içinde `text_to_speech_elevenlabs` fonksiyonunda ses ayarlarını değiştirebilirsiniz:
- `voice_id`: Farklı ses seçmek için
- `stability`: Ses kararlılığı (0-1)
- `similarity_boost`: Benzerlik artırma (0-1)

## 🔧 Sorun Giderme

### FFmpeg Bulunamadı
- FFmpeg'in PATH'e eklendiğinden emin olun
- `ffmpeg -version` komutu çalışmalı

### API Key Hatası
- Environment variable'ın doğru ayarlandığını kontrol edin
- PowerShell'de: `$env:ELEVEN_LABS_API_KEY`
- Yeni terminal açtıysanız tekrar ayarlayın

### Video Dosyası Bulunamadı
- Cypress test'inin çalıştırıldığından emin olun
- Video dosyasının `test_videos/` klasöründe olduğunu kontrol edin
- Script farklı video dosyalarını da listeleyecektir

### Ses Dosyaları Oluşturulamıyor
- API key'in geçerli olduğunu kontrol edin
- İnternet bağlantınızı kontrol edin
- API quota'nızı kontrol edin (Eleven Labs ücretsiz plan sınırlı)

## 📝 Notlar

- Script, Cypress test dosyasındaki yorumları Türkçe'ye çevirir
- Her adım için 2-3 saniyelik ses dosyaları oluşturulur
- Subtitle dosyası SRT formatındadır ve video oynatıcılarda görüntülenebilir
- API key olmadan da çalışır, sadece subtitle ekler

## 🎯 Örnek Kullanım Senaryosu

1. Cypress test'inizi çalıştırın ve video oluşturun
2. Eleven Labs API key'inizi ayarlayın
3. Script'i çalıştırın: `python create_video_with_audio.py`
4. `hospital-management-with-audio.mp4` dosyasını kontrol edin

## 💡 İpuçları

- İlk çalıştırmada API key olmadan deneyin, subtitle'ın çalıştığını görün
- Ses dosyaları oluşturulurken sabırlı olun (her adım için API çağrısı yapılır)
- Geçici ses dosyaları script sonunda temizlenir
- `merged_audio.mp3` dosyasını saklamak isterseniz script'i düzenleyin



