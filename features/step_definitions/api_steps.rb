require 'net/http'
require 'json'

Given(/^the following users exist:$/) do |table|
  table.hashes.each do |row|
    user = User.find_or_initialize_by(email: row['email'])
    user.password = row['password']
    user.password_confirmation = row['password']
    user.save!
  end
end

Given(/^the following patients exist:$/) do |table|
  table.hashes.each do |row|
    patient = Patient.find_or_initialize_by(email: row['email'])
    patient.name = row['name']
    patient.email = row['email']
    patient.phone = row['phone']
    patient.birth_date = row['birth_date'] if row['birth_date']
    patient.address = row['address'] if row['address']
    patient.save!
  end
end

Given(/^the following departments exist:$/) do |table|
  table.hashes.each do |row|
    department = Department.find_or_initialize_by(name: row['name'])
    department.description = row['description']
    department.save!
  end
end

Given(/^I am authenticated as "(.*?)"$/) do |email|
  user = User.find_by(email: email)
  @auth_token = nil # For API-only, we can skip token for now, or store user in session
  @current_user = user
end

When(/^I send a (GET|POST|PUT|DELETE) request to "(.*?)"$/) do |method, path|
  send_request(method, path, {}, {})
end

When(/^I send a (GET|POST|PUT|DELETE) request to "(.*?)" with:$/) do |method, path, table|
  params = {}
  table.hashes.first.each do |key, value|
    params[key] = value
  end
  
  # Wrap params for Rails nested params format
  if method == 'POST' || method == 'PUT'
    resource_name = path.split('/').last.singularize
    params = { resource_name.to_sym => params }
  end
  
  send_request(method, path, params, {})
end

Then(/^the response status should be "(.*?)"$/) do |expected_status|
  expect(last_response[:status]).to eq(expected_status.to_i)
end

Then(/^the response should contain "(.*?)"$/) do |text|
  response_body = last_response[:body]
  response_string = response_body.is_a?(Hash) ? response_body.to_json : response_body.to_s
  expect(response_string).to include(text)
end

Then(/^the response should contain json:$/) do |json_string|
  expected = JSON.parse(json_string)
  actual = last_response[:body]
  expect(actual).to include(expected)
end




