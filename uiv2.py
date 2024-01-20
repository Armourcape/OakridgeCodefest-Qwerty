import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os
from ultralytics import YOLO
import shutil

i=1
path = ""
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

class ThreeCardsUI:
    def __init__(self, master):
        self.master = master
        self.master.title("CDSN Lung Cancer Detector")
        self.master.attributes('-fullscreen', True)

        self.left_card = ttk.Frame(master, style="Card.TFrame")
        self.left_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(20, 10), pady=20)

        self.nav_bar = ttk.Frame(master, style="NavBar.TFrame")
        self.nav_bar.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 20), pady=20)

        master.grid_rowconfigure(0, weight=5)
        master.grid_rowconfigure(1, weight=2)
        master.grid_columnconfigure(0, weight=5)
        master.grid_columnconfigure(1, weight=2)

        self.setup_styles()
        self.add_content_to_cards()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Card.TFrame", borderwidth=2, relief="groove", bordercolor="#3498db", background="#ecf0f1")
        style.configure("NavBar.TFrame", borderwidth=2, relief="groove", bordercolor="#3498db", background="#ecf0f1")
        style.configure("TButton", padding=8, font=('Helvetica', 12), foreground="#000000", background="#ffffff")
        style.map("TButton", background=[("active", "#eeeeee")])

    def add_content_to_cards(self):
        self.left_card_label = tk.Label(self.left_card, text="CDSN Lung Cancer Detector", font=("Helvetica", 18, "bold"), bg="#ecf0f1", fg="#2c3e50")
        self.left_card_label.pack(pady=20)

        self.loading_label = tk.Label(self.left_card, text="Loading...", font=("Helvetica", 12), bg="#ecf0f1", fg="#3498db")

        drop_file_btn = ttk.Button(self.left_card, text="Drop File", command=self.upload_file)
        drop_file_btn.pack(pady=(60, 10))
        drop_file_tooltip = ToolTip(drop_file_btn, "Click to select a file")
        drop_file_btn.bind("<Button-1>", self.button_press)
        drop_file_btn.bind("<ButtonRelease-1>", self.button_release)

        self.image_label = ImageLabel(self.left_card)
        self.image_label.pack(pady=10)

        right_top_card_label = tk.Label(self.nav_bar, text="Layers", font=("Helvetica", 16, "bold"), bg="#ecf0f1", fg="#2c3e50")
        right_top_card_label.pack(side="top")

        # button1 = ttk.Button(self.nav_bar, text="Button 1", command=self.show_button1_content, width=20)
        button1 = ttk.Button(self.nav_bar, text="Show Prediction", command=self.show_button1_content, width=20)
        button1.pack(side="top", pady=(30, 10), anchor="center")

        # button2 = ttk.Button(self.nav_bar, text="Button 2", command=self.show_button2_content, width=20)
        button2 = ttk.Button(self.nav_bar, text="Cancer Delineation", command=self.show_button2_content, width=20)
        button2.pack(side="top", pady=(10, 10), anchor="center")

        button3 = ttk.Button(self.nav_bar, text="Download", command=self.show_button3_content, width=20)
        button3.pack(side="top", pady=(10, 30), anchor="center")

    def show_button1_content(self):
        global path
        if path:
            self.image_label.load_image(path)
        else:
            messagebox.showinfo("Error", "Drop an image first!")

    def show_button2_content(self):
        global path_crop
        if path_crop:
            self.image_label.load_image(path_crop)
        else:
            messagebox.showinfo("Error", "Error")

    def show_button3_content(self):
        source_path = f"predictions/runtime{str(i)}/labels/"
        destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        if destination_folder:
            try:
                files = os.listdir(source_path)
                for file in files:
                    source_file_path = os.path.join(source_path, file)
                    destination_file_path = os.path.join(destination_folder, file)
                    shutil.copy2(source_file_path, destination_file_path)
                print(f"Files downloaded from {source_path} to {destination_folder}")
            except Exception as e:
                messagebox.showinfo("Error", "Error")
        else:
            print("Error", "Error")
    
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
            global i
            i=i+1
            threading.Thread(target=self.process_file, args=(file_path, file_name, i)).start()

    def process_file(self, file_path, file_name, i):

        model = YOLO('runs/segment/train/weights/best.pt')
        model.predict(file_path, show_conf=False, save=True, imgsz=640, project="predictions", name="runtime", conf=0.7, save_txt=True, save_crop=True)
        
        #path = f"runs/segment/predict{str(p_int)}/1-{n_int}.jpg"
        #self.image_label.load_image(path)
        global path
        path =f"predictions/runtime{str(i)}/{file_name}"
        global path_crop
        path_crop=f"predictions/runtime{str(i)}/crops/lung-tumors/{file_name}"
        self.image_label.load_image(path)
        messagebox.showinfo("File Selected", f"Selected File: {file_name}")
        self.left_card_label.config(text=f"Selected File: {file_name}")
        self.loading_label.pack_forget()

class SplashScreen:
    def __init__(self, root, duration=3000):
        self.root = root
        self.splash_screen = tk.Toplevel(root)
        self.splash_screen.title("CDSN Lung Cancer Detector")
        self.splash_screen.geometry("400x200")
        self.splash_screen.state('zoomed')
        
        tk.Label(self.splash_screen, text="Welcome to CDSN", font=("Helvetica", 20)).pack(pady=30)
        tk.Label(self.splash_screen, text="Loading, please wait...", font=("Helvetica", 14)).pack()

        self.root.after(duration, self.destroy_splash_screen)

    def destroy_splash_screen(self):
        self.splash_screen.destroy()
        self.root.deiconify()

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
