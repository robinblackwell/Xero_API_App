import base64

client_id = ##your client id here##
client_secret = ##your client secret here##
redirect_url = 'https://www.xero.com/uk/'
scope = 'offline_access accounting.transactions accounting.contacts.read accounting.settings.read'
b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')