#!/usr/bin/env python3
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow


def main():
    # Get API URL from environment or use default
    api_url = os.environ.get('API_URL', 'http://localhost:5000/api')
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║    Sistema de Gerenciamento de Dietas - Interface GUI    ║
╠══════════════════════════════════════════════════════════╣
║  Conectando à API: {api_url:<37} ║
║                                                          ║
║  Certifique-se de que o servidor API está rodando!       ║
║  Execute: python run_api.py                              ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Create and run the main window
    app = MainWindow(api_url)
    app.run()


if __name__ == '__main__':
    main()
