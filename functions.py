import requests
import webbrowser

def XeroFirstAuth(client_id, redirect_url, scope, b64_id_secret):
    # 1. Send a user to authorize your app
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)
    
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    
    # 3. Exchange the code
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Authorization': 'Basic ' + b64_id_secret
                            },
                            data = {
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': redirect_url
                            })
    json_response = response.json()
    
    # 4. Receive your tokens
    return [json_response['access_token'], json_response['refresh_token']]

def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
    
    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']

# 5. Refreshing access tokens
def XeroRefreshToken(refresh_token, b64_id_secret):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                            headers = {
                                'Authorization' : 'Basic ' + b64_id_secret,
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type' : 'refresh_token',
                                'refresh_token' : refresh_token
                            })
    json_response = response.json()
    
    new_refresh_token = json_response['refresh_token']
    rt_file = open('refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()
    
    return [json_response['access_token'], json_response['refresh_token']]

# 6. Call the API
def GetXeroData(category, b64_id_secret):
    old_refresh_token = open('refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token, b64_id_secret)
    xero_tenant_id = XeroTenants(new_tokens[0])
    
    get_url = 'https://api.xero.com/api.xro/2.0/' + category
    response = requests.get(get_url,
                           headers = {
                               'Authorization': 'Bearer ' + new_tokens[0],
                               'Xero-tenant-id': xero_tenant_id,
                               'Accept': 'application/json'
                           })
    return response.json()

# 7. Create a new transaction
def XeroNewTransaction(new_data, b64_id_secret):
    old_refresh_token = open('refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token, b64_id_secret)
    xero_tenant_id = XeroTenants(new_tokens[0])

    post_url = 'https://api.xero.com/api.xro/2.0/BankTransactions/post'
    response = requests.post(post_url, json = new_data,
                           headers = {
                               'Authorization': 'Bearer ' + new_tokens[0],
                               'Xero-tenant-id': xero_tenant_id,
                               'Accept': 'application/json'
                           })
