# This file should ensure the existence of records required to run the application in every environment (production,
# development, test). The code here should be idempotent so that it can be executed at any point in every environment.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Example:
#
#   ["Action", "Comedy", "Drama", "Horror"].each do |genre_name|
#     MovieGenre.find_or_create_by!(name: genre_name)
#   end

puts "🌱 Seeding veritabanına test verileri ekleniyor..."

# Önce mevcut verileri temizle (isteğe bağlı - yorum satırını kaldırarak aktif edebilirsiniz)
# Department.destroy_all
# Patient.destroy_all
# Doctor.destroy_all
# Appointment.destroy_all
# User.destroy_all

# Departments (Departmanlar)
puts "📋 Departmanlar oluşturuluyor..."
dept1 = Department.find_or_create_by!(name: "Kardiyoloji") do |d|
  d.description = "Kalp ve dolaşım sistemi hastalıklarının tanı ve tedavisi"
end

dept2 = Department.find_or_create_by!(name: "Nöroloji") do |d|
  d.description = "Sinir sistemi hastalıklarının tanı ve tedavisi"
end

dept3 = Department.find_or_create_by!(name: "Ortopedi") do |d|
  d.description = "Kemik, eklem ve kas sistemi hastalıklarının tedavisi"
end

dept4 = Department.find_or_create_by!(name: "Genel Cerrahi") do |d|
  d.description = "Genel cerrahi müdahaleler ve operasyonlar"
end

dept5 = Department.find_or_create_by!(name: "Dahiliye") do |d|
  d.description = "İç hastalıklarının tanı ve tedavisi"
end

puts "✅ #{Department.count} departman oluşturuldu"

# Patients (Hastalar)
puts "👥 Hastalar oluşturuluyor..."
patient1 = Patient.find_or_create_by!(email: "ahmet.yilmaz@example.com") do |p|
  p.name = "Ahmet Yılmaz"
  p.phone = "05321234567"
  p.birth_date = Date.new(1985, 3, 15)
  p.address = "İstanbul, Kadıköy"
end

patient2 = Patient.find_or_create_by!(email: "ayse.demir@example.com") do |p|
  p.name = "Ayşe Demir"
  p.phone = "05329876543"
  p.birth_date = Date.new(1990, 7, 22)
  p.address = "Ankara, Çankaya"
end

patient3 = Patient.find_or_create_by!(email: "mehmet.kaya@example.com") do |p|
  p.name = "Mehmet Kaya"
  p.phone = "05321112233"
  p.birth_date = Date.new(1978, 11, 8)
  p.address = "İzmir, Konak"
end

patient4 = Patient.find_or_create_by!(email: "fatma.ozkan@example.com") do |p|
  p.name = "Fatma Özkan"
  p.phone = "05324445566"
  p.birth_date = Date.new(1995, 5, 30)
  p.address = "Bursa, Nilüfer"
end

patient5 = Patient.find_or_create_by!(email: "ali.celik@example.com") do |p|
  p.name = "Ali Çelik"
  p.phone = "05327778899"
  p.birth_date = Date.new(1982, 9, 12)
  p.address = "Antalya, Muratpaşa"
end

puts "✅ #{Patient.count} hasta oluşturuldu"

# Doctors (Doktorlar)
puts "👨‍⚕️ Doktorlar oluşturuluyor..."
doctor1 = Doctor.find_or_create_by!(email: "dr.serdar@example.com") do |d|
  d.name = "Dr. Serdar Özdemir"
  d.phone = "05321111111"
  d.specialization = "Kardiyolog"
  d.department = dept1
end

doctor2 = Doctor.find_or_create_by!(email: "dr.zeynep@example.com") do |d|
  d.name = "Dr. Zeynep Aydın"
  d.phone = "05322222222"
  d.specialization = "Nörolog"
  d.department = dept2
end

