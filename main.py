import tkinter as tk
from tkinter import messagebox


class OrderApp:
    # Constants for pricing and tax rate
    PIZZA_PRICE = 10  # $10 per pizza
    HOT_DOG_PRICE = 2  # $2 per hot dog
    DRINK_PRICE = 2  # $2 per drink
    SHAKE_PRICE = 3  # $3 per shake
    TAX_RATE = 0.07  # 7% sales tax


    # Rewards points for each item
    REWARDS_PIZZA = 1000  # 1000 points for a free pizza
    REWARDS_HOT_DOG = 200  # 200 points for a free hot dog
    REWARDS_DRINK = 50  # 50 points for a free drink
    REWARDS_SHAKE = 50  # 50 points for a free shake
    POINTS_PER_DOLLAR = 1000  # 1000 points = $1 discount


    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Dog Express")


        self.customer_points = 0  # Customer's initial reward points


        # Create the GUI components
        self.create_widgets()


    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Welcome to Pizza Dog Express!", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)


        # Order Input Frame
        order_frame = tk.Frame(self.root)
        order_frame.pack()


        # Create order variables
        self.pizza_var = tk.IntVar(value=0)
        self.chicken_pizza_var = tk.IntVar(value=0)
        self.pork_pizza_var = tk.IntVar(value=0)
        self.beef_hot_dog_var = tk.IntVar(value=0)
        self.pork_hot_dog_var = tk.IntVar(value=0)
        self.coke_var = tk.IntVar(value=0)
        self.pepsi_var = tk.IntVar(value=0)
        self.dr_pepper_var = tk.IntVar(value=0)
        self.vanilla_shake_var = tk.IntVar(value=0)
        self.chocolate_shake_var = tk.IntVar(value=0)
        self.cake_shake_var = tk.IntVar(value=0)
        self.oreo_shake_var = tk.IntVar(value=0)


        # Create entry fields with labels
        self.create_label_entry(order_frame, "Number of Beef Pizzas:", self.pizza_var)
        self.create_label_entry(order_frame, "Number of Chicken Pizzas:", self.chicken_pizza_var)
        self.create_label_entry(order_frame, "Number of Pork Pizzas:", self.pork_pizza_var)
        self.create_label_entry(order_frame, "Number of Beef Hot Dogs:", self.beef_hot_dog_var)
        self.create_label_entry(order_frame, "Number of Pork Hot Dogs:", self.pork_hot_dog_var)
        self.create_label_entry(order_frame, "Number of Cokes:", self.coke_var)
        self.create_label_entry(order_frame, "Number of Pepsis:", self.pepsi_var)
        self.create_label_entry(order_frame, "Number of Dr. Peppers:", self.dr_pepper_var)
        self.create_label_entry(order_frame, "Number of Vanilla Shakes:", self.vanilla_shake_var)
        self.create_label_entry(order_frame, "Number of Chocolate Shakes:", self.chocolate_shake_var)
        self.create_label_entry(order_frame, "Number of Cake Shakes:", self.cake_shake_var)
        self.create_label_entry(order_frame, "Number of Oreo Shakes:", self.oreo_shake_var)


        # Create a label to display rewards points
        self.rewards_label = tk.Label(self.root, text=f"Your Rewards Points: {self.customer_points}")
        self.rewards_label.pack(pady=10)


        # Button to place the order
        place_order_button = tk.Button(self.root, text="Place Order", command=self.place_order)
        place_order_button.pack(pady=10)


    def create_label_entry(self, frame, text, variable):
        """Create a label and entry widget with padding."""
        label = tk.Label(frame, text=text)
        label.pack()
        entry = tk.Entry(frame, textvariable=variable, width=10)
        entry.pack(pady=5)


    def validate_input(self, var):
        """Validate if the input is a non-negative integer."""
        try:
            value = int(var.get())
            if value is None or value < 0:
                raise ValueError("Input must be a non-negative integer")
            return value
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive integer.")
            return None


    def calculate_total(self):
        """Calculate the total bill including sales tax."""
        pizzas = self.validate_input(self.pizza_var)
        chicken_pizzas = self.validate_input(self.chicken_pizza_var)
        pork_pizzas = self.validate_input(self.pork_pizza_var)
        beef_hot_dogs = self.validate_input(self.beef_hot_dog_var)
        pork_hot_dogs = self.validate_input(self.pork_hot_dog_var)
        coke = self.validate_input(self.coke_var)
        pepsi = self.validate_input(self.pepsi_var)
        dr_pepper = self.validate_input(self.dr_pepper_var)
        vanilla_shake = self.validate_input(self.vanilla_shake_var)
        chocolate_shake = self.validate_input(self.chocolate_shake_var)
        cake_shake = self.validate_input(self.cake_shake_var)
        oreo_shake = self.validate_input(self.oreo_shake_var)


        if any(var is None for var in (pizzas, chicken_pizzas, pork_pizzas, beef_hot_dogs, pork_hot_dogs, coke, pepsi, dr_pepper, vanilla_shake, chocolate_shake, cake_shake, oreo_shake)):
            return None  # If any input is invalid, return None


        # Calculate costs
        pizza_cost = (pizzas + chicken_pizzas + pork_pizzas) * self.PIZZA_PRICE
        hot_dog_cost = (beef_hot_dogs + pork_hot_dogs) * self.HOT_DOG_PRICE
        drink_cost = (coke + pepsi + dr_pepper) * self.DRINK_PRICE
        shake_cost = (vanilla_shake + chocolate_shake + cake_shake + oreo_shake) * self.SHAKE_PRICE


        # Calculate subtotal and total with tax
        subtotal = pizza_cost + hot_dog_cost + drink_cost + shake_cost
        tax = subtotal * self.TAX_RATE
        total = subtotal + tax


        return total


    def ask_if_apply_points(self, total):
        """Ask the user if they want to apply rewards points for a discount."""
        return messagebox.askyesno("Use Points?", f"Your total is ${total:.2f}. Would you like to use your rewards points for a discount?")


    def apply_points_discount(self, total):
        """Apply rewards points to get a discount on the total."""
        max_discount = self.customer_points // self.POINTS_PER_DOLLAR  # Maximum discount in dollars


        # Ensure the discount does not exceed the total
        discount = min(max_discount, total)
        discounted_total = total - discount  # Calculate the new total with discount


        # Deduct the points used for the discount
        self.customer_points -= discount * self.POINTS_PER_DOLLAR


        return discounted_total, discount


    def place_order(self):
        """Place the order, calculate the total bill, and update rewards points."""
        total = self.calculate_total()  # Calculate the total before applying any discount
       
        if total is None:  # If total is None, it means there was an invalid input
            return


        # Ask if the customer wants to apply rewards points
        if self.ask_if_apply_points(total):
            discounted_total, discount = self.apply_points_discount(total)
        else:
            discounted_total = total
            discount = 0  # No discount applied if customer chooses not to use points


        # Accumulate new rewards points based on the items purchased
        pizzas = int(self.pizza_var.get())
        chicken_pizzas = int(self.chicken_pizza_var.get())
        pork_pizzas = int(self.pork_pizza_var.get())
        beef_hot_dogs = int(self.beef_hot_dog_var.get())
        pork_hot_dogs = int(self.pork_hot_dog_var.get())
        coke = int(self.coke_var.get())
        pepsi = int(self.pepsi_var.get())
        dr_pepper = int(self.dr_pepper_var.get())
        vanilla_shake = int(self.vanilla_shake_var.get())
        chocolate_shake = int(self.chocolate_shake_var.get())
        cake_shake = int(self.cake_shake_var.get())
        oreo_shake = int(self.oreo_shake_var.get())


        pizza_points = (pizzas + chicken_pizzas + pork_pizzas) * self.REWARDS_PIZZA
        hot_dog_points = (beef_hot_dogs + pork_hot_dogs) * self.REWARDS_HOT_DOG
        drink_points = (coke + pepsi + dr_pepper) * self.REWARDS_DRINK
        shake_points = (vanilla_shake + chocolate_shake + cake_shake + oreo_shake) * self.REWARDS_SHAKE


        # Update customer points with new rewards from the order
        self.customer_points += pizza_points + hot_dog_points + drink_points + shake_points


        # Show the total bill, discount, and new points in a message box
        messagebox.showinfo(
            "Order Summary",
            f"Total Bill (After Discount): ${discounted_total:.2f}\nDiscount Applied: ${discount:.2f}\nNew Rewards Points: {self.customer_points}"
        )


        # Reset the order quantities to zero after placing the order
        self.pizza_var.set(0)
        self.chicken_pizza_var.set(0)
        self.pork_pizza_var.set(0)
        self.beef_hot_dog_var.set(0)
        self.pork_hot_dog_var.set(0)
        self.coke_var.set(0)
        self.pepsi_var.set(0)
        self.dr_pepper_var.set(0)
        self.vanilla_shake_var.set(0)
        self.chocolate_shake_var.set(0)
        self.cake_shake_var.set(0)
        self.oreo_shake_var.set(0)


        # Update the displayed rewards points
        self.rewards_label.config(text=f"Your Rewards Points: {self.customer_points}")


# Main application logic
root = tk.Tk()
app = OrderApp(root)
root.mainloop()












