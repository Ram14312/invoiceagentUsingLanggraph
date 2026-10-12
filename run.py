"""
Quick start script for the Invoice Processor
"""
import os
import sys
import subprocess

def check_env():
    """Check if OpenAI API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment")
        print("   Please set it using:")
        print("   - Windows: set OPENAI_API_KEY=your_key")
        print("   - Linux/Mac: export OPENAI_API_KEY=your_key")
        print("   - Or create a .env file with: OPENAI_API_KEY=your_key")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("✅ OPENAI_API_KEY found")

def main():
    """Run the Streamlit app"""
    print("🚀 Starting Agentic Invoice Processor...")
    print()
    check_env()
    print()
    print("📱 Opening Streamlit app in your browser...")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main()
