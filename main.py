import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class CoffeeMachine:
    def __init__(self):
        self.water = 1000  # in ml
        self.milk = 500  # in ml
        self.coffee_beans = 200  # in grams
        self.chocolate = 100  # in grams
        self.sugar = 300  # in grams
        self.cups = 10  # number of cups
        self.money = {
            10: 0,  # 0 times 10 euros
            5: 10,   # 10 times 5 euros
            1: 50,   # 50 times 1 euro
            0.50: 50,  # 50 times 50 cents
            0.25: 30,  # 30 times 25 cents
            0.10: 100, # 100 times 10 cents
            0.05: 100  # 100 times 5 cents
        }

    def check_resources(self, water_needed, milk_needed, beans_needed, chocolate_needed, sugar_needed, cups_needed=1):
        if self.water < water_needed:
            return "Sorry, not enough water!"
        if self.milk < milk_needed:
            return "Sorry, not enough milk!"
        if self.coffee_beans < beans_needed:
            return "Sorry, not enough coffee beans!"
        if self.chocolate < chocolate_needed:
            return "Sorry, not enough chocolate!"
        if self.sugar < sugar_needed:
            return "Sorry, not enough sugar!"
        if self.cups < cups_needed:
            return "Sorry, not enough cups!"
        return "Enough resources"

    def make_coffee(self, coffee_type, sugar_level, money_inserted, money_denominations):
        if coffee_type == "Espresso":
            water_needed = 50
            milk_needed = 0
            beans_needed = 18
            chocolate_needed = 0
            cost = 2
        elif coffee_type == "Latte":
            water_needed = 200
            milk_needed = 150
            beans_needed = 24
            chocolate_needed = 0
            cost = 3
        elif coffee_type == "Cappuccino":
            water_needed = 250
            milk_needed = 100
            beans_needed = 24
            chocolate_needed = 0
            cost = 3.5
        elif coffee_type == "Americano":
            water_needed = 300
            milk_needed = 0
            beans_needed = 24
            chocolate_needed = 0
            cost = 2.5
        elif coffee_type == "Mocha":
            water_needed = 200
            milk_needed = 150
            beans_needed = 24
            chocolate_needed = 20
            cost = 4
        elif coffee_type == "Hot Chocolate":
            water_needed = 200
            milk_needed = 200
            beans_needed = 0
            chocolate_needed = 30
            cost = 3
        else:
            return "Invalid coffee type.", money_inserted

        sugar_needed = sugar_level * 5  # Each level of sugar corresponds to 5 grams
        change = money_inserted - cost

        if change < 0:
            return f"Not enough money. {coffee_type} costs ${cost}.", money_inserted

        resource_check = self.check_resources(water_needed, milk_needed, beans_needed, chocolate_needed, sugar_needed)
        if resource_check == "Enough resources":
            self.water -= water_needed
            self.milk -= milk_needed
            self.coffee_beans -= beans_needed
            self.chocolate -= chocolate_needed
            self.sugar -= sugar_needed
            self.cups -= 1

            if change > 0:
                if self.give_change(change):
                    self.update_money_storage(money_denominations)
                    return f"Here is your {coffee_type}. Enjoy! Change: ${change:.2f}", 0
                else:
                    return "Sorry, not enough change available.", money_inserted
            else:
                self.update_money_storage(money_denominations)
                return f"Here is your {coffee_type}. Enjoy!", 0
        else:
            return resource_check, money_inserted

    def update_money_storage(self, money_denominations):
        for denomination, count in money_denominations.items():
            self.money[denomination] += count

    def give_change(self, change):
        original_change = change
        denominations = sorted(self.money.keys(), reverse=True)
        change_denominations = {}

        for denomination in denominations:
            if change == 0:
                break
            count = int(change // denomination)
            if count > self.money[denomination]:
                count = self.money[denomination]
            if count > 0:
                change_denominations[denomination] = count
                self.money[denomination] -= count
                change -= count * denomination
                change = round(change, 2)  # To avoid floating point precision issues

        if change == 0:
            return True
        else:
            for denomination, count in change_denominations.items():
                self.money[denomination] += count  # Restore the money if exact change cannot be given
            return False

    def refill(self, water=0, milk=0, beans=0, chocolate=0, sugar=0, cups=0):
        self.water += water
        self.milk += milk
        self.coffee_beans += beans
        self.chocolate += chocolate
        self.sugar += sugar
        self.cups += cups
        return "Machine refilled!"

class CoffeeMachineGUI:
    def __init__(self, root, machine):
        self.machine = machine
        self.root = root
        self.root.title("Coffee Vending Machine")

        self.create_widgets()

    def create_widgets(self):
        # Load and set the background image
        self.background_image = Image.open(r"images/background.jpg")
        self.background_image = self.background_image.resize(
            (450, 600),
            Image.Resampling.LANCZOS
        )
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Canvas for rounded rectangle
        self.canvas = tk.Canvas(self.root, width=300, height=350, bg='#f0f0f0', highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.create_rounded_rectangle(10, 10, 290, 340, radius=20, fill="#d3d3d3", outline="#d3d3d3")

        # Frame for buttons
        button_frame = tk.Frame(self.canvas, padx=10, pady=10, bg='#d3d3d3')
        button_frame.place(x=25, y=25)

        self.status_label = tk.Label(button_frame, text="Status: Ready", bg='#d3d3d3', wraplength=250)
        self.status_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.espresso_button = tk.Button(button_frame, text="Espresso ($2)", command=lambda: self.insert_money("Espresso", 2))
        self.espresso_button.grid(row=1, column=0, padx=5, pady=5)

        self.latte_button = tk.Button(button_frame, text="Latte ($3)", command=lambda: self.insert_money("Latte", 3))
        self.latte_button.grid(row=1, column=1, padx=5, pady=5)

        self.cappuccino_button = tk.Button(button_frame, text="Cappuccino ($3.5)", command=lambda: self.insert_money("Cappuccino", 3.5))
        self.cappuccino_button.grid(row=2, column=0, padx=5, pady=5)

        self.americano_button = tk.Button(button_frame, text="Americano ($2.5)", command=lambda: self.insert_money("Americano", 2.5))
        self.americano_button.grid(row=2, column=1, padx=5, pady=5)

        self.mocha_button = tk.Button(button_frame, text="Mocha ($4)", command=lambda: self.insert_money("Mocha", 4))
        self.mocha_button.grid(row=3, column=0, padx=5, pady=5)

        self.hot_chocolate_button = tk.Button(button_frame, text="Hot Chocolate ($3)", command=lambda: self.insert_money("Hot Chocolate", 3))
        self.hot_chocolate_button.grid(row=3, column=1, padx=5, pady=5)

        self.refill_button = tk.Button(button_frame, text="Refill Machine", command=self.open_refill_window)
        self.refill_button.grid(row=4, column=0, padx=5, pady=5)

        self.status_button = tk.Button(button_frame, text="Display Status", command=self.display_status)
        self.status_button.grid(row=4, column=1, padx=5, pady=5)

        self.money_status_button = tk.Button(button_frame, text="Money Status", command=self.display_money_status)
        self.money_status_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def insert_money(self, coffee_type, coffee_cost):
        self.money_window = tk.Toplevel(self.root)
        self.money_window.title("Insert Money")

        tk.Label(self.money_window, text=f"Insert Money (max $10 total) for {coffee_type} (${coffee_cost})").pack(pady=10)

        self.money_entries = {}
        denominations = [10, 5, 1, 0.50, 0.25, 0.10, 0.05]
        for denomination in denominations:
            frame = tk.Frame(self.money_window)
            frame.pack(pady=5)
            tk.Label(frame, text=f"${denomination}" if denomination >= 1 else f"${denomination}").pack(side=tk.LEFT)
            self.money_entries[denomination] = tk.Entry(frame, width=5)
            self.money_entries[denomination].pack(side=tk.LEFT)

        tk.Button(self.money_window, text="Submit", command=lambda: self.process_money(coffee_type, coffee_cost)).pack(pady=10)

    def process_money(self, coffee_type, coffee_cost):
        total_money = 0
        money_denominations = {}
        for denomination, entry in self.money_entries.items():
            count = int(entry.get() or 0)
            total_money += count * denomination
            if count > 0:
                money_denominations[denomination] = count

        if total_money > 10:
            messagebox.showerror("Error", "Total money inserted exceeds $10. Please try again.")
        else:
            self.money_window.destroy()
            self.select_sugar(coffee_type, total_money, money_denominations)

    def select_sugar(self, coffee_type, money_inserted, money_denominations):
        self.sugar_window = tk.Toplevel(self.root)
        self.sugar_window.title("Select Sugar Level")

        tk.Label(self.sugar_window, text="Select Sugar Level").pack(pady=10)

        sugar_levels = [
            "\u25cb",  # Empty circle
            "\u25cf",  # Filled circle
            "\u25cf \u25cf",
            "\u25cf \u25cf \u25cf",
            "\u25cf \u25cf \u25cf \u25cf",
            "\u25cf \u25cf \u25cf \u25cf \u25cf"
        ]

        for i, level in enumerate(sugar_levels):
            tk.Button(self.sugar_window, text=level, command=lambda l=i: self.make_coffee(coffee_type, l, money_inserted, money_denominations)).pack(pady=5)

    def make_coffee(self, coffee_type, sugar_level, money_inserted, money_denominations):
        self.sugar_window.destroy()
        result, change = self.machine.make_coffee(coffee_type, sugar_level, money_inserted, money_denominations)
        self.status_label.config(text=f"Status: {result}")

    def open_refill_window(self):
        self.refill_window = tk.Toplevel(self.root)
        self.refill_window.title("Refill Machine")

        tk.Label(self.refill_window, text="Refill Options").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(self.refill_window, text="Add Water", command=self.add_water).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add Milk", command=self.add_milk).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add Coffee Beans", command=self.add_beans).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add Chocolate", command=self.add_chocolate).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add Sugar", command=self.add_sugar).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add Cups", command=self.add_cups).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.refill_window, text="Add All", command=self.add_all).grid(row=4, column=0, columnspan=2, pady=10)

    def add_water(self):
        self.machine.refill(water=1000)
        self.status_label.config(text="Status: Water refilled!")
        self.refill_window.destroy()

    def add_milk(self):
        self.machine.refill(milk=500)
        self.status_label.config(text="Status: Milk refilled!")
        self.refill_window.destroy()

    def add_beans(self):
        self.machine.refill(beans=200)
        self.status_label.config(text="Status: Coffee beans refilled!")
        self.refill_window.destroy()

    def add_chocolate(self):
        self.machine.refill(chocolate=100)
        self.status_label.config(text="Status: Chocolate refilled!")
        self.refill_window.destroy()

    def add_sugar(self):
        self.machine.refill(sugar=300)
        self.status_label.config(text="Status: Sugar refilled!")
        self.refill_window.destroy()

    def add_cups(self):
        self.machine.refill(cups=10)
        self.status_label.config(text="Status: Cups refilled!")
        self.refill_window.destroy()

    def add_all(self):
        self.machine.refill(water=1000, milk=500, beans=200, chocolate=100, sugar=300, cups=10)
        self.status_label.config(text="Status: All resources refilled!")
        self.refill_window.destroy()

    def display_status(self):
        status = (
            f"Water: {self.machine.water}ml\n"
            f"Milk: {self.machine.milk}ml\n"
            f"Coffee Beans: {self.machine.coffee_beans}g\n"
            f"Chocolate: {self.machine.chocolate}g\n"
            f"Sugar: {self.machine.sugar}g\n"
            f"Cups: {self.machine.cups}\n"
        )
        messagebox.showinfo("Machine Status", status)

    def display_money_status(self):
        money_status = "\n".join([f"${denomination}: {int(count)}" for denomination, count in sorted(self.machine.money.items(), reverse=True)])
        messagebox.showinfo("Money Status", money_status)

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x600")  # Set the window size to 3:4 ratio
    machine = CoffeeMachine()
    app = CoffeeMachineGUI(root, machine)
    root.mainloop()
