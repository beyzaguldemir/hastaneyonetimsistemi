import { defineConfig } from 'cypress'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'
import { existsSync, mkdirSync } from 'fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

// Cypress config dosyası: C:\hastaneyonetimi\frontend\cypress.config.js
// __dirname = C:\hastaneyonetimi\frontend
// Proje root = bir üst dizin = C:\hastaneyonetimi
const projectRoot = resolve(__dirname, '..')

// Video klasörleri - mutlak path ile
const videosFolder = resolve(projectRoot, 'test_videos')
const screenshotsFolder = resolve(projectRoot, 'test_screenshots')

// Klasörleri oluştur
if (!existsSync(videosFolder)) {
  mkdirSync(videosFolder, { recursive: true })
  console.log('✅ Created videos folder:', videosFolder)
}

if (!existsSync(screenshotsFolder)) {
  mkdirSync(screenshotsFolder, { recursive: true })
  console.log('✅ Created screenshots folder:', screenshotsFolder)
}

// Debug log - her Cypress başlatıldığında göreceksiniz
console.log('\n=== Cypress Video Config ===')
console.log('Config file dirname:', __dirname)
console.log('Project root:', projectRoot)
console.log('Videos will be saved to:', videosFolder)
console.log('Screenshots will be saved to:', screenshotsFolder)
console.log('Videos folder exists:', existsSync(videosFolder))
console.log('Screenshots folder exists:', existsSync(screenshotsFolder))
console.log('============================\n')

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    videoCompression: 32,
    screenshotOnRunFailure: true, // Başarısız testler için otomatik screenshot
    defaultCommandTimeout: 15000,
    requestTimeout: 15000,
    responseTimeout: 15000,
    pageLoadTimeout: 30000,
    trashAssetsBeforeRuns: false,
    // Video ve screenshot klasörlerini mutlak path ile ayarla
    videosFolder: videosFolder,
    screenshotsFolder: screenshotsFolder,
    setupNodeEvents(on, config) {
      // Cypress başladığında
      on('before:run', (details) => {
        console.log('\n📹 Cypress is starting tests...')
        console.log('📹 Videos will be saved to:', config.videosFolder || videosFolder)
        console.log('📸 Screenshots will be saved to:', config.screenshotsFolder || screenshotsFolder)
      })
      
      // Her spec (test dosyası) başladığında
      on('before:spec', (spec, results) => {
        console.log(`\n▶️ Running spec: ${spec.relative}`)
      })
      
      // Her spec (test dosyası) bittiğinde
      on('after:spec', (spec, results) => {
        console.log(`✅ Spec completed: ${spec.relative}`)
        if (results && results.stats) {
          console.log(`   Tests: ${results.stats.tests}, Passed: ${results.stats.passes}, Failed: ${results.stats.failures}`)
        }
      })
      
      // Cypress bittiğinde
      on('after:run', (results) => {
        console.log('\n📹 Cypress finished running all tests')
        console.log('📹 Total tests:', results.totalTests || 'N/A')
        console.log('📹 Passed:', results.totalPassed || 'N/A')
        console.log('📹 Failed:', results.totalFailed || 'N/A')
        console.log('📹 Videos should be in:', config.videosFolder || videosFolder)
        console.log('📸 Screenshots should be in:', config.screenshotsFolder || screenshotsFolder)
      })
      
      // Screenshot kaydedildiğinde
      on('after:screenshot', (details) => {
        console.log('📸 Screenshot saved:', details.path)
      })
      
      return config
    },
  },
})
