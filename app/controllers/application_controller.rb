class ApplicationController < ActionController::API
  # Global exception handling
  rescue_from ActiveRecord::RecordNotFound, with: :record_not_found
  rescue_from ActionController::ParameterMissing, with: :parameter_missing
  rescue_from ActiveRecord::RecordInvalid, with: :record_invalid

  # Response helpers
  def render_success(data, status: :ok)
    render json: { success: true, data: data }, status: status
  end

  def render_error(message, status: :unprocessable_entity)
    render json: { success: false, error: message }, status: status
  end

  private

  # Exception handlers
  def record_not_found(exception)
    render json: { 
      success: false, 
      error: "#{exception.model || 'Record'} not found" 
    }, status: :not_found
  end

  def parameter_missing(exception)
    render json: { 
      success: false, 
      error: "Parameter missing: #{exception.param}" 
    }, status: :bad_request
  end

  def record_invalid(exception)
    render json: { 
      success: false, 
      errors: exception.record.errors.full_messages 
    }, status: :unprocessable_entity
  end
end
