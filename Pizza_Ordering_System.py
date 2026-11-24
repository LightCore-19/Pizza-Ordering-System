import tkinter as tk
from tkinter import ttk, messagebox

pizza_prices = {
    "Overload": 420,
    "Hawaiian Classic": 280,
    "Ham & Cheese": 230,
    "Supreme": 320
}

size_prices = {
    "Small": 0,
    "Medium": 50,
    "Large": 100
}

topping_prices = {
    "Bacon": 45,
    "Pineapple": 40,
    "Garlic": 20
}

window = tk.Tk()
window.title("Pizza Ordering System")
window.configure(bg="#FFF4E6")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

initial_width = min(650, int(screen_width * 0.95))
initial_height = min(850, int(screen_height * 0.90))

window.geometry(f"{initial_width}x{initial_height}")
window.minsize(300, 400)

pizza_var = tk.StringVar(value="Pepperoni")
size_var = tk.StringVar(value="Small")
quantity_var = tk.StringVar(value="1")

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

main_frame = tk.Frame(window, bg="#FFF4E6")
main_frame.pack(fill="both", expand=True, padx=10, pady=8)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=3)
main_frame.grid_rowconfigure(4, weight=2)

title = tk.Label(
    main_frame,
    text="PIZZA PLACE",
    font=("Arial", 18, "bold"),
    bg="#FFF4E6",
    fg="#B22222",
    anchor="center",
    justify="center"
)
title.grid(row=0, column=0, pady=10, sticky="ew")

order_frame = tk.Frame(
    main_frame,
    bg="#FFFFFF",
    padx=12,
    pady=10,
    highlightbackground="#E6B566",
    highlightthickness=2
)
order_frame.grid(row=1, column=0, sticky="nsew")

order_frame.grid_columnconfigure(0, weight=1)

label_widgets = []

def create_label(parent, text, size=12):
    label = tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold"),
        bg="#FFFFFF",
        fg="#632D1F",
        anchor="w"
    )
    label.pack(anchor="w", pady=(6, 3))
    label_widgets.append((label, size))
    return label


style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground="#FFF4E6",
    background="#D94A38",
    foreground="#632D1F",
    padding=8
)

create_label(order_frame, "Select Pizza Flavor:")

pizza_dropdown = ttk.Combobox(
    order_frame,
    values=[
        f"{pizza} - ₱{price}"
        for pizza, price in pizza_prices.items()
    ],
    state="readonly",
    font=("Arial", 12)
)

pizza_dropdown.pack(fill="x", pady=4)
pizza_dropdown.current(0)

def select_pizza(event=None):
    selected = pizza_dropdown.get()
    pizza = selected.split(" - ₱")[0]
    pizza_var.set(pizza)

pizza_dropdown.bind("<<ComboboxSelected>>", select_pizza)

create_label(order_frame, "Select Pizza Size:")

size_widgets = []

for size, price in size_prices.items():
    radio = tk.Radiobutton(
        order_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 11),
        bg="#FFFFFF",
        fg="#632D1F",
        selectcolor="#FFD166",
        activebackground="#FFFFFF",
        activeforeground="#B22222",
        anchor="w"
    )
    radio.pack(anchor="w")
    size_widgets.append(radio)

create_label(order_frame, "Select Extra Toppings:")

topping_widgets = []

for topping, price in topping_prices.items():
    check = tk.Checkbutton(
        order_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 11),
        bg="#FFFFFF",
        fg="#632D1F",
        selectcolor="#FFD166",
        activebackground="#FFFFFF",
        activeforeground="#B22222",
        anchor="w"
    )
    check.pack(anchor="w")
    topping_widgets.append(check)

create_label(order_frame, "Quantity:")

quantity_frame = tk.Frame(order_frame, bg="#FFFFFF")
quantity_frame.pack(anchor="w", fill="x", pady=6)

quantity_spinbox = tk.Spinbox(
    quantity_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 20, "bold"),
    width=10,
    justify="center",
    bg="#FFF4E6",
    fg="#2B160F",
    buttonbackground="#C62828",
    insertbackground="#2B160F",
    relief="solid",
    bd=2
)

quantity_spinbox.pack(anchor="w", ipady=8, ipadx=10)