doctor3 = Doctor.find_or_create_by!(email: "dr.kaan@example.com") do |d|
  d.name = "Dr. Kaan Şahin"
  d.phone = "05323333333"
  d.specialization = "Ortopedi Uzmanı"
  d.department = dept3
end

doctor4 = Doctor.find_or_create_by!(email: "dr.burcu@example.com") do |d|
  d.name = "Dr. Burcu Yıldız"
  d.phone = "05324444444"
  d.specialization = "Genel Cerrah"
  d.department = dept4
end

doctor5 = Doctor.find_or_create_by!(email: "dr.emre@example.com") do |d|
  d.name = "Dr. Emre Kılıç"
  d.phone = "05325555555"
  d.specialization = "Dahiliye Uzmanı"
  d.department = dept5
end

doctor6 = Doctor.find_or_create_by!(email: "dr.selin@example.com") do |d|
  d.name = "Dr. Selin Arslan"
  d.phone = "05326666666"
  d.specialization = "Kardiyolog"
  d.department = dept1
end

puts "✅ #{Doctor.count} doktor oluşturuldu"

# Appointments (Randevular)
puts "📅 Randevular oluşturuluyor..."
if Appointment.count == 0
  # Gelecek tarihlerde randevular oluştur
  Appointment.create!(
    patient: patient1,
    doctor: doctor1,
    department: dept1,
    appointment_date: 3.days.from_now,
    status: "scheduled",
    notes: "EKG ve kalp kontrolü"
  )

  Appointment.create!(
    patient: patient2,
    doctor: doctor2,
    department: dept2,
    appointment_date: 5.days.from_now,
    status: "scheduled",
    notes: "Baş ağrısı şikayeti"
  )

  Appointment.create!(
    patient: patient3,
    doctor: doctor3,
    department: dept3,
    appointment_date: 7.days.from_now,
    status: "scheduled",
    notes: "Bel ağrısı muayenesi"
  )

  Appointment.create!(
    patient: patient4,
    doctor: doctor4,
    department: dept4,
    appointment_date: 10.days.from_now,
    status: "scheduled",
    notes: "Kontrol muayenesi"
  )

  Appointment.create!(
    patient: patient5,
    doctor: doctor5,
    department: dept5,
    appointment_date: 12.days.from_now,
    status: "scheduled",
    notes: "Genel kontrol"
  )

  Appointment.create!(
    patient: patient1,
    doctor: doctor6,
    department: dept1,
    appointment_date: 15.days.from_now,
    status: "scheduled",
    notes: "İkinci görüş"
  )

  puts "✅ #{Appointment.count} randevu oluşturuldu"
else
  puts "⏭️  Randevular zaten mevcut (#{Appointment.count} adet)"
end

# Users (Kullanıcılar - Login için)
puts "🔐 Kullanıcılar oluşturuluyor..."
admin_user = User.find_or_initialize_by(email: "admin@hospital.com")
admin_user.password = "admin123"
admin_user.password_confirmation = "admin123"
admin_user.save!
puts "✅ Admin kullanıcısı oluşturuldu/güncellendi"

user_user = User.find_or_initialize_by(email: "user@hospital.com")
user_user.password = "user123"
user_user.password_confirmation = "user123"
user_user.save!
puts "✅ User kullanıcısı oluşturuldu/güncellendi"

puts "✅ Toplam #{User.count} kullanıcı mevcut"

puts ""
puts "🎉 Veritabanı seed işlemi tamamlandı!"
puts "📊 Özet:"
puts "   - #{Department.count} Departman"
puts "   - #{Patient.count} Hasta"
puts "   - #{Doctor.count} Doktor"
puts "   - #{Appointment.count} Randevu"
puts "   - #{User.count} Kullanıcı"
puts ""
puts "💡 Test kullanıcı bilgileri:"
puts "   Admin: admin@hospital.com / admin123"
puts "   User:  user@hospital.com / user123"
