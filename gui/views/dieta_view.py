import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class DietaView(ttk.Frame):
    def __init__(self, parent, api_client):
        super().__init__(parent)
        self._api_client = api_client
        self._selected_id: Optional[int] = None
        
        self._setup_ui()
        self._load_dietas()
    
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
        list_frame = ttk.LabelFrame(self, text="Lista de Dietas", padding=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for listing diets
        columns = ('id', 'meta', 'refeicoes', 'exercicios')
        self._tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Define columns
        self._tree.heading('id', text='ID')
        self._tree.heading('meta', text='Meta')
        self._tree.heading('refeicoes', text='Refeições')
        self._tree.heading('exercicios', text='Exercícios')
        
        self._tree.column('id', width=50, anchor='center')
        self._tree.column('meta', width=150)
        self._tree.column('refeicoes', width=80, anchor='center')
        self._tree.column('exercicios', width=80, anchor='center')
        
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
        
        ttk.Button(btn_frame, text="Atualizar", command=self._load_dietas).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Novo", command=self._new_dieta).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Excluir", command=self._delete_dieta).pack(side='left', padx=2)
    
    def _setup_form_panel(self):
        """Setup the form panel for CRUD operations."""
        form_frame = ttk.LabelFrame(self, text="Detalhes da Dieta", padding=10)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        form_frame.columnconfigure(1, weight=1)
        
        # Meta field
        ttk.Label(form_frame, text="Meta:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self._meta_var = tk.StringVar()
        self._meta_entry = ttk.Entry(form_frame, textvariable=self._meta_var, width=40)
        self._meta_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Descricao field
        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky='ne', padx=5, pady=5)
        self._descricao_text = tk.Text(form_frame, width=40, height=8)
        self._descricao_text.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        # Dieta field (dropdown)
        ttk.Label(form_frame, text="Dieta:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self._dieta_var = tk.StringVar()
        self._dieta_combo = ttk.Combobox(form_frame, textvariable=self._dieta_var, width=25)
        self._dieta_combo.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salvar", command=self._save_dieta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self._clear_form).pack(side='left', padx=5)
    
    def _load_dietas(self):
        """Load and display all diets."""
        # Clear existing items
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        # Fetch diets from API
        dietas, error = self._api_client.get_dietas()
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar dietas: {error}")
            return
        
        # Populate treeview using loop
        for dieta in dietas:
            self._tree.insert('', 'end', values=(
                dieta.get('id'),
                dieta.get('meta'),
                dieta.get('refeicoes_count', 0),
                dieta.get('exercicios_count', 0)
            ))
    
    def _on_select(self, event):
        """Handle treeview selection."""
        selection = self._tree.selection()
        if not selection:
            return
        
        item = self._tree.item(selection[0])
        dieta_id = item['values'][0]
        
        # Fetch diet details
        dieta, error = self._api_client.get_dieta(dieta_id)
        
        if error:
            messagebox.showerror("Erro", f"Erro ao carregar dieta: {error}")
            return
        
        # Fill form
        self._selected_id = dieta.get('id')
        self._meta_var.set(dieta.get('meta', ''))
        self._descricao_text.delete('1.0', tk.END)
        self._descricao_text.insert('1.0', dieta.get('descricao', '') or '')
    
    def _new_dieta(self):
        """Clear form for new diet."""
        self._clear_form()
        self._tree.selection_remove(self._tree.selection())
    
    def _clear_form(self):
        """Clear all form fields."""
        self._selected_id = None
        self._meta_var.set('')
        self._descricao_text.delete('1.0', tk.END)
    
    def _save_dieta(self):
        """Save diet (create or update)."""
        meta = self._meta_var.get().strip()
        descricao = self._descricao_text.get('1.0', tk.END).strip()
        
        # Validate
        if not meta:
            messagebox.showwarning("Validação", "O campo Meta é obrigatório!")
            return
        
        data = {
            'meta': meta,
            'descricao': descricao if descricao else None
        }
        
        # Create or update based on selection
        if self._selected_id:
            # Update existing
            result, error = self._api_client.update_dieta(self._selected_id, data)
            action = "atualizada"
        else:
            # Create new
            result, error = self._api_client.create_dieta(data)
            action = "criada"
        
        if error:
            messagebox.showerror("Erro", f"Erro ao salvar dieta: {error}")
            return
        
        messagebox.showinfo("Sucesso", f"Dieta {action} com sucesso!")
        self._clear_form()
        self._load_dietas()
    
    def _delete_dieta(self):
        """Delete selected diet."""
        if not self._selected_id:
            messagebox.showwarning("Atenção", "Selecione uma dieta para excluir!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir esta dieta?"):
            return
        
        success, error = self._api_client.delete_dieta(self._selected_id)
        
        if not success:
            messagebox.showerror("Erro", f"Erro ao excluir dieta: {error}")
            return
        
        messagebox.showinfo("Sucesso", "Dieta excluída com sucesso!")
        self._clear_form()
        self._load_dietas()
