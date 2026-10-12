# 🤖 Agentic Invoice Processor

A beautiful, demo-ready invoice processing system built with **Streamlit** and **LangGraph** that uses AI agents to extract structured data from invoice images.

## ✨ Features

- **🤖 Pure Agentic Architecture**: Built with LangGraph for intelligent, multi-step invoice processing
- **🔍 OCR Integration**: Uses EasyOCR for text extraction from invoice images
- **🧠 AI-Powered Processing**: GPT models clean OCR text and extract structured data
- **✅ Validation**: Automatic validation of extracted invoice data
- **💾 SQLite Database**: Persistent storage of processed invoices
- **📊 Analytics Dashboard**: Visual insights into processed invoices
- **🎨 Beautiful UI**: Modern Streamlit interface with real-time processing feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd invoice_generator
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv invoice-env
source invoice-env/bin/activate  # On Windows: invoice-env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it directly:
```bash
export OPENAI_API_KEY=your_openai_api_key_here  # On Windows: set OPENAI_API_KEY=your_key
```

5. **Run the Streamlit app:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### Processing Invoices

1. **Upload an Invoice**: 
   - Go to the "Upload & Process" tab
   - Click "Choose an invoice image" and select a PNG/JPG file
   - Click "🚀 Process Invoice"

2. **View Results**:
   - See extracted data (vendor, invoice number, date, total, etc.)
   - Check processing steps status
   - View validation results
   - Inspect cleaned text and raw processing data

3. **Browse Invoices**:
   - Go to "View Invoices" tab
   - See all processed invoices in a table
   - Select an invoice to view detailed information
   - Delete invoices if needed

4. **Analytics**:
   - Go to "Analytics" tab
   - View statistics and charts
   - See trends and insights

## 🏗️ Architecture

### Agentic Workflow

The system uses LangGraph to create an agentic pipeline:

```
OCR Text → Clean Text → Extract Data → Validate → Format Output
```

Each step is handled by a specialized agent node:

1. **Clean OCR Node**: Fixes OCR errors and normalizes text
2. **Extract Data Node**: Extracts structured JSON from cleaned text
3. **Validate Node**: Validates extracted data for completeness
4. **Format Output Node**: Prepares final output

### Project Structure

```
invoice_generator/
├── app.py                 # Streamlit UI application
├── agents/
│   └── invoice_agent.py   # LangGraph agent implementation
├── utils/
│   ├── ocr.py            # OCR utilities (EasyOCR)
│   └── database.py       # SQLite database operations
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── invoice.db            # SQLite database (created automatically)
```

## 🔧 Configuration

### Model Selection

You can change the AI model in the Streamlit sidebar:
- `gpt-4o-mini` (default, fast and cost-effective)
- `gpt-4o` (more accurate, slower)
- `gpt-3.5-turbo` (fastest, less accurate)

### Database

The SQLite database (`invoice.db`) is created automatically. It stores:
- Invoice metadata (vendor, number, date, total, currency)
- Extracted JSON data
- Validation status and errors
- Processing timestamps

## 🎯 Key Components

### InvoiceProcessingAgent

The core agent class that orchestrates the LangGraph workflow:

```python
from agents.invoice_agent import InvoiceProcessingAgent

agent = InvoiceProcessingAgent(model_name="gpt-4o-mini")
result = agent.process(file_name="invoice.png", ocr_text="...")
```

### OCRReader

EasyOCR wrapper for text extraction:

```python
from utils.ocr import OCRReader

reader = OCRReader()
text = reader.read_text("invoice.png")
```

### InvoiceDB

Database operations for invoice storage:

```python
from utils.database import InvoiceDB

db = InvoiceDB()
row_id = db.insert_invoice(file_name, data, raw_json)
invoices = db.get_all_invoices()
```

## 📊 Example Output

The agent extracts structured data like:

```json
{
  "vendor": "Tech Solutions Ltd.",
  "number": "INV-1001",
  "date": "2025-09-10",
  "total": 553.88,
  "currency": "EUR",
  "line_items": [
    {
      "description": "Software License",
      "quantity": 1,
      "unit_price": 469.39,
      "amount": 469.39
    }
  ]
}
```

## 🛠️ Troubleshooting

### OCR Issues
- Ensure images are clear and readable
- Supported formats: PNG, JPG, JPEG
- First run may take longer as EasyOCR downloads models

### API Issues
- Verify your OpenAI API key is set correctly
- Check your API quota and billing
- Try a different model if one fails

### Database Issues
- Delete `invoice.db` to reset the database
- Check file permissions in the project directory

## 🚧 Future Enhancements

- [ ] Batch processing of multiple invoices
- [ ] Export to CSV/Excel
- [ ] Multi-language support
- [ ] Custom validation rules
- [ ] Webhook notifications
- [ ] Cloud storage integration

## 📝 License

This project is open source and available for demonstration purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project!

---

**Built with ❤️ using Streamlit, LangGraph, and OpenAI**
