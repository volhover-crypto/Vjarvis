from google_auth_oauthlib.flow import Flow
import json

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_auth_url():
    with open('credentials.json', 'r') as f:
        client_config = json.load(f)
    
    # Приводим конфиг к нужному виду, если он в формате "web"
    if 'web' in client_config:
        client_config = {
            "installed": {
                "client_id": client_config['web']['client_id'],
                "client_secret": client_config['web']['client_secret'],
                "auth_uri": client_config['web']['auth_uri'],
                "token_uri": client_config['web']['token_uri']
            }
        }

    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"Перейди по этой ссылке для авторизации:\n{auth_url}\n")
    print("После авторизации скопируй код и вставь его здесь:")
    
    auth_code = input("Введи код авторизации: ")
    
    flow.fetch_token(code=auth_code)
    creds = flow.credentials
    
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    print("Успешно! Токен сохранен в token.json")

if __name__ == '__main__':
    get_auth_url()
