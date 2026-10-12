"""
Streamlit UI for Agentic Invoice Processing
"""
import streamlit as st
import os
import json
from pathlib import Path
from PIL import Image
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

from agents.invoice_agent import InvoiceProcessingAgent
from utils.ocr import OCRReader
from utils.database import InvoiceDB

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY not found! Please set it in your environment or .env file.")
    st.stop()

# Page configuration - Force light theme
st.set_page_config(
    page_title="🤖 Agentic Invoice Processor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and text visibility - FORCE LIGHT MODE
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Override dark theme */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Force all text to be dark and visible */
    * {
        color: #1f2937 !important;
    }
    
    /* Text visibility improvements - OVERRIDE EVERYTHING */
    .stText, .stMarkdown, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Text area styling for better readability */
    .text-display-box {
        background-color: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.6;
        color: #111827 !important;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* OCR text display */
    .ocr-text-box {
        background-color: #f9fafb;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: #1f2937 !important;
        white-space: pre-wrap;
    }
    
    /* Cleaned text display */
    .cleaned-text-box {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.8;
        color: #1f2937 !important;
        white-space: pre-wrap;
    }
    
    /* Metric cards */
    .stMetric {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        color: #6b7280 !important;
        font-weight: 500;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Processing steps */
    .processing-step {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        font-size: 16px;
        color: #1f2937 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Data cards */
    .data-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Better visibility for all text elements */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background-color: #f9fafb !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    
    /* Selectbox and inputs */
    .stSelectbox label,
    .stTextInput label,
    .stFileUploader label {
        color: #1f2937 !important;
        font-weight: 600;
    }
    
    /* All Streamlit text elements */
    [data-testid="stMarkdownContainer"] {
        color: #1f2937 !important;
    }
    
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] div,
    [data-testid="stMarkdownContainer"] span {
        color: #1f2937 !important;
    }
    
    /* Code blocks and JSON - FORCE VISIBLE */
    .stJson {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px;
        padding: 1rem !important;
    }
    
    .stJson pre {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb !important;
    }
    
    .stJson code {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        padding: 0.25rem 0.5rem !important;
        border-radius: 4px !important;
    }
    
    /* JSON viewer specific */
    [data-testid="stJson"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    [data-testid="stJson"] pre {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
    }
    
    code {
        background-color: #f9fafb !important;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 0.2rem 0.4rem;
    }
    
    /* Expander styling - FORCE VISIBLE */
    .streamlit-expanderHeader {
        color: #111827 !important;
        font-weight: 600;
        background-color: #f9fafb !important;
        padding: 0.75rem;
        border-radius: 4px;
        border: 1px solid #e5e7eb !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        padding: 1rem;
        color: #1f2937 !important;
    }
    
    /* Ensure all text in expanders is visible */
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent code,
    .streamlit-expanderContent pre {
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }
    
    /* Success/Warning/Info boxes */
    .stSuccess {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        border: 1px solid #10b981 !important;
    }
    
    .stSuccess p, .stSuccess div, .stSuccess span {
        color: #065f46 !important;
    }
    
    .stWarning {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        border: 1px solid #f59e0b !important;
    }
    
    .stWarning p, .stWarning div, .stWarning span {
        color: #92400e !important;
    }
    
    .stInfo {
        background-color: #dbeafe !important;
        color: #1e40af !important;
        border: 1px solid #3b82f6 !important;
    }
    
    .stInfo p, .stInfo div, .stInfo span {
        color: #1e40af !important;
    }
    
    /* Button improvements */
    .stButton > button {
        font-weight: 600;
        border-radius: 8px;
    }
    
    /* Table improvements */
    .dataframe {
        background-color: #ffffff !important;
    }
    
    .dataframe th {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
        font-weight: 600;
    }
    
    .dataframe td {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "ocr_reader" not in st.session_state:
    st.session_state.ocr_reader = OCRReader()
if "agent" not in st.session_state:
    st.session_state.agent = InvoiceProcessingAgent()
if "db" not in st.session_state:
    st.session_state.db = InvoiceDB()
if "processing_history" not in st.session_state:
    st.session_state.processing_history = []


def process_invoice(uploaded_file) -> dict:
    """Process a single invoice file"""
    # Save uploaded file temporarily
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Step 1: OCR
        with st.spinner("🔍 Extracting text with OCR..."):
            ocr_text = st.session_state.ocr_reader.read_text(temp_path)
        
        # Step 2: Agentic processing
        with st.spinner("🤖 Processing with AI agent..."):
            result = st.session_state.agent.process(
                file_name=uploaded_file.name,
                ocr_text=ocr_text
            )
        
        # Step 3: Save to database
        with st.spinner("💾 Saving to database..."):
            row_id = st.session_state.db.insert_invoice(
                file_name=uploaded_file.name,
                data=result["extracted_data"],
                raw_json=result,
                validation_status=result["validation_status"],
                errors=result.get("errors", [])
            )
            result["db_id"] = row_id
        
        return result
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🤖 Agentic Invoice Processor</h1>', unsafe_allow_html=True)
    st.markdown("**AI-powered invoice extraction using LangGraph agents**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model = st.selectbox(
            "AI Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0
        )
        
        # Check if model changed (reinitialize if needed)
        try:
            current_model = getattr(st.session_state.agent.llm, 'model_name', None)
            if not current_model:
                current_model = getattr(st.session_state.agent.llm, 'model', None)
            if model != current_model:
                st.session_state.agent = InvoiceProcessingAgent(model_name=model)
        except:
            # If agent not properly initialized, create new one
            st.session_state.agent = InvoiceProcessingAgent(model_name=model)
        
        st.divider()
        
        # Database stats
        st.subheader("📊 Statistics")
        stats = st.session_state.db.get_stats()
        st.metric("Total Invoices", stats["total_invoices"])
        st.metric("Valid Invoices", stats["valid_invoices"])
        if stats["total_amount"] > 0:
            st.metric("Total Amount", f"${stats['total_amount']:,.2f}")
            st.metric("Average Amount", f"${stats['average_amount']:,.2f}")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📋 View Invoices", "📊 Analytics"])
    
    with tab1:
        st.header("📤 Upload Invoice")
        st.markdown("Upload an invoice image (PNG, JPG, or JPEG) to extract structured data using AI agents.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose an invoice image",
                type=["png", "jpg", "jpeg"],
                help="Upload an invoice image to process. Supported formats: PNG, JPG, JPEG"
            )
            
            if uploaded_file is not None:
                st.info(f"📄 **File selected:** {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        with col2:
            if uploaded_file is not None:
                st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
            else:
                st.info("👆 Upload an invoice image to get started")
        
        if uploaded_file is not None:
            if st.button("🚀 Process Invoice", type="primary", use_container_width=True):
                with st.container():
                    result = process_invoice(uploaded_file)
                    st.session_state.processing_history.append(result)
                    
                    # Display results with better visibility
                    st.success("✅ **Invoice processed successfully!** All agentic steps completed.")
                    st.balloons()  # Celebration!
                    
                    # Show extracted data with better visibility
                    st.subheader("📄 Extracted Data")
                    
                    data = result["extracted_data"]
                    
                    # Main metrics in a card-like layout
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        vendor = data.get("vendor", "N/A") or "N/A"
                        st.metric("Vendor", vendor[:30] + "..." if len(str(vendor)) > 30 else vendor)
                    with col2:
                        invoice_num = data.get("number", "N/A") or "N/A"
                        st.metric("Invoice #", invoice_num)
                    with col3:
                        date = data.get("date", "N/A") or "N/A"
                        st.metric("Date", date)
                    with col4:
                        currency = data.get("currency", "")
                        total = data.get("total", 0)
                        total_display = f"{currency} {total:,.2f}" if total else "N/A"
                        st.metric("Total", total_display)
                    
                    # Show line items if available
                    if data.get("line_items") and len(data.get("line_items", [])) > 0:
                        st.subheader("📦 Line Items")
                        line_items_df = pd.DataFrame(data["line_items"])
                        st.dataframe(line_items_df, use_container_width=True, hide_index=True)
                    
                    # Show processing steps with better styling
                    st.subheader("🔄 Processing Steps")
                    steps = [
                        ("OCR Extraction", "✅", result.get("ocr_text", "")),
                        ("Text Cleaning", "✅", result.get("clean_text", "")),
                        ("Data Extraction", "✅", result.get("extracted_data", {})),
                        ("Validation", "✅" if result["validation_status"] == "valid" else "⚠️", result["validation_status"]),
                    ]
                    
                    for step_name, status, data in steps:
                        has_data = bool(data) if data else False
                        status_icon = status if has_data else "❌"
                        st.markdown(f'<div class="processing-step">{status_icon} <strong>{step_name}</strong></div>', unsafe_allow_html=True)
                    
                    # Show validation status with better visibility
                    st.subheader("✅ Validation Status")
                    if result.get("errors"):
                        error_text = ', '.join(result['errors']) if isinstance(result['errors'], list) else str(result['errors'])
                        st.warning(f"⚠️ **Validation Warnings:** {error_text}")
                    else:
                        st.success("✅ **All validations passed!** Invoice data is complete and valid.")
                    
                    # Show OCR text
                    with st.expander("🔍 View OCR Extracted Text", expanded=False):
                        ocr_text = result.get("ocr_text", "")
                        st.markdown(f'<div class="ocr-text-box">{ocr_text}</div>', unsafe_allow_html=True)
                    
                    # Show cleaned text
                    with st.expander("📝 View AI-Cleaned Text", expanded=False):
                        clean_text = result.get("clean_text", "")
                        st.markdown(f'<div class="cleaned-text-box">{clean_text}</div>', unsafe_allow_html=True)
                    
                    # Show extracted JSON
                    with st.expander("📊 View Extracted JSON Data", expanded=False):
                        st.json(result.get("extracted_data", {}))
                    
                    # Show full processing result
                    with st.expander("🔧 View Full Processing Data", expanded=False):
                        st.json(result)
    
    with tab2:
        st.header("Processed Invoices")
        
        # Refresh button
        if st.button("🔄 Refresh", use_container_width=False):
            st.rerun()
        
        invoices = st.session_state.db.get_all_invoices(limit=100)
        
        if invoices:
            # Convert to DataFrame
            df = pd.DataFrame(invoices)
            
            # Format columns
            display_df = df[["id", "file_name", "vendor", "number", "date", "total", "currency", "validation_status", "created_at"]].copy()
            display_df.columns = ["ID", "File", "Vendor", "Invoice #", "Date", "Total", "Currency", "Status", "Created"]
            
            # Format dates
            if "Created" in display_df.columns:
                display_df["Created"] = pd.to_datetime(display_df["Created"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # Format totals
            if "Total" in display_df.columns:
                display_df["Total"] = display_df.apply(
                    lambda row: f"{row['Currency']} {row['Total']:,.2f}" if pd.notna(row['Total']) else "N/A",
                    axis=1
                )
                display_df = display_df.drop("Currency", axis=1)
            
            # Status badges
            def format_status(status):
                if status == "valid":
                    return "✅ Valid"
                elif status == "warning":
                    return "⚠️ Warning"
                else:
                    return "❌ Invalid"
            
            display_df["Status"] = display_df["Status"].apply(format_status)
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Detail view
            st.subheader("📄 Invoice Details")
            selected_id = st.selectbox(
                "Select invoice ID to view details",
                options=df["id"].tolist(),
                format_func=lambda x: f"Invoice #{x}"
            )
            
            if selected_id:
                invoice = st.session_state.db.get_invoice_by_id(selected_id)
                if invoice:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Invoice Information:**")
                        invoice_info = {
                            "Vendor": invoice.get("vendor"),
                            "Invoice Number": invoice.get("number"),
                            "Date": invoice.get("date"),
                            "Total": invoice.get("total"),
                            "Currency": invoice.get("currency"),
                            "Status": invoice.get("validation_status"),
                        }
                        # Display in a styled box
                        st.markdown(f"""
                        <div style="background-color: #f9fafb; border: 2px solid #3b82f6; border-radius: 8px; padding: 1.5rem; margin: 1rem 0;">
                            <pre style="color: #1f2937; font-family: 'Courier New', monospace; font-size: 14px; margin: 0; white-space: pre-wrap;">{json.dumps(invoice_info, indent=2, ensure_ascii=False)}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        errors = json.loads(invoice.get("errors", "[]"))
                        if errors:
                            st.markdown("**Validation Issues:**")
                            error_text = "\n".join([f"• {error}" for error in errors])
                            st.markdown(f"""
                            <div style="background-color: #fef3c7; border: 2px solid #f59e0b; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                                <p style="color: #92400e; font-weight: 600; margin: 0;">⚠️ Validation Warnings:</p>
                                <p style="color: #92400e; margin: 0.5rem 0 0 0;">{error_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="background-color: #d1fae5; border: 2px solid #10b981; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                                <p style="color: #065f46; font-weight: 600; margin: 0;">✅ No validation issues</p>
                                <p style="color: #065f46; margin: 0.5rem 0 0 0;">All invoice data is valid and complete.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Full JSON", expanded=False):
                        try:
                            raw_json = json.loads(invoice.get("raw_json", "{}"))
                            st.json(raw_json)
                        except:
                            st.text(str(invoice.get("raw_json", "{}")))
                    
                    # Show extracted text if available
                    with st.expander("📝 View Extracted Text", expanded=False):
                        try:
                            raw_json_data = json.loads(invoice.get("raw_json", "{}"))
                            if isinstance(raw_json_data, dict):
                                clean_text = raw_json_data.get("clean_text", "")
                                if clean_text:
                                    st.markdown(f'<div class="cleaned-text-box">{clean_text}</div>', unsafe_allow_html=True)
                                else:
                                    st.info("No cleaned text available for this invoice.")
                            else:
                                st.info("No text data available.")
                        except:
                            st.info("Unable to display text data.")
                    
                    if st.button("🗑️ Delete Invoice", key=f"delete_{selected_id}"):
                        if st.session_state.db.delete_invoice(selected_id):
                            st.success("Invoice deleted!")
                            st.rerun()
        else:
            st.info("No invoices processed yet. Upload an invoice to get started!")
    
    with tab3:
        st.header("📊 Analytics Dashboard")
        
        invoices = st.session_state.db.get_all_invoices(limit=1000)
        
        if invoices:
            df = pd.DataFrame(invoices)
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Invoices", len(df))
            
            with col2:
                valid_count = len(df[df["validation_status"] == "valid"])
                st.metric("Valid Invoices", valid_count)
            
            with col3:
                total_amount = df["total"].sum() if "total" in df.columns else 0
                st.metric("Total Amount", f"${total_amount:,.2f}" if total_amount > 0 else "N/A")
            
            with col4:
                avg_amount = df["total"].mean() if "total" in df.columns and len(df) > 0 else 0
                st.metric("Average Amount", f"${avg_amount:,.2f}" if avg_amount > 0 else "N/A")
            
            st.divider()
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Invoices by Status")
                status_counts = df["validation_status"].value_counts()
                st.bar_chart(status_counts)
            
            with col2:
                st.subheader("💰 Total by Currency")
                if "currency" in df.columns and "total" in df.columns:
                    currency_totals = df.groupby("currency")["total"].sum()
                    st.bar_chart(currency_totals)
            
            # Top vendors
            st.subheader("🏢 Top Vendors")
            if "vendor" in df.columns:
                vendor_counts = df["vendor"].value_counts().head(10)
                st.bar_chart(vendor_counts)
            
            # Time series
            st.subheader("📅 Processing Timeline")
            if "created_at" in df.columns:
                df["created_at"] = pd.to_datetime(df["created_at"])
                df["date"] = df["created_at"].dt.date
                daily_counts = df.groupby("date").size()
                st.line_chart(daily_counts)
        else:
            st.info("No data available. Process some invoices to see analytics!")


if __name__ == "__main__":
    main()
