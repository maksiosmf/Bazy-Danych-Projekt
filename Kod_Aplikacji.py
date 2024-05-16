import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import pyodbc
import re
import datetime

connection_string = 'Driver={SQL Server};Server=DESKTOP-9RTGUG2\\SQLEXPRESS01;Database=sklep;Trusted_Connection=Yes;'
conn = pyodbc.connect(connection_string)

def create_window(title, width, height):
    window = tk.Toplevel()
    window.title(title)
    window.geometry(f"{width}x{height}+{int(window.winfo_screenwidth()/2 - width/2)}+{int(window.winfo_screenheight()/2 - height/2)}")
    window.configure(bg='#e6e6fa')  # Light Lavender background
    return window

def show_customers():
    select_window = create_window("Customer Management", 400, 300)
    tk.Button(select_window, text="Show Customers", command=show_all_customers, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Add Customer", command=add_customer, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Edit Customers", command=edit_customers, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)

def show_all_customers():
    select_window = create_window("All Customers", 400, 300)
    customer_list = tk.Listbox(select_window, width=50, height=10, font=('Helvetica', 10))
    customer_list.pack(pady=10, padx=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM klienci")
    for customer in cursor.fetchall():
        customer_list.insert(tk.END, f"{customer[0]} - {customer[1]} {customer[2]} - {customer[3]}")

def add_customer():
    add_window = create_window("Add New Customer", 400, 300)
    tk.Label(add_window, text="First Name:", font=('Helvetica', 10)).pack(pady=5)
    first_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
    first_name_entry.pack(pady=5)
    tk.Label(add_window, text="Last Name:", font=('Helvetica', 10)).pack(pady=5)
    last_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
    last_name_entry.pack(pady=5)
    tk.Label(add_window, text="Email:", font=('Helvetica', 10)).pack(pady=5)
    email_entry = tk.Entry(add_window, font=('Helvetica', 10))
    email_entry.pack(pady=5)

    def save_customer():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        if first_name and last_name and email:
            cursor = conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(id_klienta), 0) + 1 FROM klienci")
            new_customer_id = cursor.fetchone()[0]
            print(new_customer_id, first_name, last_name, email)
            print(type(new_customer_id), type(first_name), type(last_name), type(email))
            cursor.execute("INSERT INTO klienci (imie, nazwisko, email) VALUES (?, ?, ?)",
                           (first_name, last_name, email))
            conn.commit()
            msgbox.showinfo("Success", f"New customer added: {first_name} {last_name}, Email: {email}")
            add_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter first name, last name, and email.")

    save_button = tk.Button(add_window, text="Save Customer", command=save_customer, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def edit_customers():
    edit_window = create_window("Select Customer to Edit", 600, 400)
    edit_list = tk.Listbox(edit_window, width=70, height=10, font=('Helvetica', 10))
    edit_list.pack(pady=10, padx=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM klienci")
    customers = cursor.fetchall()
    for customer in customers:
        edit_list.insert(tk.END, f"{customer[0]} - {customer[1]} {customer[2]} - {customer[3]}")

    def on_edit_selected():
        if edit_list.curselection():
            selected_text = edit_list.get(edit_list.curselection()[0])
            selected_customer_id = re.search(r'\d+$', selected_text).group()
            show_edit_customer(selected_customer_id)
        else:
            msgbox.showwarning("Selection Needed", "Please select a customer to edit.")

    select_button = tk.Button(edit_window, text="Edit Selected Customer", command=on_edit_selected, bg='#4682b4', font=('Helvetica', 12), fg='white')
    select_button.pack(pady=10)

def show_edit_customer(customer_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM klienci WHERE id_klienta = ?", (int(customer_id),))
        customer = cursor.fetchone()

        customer_edit_window = create_window("Edit Customer", 400, 300)
        tk.Label(customer_edit_window, text="First Name:", font=('Helvetica', 10)).pack(pady=5)
        first_name_entry = tk.Entry(customer_edit_window, font=('Helvetica', 10))
        first_name_entry.insert(0, customer[0])
        first_name_entry.pack(pady=5)

        tk.Label(customer_edit_window, text="Last Name:", font=('Helvetica', 10)).pack(pady=5)
        last_name_entry = tk.Entry(customer_edit_window, font=('Helvetica', 10))
        last_name_entry.insert(0, customer[1])
        last_name_entry.pack(pady=5)

        tk.Label(customer_edit_window, text="Email:", font=('Helvetica', 10)).pack(pady=5)
        email_entry = tk.Entry(customer_edit_window, font=('Helvetica', 10))
        email_entry.insert(0, customer[2])
        email_entry.pack(pady=5)

        def save_edited_customer():
            cursor.execute("UPDATE klienci SET imie = ?, nazwisko = ?, email = ? WHERE id_klienta = ?",
                           (first_name_entry.get(), last_name_entry.get(), email_entry.get(), int(customer_id)))
            conn.commit()
            msgbox.showinfo("Success", "Customer details updated successfully.")
            customer_edit_window.destroy()

        save_button = tk.Button(customer_edit_window, text="Save Changes", command=save_edited_customer, bg='#4682b4', font=('Helvetica', 12), fg='white')
        save_button.pack(pady=10)
    except Exception as e:
        msgbox.showerror("Error", str(e))

def show_products():
    select_window = create_window("Product Management", 400, 300)
    tk.Button(select_window, text="Show Products", command=show_all_products, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Add Product", command=add_product, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Edit Products", command=edit_products, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)

def show_all_products():
    select_window = create_window("All Products", 400, 300)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT p.id_produktu, p.nazwa, p.cena, k.nazwa AS kategoria FROM produkty p INNER JOIN kategorie k ON p.id_kategorii = k.id_kategorii")
    products = cursor.fetchall()
    for idx, product in enumerate(products, start=1):
        product_info = f"{idx}. {product[1]} - {product[2]} PLN - {product[3]}"
        tk.Label(select_window, text=product_info, bg='#f5f5dc', font=('Helvetica', 10)).pack(pady=2)

def add_product():
    add_window = create_window("Add New Product", 400, 300)
    tk.Label(add_window, text="Product Name:", font=('Helvetica', 10)).pack(pady=5)
    product_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
    product_name_entry.pack(pady=5)
    tk.Label(add_window, text="Price (PLN):", font=('Helvetica', 10)).pack(pady=5)
    price_entry = tk.Entry(add_window, font=('Helvetica', 10))
    price_entry.pack(pady=5)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kategorie")
    categories = [category[1] for category in cursor.fetchall()]

    tk.Label(add_window, text="Category:", font=('Helvetica', 10)).pack(pady=5)
    category_combobox = ttk.Combobox(add_window, values=categories, state="readonly", font=('Helvetica', 10))
    category_combobox.pack(pady=5)

    def save_product():
        product_name = product_name_entry.get()
        price = price_entry.get()
        category = category_combobox.get()
        if product_name and price and category:
            cursor = conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(id_produktu), 0) + 1 FROM produkty")
            new_product_id = cursor.fetchone()[0]

            cursor.execute("select id_kategorii from kategorie where nazwa = ?", (category,))
            id_kategorii = cursor.fetchone()[0]

            cursor.execute("INSERT INTO produkty (id_produktu, nazwa, cena, id_kategorii) VALUES (?, ?, ?, ?)",
                           (new_product_id, product_name, price, id_kategorii))
            conn.commit()
            msgbox.showinfo("Success", f"New product added: {product_name}, Price: {price} PLN, Category: {category}")
            add_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter product name, price, and select a category.")

    save_button = tk.Button(add_window, text="Save Product", command=save_product, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def edit_products():
    edit_window = create_window("Select Product to Edit", 600, 400)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT p.id_produktu, p.nazwa, p.cena, k.nazwa AS kategoria FROM produkty p INNER JOIN kategorie k ON p.id_kategorii = k.id_kategorii")
    products = cursor.fetchall()

    header_frame = tk.Frame(edit_window, bg='#f5f5dc')
    header_frame.grid(row=0, column=0, sticky="ew")
    tk.Label(header_frame, text="ID", bg='#f5f5dc', width=5, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=0)
    tk.Label(header_frame, text="Product", bg='#f5f5dc', width=30, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=1)
    tk.Label(header_frame, text="Price", bg='#f5f5dc', width=10, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=2)
    tk.Label(header_frame, text="Category", bg='#f5f5dc', width=20, anchor='w', font=('Helvetica', 10, 'bold')).grid(row=0, column=3)

    edit_list = tk.Listbox(edit_window, width=80, height=10, font=('Helvetica', 10))
    edit_list.grid(row=1, column=0, padx=10, pady=10)

    for product in products:
        product_info = f"{product[0]} - {product[1]} - {product[2]} PLN - {product[3]}"
        edit_list.insert(tk.END, product_info)

    def on_edit_selected():
        if edit_list.curselection():
            selected_text = edit_list.get(edit_list.curselection()[0])
            selected_product_id = selected_text.split(' - ')[0]
            show_edit_product(selected_product_id)
        else:
            msgbox.showwarning("Selection Needed", "Please select a product to edit.")

    select_button = tk.Button(edit_window, text="Edit Selected Product", command=on_edit_selected, bg='#4682b4', font=('Helvetica', 12), fg='white')
    select_button.grid(row=2, column=0, pady=10)

def show_edit_product(product_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produkty WHERE id_produktu = ?", (int(product_id),))
    product = cursor.fetchone()

    product_edit_window = create_window("Edit Product", 400, 300)
    tk.Label(product_edit_window, text="Product Name:", font=('Helvetica', 10)).pack(pady=5)
    product_name_entry = tk.Entry(product_edit_window, font=('Helvetica', 10))
    product_name_entry.insert(0, product[1])
    product_name_entry.pack(pady=5)

    tk.Label(product_edit_window, text="Price (PLN):", font=('Helvetica', 10)).pack(pady=5)
    price_entry = tk.Entry(product_edit_window, font=('Helvetica', 10))
    price_entry.insert(0, product[2])
    price_entry.pack(pady=5)

    cursor.execute("SELECT * FROM kategorie")
    categories = [category[1] for category in cursor.fetchall()]

    tk.Label(product_edit_window, text="Category:", font=('Helvetica', 10)).pack(pady=5)
    category_combobox = ttk.Combobox(product_edit_window, values=categories, state="readonly", font=('Helvetica', 10))
    category_combobox.pack(pady=5)

    def save_edited_product():
        product_name = product_name_entry.get()
        price = price_entry.get()
        category = category_combobox.get()
        if product_name and price and category:
            cursor.execute("SELECT id_kategorii FROM kategorie WHERE nazwa = ?", (category,))
            category_id = cursor.fetchone()[0]

            cursor.execute("UPDATE produkty SET nazwa = ?, cena = ?, id_kategorii = ? WHERE id_produktu = ?",
                           (product_name, price, category_id, int(product_id)))
            conn.commit()
            msgbox.showinfo("Success", "Product details updated successfully.")
            product_edit_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter product name, price, and select a category.")

    save_button = tk.Button(product_edit_window, text="Save Changes", command=save_edited_product, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def show_orders():
    select_window = create_window("Order Management", 400, 300)
    tk.Button(select_window, text="Show Orders", command=show_all_orders, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Add Order", command=add_order, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Delete Order", command=delete_order, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)

def show_all_orders():
    select_window = create_window("All Orders", 600, 400)
    order_list = tk.Listbox(select_window, width=80, height=20, font=('Helvetica', 10))
    order_list.pack(pady=10, padx=10)
    cursor = conn.cursor()
    cursor.execute("SELECT z.id_zamowienia, k.imie, k.nazwisko, z.data_zamowienia, z.suma FROM zamowienia z INNER JOIN klienci k ON z.id_klienta = k.id_klienta")
    orders = cursor.fetchall()
    for order in orders:
        order_list.insert(tk.END, f"Order ID: {order[0]}, Customer: {order[1]} {order[2]}, Date: {order[3]}, Total: {order[4]:.2f} PLN")
        cursor.execute(
            "SELECT p.nazwa, sz.ilosc, sz.cena_jednostkowa FROM szczegoly_zamowienia sz INNER JOIN produkty p ON sz.id_produktu = p.id_produktu WHERE sz.id_zamowienia = ?",
            (order[0],)
        )
        products = cursor.fetchall()
        for product in products:
            order_list.insert(tk.END, f"  Product: {product[0]}, Quantity: {product[1]}, Unit Price: {product[2]:.2f} PLN")

def add_order():
    add_window = create_window("Add New Order", 500, 400)
    tk.Label(add_window, text="Customer:", font=('Helvetica', 10)).pack(pady=5)
    cursor = conn.cursor()
    cursor.execute("SELECT id_klienta, imie, nazwisko FROM klienci")
    customers = cursor.fetchall()
    customer_options = [f"{customer[0]} - {customer[1]} {customer[2]}" for customer in customers]

    customer_combobox = ttk.Combobox(add_window, values=customer_options, state="readonly", font=('Helvetica', 10))
    customer_combobox.pack(pady=5)

    tk.Label(add_window, text="Order Date (YYYY-MM-DD):", font=('Helvetica', 10)).pack(pady=5)
    order_date_entry = tk.Entry(add_window, font=('Helvetica', 10))
    order_date_entry.pack(pady=5)

    tk.Label(add_window, text="Products:", font=('Helvetica', 10)).pack(pady=5)
    product_frame = tk.Frame(add_window)
    product_frame.pack()

    cursor.execute("SELECT id_produktu, nazwa, cena FROM produkty")
    products = cursor.fetchall()
    product_vars = []
    for product in products:
        product_var = tk.IntVar()
        quantity_var = tk.IntVar()
        product_vars.append((product[0], product_var, product[2], quantity_var))
        product_frame_row = tk.Frame(product_frame)
        product_frame_row.pack(anchor='w', padx=5, pady=2)
        tk.Checkbutton(product_frame_row, text=f"{product[1]} - {product[2]} PLN", variable=product_var, font=('Helvetica', 10)).pack(side='left')
        tk.Entry(product_frame_row, textvariable=quantity_var, width=5, font=('Helvetica', 10)).pack(side='left', padx=5)

    def save_order():
        selected_customer = customer_combobox.get()
        if not selected_customer:
            msgbox.showerror("Error", "Please select a customer.")
            return

        customer_id = selected_customer.split(" - ")[0]
        order_date = order_date_entry.get()
        selected_products = [(product[0], product[3].get(), product[2]) for product in product_vars if product[1].get()]

        if not selected_products:
            msgbox.showerror("Error", "Please select at least one product.")
            return

        total_amount = sum(product[1] * product[2] for product in selected_products)

        if customer_id and order_date and total_amount:
            try:
                order_date_obj = datetime.datetime.strptime(order_date, "%Y-%m-%d").strftime("%Y-%m-%d")

                cursor = conn.cursor()
                cursor.execute("SELECT ISNULL(MAX(id_zamowienia), 0) + 1 FROM zamowienia")
                new_order_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO zamowienia (id_zamowienia, id_klienta, data_zamowienia, suma) VALUES (?, ?, ?, ?)",
                    (new_order_id, customer_id, order_date_obj, total_amount))

                for product in selected_products:
                    cursor.execute(
                        "INSERT INTO szczegoly_zamowienia (id_zamowienia, id_produktu, ilosc, cena_jednostkowa) VALUES (?, ?, ?, ?)",
                        (new_order_id, product[0], product[1], product[2]))

                conn.commit()
                msgbox.showinfo("Success", "New order added successfully.")
                add_window.destroy()
            except ValueError:
                msgbox.showerror("Invalid Date", "The date must be in YYYY-MM-DD format.")
        else:
            msgbox.showerror("Missing Information", "Please enter order date and select products.")

    save_button = tk.Button(add_window, text="Save Order", command=save_order, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def delete_order():
    delete_window = create_window("Delete Order", 400, 300)
    tk.Label(delete_window, text="Order ID to delete:", font=('Helvetica', 10)).pack(pady=5)
    order_id_entry = tk.Entry(delete_window, font=('Helvetica', 10))
    order_id_entry.pack(pady=5)

    def confirm_delete():
        order_id = order_id_entry.get()
        if order_id:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM szczegoly_zamowienia WHERE id_zamowienia = ?", (order_id,))
            cursor.execute("DELETE FROM zamowienia WHERE id_zamowienia = ?", (order_id,))
            conn.commit()
            msgbox.showinfo("Success", f"Order ID: {order_id} deleted successfully.")
            delete_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter a valid order ID.")

    delete_button = tk.Button(delete_window, text="Delete Order", command=confirm_delete, bg='#4682b4', font=('Helvetica', 12), fg='white')
    delete_button.pack(pady=10)

def open_sale():
    sale_window = create_window("Sales", 400, 300)
    tk.Button(sale_window, text="Regular Customer", command=lambda: select_customer_for_sale(True), bg='#7fff7f', font=('Helvetica', 12)).pack(pady=10)
    tk.Button(sale_window, text="New Customer", command=lambda: select_customer_for_sale(False), bg='#7fff7f', font=('Helvetica', 12)).pack(pady=10)

def select_customer_for_sale(is_regular):
    def proceed_with_sale():
        selected_customer_id = customer_combobox.get()
        if not selected_customer_id:
            msgbox.showerror("Error", "Please select a customer.")
            return

        products_window = create_window("Products", 600, 400)
        products_window.configure(bg='#f5f5dc')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT p.id_produktu, p.nazwa, p.cena, k.nazwa AS kategoria FROM produkty p INNER JOIN kategorie k ON p.id_kategorii = k.id_kategorii")
        products = cursor.fetchall()

        def add_to_cart(product_id):
            selected_product_id = product_id
            selected_product_name = products[selected_product_id - 1][1]
            selected_product_price = products[selected_product_id - 1][2]
            selected_product_info = f"Selected Product: {selected_product_name} - {selected_product_price} PLN"
            msgbox.showinfo("Product Added", selected_product_info)

        for idx, product in enumerate(products, start=1):
            product_info = f"{idx}. {product[1]} - {product[2]} PLN - {product[3]}"
            tk.Button(products_window, text=product_info, bg='#f5f5dc', font=('Helvetica', 10), command=lambda idx=idx: add_to_cart(idx)).pack()

    if is_regular:
        select_window = create_window("Select Customer for Sale", 400, 300)
        customer_combobox = ttk.Combobox(select_window, state="readonly", font=('Helvetica', 10))
        customer_combobox.pack(pady=10)

        cursor = conn.cursor()
        cursor.execute("SELECT id_klienta, imie, nazwisko FROM klienci")
        customers = cursor.fetchall()
        customer_options = [f"{customer[0]} - {customer[1]} {customer[2]}" for customer in customers]
        customer_combobox['values'] = customer_options

        proceed_button = tk.Button(select_window, text="Proceed", command=proceed_with_sale, bg='#4682b4', font=('Helvetica', 12), fg='white')
        proceed_button.pack(pady=10)

    else:
        def create_new_customer():
            add_window = create_window("Add New Customer", 400, 300)
            tk.Label(add_window, text="First Name:", font=('Helvetica', 10)).pack(pady=5)
            first_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
            first_name_entry.pack(pady=5)
            tk.Label(add_window, text="Last Name:", font=('Helvetica', 10)).pack(pady=5)
            last_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
            last_name_entry.pack(pady=5)
            tk.Label(add_window, text="Email:", font=('Helvetica', 10)).pack(pady=5)
            email_entry = tk.Entry(add_window, font=('Helvetica', 10))
            email_entry.pack(pady=5)

            def save_customer():
                first_name = first_name_entry.get()
                last_name = last_name_entry.get()
                email = email_entry.get()
                if first_name and last_name and email:
                    cursor = conn.cursor()
                    cursor.execute("SELECT ISNULL(MAX(id_klienta), 0) + 1 FROM klienci")
                    new_customer_id = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO klienci (id_klienta, imie, nazwisko, email) VALUES (?, ?, ?, ?)",
                                   (new_customer_id, first_name, last_name, email))
                    conn.commit()
                    msgbox.showinfo("Success", f"New customer added: {first_name} {last_name}, Email: {email}")
                    add_window.destroy()

            save_button = tk.Button(add_window, text="Save Customer", command=save_customer, bg='#4682b4', font=('Helvetica', 12), fg='white')
            save_button.pack(pady=10)

        msgbox.showinfo("New Customer", "This customer is not a regular customer. Please create a new customer.")
        create_new_customer()

def show_categories():
    select_window = create_window("Category Management", 400, 300)
    tk.Button(select_window, text="Show Categories", command=show_all_categories, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Add Category", command=add_category, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Edit Category", command=edit_categories, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)
    tk.Button(select_window, text="Delete Category", command=delete_category, bg='#4682b4', font=('Helvetica', 12), fg='white').pack(pady=10)

def show_all_categories():
    select_window = create_window("All Categories", 400, 300)
    category_list = tk.Listbox(select_window, width=50, height=10, font=('Helvetica', 10))
    category_list.pack(pady=10, padx=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kategorie")
    for category in cursor.fetchall():
        category_list.insert(tk.END, f"{category[0]} - {category[1]}")

def add_category():
    add_window = create_window("Add New Category", 400, 300)
    tk.Label(add_window, text="Category Name:", font=('Helvetica', 10)).pack(pady=5)
    category_name_entry = tk.Entry(add_window, font=('Helvetica', 10))
    category_name_entry.pack(pady=5)

    def save_category():
        category_name = category_name_entry.get()
        if category_name:
            cursor = conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(id_kategorii), 0) + 1 FROM kategorie")
            new_category_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO kategorie (id_kategorii, nazwa) VALUES (?, ?)", (new_category_id, category_name))
            conn.commit()
            msgbox.showinfo("Success", f"New category added: {category_name}")
            add_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter a category name.")

    save_button = tk.Button(add_window, text="Save Category", command=save_category, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def edit_categories():
    edit_window = create_window("Select Category to Edit", 400, 300)
    edit_list = tk.Listbox(edit_window, width=50, height=10, font=('Helvetica', 10))
    edit_list.pack(pady=10, padx=10)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kategorie")
    categories = cursor.fetchall()
    for category in categories:
        edit_list.insert(tk.END, f"{category[0]} - {category[1]}")

    def on_edit_selected():
        if edit_list.curselection():
            selected_text = edit_list.get(edit_list.curselection()[0])
            selected_category_id = selected_text.split(' - ')[0]
            show_edit_category(selected_category_id)
        else:
            msgbox.showwarning("Selection Needed", "Please select a category to edit.")

    select_button = tk.Button(edit_window, text="Edit Selected Category", command=on_edit_selected, bg='#4682b4', font=('Helvetica', 12), fg='white')
    select_button.pack(pady=10)

def show_edit_category(category_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kategorie WHERE id_kategorii = ?", (int(category_id),))
    category = cursor.fetchone()

    category_edit_window = create_window("Edit Category", 400, 300)
    tk.Label(category_edit_window, text="Category Name:", font=('Helvetica', 10)).pack(pady=5)
    category_name_entry = tk.Entry(category_edit_window, font=('Helvetica', 10))
    category_name_entry.insert(0, category[1])
    category_name_entry.pack(pady=5)

    def save_edited_category():
        category_name = category_name_entry.get()
        if category_name:
            cursor.execute("UPDATE kategorie SET nazwa = ? WHERE id_kategorii = ?", (category_name, int(category_id)))
            conn.commit()
            msgbox.showinfo("Success", "Category details updated successfully.")
            category_edit_window.destroy()
        else:
            msgbox.showerror("Missing Information", "Please enter category name.")

    save_button = tk.Button(category_edit_window, text="Save Changes", command=save_edited_category, bg='#4682b4', font=('Helvetica', 12), fg='white')
    save_button.pack(pady=10)

def delete_category():
    delete_window = create_window("Delete Category", 400, 300)
    tk.Label(delete_window, text="Category ID to delete:", font=('Helvetica', 10)).pack(pady=5)
    category_id_entry = tk.Entry(delete_window, font=('Helvetica', 10))
    category_id_entry.pack(pady=5)

    def confirm_delete():
        category_id = category_id_entry.get()
        if category_id:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM produkty WHERE id_kategorii = ?", (category_id,))
            product_count = cursor.fetchone()[0]
            if product_count == 0:
                cursor.execute("DELETE FROM kategorie WHERE id_kategorii = ?", (category_id,))
                conn.commit()
                msgbox.showinfo("Success", f"Category ID: {category_id} deleted successfully.")
                delete_window.destroy()
            else:
                msgbox.showerror("Cannot Delete", "Category is assigned to products and cannot be deleted.")
        else:
            msgbox.showerror("Missing Information", "Please enter a valid category ID.")

    delete_button = tk.Button(delete_window, text="Delete Category", command=confirm_delete, bg='#4682b4', font=('Helvetica', 12), fg='white')
    delete_button.pack(pady=10)

root = tk.Tk()
root.title("Store Application")
root.geometry("350x450")
root.configure(bg='#add8e6')

tk.Button(root, text="Manage Customers", command=show_customers, bg='#4682b4', font=('Helvetica', 14), fg='white').pack(pady=10)
tk.Button(root, text="Manage Products", command=show_products, bg='#4682b4', font=('Helvetica', 14), fg='white').pack(pady=10)
tk.Button(root, text="Manage Orders", command=show_orders, bg='#4682b4', font=('Helvetica', 14), fg='white').pack(pady=10)
tk.Button(root, text="Manage Categories", command=show_categories, bg='#4682b4', font=('Helvetica', 14), fg='white').pack(pady=10)
tk.Button(root, text="Open Sale", command=open_sale, bg='#4682b4', font=('Helvetica', 14), fg='white').pack(pady=10)

root.mainloop()
conn.close()
