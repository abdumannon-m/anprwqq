import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import json



# Function placeholders
def capture_and_process():
    pass

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_vehicle_data(new_data):
    with open('vehicle.json', 'w') as f:
         json.dump(new_data, f)

def add_vehicle():
    vehicles = load_json("vehicle.json")
    plate = license_entry.get().strip().upper()
    expiry = date_entry.get().strip()
    
    if not plate or not expiry:
        search_results_label.config(text="Iltimos ikkala fieldni to'ldiring")
        return
    
    vehicle_found = False
    
    # Check if the vehicle is already in the list
    for vehicle in vehicles:
        if vehicle['license_plate'] == plate:
            vehicle['expiry_date'] = expiry  # Update expiry date
            search_results_label.config(text=f"Updated {plate} with Expiry: {expiry}")
            vehicle_found = True
            break
    
    if not vehicle_found:
        # Add new vehicle
        vehicles.append({"license_plate": plate, "expiry_date": expiry})
        search_results_label.config(text=f"Added new vehicle {plate} with Expiry: {expiry}")
    
    # Save updated data
    save_vehicle_data(vehicles)

    # Clear input fields
    license_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    
    # Refresh vehicle list
    refresh_vehicle_list()

    # Function to refresh the vehicle list in the admin section
def refresh_vehicle_list():
    vehicle_list.delete(0, tk.END)
    vehicles = load_json("vehicle.json")
    
    for vehicle in vehicles:
        vehicle_list.insert(tk.END, f"Plate: {vehicle['license_plate']}, Expiry: {vehicle['expiry_date']}")



def search_vehicle():
    plate_to_search = search_entry.get().strip().upper()
    vehicle_found = False
    
    # Load the vehicle data
    vehicles = load_json("vehicle.json")
    
    # Search for the plate
    for vehicle in vehicles:
        if vehicle["license_plate"] == plate_to_search:
            search_results_label.config(text=f"License Plate: {vehicle['license_plate']}\nExpiry Date: {vehicle['expiry_date']}")
            vehicle_found = True
            break

    if not vehicle_found:
        search_results_label.config(text=f"Vehicle plate not found")




def generate_vehicle_cards(parent, vehicles):
    for widget in parent.winfo_children():
        widget.destroy()  # Clear the frame before updating
    for idx, vehicle in enumerate(vehicles):
        card_frame = ttk.Frame(parent, bootstyle="secondary", padding=10)
        card_frame.grid(row=idx//2, column=idx%2, padx=10, pady=10, sticky="nsew")  # Two cards per row

        # Text version of the license plate (top left)
        text_plate_label = ttk.Label(card_frame, text=f"Text Plate: {vehicle['text_plate']}", bootstyle="inverse")
        text_plate_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # License plate image placeholder (right)
        license_plate_label = ttk.Label(card_frame, text=f"License Plate: {vehicle['plate']}", bootstyle="inverse")
        license_plate_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Expiry date (bottom left)
        expiry_label = ttk.Label(card_frame, text=f"Expiry Date: {vehicle['expiry']}", bootstyle="inverse")
        expiry_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)

vehicles = [
    {"plate": "ABC123", "text_plate": "ABC123", "expiry": "2024-10-15"},
    {"plate": "XYZ456", "text_plate": "XYZ456", "expiry": "2025-01-10"},
] * 10  # Simulating 10 or 15 cards

# Main Window
window = ttk.Window(themename="flatly")
window.title("License Plate Recognition System")
window.geometry("900x600")

# Styling
button_style = {"bootstyle": SUCCESS, "padding": 10}

# Left Section: Live Camera Feed
camera_frame = ttk.Frame(window)
camera_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

# Camera Feed Subsection
live_feed_frame = ttk.LabelFrame(camera_frame, text="Live Camera Feed", padding=10, bootstyle="primary")
live_feed_frame.pack(fill="both", expand=True, padx=10, pady=10)

camera_label = ttk.Label(live_feed_frame, text="Camera Feed Here", bootstyle="inverse", width=40, anchor="center")
camera_label.pack(fill="both", expand=True, padx=10, pady=10)

capture_button = ttk.Button(live_feed_frame, text="Capture & Process", command=capture_and_process, **button_style)
capture_button.pack(pady=10)

# Vehicle Cards Subsection
cards_frame = ttk.LabelFrame(camera_frame, text="Vehicle Information", padding=10, bootstyle="primary")
cards_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Generate vehicle cards
generate_vehicle_cards(cards_frame, vehicles)

# Top Right Section: Vehicle Status (Divided into 2 parts)
status_frame = ttk.LabelFrame(window, text="Vehicle Status", padding=10, bootstyle="info")
status_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Vehicle Plate Section (Left Part)
vehicle_plate_frame = ttk.Frame(status_frame, padding=5, bootstyle="secondary")
vehicle_plate_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
vehicle_plate_frame.grid_columnconfigure(0, weight=1)  # Ensure it fills available space
vehicle_plate_frame.grid_rowconfigure(0, weight=1)

vehicle_plate_label = ttk.Label(vehicle_plate_frame, text="Vehicle Plate: ABC123", bootstyle="inverse")
vehicle_plate_label.pack(fill="both", padx=5, pady=5)

# License Plate and Expiry Date Section (Right Part)
info_frame = ttk.Frame(status_frame, padding=5, bootstyle="secondary")
info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
info_frame.grid_columnconfigure(0, weight=1)  # Ensure it fills available space
info_frame.grid_rowconfigure(0, weight=1)
info_frame.grid_rowconfigure(1, weight=1)

license_plate_text_label = ttk.Label(info_frame, text="License Plate: ABC123", bootstyle="inverse")
license_plate_text_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

expiry_date_label = ttk.Label(info_frame, text="Expiry Date: 2024-10-15", bootstyle="inverse")
expiry_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Bottom Right Section: Admin Panel
controls_frame = ttk.LabelFrame(window, text="Admin Controls", padding=10, bootstyle="secondary")
controls_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# Add Vehicle Controls
add_frame = ttk.Frame(controls_frame)
add_frame.pack(pady=10)

license_label = ttk.Label(add_frame, text="Mashina raqami (01A999AA):")
license_label.grid(row=0, column=0, padx=5, pady=5)
license_entry = ttk.Entry(add_frame)
license_entry.grid(row=0, column=1, padx=5, pady=5)

date_label = ttk.Label(add_frame, text="Ruxsatnoma Muddati (YIL-OY-KUN):")
date_label.grid(row=1, column=0, padx=5, pady=5)
date_entry = ttk.Entry(add_frame)
date_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Qo'shish/Yangilash", command=add_vehicle, **button_style)
add_button.grid(row=2, columnspan=2, pady=10)

# Search Vehicle Controls
search_frame = ttk.Frame(controls_frame)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Raqam qidirish (01A999AA):")
search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Qidirish", command=search_vehicle, **button_style)
search_button.grid(row=1, columnspan=2, pady=10)

search_results_label = ttk.Label(search_frame, text="", bootstyle="inverse", anchor="center")
search_results_label.grid(row=2, columnspan=2, pady=10)

# Vehicle List
list_frame = ttk.Frame(controls_frame)
list_frame.pack(fill="both", expand=True, pady=10)

vehicle_list = tk.Listbox(list_frame)
vehicle_list.pack(fill="both", expand=True, padx=5, pady=5)

# Adjust grid weights for responsiveness
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=1)

# Start the GUI loop
window.mainloop()