def calculate_total():

    pizza = pizza_var.get()
    size = size_var.get()

    try:
        quantity = int(quantity_var.get().strip())

        if quantity < 1 or quantity > 50:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a whole number between 1 and 50."
        )
        return

    if pizza not in pizza_prices:
        messagebox.showerror(
            "Invalid Pizza",
            "Please select a valid pizza flavor."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

    total_per_pizza = pizza_price + size_price + topping_price
    total = total_per_pizza * quantity

    receipt_text.delete("1.0", tk.END)

    receipt_text.insert(
        tk.END,
        "ORDER RECEIPT \n\n"
    )

    receipt_text.insert(
        tk.END,
        f"Pizza Flavor: {pizza}\n"
    )

    receipt_text.insert(
        tk.END,
        f"Pizza Price: ₱{pizza_price:,.2f}\n"
    )

    receipt_text.insert(
        tk.END,
        f"Pizza Size: {size} (+₱{size_price:,.2f})\n"
    )

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"{topping}: ₱{topping_prices[topping]:,.2f}\n"
            )
    else:
        receipt_text.insert(
            tk.END,
            "Extra Toppings: None\n"
        )

    receipt_text.insert(tk.END, "\n")

    receipt_text.insert(
        tk.END,
        f"Price per Pizza: ₱{total_per_pizza:,.2f}\n"
    )

    receipt_text.insert(
        tk.END,
        f"Quantity: {quantity} pcs\n"
    )

    receipt_text.insert(
        tk.END,
        "\n\n"
    )

    receipt_text.insert(
        tk.END,
        f"TOTAL AMOUNT: ₱{total:,.2f}\n"
    )

    receipt_text.insert(
        tk.END,
        "\nThank you for ordering!\n"
    )


def reset_order():

    pizza_var.set("Pepperoni")
    pizza_dropdown.current(0)
    size_var.set("Small")
    quantity_var.set("1")

    for variable in topping_vars.values():
        variable.set(False)

    receipt_text.delete("1.0", tk.END)


button_frame = tk.Frame(
    main_frame,
    bg="#FFF4E6"
)

button_frame.grid(
    row=2,
    column=0,
    sticky="ew",
    pady=10
)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

calculate_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg="#C62828",
    fg="white",
    activebackground="#A51D1D",
    activeforeground="white",
    command=calculate_total,
    padx=8,
    pady=11,
    relief="flat"
)

calculate_button.grid(
    row=0,
    column=0,
    padx=4,
    sticky="ew"
)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg="#E6A23C",
    fg="#FFFFFF",
    activebackground="#C98724",
    activeforeground="white",
    command=reset_order,
    padx=8,
    pady=11,
    relief="flat"
)

reset_button.grid(
    row=0,
    column=1,
    padx=4,
    sticky="ew"
)

summary_label = tk.Label(
    main_frame,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg="#FFF4E6",
    fg="#B22222"
)

summary_label.grid(
    row=3,
    column=0,
    sticky="new",
    pady=(4, 0)
)

receipt_frame = tk.Frame(
    main_frame,
    bg="#FFF4E6"
)

receipt_frame.grid(
    row=4,
    column=0,
    sticky="nsew",
    pady=5
)

receipt_frame.grid_rowconfigure(0, weight=1)
receipt_frame.grid_columnconfigure(0, weight=1)

receipt_text = tk.Text(
    receipt_frame,
    height=10,
    font=("Consolas", 10),
    bg="#FFFFFF",
    fg="#632D1F",
    insertbackground="#632D1F",
    wrap="word",
    relief="solid",
    bd=2
)

receipt_text.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scrollbar = ttk.Scrollbar(
    receipt_frame,
    orient="vertical",
    command=receipt_text.yview
)

scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

receipt_text.configure(
    yscrollcommand=scrollbar.set
)


def resize_interface(event):

    if event.widget != window:
        return

    width = event.width

    if width < 350:
        scale = 0.75
    elif width < 400:
        scale = 0.85
    elif width < 600:
        scale = 0.95
    elif width < 900:
        scale = 1.0
    else:
        scale = 1.10

    title.config(
        font=("Arial", max(12, int(18 * scale)), "bold")
    )

    summary_label.config(
        font=("Arial", max(11, int(14 * scale)), "bold")
    )

    for label, original_size in label_widgets:
        label.config(
            font=("Arial", max(10, int(original_size * scale)), "bold")
        )

    for widget in size_widgets + topping_widgets:
        widget.config(
            font=("Arial", max(10, int(11 * scale)))
        )

    pizza_dropdown.config(
        font=("Arial", max(9, int(12 * scale)))
    )

    quantity_spinbox.config(
        font=("Arial", max(16, int(20 * scale)), "bold")
    )

    calculate_button.config(
        font=("Arial", max(9, int(11 * scale)), "bold")
    )

    reset_button.config(
        font=("Arial", max(9, int(11 * scale)), "bold")
    )

    receipt_text.config(
        font=("Consolas", max(9, int(10 * scale)))
    )


window.bind("<Configure>", resize_interface)

window.mainloop()