class DoctorsController < ApplicationController
  before_action :set_doctor, only: [:show, :update, :destroy]

  # GET /doctors
  def index
    @doctors = Doctor.all.includes(:department)
    render json: @doctors, include: [:department, :appointments]
  end

  # GET /doctors/1
  def show
    render json: @doctor, include: [:department, :appointments]
  end

  # POST /doctors
  def create
    @doctor = Doctor.new(doctor_params)

    if @doctor.save
      render json: @doctor, include: :department, status: :created
    else
      render json: @doctor.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /doctors/1
  def update
    if @doctor.update(doctor_params)
      render json: @doctor, include: :department
    else
      render json: @doctor.errors, status: :unprocessable_entity
    end
  end

  # DELETE /doctors/1
  def destroy
    @doctor.destroy
    head :no_content
  end

  private

  def set_doctor
    @doctor = Doctor.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    render json: { error: "Doctor not found" }, status: :not_found
  end

  def doctor_params
    params.require(:doctor).permit(:name, :email, :phone, :specialization, :department_id)
  end
end

