class CreateDoctors < ActiveRecord::Migration[8.0]
  def change
    create_table :doctors do |t|
      t.string :name
      t.string :email
      t.string :phone
      t.string :specialization
      t.references :department, null: false, foreign_key: true

      t.timestamps
    end
    add_index :doctors, :email
  end
end
