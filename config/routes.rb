Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # Users routes
  resources :users, except: [:new, :edit] do
    collection do
      post :login
    end
  end

  # Departments routes
  resources :departments, except: [:new, :edit]

  # Patients routes
  resources :patients, except: [:new, :edit]

  # Doctors routes
  resources :doctors, except: [:new, :edit]

  # Appointments routes
  resources :appointments, except: [:new, :edit]

  # Root path
  root "departments#index"
end
