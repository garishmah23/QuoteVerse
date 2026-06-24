import tkinter as tk
from tkinter import messagebox
import json
import random
import requests


class QuoteManager:
    def __init__(self):
        self.local_quotes = self.load_local_quotes()

    def load_local_quotes(self):
        try:
            with open("quotes.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []

    def get_local_quote(self):
        if self.local_quotes:
            return random.choice(self.local_quotes)

        return {
            "quote": "Stay positive and keep learning.",
            "author": "QuoteVerse"
        }

    def get_api_quote(self):
        try:
            response = requests.get(
                "https://api.quotable.io/random",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()

                return {
                    "quote": data["content"],
                    "author": data["author"]
                }

        except Exception:
            pass

        return self.get_local_quote()


class FavoritesManager:
    def __init__(self):
        self.file = "favorites.json"

    def save_favorite(self, quote):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                favorites = json.load(f)

            favorites.append(quote)

            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(
                    favorites,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception:
            return False


class QuoteVerseUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QuoteVerse")
        self.root.geometry("850x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")

        self.quote_manager = QuoteManager()
        self.favorite_manager = FavoritesManager()

        self.current_quote = None

        self.create_widgets()
        self.load_new_quote()

    def create_widgets(self):

        # Title
        self.title_label = tk.Label(
            self.root,
            text="📖 QuoteVerse",
            font=("Segoe UI", 26, "bold"),
            bg="#121212",
            fg="#00ADB5"
        )
        self.title_label.pack(pady=20)

        # Quote Card
        self.quote_frame = tk.Frame(
            self.root,
            bg="#1E1E1E",
            padx=30,
            pady=30
        )
        self.quote_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        # Quote Text
        self.quote_text = tk.Label(
            self.quote_frame,
            text="",
            wraplength=700,
            justify="center",
            font=("Segoe UI", 18),
            bg="#1E1E1E",
            fg="white"
        )
        self.quote_text.pack(pady=40)

        # Author
        self.author_text = tk.Label(
            self.quote_frame,
            text="",
            font=("Segoe UI", 14, "italic"),
            bg="#1E1E1E",
            fg="#00ADB5"
        )
        self.author_text.pack()

        # Button Frame
        self.button_frame = tk.Frame(
            self.root,
            bg="#121212"
        )
        self.button_frame.pack(pady=20)

        # New Quote Button
        self.new_btn = tk.Button(
            self.button_frame,
            text="New Quote",
            width=15,
            font=("Segoe UI", 12, "bold"),
            bg="#00ADB5",
            fg="white",
            activebackground="#008891",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            command=self.load_new_quote
        )
        self.new_btn.grid(row=0, column=0, padx=10)

        # Save Favorite Button
        self.favorite_btn = tk.Button(
            self.button_frame,
            text="Save Favorite",
            width=15,
            font=("Segoe UI", 12, "bold"),
            bg="#00ADB5",
            fg="white",
            activebackground="#008891",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            command=self.save_favorite
        )
        self.favorite_btn.grid(row=0, column=1, padx=10)

        # Copy Button
        self.copy_btn = tk.Button(
            self.button_frame,
            text="Copy Quote",
            width=15,
            font=("Segoe UI", 12, "bold"),
            bg="#00ADB5",
            fg="white",
            activebackground="#008891",
            activeforeground="white",
            cursor="hand2",
            bd=0,
            command=self.copy_quote
        )
        self.copy_btn.grid(row=0, column=2, padx=10)

        # Hover Effects
        self.new_btn.bind("<Enter>", self.on_enter)
        self.new_btn.bind("<Leave>", self.on_leave)

        self.favorite_btn.bind("<Enter>", self.on_enter)
        self.favorite_btn.bind("<Leave>", self.on_leave)

        self.copy_btn.bind("<Enter>", self.on_enter)
        self.copy_btn.bind("<Leave>", self.on_leave)

        # Footer
        self.footer = tk.Label(
            self.root,
            text="Built with Python ❤️",
            font=("Segoe UI", 10),
            bg="#121212",
            fg="gray"
        )
        self.footer.pack(pady=10)

    def on_enter(self, event):
        event.widget.config(bg="#008891")

    def on_leave(self, event):
        event.widget.config(bg="#00ADB5")

    def load_new_quote(self):
        self.current_quote = self.quote_manager.get_api_quote()

        self.quote_text.config(
            text=f'"{self.current_quote["quote"]}"'
        )

        self.author_text.config(
            text=f'— {self.current_quote["author"]}'
        )

    def save_favorite(self):

        if self.favorite_manager.save_favorite(
                self.current_quote):
            messagebox.showinfo(
                "Success",
                "Quote saved successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Failed to save quote."
            )

    def copy_quote(self):

        text = (
            f'{self.current_quote["quote"]}'
            f'\n\n— {self.current_quote["author"]}'
        )

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

        messagebox.showinfo(
            "Copied",
            "Quote copied to clipboard!"
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = QuoteVerseUI(root)

    root.mainloop()