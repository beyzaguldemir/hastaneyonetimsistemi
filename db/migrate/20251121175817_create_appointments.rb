class CreateAppointments < ActiveRecord::Migration[8.0]
  def change
    create_table :appointments do |t|
      t.datetime :appointment_date
      t.string :status
      t.references :patient, null: false, foreign_key: true
      t.references :doctor, null: false, foreign_key: true
      t.references :department, null: false, foreign_key: true
      t.text :notes

      t.timestamps
    end
  end
end
