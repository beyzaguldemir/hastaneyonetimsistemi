class UsersController < ApplicationController
  before_action :set_user, only: [:show, :update, :destroy]

  # POST /users/login
  def login
    @user = User.find_by(email: params[:email])
    
    if @user && @user.authenticate(params[:password])
      render json: { 
        message: "Login successful", 
        user: { id: @user.id, email: @user.email } 
      }, status: :ok
    else
      render json: { error: "Invalid email or password" }, status: :unauthorized
    end
  end

  # GET /users
  def index
    @users = User.all
    render json: @users.select(:id, :email, :created_at, :updated_at)
  end

  # GET /users/1
  def show
    render json: { id: @user.id, email: @user.email, created_at: @user.created_at, updated_at: @user.updated_at }
  end

  # POST /users
  def create
    @user = User.new(user_params)

    if @user.save
      render json: { id: @user.id, email: @user.email }, status: :created
    else
      render json: @user.errors, status: :unprocessable_entity
    end
  end

  # PATCH/PUT /users/1
  def update
    if @user.update(user_params)
      render json: { id: @user.id, email: @user.email }
    else
      render json: @user.errors, status: :unprocessable_entity
    end
  end

  # DELETE /users/1
  def destroy
    @user.destroy
    head :no_content
  end

  private

  def set_user
    @user = User.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    render json: { error: "User not found" }, status: :not_found
  end

  def user_params
    params.require(:user).permit(:email, :password, :password_confirmation)
  end
end

