"""
COGNIX AI - Server Startup Script
"""

import uvicorn
import sys
import os

# Change to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting COGNIX AI Backend Server")
    print("=" * 60)
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[0]}")
    print()
    print("Server will be available at:")
    print("   http://localhost:8000")
    print("   http://localhost:8000/docs (Swagger UI)")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
