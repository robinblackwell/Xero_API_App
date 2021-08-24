from params import *
from functions import *

old_tokens = XeroFirstAuth(client_id, redirect_url, scope, b64_id_secret)
XeroRefreshToken(old_tokens[1], b64_id_secret)