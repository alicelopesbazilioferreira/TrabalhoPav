import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
class RefeicaoView(ttk.Frame):
    # Valid meal types
    TIPOS_REFEICAO = [
        'café da manhã',
        'almoço',
        'jantar',
        'lanche',
        'ceia',
        'pré-treino',
        'pós-treino'
    ]
    # Pre-computed lowercase version for validation
    TIPOS_REFEICAO_LOWER = [t.lower() for t in TIPOS_REFEICAO]
    
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self._api_client = api_client
        self._selected_id: Optional[int] = None
        self._dietas_cache = []
        
        self._setup_ui()
        self._load_dietas()
        self._load_refeicoes()
    
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
        list_frame = ttk.LabelFrame(self, text="Lista de Refeições", padding=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for listing meals
        columns = ('id', 'tipo', 'quantidade', 'alimentos', 'dieta')
        self._tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Define columns
        self._tree.heading('id', text='ID')
        self._tree.heading('tipo', text='Tipo')
        self._tree.heading('quantidade', text='Qtd (g/ml)')
        self._tree.heading('alimentos', text='Alimentos')
        self._tree.heading('dieta', text='Dieta ID')
        
        self._tree.column('id', width=40, anchor='center')
        self._tree.column('tipo', width=100)
        self._tree.column('quantidade', width=70, anchor='center')
        self._tree.column('alimentos', width=150)
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
        
        ttk.Button(btn_frame, text="Atualizar", command=self._load_refeicoes).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Novo", command=self._new_refeicao).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Excluir", command=self._delete_refeicao).pack(side='left', padx=2)
    
    def _setup_form_panel(self):
        """Setup the form panel for CRUD operations."""
        form_frame = ttk.LabelFrame(self, text="Detalhes da Refeição", padding=10)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        form_frame.columnconfigure(1, weight=1)
        
        # Tipo Refeição field (dropdown)
        ttk.Label(form_frame, text="Tipo:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self._tipo_var = tk.StringVar()
        self._tipo_combo = ttk.Combobox(form_frame, textvariable=self._tipo_var, values=self.TIPOS_REFEICAO, width=20)
        self._tipo_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # Quantidade field
        ttk.Label(form_frame, text="Quantidade (g/ml):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self._quantidade_var = tk.StringVar()
        self._quantidade_entry = ttk.Entry(form_frame, textvariable=self._quantidade_var, width=15)
        self._quantidade_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Alimentos field
        ttk.Label(form_frame, text="Alimentos:").grid(row=2, column=0, sticky='ne', padx=5, pady=5)
        alimentos_frame = ttk.Frame(form_frame)
        alimentos_frame.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        self._alimentos_text = tk.Text(alimentos_frame, width=30, height=5)
        self._alimentos_text.pack(side='left', fill='both', expand=True)
        ttk.Label(alimentos_frame, text="(um por linha)", font=('Arial', 8)).pack(side='right', padx=5)
        
        # Dieta field (dropdown)
        ttk.Label(form_frame, text="Dieta:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self._dieta_var = tk.StringVar()
        self._dieta_combo = ttk.Combobox(form_frame, textvariable=self._dieta_var, width=25)
        self._dieta_combo.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self._save_refeicao).pack(side='left', padx=5)
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
    
    def _load_refeicoes(self):
        """Load and display all meals."""
        # Clear existing items
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        # Also refresh dietas
        self._load_dietas()
        
        # Fetch meals from API
        refeicoes, error = self._api_client.get_refeicoes()
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar refeições: {error}")
            return
        
        # Populate treeview using loop
        for refeicao in refeicoes:
            alimentos = refeicao.get('alimentos', [])
            alimentos_str = ', '.join(alimentos[:2])
            if len(alimentos) > 2:
                alimentos_str += '...'
            
            self._tree.insert('', 'end', values=(
                refeicao.get('id'),
                refeicao.get('tipo_refeicao'),
                refeicao.get('quantidade'),
                alimentos_str,
                refeicao.get('dieta_id') or '-'
            ))
    
    def _on_select(self, event):
        """Handle treeview selection."""
        selection = self._tree.selection()
        if not selection:
            return
        
        item = self._tree.item(selection[0])
        refeicao_id = item['values'][0]
        
        # Fetch meal details
        refeicao, error = self._api_client.get_refeicao(refeicao_id)
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar refeição: {error}")
            return
        
        # Fill form
        self._selected_id = refeicao.get('id')
        self._tipo_var.set(refeicao.get('tipo_refeicao', ''))
        self._quantidade_var.set(str(refeicao.get('quantidade', '')))
        
        # Alimentos
        self._alimentos_text.delete('1.0', tk.END)
        alimentos = refeicao.get('alimentos', [])
        self._alimentos_text.insert('1.0', '\n'.join(alimentos))
        
        # Dieta
        dieta_id = refeicao.get('dieta_id')
        if dieta_id:
            # Find dieta in cache
            for d in self._dietas_cache:
                if d['id'] == dieta_id:
                    self._dieta_var.set(f"{d['id']} - {d['meta']}")
                    break
        else:
            self._dieta_var.set('')
    
    def _new_refeicao(self):
        """Clear form for new meal."""
        self._clear_form()
        self._tree.selection_remove(self._tree.selection())
    
    def _clear_form(self):
        """Clear all form fields."""
        self._selected_id = None
        self._tipo_var.set('')
        self._quantidade_var.set('')
        self._alimentos_text.delete('1.0', tk.END)
        self._dieta_var.set('')
    
    def _save_refeicao(self):
        """Save meal (create or update)."""
        tipo = self._tipo_var.get().strip()
        quantidade_str = self._quantidade_var.get().strip()
        alimentos_raw = self._alimentos_text.get('1.0', tk.END).strip()
        dieta_str = self._dieta_var.get().strip()
        
        # Validate tipo
        if not tipo:
            messagebox.showwarning("Validação", "O campo Tipo é obrigatório!")
            return
        
        if tipo.lower() not in self.TIPOS_REFEICAO_LOWER:
            messagebox.showwarning("Validação", f"Tipo de refeição inválido!\nTipos válidos: {', '.join(self.TIPOS_REFEICAO)}")
            return
        
        # Validate quantidade
        if not quantidade_str:
            messagebox.showwarning("Validação", "O campo Quantidade é obrigatório!")
            return
        
        try:
            quantidade = int(quantidade_str)
            if quantidade < 0:
                messagebox.showwarning("Validação", "A quantidade não pode ser negativa!")
                return
        except ValueError:
            messagebox.showwarning("Validação", "A quantidade deve ser um número inteiro!")
            return
        
        # Parse alimentos
        alimentos = [a.strip() for a in alimentos_raw.split('\n') if a.strip()]
        if not alimentos:
            messagebox.showwarning("Validação", "Informe pelo menos um alimento!")
            return
        
        # Parse dieta_id
        dieta_id = None
        if dieta_str:
            try:
                dieta_id = int(dieta_str.split(' - ')[0])
            except (ValueError, IndexError):
                pass
        
        data = {
            'tipo_refeicao': tipo,
            'quantidade': quantidade,
            'alimentos': alimentos,
            'dieta_id': dieta_id
        }
        
        # Create or update based on selection
        if self._selected_id:
            # Update existing
            result, error = self._api_client.update_refeicao(self._selected_id, data)
            action = "atualizada"
        else:
            # Create new
            result, error = self._api_client.create_refeicao(data)
            action = "criada"
        
        if error:
            messagebox.showerror("Erro", f"Erro ao salvar refeição: {error}")
            return
        
        messagebox.showinfo("Sucesso", f"Refeição {action} com sucesso!")
        self._clear_form()
        self._load_refeicoes()
    
    def _delete_refeicao(self):
        """Delete selected meal."""
        if not self._selected_id:
            messagebox.showwarning("Atenção", "Selecione uma refeição para excluir!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir esta refeição?"):
            return
        
        success, error = self._api_client.delete_refeicao(self._selected_id)
        
        if not success:
            messagebox.showerror("Erro", f"Erro ao excluir refeição: {error}")
            return
        
        messagebox.showinfo("Sucesso", "Refeição excluída com sucesso!")
        self._clear_form()
        self._load_refeicoes()
