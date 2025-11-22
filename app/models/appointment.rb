class Appointment < ApplicationRecord
  belongs_to :patient
  belongs_to :doctor
  belongs_to :department
  
  validates :appointment_date, presence: true
  validates :status, presence: true, inclusion: { in: %w[scheduled completed cancelled] }
  
  validate :appointment_date_cannot_be_in_the_past, on: :create
  
  private
  
  def appointment_date_cannot_be_in_the_past
    if appointment_date.present? && appointment_date < Time.current
      errors.add(:appointment_date, "can't be in the past")
    end
  end
end

