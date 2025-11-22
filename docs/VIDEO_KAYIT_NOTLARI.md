# ⚠️ ÖNEMLİ: Cypress Video Kaydı

## Cypress Video Kaydı Nasıl Çalışır?

### Cypress Open (Interactive Mode) vs Cypress Run (Headless Mode)

**ÖNEMLİ FARK:**

1. **`cypress open` (Interactive Mode - GUI):**
   - ⚠️ **SADECE başarısız testler için video kaydeder**
   - Başarılı testler için video kaydetmez
   - Test sırasında manuel olarak görebilirsiniz ama video dosyası oluşmaz

2. **`cypress run` (Headless Mode - Terminal):**
   - ✅ **Tüm testler için video kaydeder** (başarılı ve başarısız)
   - Video dosyası mutlaka oluşur
   - `videoUploadOnPasses: true` ayarı ile başarılı testler için de kaydeder

---

## Video Kaydı İçin Doğru Komut

### ❌ Video kaydetmez (interactive mode):
```bash
cd frontend
npm run cypress:open
```

### ✅ Video kaydeder (headless mode):
```bash
cd frontend
npm run cypress:run
```

veya belirli test dosyası için:
```bash
cd frontend
npx cypress run --spec "cypress/e2e/hospital-management.cy.js"
```

---

## Video Dosyası Konumu

Video dosyaları şu klasörde saklanır:
```
C:\hastaneyonetimi\test_videos\hospital-management.cy.js.mp4
```

---

## Test Sonrası Video Kontrolü

Test tamamlandıktan sonra:

```powershell
# Video dosyasını kontrol et
Get-ChildItem -Path "test_videos" -Filter "*.mp4" | Select-Object Name, Length, LastWriteTime
```

---

## Sorun Giderme

### Video dosyası oluşmuyorsa:

1. **Test modunu kontrol edin:**
   - `cypress run` kullanıyorsanız video kaydedilir
   - `cypress open` kullanıyorsanız sadece başarısız testler için kaydedilir

2. **Config dosyasını kontrol edin:**
   - `frontend/cypress.config.js` dosyasında `video: true` olduğundan emin olun
   - `videoUploadOnPasses: true` olduğundan emin olun

3. **Video klasörünü kontrol edin:**
   - `test_videos/` klasörünün var olduğundan emin olun
   - Klasör yazma izinlerini kontrol edin

---

## Önerilen Test Çalıştırma Yöntemi

**Video kaydı için:**
```bash
cd frontend
npm run cypress:run
```

Bu komut:
- ✅ Testleri headless mode'da çalıştırır
- ✅ Tüm testler için video kaydeder
- ✅ Videoları `test_videos/` klasörüne kaydeder
- ✅ Test sonuçlarını terminal'de gösterir

---

## Özet

- **Video görmek istiyorsanız:** `npm run cypress:run` kullanın
- **Interaktif test yapmak istiyorsanız:** `npm run cypress:open` kullanın (ama video kaydedilmez)
- **Video dosyası:** `test_videos/hospital-management.cy.js.mp4`

