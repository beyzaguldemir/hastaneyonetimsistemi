class AppointmentsController < ApplicationController
  before_action :set_appointment, only: [:show, :update, :destroy]

  # GET /appointments
  def index
    @appointments = Appointment.all.includes(:patient, :doctor, :department)
    render json: @appointments, include: [:patient, :doctor, :department]
  end

  # GET /appointments/1
  def show
    render json: @appointment, include: [:patient, :doctor, :department]
  end

  # POST /appointments
  def create
    @appointment = Appointment.new(appointment_params)

    if @appointment.save
      render json: @appointment, include: [:patient, :doctor, :department], status: :created
    else
      render json: @appointment.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /appointments/1
  def update
    if @appointment.update(appointment_params)
      render json: @appointment, include: [:patient, :doctor, :department]
    else
      render json: @appointment.errors, status: :unprocessable_entity
    end
  end

  # DELETE /appointments/1
  def destroy
    @appointment.destroy
    head :no_content
  end

  private

  def set_appointment
    @appointment = Appointment.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    render json: { error: "Appointment not found" }, status: :not_found
  end

  def appointment_params
    params.require(:appointment).permit(:appointment_date, :status, :patient_id, :doctor_id, :department_id, :notes)
  end
end

