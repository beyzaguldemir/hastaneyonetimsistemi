# Test Documentation

Bu dokümantasyon, Hastane Yönetim Sistemi için oluşturulan test senaryolarını açıklar.

## Test Yapıları

### 1. Cucumber (Backend API Tests)

Cucumber, Rails backend API'leri için BDD (Behavior-Driven Development) testleri yapmak için kullanılır.

#### Kurulum

```bash
bundle install
```

#### Test Senaryoları

Cucumber feature dosyaları `features/` dizininde bulunur:

- **Login Tests** (`features/login.feature`)
  - Successful login with valid credentials
  - Failed login with invalid credentials

- **Patients Tests** (`features/patients.feature`)
  - View patients list
  - Create a new patient

- **Departments Tests** (`features/departments.feature`)
  - View departments list
  - Create a new department

#### Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
bundle exec cucumber

# Belirli bir feature dosyasını çalıştır
bundle exec cucumber features/login.feature

# Belirli bir senaryoyu çalıştır
bundle exec cucumber features/login.feature:10
```

#### Test Adımları (Step Definitions)

Test adımları `features/step_definitions/` dizininde tanımlanmıştır:
- `api_steps.rb` - API request/response test adımları

#### Helper Methods

`features/support/api_helpers.rb` dosyasında API test helper metodları bulunur.

---

### 2. Cypress (Frontend E2E Tests)

Cypress, React frontend uygulaması için end-to-end (E2E) testleri yapmak için kullanılır.

#### Kurulum

```bash
cd frontend
npm install
```

#### Test Senaryoları

Cypress test dosyaları `frontend/cypress/e2e/` dizininde bulunur:

- **Hospital Management E2E Tests** (`hospital-management.cy.js`)
  - Site açılması ve admin kullanıcı ile giriş yapılması
  - Patients sayfasına gidilmesi ve yeni hasta eklenmesi
  - Departments sayfasına gidilmesi ve yeni departman eklenmesi
  - Tam workflow: Login → Add Patient → Add Department

#### Testleri Çalıştırma

**Headless Mode (Video kaydı ile):**
```bash
cd frontend
npm run cypress:run
```

**Interactive Mode (Cypress GUI ile):**
```bash
cd frontend
npm run cypress:open
```

**Belirli bir test dosyasını çalıştır:**
```bash
cd frontend
npx cypress run --spec "cypress/e2e/hospital-management.cy.js"
```

#### Video Kaydı

Cypress testleri otomatik olarak video kaydı yapar. Videolar `frontend/cypress/videos/` dizininde saklanır.

Video kaydı yapılandırması `frontend/cypress.config.js` dosyasında ayarlanmıştır:
- `video: true` - Video kaydı aktif
- `videoCompression: 32` - Video sıkıştırma oranı
- `screenshotOnRunFailure: true` - Hata durumunda ekran görüntüsü al

#### Cypress Yapılandırması

`frontend/cypress.config.js` dosyasında:
- `baseUrl`: `http://localhost:5173`
- `viewportWidth`: 1280
- `viewportHeight`: 720
- Video kaydı ve ekran görüntüsü ayarları

---

## Test Çalıştırma Öncesi Gereksinimler

### Backend Sunucusu
Rails backend sunucusu çalışıyor olmalı:
```bash
rails server
# veya
rails s
```
Backend `http://localhost:3000` adresinde çalışmalı.

### Frontend Sunucusu (Cypress için)
React frontend sunucusu çalışıyor olmalı:
```bash
cd frontend
npm run dev
```
Frontend `http://localhost:5173` adresinde çalışmalı.

### Veritabanı
Test veritabanı hazır olmalı:
```bash
rails db:test:prepare
# veya
rails db:migrate RAILS_ENV=test
```

---

## Test Senaryoları Detayları

### Cucumber Test Senaryoları

#### 1. Login Tests

**Scenario: Successful login with valid credentials**
- POST request to `/users/login` with valid email and password
- Response status should be 200
- Response should contain "Login successful"

**Scenario: Failed login with invalid credentials**
- POST request to `/users/login` with invalid password
- Response status should be 401
- Response should contain "Invalid email or password"

#### 2. Patients Tests

**Scenario: View patients list**
- GET request to `/patients`
- Response should contain patient names

**Scenario: Create a new patient**
- POST request to `/patients` with patient data
- Response status should be 201
- Patient should appear in list

#### 3. Departments Tests

**Scenario: View departments list**
- GET request to `/departments`
- Response should contain department names

**Scenario: Create a new department**
- POST request to `/departments` with department data
- Response status should be 201
- Department should appear in list

---

### Cypress E2E Test Senaryoları

#### 1. Site Açılması ve Login
- Site açılır
- Login sayfası görüntülenir
- Admin kullanıcı bilgileri ile giriş yapılır
- Dashboard sayfasına yönlendirilir

#### 2. Yeni Hasta Ekleme
- Patients sayfasına gidilir
- "Yeni Hasta" butonuna tıklanır
- Hasta formu doldurulur
- Hasta oluşturulur ve listede görünür

#### 3. Yeni Departman Ekleme
- Departments sayfasına gidilir
- "Yeni Departman" butonuna tıklanır
- Departman formu doldurulur
- Departman oluşturulur ve listede görünür

#### 4. Tam Workflow
- Login yapılır
- Hasta eklenir
- Departman eklenir
- Tüm işlemler video kaydında görünür

---

## Test Sonuçları

### Cucumber Test Sonuçları
Test sonuçları terminal'de görüntülenir. Başarılı testler yeşil, başarısız testler kırmızı gösterilir.

### Cypress Test Sonuçları
- Test sonuçları terminal'de görüntülenir
- Video kayıtları `frontend/cypress/videos/` dizininde saklanır
- Ekran görüntüleri `frontend/cypress/screenshots/` dizininde saklanır

---

## Notlar

1. **Backend ve Frontend Sunucuları**: Testlerin çalışması için her iki sunucu da çalışıyor olmalı.

2. **Test Verileri**: Cucumber testleri için test verileri otomatik olarak oluşturulur ve temizlenir.

3. **Video Kaydı**: Cypress testleri otomatik olarak video kaydı yapar. Videolar test sırasında yapılan tüm işlemleri gösterir.

4. **Test Kullanıcıları**: Testler için kullanılan kullanıcı bilgileri:
   - Email: `admin@hospital.com`
   - Password: `admin123`

---

## Sorun Giderme

### Cucumber Testleri Çalışmıyor
- Backend sunucusunun çalıştığından emin olun
- Veritabanı migration'larının çalıştığından emin olun: `rails db:migrate RAILS_ENV=test`

### Cypress Testleri Çalışmıyor
- Frontend sunucusunun çalıştığından emin olun (`npm run dev`)
- Backend sunucusunun çalıştığından emin olun (`rails server`)
- Cypress'in doğru baseUrl'i kullandığından emin olun

### Video Kaydı Oluşmuyor
- `cypress.config.js` dosyasında `video: true` olduğundan emin olun
- Disk alanı kontrolü yapın


