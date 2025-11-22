class Department < ApplicationRecord
  has_many :doctors, dependent: :destroy
  has_many :appointments, dependent: :destroy
  
  validates :name, presence: true
end

