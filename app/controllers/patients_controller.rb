class PatientsController < ApplicationController
  before_action :set_patient, only: [:show, :update, :destroy]

  # GET /patients
  def index
    @patients = Patient.all
    render json: @patients, include: :appointments
  end

  # GET /patients/1
  def show
    render json: @patient, include: :appointments
  end

  # POST /patients
  def create
    @patient = Patient.new(patient_params)

    if @patient.save
      render json: @patient, status: :created
    else
      render json: @patient.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /patients/1
  def update
    if @patient.update(patient_params)
      render json: @patient
    else
      render json: @patient.errors, status: :unprocessable_entity
    end
  end

  # DELETE /patients/1
  def destroy
    @patient.destroy
    head :no_content
  end

  private

  def set_patient
    @patient = Patient.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    render json: { error: "Patient not found" }, status: :not_found
  end

  def patient_params
    params.require(:patient).permit(:name, :email, :phone, :birth_date, :address)
  end
end

