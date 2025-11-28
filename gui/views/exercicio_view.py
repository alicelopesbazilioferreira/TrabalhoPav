import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
class ExercicioView(ttk.Frame):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self._api_client = api_client
        self._selected_id: Optional[int] = None
        self._dietas_cache = []
        
        self._setup_ui()
        self._load_dietas()
        self._load_exercicios()
    
    def _setup_ui(self):
        """Setup the user interface components."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        
        # Left panel - List
        self._setup_list_panel()
        
        # Right panel - Form
        self._setup_form_panel()
    
    def _setup_list_panel(self):
        """Setup the list panel with treeview."""
        list_frame = ttk.LabelFrame(self, text="Lista de Exercícios", padding=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for listing exercises
        columns = ('id', 'tipo', 'repeticoes', 'ciclos', 'pausa', 'dieta')
        self._tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Define columns
        self._tree.heading('id', text='ID')
        self._tree.heading('tipo', text='Tipo')
        self._tree.heading('repeticoes', text='Repetições')
        self._tree.heading('ciclos', text='Ciclos')
        self._tree.heading('pausa', text='Pausa (s)')
        self._tree.heading('dieta', text='Dieta ID')
        
        self._tree.column('id', width=40, anchor='center')
        self._tree.column('tipo', width=100)
        self._tree.column('repeticoes', width=70, anchor='center')
        self._tree.column('ciclos', width=50, anchor='center')
        self._tree.column('pausa', width=60, anchor='center')
        self._tree.column('dieta', width=60, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        self._tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind selection event
        self._tree.bind('<<TreeviewSelect>>', self._on_select)
        
        # Buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Atualizar", command=self._load_exercicios).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Novo", command=self._new_exercicio).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Excluir", command=self._delete_exercicio).pack(side='left', padx=2)
    
    def _setup_form_panel(self):
        """Setup the form panel for CRUD operations."""
        form_frame = ttk.LabelFrame(self, text="Detalhes do Exercício", padding=10)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        form_frame.columnconfigure(1, weight=1)
        
        # Tipo Exercício field
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self._tipo_var = tk.StringVar()
        self._tipo_entry = ttk.Entry(form_frame, textvariable=self._tipo_var, width=30)
        self._tipo_entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # Quantidade Repetições field
        ttk.Label(form_frame, text="Repetições:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self._repeticoes_var = tk.StringVar()
        self._repeticoes_entry = ttk.Entry(form_frame, textvariable=self._repeticoes_var, width=15)
        self._repeticoes_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Ciclos field
        ttk.Label(form_frame, text="Ciclos:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self._ciclos_var = tk.StringVar()
        self._ciclos_entry = ttk.Entry(form_frame, textvariable=self._ciclos_var, width=15)
        self._ciclos_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        ttk.Label(form_frame, text="(não pode ser negativo)", font=('Arial', 8)).grid(row=2, column=2, sticky='w')
        
        # Pausa entre ciclos field
        ttk.Label(form_frame, text="Pausa (segundos):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self._pausa_var = tk.StringVar()
        self._pausa_entry = ttk.Entry(form_frame, textvariable=self._pausa_var, width=15) 
        self._pausa_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5) 
        
        # Dieta field (dropdown)
        ttk.Label(form_frame, text="Dieta:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self._dieta_var = tk.StringVar()
        self._dieta_combo = ttk.Combobox(form_frame, textvariable=self._dieta_var, width=25)
        self._dieta_combo.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self._save_exercicio).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._clear_form).pack(side='left', padx=5)
    
    def _load_dietas(self):
        """Load diets for dropdown."""
        dietas, error = self._api_client.get_dietas()
        
        if error:
            self._dietas_cache = []
            return
        
        self._dietas_cache = dietas
        # Format: "ID - Meta"
        values = [''] + [f"{d['id']} - {d['meta']}" for d in dietas]
        self._dieta_combo['values'] = values
    
    def _load_exercicios(self):
        """Load and display all exercises."""
        # Clear existing items
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        # Also refresh dietas
        self._load_dietas()
        
        # Fetch exercises from API
        exercicios, error = self._api_client.get_exercicios()
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar exercícios: {error}")
            return
        
        # Populate treeview using loop
        for exercicio in exercicios:
            self._tree.insert('', 'end', values=(
                exercicio.get('id'),
                exercicio.get('tipo_exercicio'),
                exercicio.get('quantidade_repeticoes'),
                exercicio.get('ciclos'),
                exercicio.get('pausa_entre_ciclos'),
                exercicio.get('dieta_id') or '-'
            ))
    
    def _on_select(self, event):
        """Handle treeview selection."""
        selection = self._tree.selection()
        if not selection:
            return
        
        item = self._tree.item(selection[0])
        exercicio_id = item['values'][0]
        
        # Fetch exercise details
        exercicio, error = self._api_client.get_exercicio(exercicio_id)
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar exercício: {error}")
            return
        
        # Fill form
        self._selected_id = exercicio.get('id')
        self._tipo_var.set(exercicio.get('tipo_exercicio', ''))
        self._repeticoes_var.set(str(exercicio.get('quantidade_repeticoes', '')))
        self._ciclos_var.set(str(exercicio.get('ciclos', '')))
        self._pausa_var.set(str(exercicio.get('pausa_entre_ciclos', '')))
        
        # Dieta
        dieta_id = exercicio.get('dieta_id')
        if dieta_id:
            # Find dieta in cache
            for d in self._dietas_cache:
                if d['id'] == dieta_id:
                    self._dieta_var.set(f"{d['id']} - {d['meta']}")
                    break
        else:
            self._dieta_var.set('')
    
    def _new_exercicio(self):
        """Clear form for new exercise."""
        self._clear_form()
        self._tree.selection_remove(self._tree.selection())
    
    def _clear_form(self):
        """Clear all form fields."""
        self._selected_id = None
        self._tipo_var.set('')
        self._repeticoes_var.set('')
        self._ciclos_var.set('')
        self._pausa_var.set('')
        self._dieta_var.set('')
    
    def _save_exercicio(self):
        """Save exercise (create or update)."""
        tipo = self._tipo_var.get().strip()
        repeticoes_str = self._repeticoes_var.get().strip()
        ciclos_str = self._ciclos_var.get().strip()
        pausa_str = self._pausa_var.get().strip()
        dieta_str = self._dieta_var.get().strip()
        
        # Validate tipo
        if not tipo:
            messagebox.showwarning("Validação", "O campo Tipo é obrigatório!")
            return
        
        # Validate repeticoes
        if not repeticoes_str:
            messagebox.showwarning("Validação", "O campo Repetições é obrigatório!")
            return
        
        try:
            repeticoes = int(repeticoes_str)
            if repeticoes < 0:
                messagebox.showwarning("Validação", "O número de repetições não pode ser negativo!")
                return
        except ValueError:
            messagebox.showwarning("Validação", "O número de repetições deve ser um número inteiro!")
            return
        
        # Validate ciclos (Business rule: cannot be negative)
        if not ciclos_str:
            messagebox.showwarning("Validação", "O campo Ciclos é obrigatório!")
            return
        
        try:
            ciclos = int(ciclos_str)
            if ciclos < 0:
                messagebox.showwarning("Validação", "O número de ciclos não pode ser negativo!")
                return
        except ValueError:
            messagebox.showwarning("Validação", "O número de ciclos deve ser um número inteiro!")
            return
        
        # Validate pausa
        if not pausa_str:
            messagebox.showwarning("Validação", "O campo Pausa é obrigatório!")
            return
        
        try:
            pausa = int(pausa_str)
            if pausa < 0:
                messagebox.showwarning("Validação", "A pausa não pode ser negativa!")
                return
        except ValueError:
            messagebox.showwarning("Validação", "A pausa deve ser um número inteiro!")
            return
        
        # Parse dieta_id
        dieta_id = None
        if dieta_str:
            try:
                dieta_id = int(dieta_str.split(' - ')[0])
            except (ValueError, IndexError):
                pass
        
        data = {
            'tipo_exercicio': tipo,
            'quantidade_repeticoes': repeticoes,
            'ciclos': ciclos,
            'pausa_entre_ciclos': pausa,
            'dieta_id': dieta_id
        }
        
        # Create or update based on selection
        if self._selected_id:
            # Update existing
            result, error = self._api_client.update_exercicio(self._selected_id, data)
            action = "atualizado"
        else:
            # Create new
            result, error = self._api_client.create_exercicio(data)
            action = "criado"
        
        if error:
            messagebox.showerror("Erro", f"Erro ao salvar exercício: {error}")
            return
        
        messagebox.showinfo("Sucesso", f"Exercício {action} com sucesso!")
        self._clear_form()
        self._load_exercicios()
    
    def _delete_exercicio(self):
        """Delete selected exercise."""
        if not self._selected_id:
            messagebox.showwarning("Atenção", "Selecione um exercício para excluir!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este exercício?"):
            return
        
        success, error = self._api_client.delete_exercicio(self._selected_id)
        
        if not success:
            messagebox.showerror("Erro", f"Erro ao excluir exercício: {error}")
            return
        
        messagebox.showinfo("Sucesso", "Exercício excluído com sucesso!")
        self._clear_form()
        self._load_exercicios()
