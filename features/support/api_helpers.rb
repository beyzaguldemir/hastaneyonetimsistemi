module ApiHelpers
  def api_base_url
    'http://localhost:3000'
  end

  def send_request(method, path, params = {}, headers = {})
    uri = URI("#{api_base_url}#{path}")
    
    case method.upcase
    when 'GET'
      request = Net::HTTP::Get.new(uri)
    when 'POST'
      request = Net::HTTP::Post.new(uri)
      request.body = params.to_json
      request['Content-Type'] = 'application/json'
    when 'PUT'
      request = Net::HTTP::Put.new(uri)
      request.body = params.to_json
      request['Content-Type'] = 'application/json'
    when 'DELETE'
      request = Net::HTTP::Delete.new(uri)
    end

    headers.each { |key, value| request[key] = value }
    
    response = Net::HTTP.start(uri.hostname, uri.port) do |http|
      http.request(request)
    end

    @last_response = {
      status: response.code.to_i,
      body: JSON.parse(response.body) rescue response.body,
      headers: response.to_hash
    }
  end

  def last_response
    @last_response
  end

  def parse_json(response_body)
    JSON.parse(response_body)
  rescue JSON::ParserError
    response_body
  end
end

World(ApiHelpers)




