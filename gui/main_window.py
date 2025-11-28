import tkinter as tk
from tkinter import ttk, messagebox

from gui.utils.api_client import ApiClient
from gui.views.dieta_view import DietaView
from gui.views.refeicao_view import RefeicaoView
from gui.views.exercicio_view import ExercicioView


class MainWindow:    
    def __init__(self, api_url: str = 'http://localhost:5000/api'):
        self._api_url = api_url
        self._api_client = ApiClient(api_url)
        
        # Create main window
        self._root = tk.Tk()
        self._root.title("Sistema de Gerenciamento de Dietas")
        self._root.geometry("1000x600")
        self._root.minsize(800, 500)
        
        # Setup UI
        self._setup_menu()
        self._setup_main_content()
        self._setup_status_bar()
        
        # Check API connection
        self._check_connection()
    
    def _setup_menu(self):
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Verificar Conexão", command=self._check_connection)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self._on_exit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self._show_about)
    
    def _setup_main_content(self):
        # Create notebook (tabbed interface)
        self._notebook = ttk.Notebook(self._root)
        self._notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self._dieta_view = DietaView(self._notebook, self._api_client)
        self._refeicao_view = RefeicaoView(self._notebook, self._api_client)
        self._exercicio_view = ExercicioView(self._notebook, self._api_client)
        
        # Add tabs to notebook
        self._notebook.add(self._dieta_view, text="Dietas")
        self._notebook.add(self._refeicao_view, text="Refeições")
        self._notebook.add(self._exercicio_view, text="Exercícios")
    
    def _setup_status_bar(self):
        status_frame = ttk.Frame(self._root)
        status_frame.pack(fill='x', side='bottom')
        
        self._status_label = ttk.Label(status_frame, text="Verificando conexão...", relief='sunken')
        self._status_label.pack(fill='x', padx=2, pady=2)
    
    def _check_connection(self):
        connected, error = self._api_client.check_connection()
        
        if connected:
            self._status_label.config(text=f"✓ Conectado à API: {self._api_url}")
            self._status_label.config(foreground='green')
        else:
            self._status_label.config(text=f"✗ Desconectado: {error}")
            self._status_label.config(foreground='red')
            messagebox.showwarning(
                "Conexão",
                f"Não foi possível conectar à API.\n\nErro: {error}\n\n"
                "Verifique se o servidor está rodando."
            )
    
    def _show_about(self):
        messagebox.showinfo(
            "Sobre",
            "Sistema de Gerenciamento de Dietas\n\n"
            "Versão: 1.0.0\n\n"
            "Desenvolvido com Python, Flask e Tkinter.\n\n"
            "Funcionalidades:\n"
            "• Gerenciamento de Dietas\n"
            "• Gerenciamento de Refeições\n"
            "• Gerenciamento de Exercícios"
        )
    
    def _on_exit(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self._root.quit()
    
    def run(self):
        self._root.mainloop()


def main():
    app = MainWindow()
    app.run()


if __name__ == '__main__':
    main()
