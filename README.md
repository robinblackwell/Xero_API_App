# Xero_API_App
A simple app to post transactions in bulk to the Xero accounting software using the Xero API. Originally designed  with a specific data format in mind, the code will need to be altered to incorporate new data sources accordingly.

App consists of four Python files: firsttimerun.py, functions.py, main.py and params.py.
Please have these four files in their own directory before running anything.

## First time run:
1). Run firsttimerun.py. The command line will read: "What is the response URL?"  
2). A new browser page will pop up, asking you to log in with your Xero username/password.  
3). Log in and select which Xero account you would like to connect with.  
4). You will be redirected to the Xero homepage.  
5). Now please copy the full website address of the redirected Xero homepage.  
6). Paste it in the Python command line and hit enter.  
7). You should now have a refresh_token.txt file in your folder. Please keep this here and do not edit/move it.  

## Uploading transactions:

1). Ensure the above steps have been run once and a refresh_token.txt file exists in your working directory.  
2). Place a .csv file containing the transactions for the period you wish to upload for in the same directory as the .py files and change the main.py code to recognise the name and structure of the .csv file.  
3). Run main.py.  

Your Xero Bandcamp transactions should now be uploaded.
