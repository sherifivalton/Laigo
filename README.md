# Mindee OCR Microservice

This project provides a FastAPI microservice for performing OCR on uploaded image and PDF files using the Mindee API.

## Features

- Accepts PDF and image file uploads
- Supports single-page and multi-page PDF documents
- Integrates with Mindee for OCR
- Post-processes OCR output into structured text
- Parses and converts digit characters to real numbers

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sherifivalton/Laigo
   cd <repository-name>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv mindee_env
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\mindee_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source mindee_env/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API documentation**:
   - Open your browser and go to `http://localhost:8000/docs` for Swagger UI.
   - Go to `http://localhost:8000/redoc` for ReDoc documentation.


## Running Tests

Tests are included to verify the functionality of the OCR service. To run the tests:

1. Ensure you are in the project directory and the virtual environment is activated.

2. Run the tests using `pytest`:
    ```bash
    pytest
    ```
