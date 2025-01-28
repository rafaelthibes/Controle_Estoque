import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

class InventoryControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Estoque")

        self.products = {}

        # Carregar produtos do arquivo CSV, se existir
        self.load_products()

        # Frame principal com margem de 2 cm nos 4 lados
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill='both', expand=True)

        # Frame para adicionar números de série
        self.add_serial_group = tk.LabelFrame(self.main_frame, text="Adicionar número de série", bg="#f0f0f0", padx=10, pady=10)
        self.add_serial_group.pack(pady=10, fill='x')

        # Frame para selecionar produtos cadastrados
        self.select_product_frame = tk.Frame(self.add_serial_group, bg="#f0f0f0")
        self.select_product_frame.grid(row=0, column=0, padx=5, pady=5)

        self.select_product_label = tk.Label(self.select_product_frame, text="Produto:", bg="#f0f0f0")
        self.select_product_label.grid(row=0, column=0, padx=5)

        self.selected_product = tk.StringVar()
        self.product_combobox = ttk.Combobox(self.select_product_frame, textvariable=self.selected_product)
        self.product_combobox['values'] = list(self.products.keys())
        self.product_combobox.grid(row=0, column=1, padx=5)
        self.product_combobox.bind("<<ComboboxSelected>>", self.update_model_combobox)

        # Frame para selecionar modelos cadastrados
        self.select_model_frame = tk.Frame(self.add_serial_group, bg="#f0f0f0")
        self.select_model_frame.grid(row=0, column=1, padx=5, pady=5)

        self.select_model_label = tk.Label(self.select_model_frame, text="Modelo:", bg="#f0f0f0")
        self.select_model_label.grid(row=0, column=0, padx=5)

        self.selected_model = tk.StringVar()
        self.model_combobox = ttk.Combobox(self.select_model_frame, textvariable=self.selected_model)
        self.model_combobox.grid(row=0, column=1, padx=5)

        # Frame para adicionar números de série
        self.add_serial_frame = tk.Frame(self.add_serial_group, bg="#f0f0f0")
        self.add_serial_frame.grid(row=0, column=2, padx=5, pady=5)

        self.serial_label = tk.Label(self.add_serial_frame, text="Num Serie:", bg="#f0f0f0")
        self.serial_label.grid(row=0, column=0, padx=5)

        self.serial_entry = tk.Entry(self.add_serial_frame)
        self.serial_entry.grid(row=0, column=1, padx=5)

        self.add_serial_button = tk.Button(self.add_serial_frame, text="Adicionar", command=self.add_serial_number)
        self.add_serial_button.grid(row=0, column=2, padx=5)

        self.remove_serial_button = tk.Button(self.add_serial_frame, text="Remover", command=self.remove_serial_number)
        self.remove_serial_button.grid(row=0, column=3, padx=5)

        # Frame para cadastrar novos produtos
        self.register_product_frame = tk.Frame(self.main_frame)
        self.register_product_frame.pack(pady=10, anchor='w', fill='x')

        self.register_product_button = tk.Button(self.register_product_frame, text="Cadastrar Produto", command=self.show_register_product_fields)
        self.register_product_button.grid(row=0, column=0, padx=5)

        # Botão Home para exibir todos os produtos e números de série
        self.home_button = tk.Button(self.register_product_frame, text="Home", command=self.display_all_products)
        self.home_button.grid(row=0, column=1, padx=5)

        # Botão Exportar para exportar os produtos mostrados
        self.export_button = tk.Button(self.register_product_frame, text="Exportar", command=self.export_products)
        self.export_button.grid(row=0, column=2, padx=5)

        # Frame para pesquisar produtos e números de série
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(pady=10, anchor='e', fill='x')

        self.search_label = tk.Label(self.search_frame, text="Pesquisar:")
        self.search_label.grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Pesquisar", command=self.search)
        self.search_button.grid(row=0, column=2, padx=5)

        # Frame para adicionar novos produtos (inicialmente oculto)
        self.add_product_frame = tk.Frame(self.main_frame)

        self.product_label = tk.Label(self.add_product_frame, text="Produto:")
        self.product_label.grid(row=0, column=0, padx=5)

        self.product_entry = tk.Entry(self.add_product_frame)
        self.product_entry.grid(row=0, column=1, padx=5)

        self.model_label = tk.Label(self.add_product_frame, text="Modelo:")
        self.model_label.grid(row=1, column=0, padx=5)

        self.model_entry = tk.Entry(self.add_product_frame)
        self.model_entry.grid(row=1, column=1, padx=5)

        self.add_product_button = tk.Button(self.add_product_frame, text="Adicionar", command=self.add_product)
        self.add_product_button.grid(row=2, column=0, padx=5)

        self.remove_product_button = tk.Button(self.add_product_frame, text="Remover", command=self.remove_product)
        self.remove_product_button.grid(row=2, column=1, padx=5)

        # Frame para exibir resultados com barras de rolagem
        self.result_frame = tk.Frame(self.main_frame)
        self.result_frame.pack(pady=10, fill='both', expand=True)

        self.result_canvas = tk.Canvas(self.result_frame)
        self.result_canvas.pack(side=tk.LEFT, fill='both', expand=True)

        self.result_scrollbar_y = tk.Scrollbar(self.result_frame, orient="vertical", command=self.result_canvas.yview)
        self.result_scrollbar_y.pack(side=tk.RIGHT, fill='y')

        self.result_scrollbar_x = tk.Scrollbar(self.result_frame, orient="horizontal", command=self.result_canvas.xview)
        self.result_scrollbar_x.pack(side=tk.BOTTOM, fill='x')

        self.result_canvas.configure(yscrollcommand=self.result_scrollbar_y.set, xscrollcommand=self.result_scrollbar_x.set)

        self.result_inner_frame = tk.Frame(self.result_canvas)
        self.result_canvas.create_window((0, 0), window=self.result_inner_frame, anchor='nw')

        self.result_inner_frame.bind("<Configure>", lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all")))

        # Exibir todos os produtos ao iniciar
        self.display_all_products()

    def show_register_product_fields(self):
        self.add_product_frame.pack(pady=10, anchor='w')

    def update_model_combobox(self, event):
        product = self.selected_product.get()
        if product in self.products:
            models = list(self.products[product].keys())
            self.model_combobox['values'] = models
        else:
            self.model_combobox['values'] = []

    def add_product(self):
        product = self.product_entry.get()
        model = self.model_entry.get()
        if product:
            if product not in self.products:
                self.products[product] = {}
            if model:
                if model not in self.products[product]:
                    self.products[product][model] = []
                messagebox.showinfo("Sucesso", f"Produto '{product}' com modelo '{model}' adicionado com sucesso!")
                # Atualizar a lista de produtos no combobox
                self.product_combobox['values'] = list(self.products.keys())
                # Salvar produtos no arquivo CSV
                self.save_products()
                # Registrar log da movimentação
                self.log_movement(product, model, "adicionado")
            else:
                messagebox.showinfo("Sucesso", f"Produto '{product}' adicionado com sucesso!")
                # Atualizar a lista de produtos no combobox
                self.product_combobox['values'] = list(self.products.keys())
                # Salvar produtos no arquivo CSV
                self.save_products()
                # Registrar log da movimentação
                self.log_movement(product, "", "adicionado")
            self.product_entry.delete(0, tk.END)
            self.model_entry.delete(0, tk.END)
            # Atualizar a exibição de todos os produtos
            self.display_all_products()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do produto.")

    def remove_product(self):
        product = self.product_entry.get()
        model = self.model_entry.get()
        
        if product:
            if product in self.products:
                if model:
                    if model in self.products[product]:
                        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o modelo '{model}' do produto '{product}'?")
                        if confirm:
                            del self.products[product][model]
                            messagebox.showinfo("Sucesso", f"Modelo '{model}' removido do produto '{product}' com sucesso!")
                            # Salvar produtos no arquivo CSV
                            self.save_products()
                            # Registrar log da movimentação
                            self.log_movement(product, model, "removido")
                    else:
                        messagebox.showwarning("Aviso", f"Modelo '{model}' não encontrado no produto '{product}'.")
                else:
                    confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o produto '{product}'?")
                    if confirm:
                        del self.products[product]
                        messagebox.showinfo("Sucesso", f"Produto '{product}' removido com sucesso!")
                        # Atualizar a lista de produtos no combobox
                        self.product_combobox['values'] = list(self.products.keys())
                        # Salvar produtos no arquivo CSV
                        self.save_products()
                        # Registrar log da movimentação
                        self.log_movement(product, "", "removido")
                # Atualizar a exibição de todos os produtos
                self.display_all_products()
            else:
                messagebox.showwarning("Aviso", f"Produto '{product}' não encontrado.")
            self.product_entry.delete(0, tk.END)
            self.model_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do produto.")

    def add_serial_number(self):
        product = self.selected_product.get()
        model = self.selected_model.get()
        serial_number = self.serial_entry.get()
        
        if product and serial_number:
            if product in self.products:
                if model:
                    if model in self.products[product]:
                        if serial_number not in self.products[product][model]:
                            self.products[product][model].append(serial_number)
                            messagebox.showinfo("Sucesso", f"Num Serie '{serial_number}' adicionado ao modelo '{model}' do produto '{product}'!")
                            # Salvar produtos no arquivo CSV
                            self.save_products()
                            # Registrar log da movimentação
                            self.log_movement(product, serial_number, "adicionado")
                        else:
                            messagebox.showwarning("Aviso", f"Num Serie '{serial_number}' já existe para o modelo '{model}' do produto '{product}'!")
                    else:
                        messagebox.showwarning("Aviso", f"Modelo '{model}' não encontrado no produto '{product}'.")
                else:
                    messagebox.showwarning("Aviso", "Por favor, selecione um modelo.")
            else:
                messagebox.showwarning("Aviso", f"Produto '{product}' não encontrado. Adicione o produto primeiro.")
            self.serial_entry.delete(0, tk.END)
            # Atualizar a exibição de todos os produtos
            self.display_all_products()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do produto e o número de série.")

    def remove_serial_number(self):
        product = self.selected_product.get()
        model = self.selected_model.get()
        serial_number = self.serial_entry.get()
        
        if product and serial_number:
            if product in self.products and model in self.products[product] and serial_number in self.products[product][model]:
                confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o número de série '{serial_number}' do modelo '{model}' do produto '{product}'?")
                if confirm:
                    self.products[product][model].remove(serial_number)
                    messagebox.showinfo("Sucesso", f"Num Serie '{serial_number}' removido do modelo '{model}' do produto '{product}' com sucesso!")
                    # Salvar produtos no arquivo CSV
                    self.save_products()
                    # Registrar log da movimentação
                    self.log_movement(product, serial_number, "removido")
                    # Atualizar a exibição de todos os produtos
                    self.display_all_products()
            else:
                messagebox.showwarning("Aviso", f"Num Serie '{serial_number}' não encontrado para o modelo '{model}' do produto '{product}'.")
            self.serial_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do produto e o número de série.")

    def search(self):
        query = self.search_entry.get()
        
        if query:
            for widget in self.result_inner_frame.winfo_children():
                widget.destroy()

            result = ""
            total = 0
            col = 0
            if query in self.products:
                product_frame = tk.Frame(self.result_inner_frame, padx=10, pady=10, borderwidth=2, relief="groove")
                product_frame.grid(row=0, column=col, padx=5, pady=5, sticky="n")

                product_label = tk.Label(product_frame, text=f"Produto: {query}", font=("Arial", 12, "bold"))
                product_label.pack()

                for model, serials in self.products[query].items():
                    model_label = tk.Label(product_frame, text=f"  Modelo: {model}", font=("Arial", 10, "italic"))
                    model_label.pack(anchor="w")

                    for serial in serials:
                        serial_label = tk.Label(product_frame, text=f"    - {serial}")
                        serial_label.pack(anchor="w")

                    model_total_label = tk.Label(product_frame, text=f"    Total {model}: {len(serials)}", font=("Arial", 10, "bold"))
                    model_total_label.pack(anchor="w")

                    total += len(serials)

                total_label = tk.Label(product_frame, text=f"\nTotal: {total}", font=("Arial", 12, "bold"))
                total_label.pack(anchor="w")

                col += 1
            else:
                for product, models in self.products.items():
                    if query in models:
                        product_frame = tk.Frame(self.result_inner_frame, padx=10, pady=10, borderwidth=2, relief="groove")
                        product_frame.grid(row=0, column=col, padx=5, pady=5, sticky="n")

                        product_label = tk.Label(product_frame, text=f"Produto: {product}", font=("Arial", 12, "bold"))
                        product_label.pack()

                        model_label = tk.Label(product_frame, text=f"  Modelo: {query}", font=("Arial", 10, "italic"))
                        model_label.pack(anchor="w")

                        for serial in models[query]:
                            serial_label = tk.Label(product_frame, text=f"    - {serial}")
                            serial_label.pack(anchor="w")

                        model_total_label = tk.Label(product_frame, text=f"    Total {query}: {len(models[query])}", font=("Arial", 10, "bold"))
                        model_total_label.pack(anchor="w")

                        total = len(models[query])

                        total_label = tk.Label(product_frame, text=f"\nTotal: {total}", font=("Arial", 12, "bold"))
                        total_label.pack(anchor="w")

                        col += 1
                        break
                else:
                    result += "Nenhum resultado encontrado."
                    result_label = tk.Label(self.result_inner_frame, text=result, font=("Arial", 12, "bold"))
                    result_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

            self.result_canvas.update_idletasks()
            self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))

            self.search_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, insira um termo de pesquisa.")

    def display_all_products(self):
        for widget in self.result_inner_frame.winfo_children():
            widget.destroy()

        col = 0
        for product, models in sorted(self.products.items()):
            product_frame = tk.Frame(self.result_inner_frame, padx=10, pady=10, borderwidth=2, relief="groove")
            product_frame.grid(row=0, column=col, padx=5, pady=5, sticky="n")

            product_label = tk.Label(product_frame, text=f"Produto: {product}", font=("Arial", 12, "bold"))
            product_label.pack()

            for model, serials in models.items():
                model_label = tk.Label(product_frame, text=f"  Modelo: {model}", font=("Arial", 10, "italic"))
                model_label.pack(anchor="w")

                for serial in serials:
                    serial_label = tk.Label(product_frame, text=f"    - {serial}")
                    serial_label.pack(anchor="w")

            col += 1

        self.result_canvas.update_idletasks()
        self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))

    def export_products(self):
        with open('export.txt', 'w') as file:
            for widget in self.result_inner_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for sub_widget in widget.winfo_children():
                        if isinstance(sub_widget, tk.Label):
                            file.write(sub_widget.cget("text") + "\n")

    def save_products(self):
        with open('products.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for product, models in sorted(self.products.items()):
                for model, serials in models.items():
                    writer.writerow([product, model] + serials)

    def load_products(self):
        if os.path.exists('products.csv'):
            with open('products.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:
                        product = row[0]
                        model = row[1]
                        serials = row[2:]
                        if product not in self.products:
                            self.products[product] = {}
                        self.products[product][model] = serials

    def log_movement(self, product, serial_number, action):
        with open('log.txt', 'a') as logfile:
            logfile.write(f"{product},{serial_number},{action},{datetime.now()}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryControl(root)
    root.mainloop()