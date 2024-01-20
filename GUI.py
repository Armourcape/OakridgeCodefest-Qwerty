import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.display_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def display_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#3498db", foreground="#ffffff",
                         justify='left', relief='solid', borderwidth=1, padx=4, pady=2)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()

class ImageLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image = None
        self.configure(anchor="center")

    def load_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((400, 400))  # Adjust the size as needed
        self.image = ImageTk.PhotoImage(image)
        self.config(image=self.image)

class SplashScreen:
    def __init__(self, root, duration=3000):
        self.root = root
        self.splash_screen = tk.Toplevel(root)
        self.splash_screen.title("Splash Screen")
        self.splash_screen.geometry("400x200")
        self.splash_screen.state('zoomed')
        
        tk.Label(self.splash_screen, text="Welcome to 3 Cards UI", font=("Helvetica", 20)).pack(pady=30)
        tk.Label(self.splash_screen, text="Loading, please wait...", font=("Helvetica", 14)).pack()

        self.root.after(duration, self.destroy_splash_screen)

    def destroy_splash_screen(self):
        self.splash_screen.destroy()
        self.root.deiconify()

class ThreeCardsUI:
    def __init__(self, master):
        self.master = master
        self.master.title("3 Cards UI")
        self.master.attributes('-fullscreen', True)

        self.left_card = ttk.Frame(master, style="Card.TFrame")
        self.left_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=20, pady=20)

        self.right_top_card = ttk.Frame(master, style="Card.TFrame")
        self.right_top_card.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.right_bottom_card = ttk.Frame(master, style="Card.TFrame")
        self.right_bottom_card.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=2)
        master.grid_columnconfigure(1, weight=1)

        self.setup_styles()
        self.add_content_to_cards()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Card.TFrame", borderwidth=2, relief="groove", bordercolor="#3498db", background="#ecf0f1")
        style.configure("TButton", padding=8, font=('Helvetica', 12), foreground="#000000", background="#ffffff")
        style.map("TButton", background=[("active", "#eeeeee")])

    def add_content_to_cards(self):
        self.left_card_label = tk.Label(self.left_card, text="Left Big Card", font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.left_card_label.pack(pady=20)

        self.loading_label = tk.Label(self.left_card, text="Loading...", font=("Helvetica", 12), bg="#ecf0f1", fg="#3498db")

        drop_file_btn = ttk.Button(self.left_card, text="Drop File", command=self.upload_file)
        drop_file_btn.pack(pady=(60, 10))
        drop_file_tooltip = ToolTip(drop_file_btn, "Click to select a file")
        drop_file_btn.bind("<Button-1>", self.button_press)
        drop_file_btn.bind("<ButtonRelease-1>", self.button_release)

        self.image_label = ImageLabel(self.left_card)
        self.image_label.pack(pady=10)

        right_top_card_label = tk.Label(self.right_top_card, text="Right Top Card", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        right_top_card_label.pack()

        right_bottom_card_label = tk.Label(self.right_bottom_card, text="Right Bottom Card", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        right_bottom_card_label.pack()

    def button_press(self, event):
        event.widget.configure(background="#dddddd")

    def button_release(self, event):
        event.widget.configure(background="#ffffff")

    def upload_file(self):
        self.loading_label.pack_forget()
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            file_name = file_path.split("/")[-1]
            self.loading_label.pack(pady=10)
            threading.Thread(target=self.process_file, args=(file_path, file_name)).start()

    def process_file(self, file_path, file_name):
        import time
        time.sleep(2)

        self.image_label.load_image(file_path)

        messagebox.showinfo("File Selected", f"Selected File: {file_name}")
        self.left_card_label.config(text=f"Selected File: {file_name}")
        self.loading_label.pack_forget()

def main():
    root = tk.Tk()
    root.withdraw()

    splash = SplashScreen(root, duration=3000)

    app = ThreeCardsUI(root)
    root.geometry("800x600")
    root.configure(bg="#ecf0f1")
    root.mainloop()

if __name__ == "__main__":
    main()
