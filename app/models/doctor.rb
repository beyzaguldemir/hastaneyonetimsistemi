class Doctor < ApplicationRecord
  belongs_to :department
  has_many :appointments, dependent: :destroy
  
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :phone, presence: true
  validates :specialization, presence: true
end

