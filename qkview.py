import streamlit as st
import os
import requests
import base64
from datetime import datetime

def _download(host, creds, fp):
    chunk_size = 512 * 1024

    headers = {
        'Content-Type': 'application/octet-stream'
    }
    filename = os.path.basename(fp)
    uri = f'https://{host}/mgmt/cm/autodeploy/qkview-downloads/{filename}'
    requests.packages.urllib3.disable_warnings()

    with open(fp, 'wb') as f:
        start = 0
        end = chunk_size - 1
        size = 0
        current_bytes = 0

        while True:
            content_range = f"{start}-{end}/{size}"
            headers['Content-Range'] = content_range

            resp = requests.get(uri,
                                auth=creds,
                                headers=headers,
                                verify=False,
                                stream=True)

            if resp.status_code == 200:
                if size > 0:
                    current_bytes += chunk_size
                    for chunk in resp.iter_content(chunk_size):
                        f.write(chunk)

                if end == size:
                    break

            crange = resp.headers['Content-Range']

            if size == 0:
                size = int(crange.split('/')[-1]) - 1

                if chunk_size > size:
                    end = size

                continue

            start += chunk_size

            if (current_bytes + chunk_size) > size:
                end = size
            else:
                end = start + chunk_size - 1

def get_ihealth_token(client_id, client_secret):
    url = "https://identity.account.f5.com/oauth2/ausp95ykc80HOU7SQ357/v1/token"
    auth_header = f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    
    headers = {
        "accept": "application/json",
        "authorization": auth_header,
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded"
    }
    
    data = "grant_type=client_credentials&scope=ihealth"
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        st.error(f"Failed to get iHealth token. Status: {response.status_code}")
        return None

def upload_to_ihealth(token, qkview_file, support_case_id=None):
    url = "https://ihealth2-api.f5.com/qkview-analyzer/api/qkviews"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.f5.ihealth.api",
        "User-Agent": "MyGreatiHealthClient"
    }
    
    files = {
        'qkview': (os.path.basename(qkview_file), open(qkview_file, 'rb')),
        'visible_in_gui': (None, 'True')
    }
    
    # Include the support case ID only if provided
    if support_case_id:
        files['f5_support_case'] = (None, support_case_id)
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200 or response.status_code == 202:
        st.success("QKView file uploaded successfully to iHealth and is being processed.")
    else:
        st.error(f"Failed to upload QKView to iHealth. Status: {response.status_code}")

# Streamlit UI setup
st.title("F5 BIG-IP QKView Downloader and iHealth Uploader")

# Input fields for BIG-IP details
big_ip_host = st.text_input("BIG-IP Host (e.g., 172.16.10.141)")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
output_filename = st.text_input("Output Filename", f"{big_ip_host}.qkview")

# Input fields for F5 iHealth credentials
client_id = st.text_input("F5 iHealth Client ID", type="password")
client_secret = st.text_input("F5 iHealth Client Secret", type="password")

# Input field for F5 Support Case ID (optional)
support_case_id = st.text_input("F5 Support Case ID (optional)")

if st.button("Download QKView"):
    if big_ip_host and username and password and output_filename:
        st.write("Starting QKView download...")

        try:
            # Ensure the static directory exists
            os.makedirs("static", exist_ok=True)
            
            # Save the file to the static directory
            output_path = os.path.join("static", output_filename)
            _download(big_ip_host, (username, password), output_path)
            st.success(f"QKView downloaded successfully as {output_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please fill in all the fields.")

# Dropdown list of .qkview files in static folder
static_folder = "static"
if os.path.exists(static_folder):
    qkview_files = [f for f in os.listdir(static_folder) if f.endswith('.qkview')]
    if qkview_files:
        selected_file = st.selectbox("Select a QKView file from the static folder:", qkview_files)
        file_path = os.path.join(static_folder, selected_file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert size to MB
        file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        st.write(f"Selected File: {selected_file} - {file_size:.2f} MB - Created: {file_creation_time}")
        
        if st.button("Upload to iHealth"):
            if client_id and client_secret:
                st.write("Requesting iHealth token...")
                
                token = get_ihealth_token(client_id, client_secret)
                
                if token:
                    st.write("Uploading QKView to iHealth...")
                    upload_to_ihealth(token, file_path, support_case_id)
            else:
                st.error("Please provide iHealth credentials.")
    else:
        st.write("No .qkview files found in the static folder.")
else:
    st.write("Static folder does not exist.")
