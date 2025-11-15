import tkinter as tk
from tkinter import ttk
import random

DICE_TYPES = [4, 6, 8, 10, 12, 20]

# Dice skins (color themes)
DICE_SKINS = {
    "Default": {"fg": "black"},
    "Arcane Blue": {"fg": "#4da6ff"},
    "Inferno Red": {"fg": "#ff4d4d"},
    "Emerald": {"fg": "#00cc66"},
    "Shadow Purple": {"fg": "#9933ff"},
}


class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        root.title("Pretty Dice")
        root.geometry("500x650")

        self.currency = 50  # in-game coins
        self.unlocked_skins = {"Default"}
        self.selected_skin = "Default"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=6)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 18, "bold"))

        ttk.Label(root, text="Pretty Dice", style="Header.TLabel").pack(pady=15)

        main = ttk.Frame(root)
        main.pack(pady=5)

        # dice selection
        ttk.Label(main, text="Dice Type").grid(row=0, column=0)
        ttk.Label(main, text="Quantity").grid(row=0, column=1)

        self.dice_entries = {}
        for i, dt in enumerate(DICE_TYPES, start=1):
            ttk.Label(main, text=f"d{dt}").grid(row=i, column=0)
            entry = ttk.Entry(main, width=5)
            entry.insert(0, "0")
            entry.grid(row=i, column=1)
            self.dice_entries[dt] = entry

        ttk.Button(root, text="Roll Dice", command=self.roll_dice).pack(pady=10)

        ttk.Label(root, text="Selected Dice Skin:").pack(pady=(10, 0))
        self.skin_display = ttk.Label(root, text=self.selected_skin, font=("Arial", 12, "bold"))
        self.skin_display.pack()

        ttk.Button(root, text="Open Dice Shop", command=self.open_shop).pack(pady=10)

        ttk.Label(root, text="Results:", font=("Arial", 14, "bold")).pack(pady=5)
        self.results_text = tk.Text(root, height=12, width=45, font=("Consolas", 11))
        self.results_text.pack()

        ttk.Button(root, text="Sum Rolls", command=self.sum_rolls).pack(pady=10)

    def roll_dice(self):
        self.results_text.delete(1.0, tk.END)
        self.last_rolls = []

        skin = DICE_SKINS[self.selected_skin]

        for dice_type, entry in self.dice_entries.items():
            try:
                qty = int(entry.get())
            except ValueError:
                qty = 0

            if qty > 0:
                rolls = [random.randint(1, dice_type) for _ in range(qty)]
                self.last_rolls.extend(rolls)

                # Insert with skin color
                self.results_text.insert(tk.END, f"d{dice_type} x{qty}: ", skin["fg"])
                self.results_text.insert(tk.END, f"{rolls}\n", skin["fg"])

        # Color tag setup
        for color in {s["fg"] for s in DICE_SKINS.values()}:
            self.results_text.tag_configure(color, foreground=color)

        if not self.last_rolls:
            self.results_text.insert(tk.END, "No dice rolled.\n")

    def sum_rolls(self):
        if hasattr(self, "last_rolls") and self.last_rolls:
            total = sum(self.last_rolls)
            self.results_text.insert(tk.END, f"\nSum of all rolls: {total}\n")
        else:
            self.results_text.insert(tk.END, "No rolls to sum.\n")

    def open_shop(self):
        shop = tk.Toplevel(self.root)
        shop.title("Dice Skin Shop")
        shop.geometry("350x400")

        ttk.Label(shop, text="Dice Shop", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(shop, text=f"Your Coins: {self.currency}", font=("Arial", 12)).pack()

        for skin_name, skin_data in DICE_SKINS.items():
            frame = ttk.Frame(shop)
            frame.pack(pady=5)

            label = ttk.Label(frame, text=skin_name, foreground=skin_data["fg"])
            label.grid(row=0, column=0, padx=5)

            if skin_name in self.unlocked_skins:
                btn = ttk.Button(frame, text="Select",
                                 command=lambda s=skin_name: self.select_skin(s))
            else:
                btn = ttk.Button(frame, text="Buy 20 coins",
                                 command=lambda s=skin_name: self.buy_skin(s))

            btn.grid(row=0, column=1, padx=5)

    def buy_skin(self, skin_name):
        if self.currency >= 20:
            self.currency -= 20
            self.unlocked_skins.add(skin_name)
            self.select_skin(skin_name)

        else:
            self.results_text.insert(tk.END, "\nNot enough coins!\n")

    def select_skin(self, skin_name):
        self.selected_skin = skin_name
        self.skin_display.config(text=skin_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollerApp(root)
    root.mainloop()