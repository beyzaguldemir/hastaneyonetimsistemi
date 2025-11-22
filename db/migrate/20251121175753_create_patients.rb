class CreatePatients < ActiveRecord::Migration[8.0]
  def change
    create_table :patients do |t|
      t.string :name
      t.string :email
      t.string :phone
      t.date :birth_date
      t.text :address

      t.timestamps
    end
    add_index :patients, :email
  end
end
