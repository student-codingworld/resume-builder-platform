# Professional Resume Builder

A full-stack web application to generate professional, ATS-friendly PDF resumes. The application features a dynamic React frontend for easy data entry and a Django backend powered by ReportLab for precision PDF generation.

## 🚀 Features

*   **Professional PDF Layout**: strict formatting, clean spacing, and ATS-friendly structure.
*   **Dynamic Sections**: Add/Remove entries for Education, Experience, Projects, Skills, and Certifications.
*   **Real-time Form**: Interactive UI to input all your professional details.
*   **Instant Download**: Generate and download your PDF resume instantly.

---

## 🛠️ Prerequisites

*   **Node.js** (v14 or higher)
*   **Python** (v3.8 or higher)

---

## 📥 Installation Guide

### 1. Backend Setup (Django)

1.  Navigate to the backend directory:
    ```bash
    cd backend/core
    ```

2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    # Windows
    python -m venv venv
    ..\venv\Scripts\activate
    ```

3.  Install Python dependencies:
    ```bash
    pip install django djangorestframework reportlab django-cors-headers
    ```

4.  Apply database migrations:
    ```bash
    python manage.py migrate
    ```

5.  Run the backend server:
    ```bash
    python manage.py runserver
    ```
    The backend will start at `http://127.0.0.1:8000`.

### 2. Frontend Setup (React)

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install Node dependencies:
    ```bash
    npm install
    ```
    *Note: `axios` and core React libraries will be installed.*

3.  Start the development server:
    ```bash
    npm start
    ```
    The frontend will open at `http://localhost:3000`.

---

## 📖 User Manual

1.  **Open the Application**: Go to `http://localhost:3000` in your browser.
2.  **Personal Info**: Fill in your Name, Email, Phone, and Location. Add your LinkedIn/GitHub URLs.
3.  **Add Sections**:
    *   Click **+ Add Education/Experience/Project** to add new entries.
    *   Fill in various details (Institution, Degree, Job Title, Company, etc.).
    *   **Pro Tip**: For descriptions, use bullet points. The PDF generator formats them automatically.
4.  **Skills**: Add skills by category (e.g., Category: "Languages", Items: "Python, JavaScript").
5.  **Generate**: Click the **Generate Resume** button.
6.  **Download**: Once generated, a **Download PDF** button will appear. Click it to save your file.

---

## 🔧 Troubleshooting

*   **"Resume not found" error**: Ensure you clicked "Generate Resume" first and waited for the success message.
*   **CORS errors**: Make sure both backend (port 8000) and frontend (port 3000) are running.
*   **PDF formatting issues**: Ensure descriptions are plain text. Special characters might need manual handling.

---

## 📁 Project Structure

```
resume/
├── backend/
│   └── core/
│       ├── manage.py
│       ├── core/       # Settings & Config
│       └── resume/     # App logic (Models, Views, PDF Engine)
└── frontend/
    ├── src/
    │   ├── components/ # ResumeForm.jsx
    │   ├── App.js
    │   └── App.css     # Styling
    └── public/
```
