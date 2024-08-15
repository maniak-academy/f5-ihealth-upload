
# F5 BIG-IP QKView Downloader and iHealth Uploader

This micro web application provides a quick and easy way to download QKView files from an F5 BIG-IP device and upload them to F5 iHealth for analysis. The app is designed to streamline the process of sending QKView files to F5 iHealth, making it more efficient and user-friendly.

## Features

- **Download QKView Files**: Retrieve QKView files directly from your F5 BIG-IP device.
- **Upload to F5 iHealth**: Quickly upload the QKView files to F5 iHealth for diagnostics and analysis.
- **User-Friendly Interface**: Intuitive Streamlit-based web interface for managing QKView files.

## Getting Started

### Prerequisites

- Docker installed on your machine.
- An F5 BIG-IP device with QKView capabilities.
- F5 iHealth account credentials.

### Downloading and Running the App

To run the application using Docker, follow these simple steps:

1. **Pull the Docker Image**

   Download the Docker image from Docker Hub:

   ```bash
   docker pull sebbycorp/f5-qkview-app
   ```

1. **Run the Docker Container**
    
    Run the application in a Docker container:

    ```bash
    docker run -p 8501:8501 sebbycorp/f5-qkview-app:latest
    ```

This command will start the application, and you can access it by navigating to http://localhost:8501 in your web browser.

# Using the Application

## Download QKView:

1. Enter the **BIG-IP Host** (e.g., `192.168.1.1`), **Username**, and **Password**.
2. Specify the **Output Filename** for the QKView file.
3. Click the **Download QKView** button to download the file from the F5 BIG-IP device. The file will be saved in the `static` folder within the container.

## Upload to iHealth:

1. Enter your **F5 iHealth Client ID** and **Client Secret**.
2. (Optional) Enter a **F5 Support Case ID** if you want to associate the QKView file with a specific support case.
3. Select the desired QKView file from the dropdown list.
4. Click the **Upload to iHealth** button to upload the selected QKView file to F5 iHealth.

## Generating an API Token in F5 iHealth

To use the iHealth API, you need to generate an API token. Follow these steps:

### Log in to F5 iHealth:
- Navigate to the [F5 iHealth Portal](https://ihealth.f5.com/) and log in with your F5 credentials.

### Navigate to API Management:
- After logging in, go to your profile or account settings, and look for an API management or OAuth token section.

### Create a New API Token:
- Create a new API token by specifying a name or description for the token. This helps in identifying the token later.
- Select the necessary scopes or permissions required for accessing the iHealth API.

### Save the Client ID and Client Secret:
- After generating the token, save the **Client ID** and **Client Secret**. You will need these credentials to authenticate API requests.

### Use the API Token:
- Use the **Client ID** and **Client Secret** in the application to obtain an authorization token, which is then used to interact with the iHealth API.

## Example Usage

```bash
docker pull sebbycorp/f5-qkview-app
docker run -p 8501:8501 sebbycorp/f5-qkview-app:latest
```

## Troubleshooting

- QKView Download Issues: Make sure the BIG-IP device is reachable and that the credentials provided are correct.
iHealth Upload Issues: Double-check your iHealth credentials and ensure that any required fields, such as the Support Case ID, are correctly filled.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any issues or questions, please open an issue in the repository or contact the repository owner.
