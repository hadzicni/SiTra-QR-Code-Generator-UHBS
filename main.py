import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import main
import os
import subprocess
import random
from tkcalendar import DateEntry
from datetime import datetime, date
import json
from PIL import Image, ImageTk
import io

class QRCodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SiTra QR Code Generator")
        self.root.geometry("500x750")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TLabel', padding=5)
        self.style.configure('TEntry', padding=5)
        self.style.configure('TButton', padding=5)
        self.style.configure('TCombobox', padding=5)
        self.style.configure('TCheckbutton', padding=5)
        
        # Create menu bar
        self.create_menu()
        
        # Create main frame with scrollbar
        main_canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
        self.main_frame = ttk.Frame(main_canvas, padding="20")
        
        # Configure scrolling
        main_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas scrolling
        def configure_scroll_region(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        self.main_frame.bind("<Configure>", configure_scroll_region)
        
        # Title
        title_label = ttk.Label(self.main_frame, text="SiTra Test QR Code Generator", 
                              font=('Helvetica', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # First Name
        ttk.Label(self.main_frame, text="First Name:").grid(row=1, column=0, sticky=tk.W)
        first_name_frame = ttk.Frame(self.main_frame)
        first_name_frame.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_first = tk.BooleanVar(value=True)
        self.random_first_check = ttk.Checkbutton(
            first_name_frame,
            text="Random",
            variable=self.use_random_first,
            command=self.toggle_name_fields
        )
        self.random_first_check.pack(side=tk.LEFT)
        
        self.first_name = ttk.Entry(first_name_frame, width=25, state='disabled')
        self.first_name.insert(0, "Random")
        self.first_name.pack(side=tk.LEFT, padx=5)
        
        # Last Name
        ttk.Label(self.main_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W)
        last_name_frame = ttk.Frame(self.main_frame)
        last_name_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_last = tk.BooleanVar(value=True)
        self.random_last_check = ttk.Checkbutton(
            last_name_frame,
            text="Random",
            variable=self.use_random_last,
            command=self.toggle_name_fields
        )
        self.random_last_check.pack(side=tk.LEFT)
        
        self.last_name = ttk.Entry(last_name_frame, width=25, state='disabled')
        self.last_name.insert(0, "Random")
        self.last_name.pack(side=tk.LEFT, padx=5)
        
        # Birth Date
        ttk.Label(self.main_frame, text="Birth Date:").grid(row=3, column=0, sticky=tk.W)
        birth_date_frame = ttk.Frame(self.main_frame)
        birth_date_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_date = tk.BooleanVar(value=True)
        self.random_date_check = ttk.Checkbutton(
            birth_date_frame,
            text="Random",
            variable=self.use_random_date,
            command=self.toggle_date_picker
        )
        self.random_date_check.pack(side=tk.LEFT)
        
        self.birth_date = DateEntry(
            birth_date_frame,
            width=15,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            year=1970,
            mindate=date(1970, 1, 1),
            maxdate=date.today(),
            state='disabled',
            date_pattern='dd.mm.yyyy'  # Using the same format as in main.py
        )
        self.birth_date.pack(side=tk.LEFT, padx=5)
        
        # Blood Product
        ttk.Label(self.main_frame, text="Blood Product:").grid(row=4, column=0, sticky=tk.W)
        blood_product_frame = ttk.Frame(self.main_frame)
        blood_product_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_product = tk.BooleanVar(value=True)
        self.random_product_check = ttk.Checkbutton(
            blood_product_frame,
            text="Random",
            variable=self.use_random_product,
            command=lambda: self.blood_product.configure(
                state='disabled' if self.use_random_product.get() else 'readonly'
            )
        )
        self.random_product_check.pack(side=tk.LEFT)
        
        self.blood_product = ttk.Combobox(blood_product_frame, width=22, state="disabled")
        self.blood_product['values'] = list(main.BLOOD_PRODUCTS.keys())
        self.blood_product.pack(side=tk.LEFT, padx=5)
        
        # Patient Blood Group
        ttk.Label(self.main_frame, text="Patient Blood Group:").grid(row=5, column=0, sticky=tk.W)
        patient_blood_frame = ttk.Frame(self.main_frame)
        patient_blood_frame.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_patient_group = tk.BooleanVar(value=True)
        self.random_patient_group_check = ttk.Checkbutton(
            patient_blood_frame,
            text="Random",
            variable=self.use_random_patient_group,
            command=self.toggle_blood_fields
        )
        self.random_patient_group_check.pack(side=tk.LEFT)
        
        self.patient_blood_group = ttk.Combobox(patient_blood_frame, width=22, state="disabled")
        blood_groups = [group.split("|")[0] for group in main.BLOOD_GROUPS]
        self.patient_blood_group['values'] = blood_groups
        self.patient_blood_group.pack(side=tk.LEFT, padx=5)
        
        # Product Blood Group
        ttk.Label(self.main_frame, text="Product Blood Group:").grid(row=6, column=0, sticky=tk.W)
        product_blood_frame = ttk.Frame(self.main_frame)
        product_blood_frame.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_product_group = tk.BooleanVar(value=True)
        self.random_product_group_check = ttk.Checkbutton(
            product_blood_frame,
            text="Random",
            variable=self.use_random_product_group,
            command=self.toggle_blood_fields
        )
        self.random_product_group_check.pack(side=tk.LEFT)
        
        self.product_blood_group = ttk.Combobox(product_blood_frame, width=22, state="disabled")
        self.product_blood_group['values'] = blood_groups
        self.product_blood_group.pack(side=tk.LEFT, padx=5)
        
        # Station ID
        ttk.Label(self.main_frame, text="Station ID:").grid(row=7, column=0, sticky=tk.W)
        station_frame = ttk.Frame(self.main_frame)
        station_frame.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.use_random_station = tk.BooleanVar(value=True)
        self.random_station_check = ttk.Checkbutton(
            station_frame,
            text="Random",
            variable=self.use_random_station,
            command=self.toggle_station_field
        )
        self.random_station_check.pack(side=tk.LEFT)
        
        self.station_id = ttk.Combobox(station_frame, width=22, state="disabled")
        self.station_id['values'] = main.STATION_IDS
        self.station_id.pack(side=tk.LEFT, padx=5)
        
        # Expiration Days
        ttk.Label(self.main_frame, text="Expiration Days:").grid(row=8, column=0, sticky=tk.W)
        expiry_frame = ttk.Frame(self.main_frame)
        expiry_frame.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.expiry_days = ttk.Spinbox(
            expiry_frame,
            from_=1,
            to=30,
            width=5
        )
        self.expiry_days.set("7")
        self.expiry_days.pack(side=tk.LEFT)
        ttk.Label(expiry_frame, text="days").pack(side=tk.LEFT, padx=5)
        
        # PDF Options Frame
        pdf_frame = ttk.LabelFrame(self.main_frame, text="PDF Options", padding=10)
        pdf_frame.grid(row=9, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Output Directory
        ttk.Label(pdf_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        dir_frame = ttk.Frame(pdf_frame)
        dir_frame.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.output_dir = ttk.Entry(dir_frame, width=30)
        self.output_dir.insert(0, os.getcwd())
        self.output_dir.pack(side=tk.LEFT, padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.pack(side=tk.LEFT)
        
        # File Name Format
        ttk.Label(pdf_frame, text="File Name Format:").grid(row=1, column=0, sticky=tk.W)
        self.filename_format = ttk.Entry(pdf_frame, width=40)
        self.filename_format.insert(0, "sitra_qr_codes_%H-%M-%S")
        self.filename_format.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Auto-open PDF
        self.auto_open = tk.BooleanVar(value=True)
        ttk.Checkbutton(pdf_frame, text="Open PDF after generation", 
                       variable=self.auto_open).grid(row=2, column=0, 
                       columnspan=2, sticky=tk.W, pady=5)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=10, column=0, columnspan=2, pady=10)
        
        # Preview Button
        preview_btn = ttk.Button(buttons_frame, text="Preview QR Codes", 
                               command=self.preview_qr_codes)
        preview_btn.pack(pady=(0, 5))
        
        # Generate Button
        generate_btn = ttk.Button(buttons_frame, text="Generate PDF", 
                                command=self.save_pdf)
        generate_btn.pack()
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Load settings
        self.load_settings()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Preview QR Codes", command=self.preview_qr_codes)
        file_menu.add_command(label="Set Output Directory", command=self.browse_output_dir)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(initialdir=self.output_dir.get())
        if dir_path:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, dir_path)
            self.save_settings()

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x200")
        
        # Make window modal
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Add content frame
        content_frame = ttk.Frame(about_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(content_frame, 
                 text="SiTra QR Code Generator", 
                 font=('Helvetica', 14, 'bold')).pack(pady=(0, 10))
        
        # Version
        ttk.Label(content_frame, 
                 text="Version 1.0").pack(pady=(0, 20))
        
        # Description
        ttk.Label(content_frame, 
                 text="A tool for generating QR codes for blood products").pack(pady=(0, 20))
        
        # GitHub link
        link_frame = ttk.Frame(content_frame)
        link_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(link_frame, text="GitHub Repository:").pack(side=tk.LEFT)
        
        github_link = ttk.Label(link_frame, 
                              text=main.GITHUB_REPO_URL,
                              foreground="blue",
                              cursor="hand2")
        github_link.pack(side=tk.LEFT, padx=(5, 0))
        
        # Make link clickable
        github_link.bind("<Button-1>", lambda e: os.startfile(main.GITHUB_REPO_URL))
        
        # Close button
        ttk.Button(content_frame, 
                  text="Close",
                  command=about_window.destroy).pack(pady=(0, 10))
        
        # Center the window
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = about_window.winfo_rootx() + (about_window.winfo_width() // 2) - (width // 2)
        y = about_window.winfo_rooty() + (about_window.winfo_height() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')

    def save_settings(self):
        settings = {
            'output_dir': self.output_dir.get(),
            'filename_format': self.filename_format.get(),
            'auto_open': self.auto_open.get()
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.output_dir.delete(0, tk.END)
                self.output_dir.insert(0, settings.get('output_dir', os.getcwd()))
                self.filename_format.delete(0, tk.END)
                self.filename_format.insert(0, settings.get('filename_format', 'sitra_qr_codes_%H-%M-%S'))
                self.auto_open.set(settings.get('auto_open', True))
        except Exception as e:
            print(f"Error loading settings: {e}")

    def toggle_date_picker(self):
        if self.use_random_date.get():
            self.birth_date.configure(state='disabled')
        else:
            self.birth_date.configure(state='normal')

    def toggle_name_fields(self):
        # Toggle first name field
        if self.use_random_first.get():
            self.first_name.configure(state='disabled')
            self.first_name.delete(0, tk.END)
            self.first_name.insert(0, "Random")
        else:
            self.first_name.configure(state='normal')
            self.first_name.delete(0, tk.END)
        
        # Toggle last name field
        if self.use_random_last.get():
            self.last_name.configure(state='disabled')
            self.last_name.delete(0, tk.END)
            self.last_name.insert(0, "Random")
        else:
            self.last_name.configure(state='normal')
            self.last_name.delete(0, tk.END)

    def toggle_blood_fields(self):
        # Toggle patient blood group
        if self.use_random_patient_group.get():
            self.patient_blood_group.configure(state='disabled')
            self.patient_blood_group.delete(0, tk.END)
        else:
            self.patient_blood_group.configure(state='readonly')
            self.patient_blood_group.set(self.patient_blood_group['values'][0])
            
        # Toggle product blood group
        if self.use_random_product_group.get():
            self.product_blood_group.configure(state='disabled')
            self.product_blood_group.delete(0, tk.END)
        else:
            self.product_blood_group.configure(state='readonly')
            self.product_blood_group.set(self.product_blood_group['values'][0])

    def toggle_station_field(self):
        if self.use_random_station.get():
            self.station_id.configure(state='disabled')
            self.station_id.delete(0, tk.END)
        else:
            self.station_id.configure(state='readonly')
            self.station_id.set(self.station_id['values'][0])

    def get_birth_date(self):
        if self.use_random_date.get():
            return main.generate_random_birthdate()
        return self.birth_date.get_date()

    def preview_qr_codes(self):
        try:
            # Get all the values as before
            first_name = None if self.use_random_first.get() else self.first_name.get().strip()
            last_name = None if self.use_random_last.get() else self.last_name.get().strip()
            blood_product = None if self.use_random_product.get() else self.blood_product.get()
            
            if self.use_random_patient_group.get() and self.use_random_product_group.get():
                blood_group = None
            else:
                patient_group = self.patient_blood_group.get() if not self.use_random_patient_group.get() else random.choice([g.split("|")[0] for g in main.BLOOD_GROUPS])
                product_group = self.product_blood_group.get() if not self.use_random_product_group.get() else random.choice([g.split("|")[0] for g in main.BLOOD_GROUPS])
                blood_group = f"{patient_group}|{product_group}|"
            
            station_id = None if self.use_random_station.get() else self.station_id.get()
            birth_date = self.get_birth_date()
            expiry_days = int(self.expiry_days.get())
            
            # Generate new patient data
            patient_data = main.generate_patient_data(
                first_name=first_name,
                last_name=last_name,
                blood_product=blood_product,
                blood_group=blood_group,
                station_id=station_id,
                birth_date=birth_date,
                expiry_days=expiry_days
            )
            
            # Get QR code contents
            contents = main.generate_content_strings(patient_data)
            
            # Generate QR codes
            qr_codes = []
            for content in contents:
                qr = main.generate_qr_code(content)
                img_byte_arr = io.BytesIO()
                qr.save(img_byte_arr, format='PNG')
                qr_codes.append(img_byte_arr.getvalue())
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("QR Code Preview")
            preview_window.geometry("800x800")
            
            # Create canvas with scrollbar
            canvas = tk.Canvas(preview_window)
            scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add title labels
            titles = ["Bloodproduct", "Meona Code", "Patient wristband (Fall-ID)"]
            
            # Add QR codes to preview
            for i, (qr, title, content) in enumerate(zip(qr_codes, titles, contents)):
                # Create frame for each QR code
                qr_frame = ttk.Frame(scrollable_frame)
                qr_frame.pack(pady=20)
                
                # Add title
                ttk.Label(qr_frame, text=title, font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
                
                # Convert QR code to PhotoImage
                img = Image.open(io.BytesIO(qr))
                photo = ImageTk.PhotoImage(img)
                
                # Display QR code
                label = ttk.Label(qr_frame, image=photo)
                label.image = photo  # Keep a reference
                label.pack()
                
                # Add content label
                content_label = ttk.Label(qr_frame, text="Content:", font=('Helvetica', 10, 'bold'))
                content_label.pack(pady=(10, 0))
                
                # Add content in a text widget for better display and copy-paste
                content_text = tk.Text(qr_frame, height=2, width=60, wrap=tk.WORD)
                content_text.insert('1.0', content)
                content_text.configure(state='disabled')  # Make it read-only
                content_text.pack(padx=10)
            
            # Add buttons
            button_frame = ttk.Frame(preview_window)
            button_frame.pack(fill=tk.X, padx=10, pady=10)
            
            ttk.Button(button_frame, text="Generate PDF", 
                      command=lambda: [self.save_pdf(), preview_window.destroy()]).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Close", 
                      command=preview_window.destroy).pack(side=tk.RIGHT, padx=5)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_pdf(self):
        try:
            # Get all the values
            first_name = None if self.use_random_first.get() else self.first_name.get().strip()
            last_name = None if self.use_random_last.get() else self.last_name.get().strip()
            blood_product = None if self.use_random_product.get() else self.blood_product.get()
            
            if self.use_random_patient_group.get() and self.use_random_product_group.get():
                blood_group = None
            else:
                patient_group = self.patient_blood_group.get() if not self.use_random_patient_group.get() else random.choice([g.split("|")[0] for g in main.BLOOD_GROUPS])
                product_group = self.product_blood_group.get() if not self.use_random_product_group.get() else random.choice([g.split("|")[0] for g in main.BLOOD_GROUPS])
                blood_group = f"{patient_group}|{product_group}|"
            
            station_id = None if self.use_random_station.get() else self.station_id.get()
            birth_date = self.get_birth_date()
            expiry_days = int(self.expiry_days.get())
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime(self.filename_format.get())
            pdf_file_path = os.path.join(self.output_dir.get(), f"{timestamp}.pdf")
            
            # Generate new patient data and create PDF
            patient_data = main.generate_patient_data(
                first_name=first_name,
                last_name=last_name,
                blood_product=blood_product,
                blood_group=blood_group,
                station_id=station_id,
                birth_date=birth_date,
                expiry_days=expiry_days
            )
            
            # Get QR code contents
            contents = main.generate_content_strings(patient_data)
            
            # Generate QR codes
            qr_codes = []
            for content in contents:
                qr = main.generate_qr_code(content)
                img_byte_arr = io.BytesIO()
                qr.save(img_byte_arr, format='PNG')
                qr_codes.append(img_byte_arr.getvalue())
            
            # Create PDF
            pdf_buffer = main.generate_pdf_from_qrcodes(qr_codes, patient_data)
            
            # Save the PDF
            with open(pdf_file_path, "wb") as f:
                f.write(pdf_buffer.getvalue())
            
            # Open the generated PDF if auto-open is enabled
            if self.auto_open.get():
                os.startfile(pdf_file_path)
            
            # Show success message
            messagebox.showinfo("Success", f"QR codes generated successfully!\nSaved to: {pdf_file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorGUI(root)
    root.mainloop()
