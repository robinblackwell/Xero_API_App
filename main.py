import pandas as pd
import numpy as np
import os
from params import *
from functions import *

# Get contacts and bank account details from Xero to specify where/who to post transactions to
xero_contacts = GetXeroData('Contacts', b64_id_secret)
xero_accounts = GetXeroData('Accounts', b64_id_secret)

account_name = ##account name that you wish to upload to##
contact_name = ##contact name related to the transactions##

accounts_list = [0]*len(xero_accounts['Accounts'])
for i in range(len(xero_accounts['Accounts'])):
    accounts_list[i] = xero_accounts['Accounts'][i]['Name']
account_code = xero_accounts['Accounts'][accounts_list.index(account_name)]['AccountID']

contact_list = [0]*len(xero_contacts['Contacts'])
for i in range(len(xero_contacts['Contacts'])):
    contact_list[i] = xero_contacts['Contacts'][i]['Name']
contact_id = xero_contacts['Contacts'][contact_list.index(contact_name)]['ContactID']

# Load transaction data
#here we are using bandcamp data as an example
bandcamp_data = pd.read_csv([s for s in os.listdir() if "bandcamp" in s][0], encoding = 'utf-16')

# Build upload dictionary containing all transactions we wish to post
unique_refs = bandcamp_data['paypal transaction id'].unique() #list of unique transaction references/IDs
to_upload = [0]*len(unique_refs)

for i in range(len(unique_refs)):
    to_upload[i] = {}
    to_upload[i]['Type'] = 'RECEIVE'
    to_upload[i]['Contact'] = {'ContactID': contact_id}
    to_upload[i]['BankAccount'] = {'AccountID': account_code}
    date = list(bandcamp_data.loc[bandcamp_data['paypal transaction id'] == unique_refs[i], 'date'])[0].split('/')
    date[2] = date[2][0:2]
    to_upload[i]['Date'] = '20' + date[2] + '-' + ('0' if len(date[0]) == 1 else '') + date[0] + '-' + ('0' if len(date[1]) == 1 else '') + date[1]
    to_upload[i]['Reference'] = unique_refs[i]
    to_upload[i]['LineAmountTypes'] = 'Exclusive'
    data_subset = bandcamp_data.loc[bandcamp_data['paypal transaction id'] == unique_refs[i]]
    add_line_items = []
    for j in range(len(data_subset)):
        add_line_items = add_line_items + [{'Description': 'Bandcamp Physical Sale - ' + data_subset.iloc[j]['item name'] +
                                          ' - ' + data_subset.iloc[j]['city'] + ', ' + data_subset.iloc[j]['country'],
                                      'TaxType': ('OUTPUT2' if not np.isnan(data_subset.iloc[j]['tax']) else 'NONE'),
                                      'UnitAmount': str(data_subset.iloc[j]['sub total']), 'AccountCode': '200',
                                  "Tracking": [{"Name": "Music Records", "Option": data_subset.iloc[j]['catalog number']}]}] + [{'Description': 'Shipping Costs', 'TaxType': 'NONE',
                                  'UnitAmount': str(data_subset.iloc[j]['shipping']), 'AccountCode': '200',
                                 "Tracking": [{"Name": "Music Records", "Option": "Shipping"}]}]
    to_upload[i]['LineItems'] = add_line_items

upload_dic = {}
upload_dic['BankTransactions'] = to_upload

# Post new transactions to Xero
XeroNewTransaction(upload_dic, b64_id_secret)