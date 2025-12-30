# DataClone AI

**DataClone AI** is a Duplicate Document & Identity Forgery Detection System. It leverages AI/ML techniques to detect anomalies in documents, effectively identifying potential forgeries and duplicates.

## Features

- **Document Analysis**: Detects inconsistencies, overwritten text, and font anomalies.
- **Identity Verification**: Verifies identity documents against known patterns.
- **Reporting**: Generates detailed reports of the analysis.
- **Dashboard**: A user-friendly dashboard to view statistics and recent activities.

## Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Visualization**: Recharts
- **PDF Generation**: html2canvas, jspdf
- **Animations**: Framer Motion

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MySQL (via SQLAlchemy)
- **Authentication**: JWT (python-jose)
- **Computer Vision / OCR**: OpenCV, PyTesseract
- **Data Processing**: NumPy, Pandas

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- MySQL Server

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (create a `.env` file based on your configuration).
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the project root:
   ```bash
   # (If you are in backend, go back up)
   cd ..
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## License
[Add License Information Here]
