# Hastane Yönetim Sistemi - Frontend

Modern React + Vite frontend uygulaması.

## Kurulum

```bash
# Bağımlılıkları yükle (zaten yüklü)
npm install

# Development sunucusunu başlat
npm run dev

# Production build
npm run build
```

## Özellikler

- ✅ Modern React 19 + Vite
- ✅ React Router ile routing
- ✅ Tailwind CSS ile stil
- ✅ Axios ile API entegrasyonu
- ✅ Authentication (Login/Logout)
- ✅ Protected Routes
- ✅ Dashboard
- ✅ CRUD işlemleri:
  - Departmanlar
  - Doktorlar
  - Hastalar
  - Randevular

## Kullanım

1. Backend sunucusunun çalıştığından emin olun (`http://localhost:3000`)
2. Frontend sunucusunu başlatın: `npm run dev`
3. Tarayıcıda `http://localhost:5173` adresini açın
4. Test kullanıcıları ile giriş yapın:
   - Admin: `admin@hospital.com` / `admin123`
   - User: `user@hospital.com` / `user123`

## Yapı

```
frontend/
├── src/
│   ├── components/      # Layout component
│   ├── context/         # Auth context
│   ├── pages/           # Sayfalar (Login, Dashboard, Departments, vb.)
│   ├── services/        # API servisleri
│   ├── App.jsx          # Ana component
│   └── main.jsx         # Entry point
├── public/
└── package.json
```

## API Entegrasyonu

Backend API'ye bağlanır: `http://localhost:3000`

Tüm API çağrıları `src/services/api.js` dosyasında tanımlanmıştır.
