import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # To handle JPEG and PNG images

class OrderApp:
    # Constants for pricing and tax rate
    PIZZA_PRICE = 10
    HOT_DOG_PRICE = 2
    DRINK_PRICE = 2
    SHAKE_PRICE = 3
    TAX_RATE = 0.07

    # Constants for rewards points
    HOT_DOG_POINTS = 500
    PIZZA_POINTS = 1000
    DRINK_POINTS = 200
    SHAKE_POINTS = 200
    POINTS_TO_DOLLAR = 1000  # 1000 points = $1

    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Dog Express")

        # Load and resize images
        pizza_image = Image.open("pizza.jpg").resize((100, 100))
        hotdog_image = Image.open("hotdog.jpg").resize((100, 100))
        coke_image = Image.open("coke.png").resize((100, 100))
        shake_image = Image.open("shake.jpg").resize((100, 100))

        # Convert to PhotoImage for Tkinter
        self.pizza_photo = ImageTk.PhotoImage(pizza_image)
        self.hotdog_photo = ImageTk.PhotoImage(hotdog_image)
        self.coke_photo = ImageTk.PhotoImage(coke_image)
        self.shake_photo = ImageTk.PhotoImage(shake_image)

        # Create a frame to hold the image labels and ensure it's centered
        image_frame = tk.Frame(self.root)
        image_frame.pack(fill=tk.X, pady=10)  # Centered, with vertical padding

        # Add images to the frame with equal padding for symmetry
        pizza_label = tk.Label(image_frame, image=self.pizza_photo)
        pizza_label.pack(side=tk.LEFT, padx=(10, 10))  # Equal padding for symmetry

        hotdog_label = tk.Label(image_frame, image=self.hotdog_photo)
        hotdog_label.pack(side=tk.LEFT, padx=(10, 10))

        coke_label = tk.Label(image_frame, image=self.coke_photo)
        coke_label.pack(side=tk.LEFT, padx=(10, 10))

        shake_label = tk.Label(image_frame, image=self.shake_photo)
        shake_label.pack(side=tk.LEFT, padx=(10, 10))

        # Title label, placed below the image frame
        title_label = tk.Label(self.root, text="Welcome to Pizza Dog Express!", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)  # Padding below the images

        # Create points label
        self.points = tk.IntVar(value=0)
        points_label = tk.Label(self.root, text="Your current points are", font=("Arial", 12))
        points_label.pack()
        points_value_label = tk.Label(self.root, textvariable=self.points, font=("Arial", 12))
        points_value_label.pack()

        # Create other GUI components
        self.create_widgets()

    def create_widgets(self):
        # Order Input Frame
        order_frame = tk.Frame(self.root)
        order_frame.pack()  # Create a new frame for order inputs

        # Create order variables and input fields with labels
        order_vars = [
            ("Number of Beef Pizzas:", self.PIZZA_PRICE, self.pizza_photo, self.PIZZA_POINTS),
            ("Number of Chicken Pizzas:", self.PIZZA_PRICE, self.pizza_photo, self.PIZZA_POINTS),
            ("Number of Pork Pizzas:", self.PIZZA_PRICE, self.pizza_photo, self.PIZZA_POINTS),
            ("Number of Beef Hot Dogs:", self.HOT_DOG_PRICE, self.hotdog_photo, self.HOT_DOG_POINTS),
            ("Number of Pork Hot Dogs:", self.HOT_DOG_PRICE, self.hotdog_photo, self.HOT_DOG_POINTS),
            ("Number of Cokes:", self.DRINK_PRICE, self.coke_photo, self.DRINK_POINTS),
            ("Number of Pepsis:", self.DRINK_PRICE, self.coke_photo, self.DRINK_POINTS),
            ("Number of Dr. Peppers:", self.DRINK_PRICE, self.coke_photo, self.DRINK_POINTS),
            ("Number of Vanilla Shakes:", self.SHAKE_PRICE, self.shake_photo, self.SHAKE_POINTS),
            ("Number of Chocolate Shakes:", self.SHAKE_PRICE, self.shake_photo, self.SHAKE_POINTS),
            ("Number of Cake Shakes:", self.SHAKE_PRICE, self.shake_photo, self.SHAKE_POINTS),
            ("Number of Oreo Shakes:", self.SHAKE_PRICE, self.shake_photo, self.SHAKE_POINTS)
        ]

        row = 0
        column = 0

        self.entry_vars = []

        for label_text, price, photo, points in order_vars:
            label = tk.Label(order_frame, text=label_text)
            label.grid(row=row, column=column, padx=10, pady=5, sticky="w")

            var = tk.StringVar(value="0")
            entry = tk.Entry(order_frame, textvariable=var, width=10)
            entry.grid(row=row, column=column+1, padx=10, pady=5)

            self.entry_vars.append((var, price, points))

            # Move to the next row if the current row is filled
            column += 2
            if column > 5:
                column = 0
                row += 1

        # Use reward points option
        self.use_points_var = tk.BooleanVar()
        use_points_checkbutton = tk.Checkbutton(self.root, text="Use Reward Points", variable=self.use_points_var)
        use_points_checkbutton.pack()

        # Place order button
        place_order_button = tk.Button(self.root, text="Place Order", command=self.place_order)
        place_order_button.pack(pady=10)

        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        exit_button.pack(pady=10)

    def exit_program(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.destroy()

    def place_order(self):
        total_cost = 0
        total_points = self.points.get()
        for var, price, points in self.entry_vars:
            quantity = int(var.get())
            total_cost += quantity * price
            total_points += quantity * points

        if self.use_points_var.get():
            # Calculate discount based on points
            discount = min(total_points // self.POINTS_TO_DOLLAR, total_cost)
            total_cost -= discount
            total_points -= discount * self.POINTS_TO_DOLLAR

        # Add sales tax
        total_cost_with_tax = total_cost * (1 + self.TAX_RATE)

        if self.use_points_var.get():
            messagebox.showinfo("Total Cost", f"Total Cost (including 7% sales tax): ${total_cost_with_tax:.2f}\nRemaining Points: {total_points}")
        else:
            messagebox.showinfo("Total Cost", f"Total Cost (including 7% sales tax): ${total_cost_with_tax:.2f}")

        # Update points
        self.points.set(total_points)

        # Reset order quantities
        for var, _, _ in self.entry_vars:
            var.set("0")

# Main application logic
root = tk.Tk()
app = OrderApp(root)
root.mainloop()













