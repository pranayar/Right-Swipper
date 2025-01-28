import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading
from PIL import Image, ImageTk

class RightSwipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Right Swipper")
        self.root.geometry("600x750")  # Adjusted window size for better spacing
        self.root.configure(bg="#121212")  # Dark background for a sleek look

        # Set the window icon with logo
        logo = Image.open('logo.jpg')  # Or .jpg or .png
        self.root.tk.call('wm', 'iconphoto', self.root._w, ImageTk.PhotoImage(logo))

        # Title label with adjusted font size and color
        self.title_label = tk.Label(root, text="Right Swipper", font=("Helvetica", 30, "bold"), bg="#121212", fg="#FF5733")
        self.title_label.pack(pady=40)

        # Subtitle label with clear white text
        self.desc_label = tk.Label(root, text="Automate your right swipes effortlessly!", font=("Helvetica", 16), bg="#121212", fg="#FFFFFF")
        self.desc_label.pack(pady=15)

        # Input frame for swipe count with updated styles
        self.input_frame = tk.Frame(root, bg="#121212")
        self.input_frame.pack(pady=20)

        self.input_label = tk.Label(self.input_frame, text="Number of Swipes:", font=("Helvetica", 14), bg="#121212", fg="#FFFFFF")
        self.input_label.pack(side="left", padx=15)

        self.swipe_count_var = tk.StringVar(value="10")
        self.swipe_count_entry = tk.Entry(self.input_frame, textvariable=self.swipe_count_var, font=("Helvetica", 14), width=5, justify="center", bd=0, relief="solid", fg="#333", bg="#FFFFFF", insertbackground="#FF5733")
        self.swipe_count_entry.pack(side="left", padx=15)

        # Time interval section with updated colors
        self.interval_frame = tk.Frame(root, bg="#121212")
        self.interval_frame.pack(pady=15)

        self.interval_label = tk.Label(self.interval_frame, text="Time Between Swipes (s):", font=("Helvetica", 14), bg="#121212", fg="#FFFFFF")
        self.interval_label.pack(side="left", padx=15)

        self.interval_var = tk.StringVar(value="0.1")
        self.interval_entry = tk.Entry(self.interval_frame, textvariable=self.interval_var, font=("Helvetica", 14), width=5, justify="center", bd=0, relief="solid", fg="#333", bg="#FFFFFF", insertbackground="#FF5733")
        self.interval_entry.pack(side="left", padx=15)

        # Divider with a soft orange accent
        self.divider = tk.Frame(root, height=2, bg="#FF5733")
        self.divider.pack(fill="x", padx=50)

        # Start swiping button with modern colors
        self.swipe_button = tk.Button(root, text="Start Swiping", command=self.right_swipe, font=("Helvetica", 18, "bold"), bg="#FF5733", fg="#FFFFFF", activebackground="#FF3300", activeforeground="white", bd=0, padx=50, pady=15, relief="flat", cursor="hand2")
        self.swipe_button.pack(pady=30)

        # Keybinding to stop swipes when Escape is pressed
        self.root.bind("<Escape>", self.stop_swipes)

        # Flag to control whether the swipes should continue
        self.swiping = False

        # Countdown label at the bottom with updated style
        self.countdown_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="#121212", fg="#FF5733")
        self.countdown_label.pack(side="bottom", pady=10)

        # Steps Section with improved layout and optimized text
        self.steps_label = tk.Label(root, text="How to Use:", font=("Helvetica", 18, "bold"), bg="#121212", fg="#FF5733")
        self.steps_label.pack(pady=10)

        self.steps_text = tk.Label(root, text="1. Open bumble.com/app in any browser.\n2. Click 'Start Swiping'.\n3. Focus the Bumble page by clicking anywhere.", font=("Helvetica", 14), bg="#121212", fg="#FFFFFF", justify="left", anchor="w")
        self.steps_text.pack(pady=15, padx=30, anchor="w")

    def right_swipe(self):
        try:
            self.swipe_count = int(self.swipe_count_var.get())
            if self.swipe_count <= 0:
                raise ValueError("Number of swipes must be greater than 0.")
        except ValueError:
            self.show_message("Invalid Input", "Please enter a valid positive integer for the number of swipes.")
            return

        try:
            self.interval = float(self.interval_var.get())
            if self.interval <= 0:
                raise ValueError("Time interval must be greater than 0.")
        except ValueError:
            self.show_message("Invalid Input", "Please enter a valid positive number for the time interval.")
            return

        # Start countdown and then begin swiping
        self.start_countdown()

    def start_countdown(self):
        """Starts the countdown before swiping begins"""
        countdown_time = 5

        def update_timer():
            nonlocal countdown_time
            if countdown_time > 0:
                self.countdown_label.config(text=f"Swiping will start in {countdown_time}...")
                self.root.after(1000, update_timer)  # Update every 1 second
                countdown_time -= 1
            else:
                self.countdown_label.config(text="")  # Clear the countdown label
                self.perform_swiping()  # Start swiping after countdown

        # Begin the countdown timer
        update_timer()

    def perform_swiping(self):
        """Function to perform the right swipes"""
        def swipe_thread():
            try:
                for _ in range(self.swipe_count):
                    if not self.swiping:  # If Escape key was pressed, stop swiping
                        break
                    pyautogui.press('right')
                    time.sleep(self.interval)

                if self.swiping:
                    self.show_message("Success", f"You swiped right on {self.swipe_count} people!")
            except Exception as e:
                self.show_message("Error", f"An error occurred: {e}")

        # Start swiping in a separate thread to avoid blocking UI
        self.swiping = True
        threading.Thread(target=swipe_thread).start()

    def stop_swipes(self, event):
        """Function to stop the swipes if Escape key is pressed"""
        self.swiping = False
        self.show_message("Stopped", "Swiping has been stopped.")

    def show_message(self, title, message):
        """Function to show message boxes in the main thread"""
        self.root.after(0, messagebox.showinfo, title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = RightSwipperApp(root)
    root.mainloop()
