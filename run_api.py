#!/usr/bin/env python3

import os
from app import create_app

# Create the application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    server_url = f"http://{host}:{port}"
    
    print("""
╔══════════════════════════════════════════════════════════╗
║      Sistema de Gerenciamento de Dietas - API REST       ║
╠══════════════════════════════════════════════════════════╣""")
    print(f"║  Servidor iniciando em: {server_url:<33}║")
    print("""║                                                          ║
║  Endpoints disponíveis:                                  ║
║    • GET/POST    /api/dietas                             ║
║    • GET/PUT/DEL /api/dietas/<id>                        ║
║    • GET/POST    /api/refeicoes                          ║
║    • GET/PUT/DEL /api/refeicoes/<id>                     ║
║    • GET/POST    /api/exercicios                         ║
║    • GET/PUT/DEL /api/exercicios/<id>                    ║
║                                                          ║
║  Pressione Ctrl+C para parar o servidor                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Run the application
    app.run(host=host, port=port, debug=debug)
