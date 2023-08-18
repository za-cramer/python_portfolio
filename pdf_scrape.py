import os

import requests

# Set your website credentials
LOGIN_URL = 'https://members.associationonline.com/account/logon'

USERNAME = 'your_username'
PASSWORD = 'your_password'

# Login to the website and get the session
session = requests.Session()
login_data = {
    'Username:': USERNAME,
    'Password:': PASSWORD
}
session.post(LOGIN_URL, data=login_data)
# Direct links to PDFs
pdf_links = [
  # List of PDF Links from Website #
]

# Download PDFs to Location
download_folder = 'FILE PATH'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

for pdf_link in pdf_links:
    pdf_filename = pdf_link.split('=')[-1] + '.pdf'  # Extract the documentId from the link
    pdf_path = os.path.join(download_folder, pdf_filename)
    
    pdf_response = session.get(pdf_link, stream=True)
    
    if pdf_response.status_code == 200:
        with open(pdf_path, 'wb') as pdf_file:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        
        print(f"Downloaded: {pdf_filename} to {pdf_path}")
    else:
        print(f"Failed to download: {pdf_filename} - Status Code: {pdf_response.status_code}")

print("Download complete.")
