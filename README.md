🧾 Invoice Agent — AI-Powered Invoice Analyzer
Invoice Agent is a FastAPI-based AI service that extracts structured data from invoice images using Optical Character Recognition (OCR) and intelligent parsing. It outputs clean, validated JSON including vendor, invoice number, dates, totals, and line items.

🚀 Features
✅ Upload any invoice (photo, scanned, or digital) ✅ OCR extraction using Tesseract ✅ Heuristic parsing of key invoice fields ✅ Structured JSON output validated with Pydantic ✅ Ready for Docker + Render deployment ✅ Includes 5+ pytest test cases ✅ Optional Layout Parser support for table detection

🌐 Deployment Links
GitHub Repository: https://github.com/jajj57/invoice-agent_Ejaj.git
Render Deployment: https://invoice-agent-ejaj.onrender.com/docs

🧩 Architecture Overview
Request → FastAPI → OCR (Tesseract) → Parser → Pydantic Validation → JSON Response

🛠️ Setup (Local)
1️⃣ Clone the repository
git clone https://github.com/jajj57/invoice-agent_Ejaj.git cd invoice-agent_Ejaj
2️⃣ Create a virtual environment
python -m venv .venv source .venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run locally
uvicorn main:app --reload
Open: http://localhost:8000/docs

🐳 Run with Docker (Local)
docker compose up --build
Access: http://localhost:8000/docs

🌐 Deployment on Render
Push to GitHub 
Connect to Render Web Service 
Build Command: docker build -t invoice-agent . 
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

📡 API Documentation
POST /analyze — Upload an invoice image for analysis.
Example cURL
curl -X POST "http://localhost:8000/analyze"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "file=@sample_invoice_1.jpg"

✅ Example JSON Response
{ “vendor”: “ACME Corporation”, “invoice_number”: “INV-12345”, “invoice_date”: “2025-01-12”, “currency”: “USD”, “subtotal”: 1200.00, “tax”: 96.00, “total”: 1296.00, “line_items”: [ {“description”: “Widget A”, “quantity”: 10, “unit_price”: 120.00, “amount”: 1200.00} ], “layout”: [{“x1”:10,“y1”:20,“x2”:120,“y2”:40,“text”:“INVOICE”,“confidence”:95.2}], “ocr_text”: “INVOICE NO INV-12345 ACME Corporation …”, “confidence_overall”: 94.7 }

🧪 Testing
pytest -v
Includes 5+ sample invoice test cases (photo, scanned, and digital).

🧱 Folder Structure
invoice-agent_Ejaj/ │ ├── app/ │ ├── templates/ │ ├── static/ │ ├── services/ │ ├── models.py │ ├── config.py │ └── main.py │ ├── tests/ ├── Dockerfile ├── docker-compose.yml ├── requirements.txt └── README.md

🎯 Future Enhancements
Integrate Layout Parser for table detection 
Use LLM for smarter parsing 
Add DB for invoice history 
Web frontend for visualization

👤 Author
Ejaj Ul Ambia 📧 GitHub Profile

🏁 Summary

