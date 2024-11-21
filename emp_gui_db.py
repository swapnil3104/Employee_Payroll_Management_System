import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tkcalendar import DateEntry 
import os

class EmployeePMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee PMS")
        self.root.geometry("1050x700")  # Adjust window size to accommodate side-by-side layout
        self.root.resizable(False, False)
        # Connect to SQLite database
        self.conn = sqlite3.connect('employee_pms.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if they do not exist
        self.create_tables()
        
        # Create main container and grid layout for side-by-side sections
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        
        # Employee Details Section (Left side)
        self.create_employee_details(container)
        
        # Salary Details Section (Right side)
        self.create_salary_details(container)

    def create_tables(self):
        # Create employee table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
            emp_code TEXT NOT NULL,
            designation TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            dob TEXT,
            doj TEXT,
            experience TEXT,
            proof_id TEXT,
            contact TEXT,
            status TEXT,
            address TEXT
        )''')

        # Create salary table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS salary_details (
            emp_code TEXT NOT NULL,
            month TEXT,
            year INTEGER,
            salary INTEGER,
            total_days INTEGER,
            absents INTEGER,
            medical REAL,
            convence REAL,
            pf REAL,
            net_salary REAL
        )''')

        # Commit the changes to the database
        self.conn.commit()

#-------------------------------------------------------------------------GUI-------------------------------------------------------------------------
    
    def create_employee_details(self, container):
               # Frame for Employee Details (Left side)
        employee_frame = ttk.LabelFrame(container, text="Employee Details", padding="20")
        employee_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Grid in left column
        
        # Employee Code
        ttk.Label(employee_frame, text="Employee Code*").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.emp_code_entry = ttk.Entry(employee_frame, width=30)
        self.emp_code_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.emp_code_entry.insert(0, "EMP-XXXX")
        self.emp_code_entry.bind('<FocusIn>', lambda e: self.on_entry_click(self.emp_code_entry, "EMP-XXXX"))
        self.emp_code_entry.bind('<FocusOut>', lambda e: self.on_focus_out(self.emp_code_entry, "EMP-XXXX"))
        
        # Fetch Button
        fetch_button = ttk.Button(employee_frame, text="Fetch Data", command=self.fetch_employee_data)
        fetch_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Employee Designation
        ttk.Label(employee_frame, text="Employee Designation*").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.designation_field = ttk.Combobox(employee_frame, width=27, 
            values=["Software Engineer", "Manager", "HR", "Sales", "Support", "Marketing", "Other"])
        self.designation_field.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.designation_field.set("Select Designation")
        
        # Employee Name
        ttk.Label(employee_frame, text="Employee Name*").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.name_field = ttk.Entry(employee_frame, width=30)
        self.name_field.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.name_field.insert(0, "Full Name")
        self.name_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.name_field, "Full Name"))
        self.name_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.name_field, "Full Name"))
        
        # Age
        ttk.Label(employee_frame, text="Age*").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.age_field = ttk.Entry(employee_frame, width=30)
        self.age_field.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.age_field.insert(0, "18-60")
        self.age_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.age_field, "18-60"))
        self.age_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.age_field, "18-60"))
        
        # Gender
        ttk.Label(employee_frame, text="Gender*").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.gender_field = ttk.Combobox(employee_frame, width=27, 
            values=["Male", "Female", "Other"])
        self.gender_field.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.gender_field.set("Select Gender")
        
        # Email
        ttk.Label(employee_frame, text="Email*").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.email_field = ttk.Entry(employee_frame, width=30)
        self.email_field.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.email_field.insert(0, "example@company.com")
        self.email_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.email_field, "example@company.com"))
        self.email_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.email_field, "example@company.com"))
        
        # Date of Birth
        ttk.Label(employee_frame, text="Date of Birth*").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.dob_field = DateEntry(employee_frame, width=27, 
            background='darkblue', foreground='white', borderwidth=2, 
            date_pattern='yyyy-mm-dd')
        self.dob_field.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        
        # Date of Joining
        ttk.Label(employee_frame, text="Date of Joining*").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.doj_field = DateEntry(employee_frame, width=27, 
            background='darkblue', foreground='white', borderwidth=2, 
            date_pattern='yyyy-mm-dd')
        self.doj_field.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        
        # Experience
        ttk.Label(employee_frame, text="Experience (Years)*").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.experience_field = ttk.Entry(employee_frame, width=30)
        self.experience_field.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.experience_field.insert(0, "0-50")
        self.experience_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.experience_field, "0-50"))
        self.experience_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.experience_field, "0-50"))
        
        # Proof ID
        ttk.Label(employee_frame, text="Proof ID*").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.proof_id_field = ttk.Entry(employee_frame, width=30)
        self.proof_id_field.grid(row=9, column=1, padx=5, pady=5, sticky="w")
        self.proof_id_field.insert(0, "Aadhar/PAN/Passport")
        self.proof_id_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.proof_id_field, "Aadhar/PAN/Passport"))
        self.proof_id_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.proof_id_field, "Aadhar/PAN/Passport"))
        
        # Contact Number
        ttk.Label(employee_frame, text="Contact Number*").grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.contact_field = ttk.Entry(employee_frame, width=30)
        self.contact_field.grid(row=10, column=1, padx=5, pady=5, sticky="w")
        self.contact_field.insert(0, "+91XXXXXXXXXX")
        self.contact_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.contact_field, "+91XXXXXXXXXX"))
        self.contact_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.contact_field, "+91XXXXXXXXXX"))
        
        # Status
        ttk.Label(employee_frame, text="Status*").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.status_field = ttk.Combobox(employee_frame, width=27, 
            values=["Active", "Inactive", "Probation", "On Leave"])
        self.status_field.grid(row=11, column=1, padx=5, pady=5, sticky="w")
        self.status_field.set("Select Status")
        
        # Address
        ttk.Label(employee_frame, text="Address*").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.address_text = tk.Text(employee_frame, height=4, width=30)
        self.address_text.grid(row=12, column=1, padx=5, pady=5)
        self.address_text.insert(tk.END, "Full Postal Address")
        self.address_text.bind('<FocusIn>', lambda e: self.on_text_click(self.address_text, "Full Postal Address"))
        self.address_text.bind('<FocusOut>', lambda e: self.on_text_focus_out(self.address_text, "Full Postal Address"))
        
        # Buttons: Save Employee, Clear Form
        button_frame = ttk.Frame(employee_frame)
        button_frame.grid(row=14, column=1, pady=10, sticky="e")
        
        save_button = ttk.Button(button_frame, text="Save Employee", command=self.save_employee_data)
        save_button.grid(row=0, column=0, padx=5, pady=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Form", command=self.clear_employee_form)
        clear_button.grid(row=0, column=1, padx=5, pady=5)

    def on_entry_click(self, entry, placeholder):
        """Handle focus in for Entry widgets"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(self, entry, placeholder):
        """Handle focus out for Entry widgets"""
        if entry.get().strip() == '':
            entry.insert(0, placeholder)
            entry.config(foreground='gray')

    def on_text_click(self, text_widget, placeholder):
        """Handle focus in for Text widgets"""
        if text_widget.get("1.0", tk.END).strip() == placeholder:
            text_widget.delete("1.0", tk.END)
            text_widget.config(foreground='black')

    def on_text_focus_out(self, text_widget, placeholder):
        """Handle focus out for Text widgets"""
        if text_widget.get("1.0", tk.END).strip() == '':
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, placeholder)
            text_widget.config(foreground='gray')

    def clear_employee_form(self):
        """Clear all form fields"""
        # Reset Entry fields
        fields_to_reset = [
            (self.emp_code_entry, "EMP-XXXX"),
            (self.name_field, "Full Name"),
            (self.age_field, "18-60"),
            (self.email_field, "example@company.com"),
            (self.experience_field, "0-50"),
            (self.proof_id_field, "Aadhar/PAN/Passport"),
            (self.contact_field, "+91XXXXXXXXXX")
        ]
        
        for field, placeholder in fields_to_reset:
            field.delete(0, tk.END)
            field.insert(0, placeholder)
            field.config(foreground='gray')
        
        # Reset Comboboxes
        self.designation_field.set("Select Designation")
        self.gender_field.set("Select Gender")
        self.status_field.set("Select Status")
        
        # Reset Date fields
        self.dob_field.set_date(None)
        self.doj_field.set_date(None)
        
        # Reset Address
        self.address_text.delete("1.0", tk.END)
        self.address_text.insert(tk.END, "Full Postal Address")
        self.address_text.config(foreground='gray')

#---------------------------------------------------------Code to fatch Employee---------------------------------------------------------------
    
    def fetch_employee_data(self):
        # Fetch employee data based on Employee Code
        emp_code = self.emp_code_entry.get()
        if not emp_code:
            messagebox.showerror("Error", "Please enter Employee Code.")
            return

        # Query the database for the employee details
        self.cursor.execute('''SELECT * FROM employee WHERE emp_code = ?''', (emp_code,))
        employee_data = self.cursor.fetchone()

        self.display_text_area.config(state='normal')  
        display_text = "EMPLOYEE DETAILS\n"

        if employee_data:
            # Populate employee fields with the fetched data
            self.name_field.delete(0, tk.END)
            self.name_field.insert(0, employee_data[1])  # Name
            self.age_field.delete(0, tk.END)
            self.age_field.insert(0, employee_data[2])  # Age
            self.designation_field.delete(0, tk.END)
            self.designation_field.insert(0, employee_data[3])  # Designation
            self.gender_field.set(employee_data[4])  # Gender
            self.email_field.delete(0, tk.END)
            self.email_field.insert(0, employee_data[5])  # Email
            self.dob_field.delete(0, tk.END)
            self.dob_field.insert(0, employee_data[6])  # Date of Birth
            self.doj_field.delete(0, tk.END)
            self.doj_field.insert(0, employee_data[7])  # Date of Joining
            self.experience_field.delete(0, tk.END)
            self.experience_field.insert(0, employee_data[8])  # Experience
            self.proof_id_field.delete(0, tk.END)
            self.proof_id_field.insert(0, employee_data[9])  # Proof ID
            self.contact_field.delete(0, tk.END)
            self.contact_field.insert(0, employee_data[10])  # Contact
            self.status_field.set(employee_data[11])  # Status
            self.address_text.delete(1.0, tk.END)
            self.address_text.insert(tk.END, employee_data[12])  # Address
            
            # Now, fetch salary details
            self.cursor.execute('''SELECT * FROM salary_details WHERE emp_code = ?''', (emp_code,))
            salary_data = self.cursor.fetchone()
            
            display_text += "-" * 30 + "\n"
            display_text += f"Employee Code    : {employee_data[0]}\n"
            display_text += f"Name             : {employee_data[2]}\n"
            display_text += f"Designation      : {employee_data[1]}\n"
            display_text += f"Age              : {employee_data[3]}\n"
            display_text += f"Gender           : {employee_data[4]}\n"
            display_text += f"Email            : {employee_data[5]}\n"
            display_text += f"Date of Birth    : {employee_data[6]}\n"
            display_text += f"Date of Joining  : {employee_data[7]}\n"
            display_text += f"Experience       : {employee_data[8]}\n"
            display_text += f"Proof ID         : {employee_data[9]}\n"
            display_text += f"Contact          : {employee_data[10]}\n"
            display_text += f"Status           : {employee_data[11]}\n"
            display_text += f"Address          : {employee_data[12].strip()}\n\n"

            if salary_data:
                # Populate salary fields with the fetched data
                self.month_field.delete(0, tk.END)
                self.month_field.insert(0, salary_data[1])  # Month
                self.year_field.delete(0, tk.END)
                self.year_field.insert(0, salary_data[2])  # Year
                self.salary_field.delete(0, tk.END)
                self.salary_field.insert(0, salary_data[3])  # Salary
                self.total_days_field.delete(0, tk.END)
                self.total_days_field.insert(0, salary_data[4])  # Total Days
                self.absents_field.delete(0, tk.END)
                self.absents_field.insert(0, salary_data[5])  # Absents
                self.medical_field.delete(0, tk.END)
                self.medical_field.insert(0, salary_data[6])  # Medical
                self.convence_field.delete(0, tk.END)
                self.convence_field.insert(0, salary_data[7])  # Convence
                self.pf_field.delete(0, tk.END)
                self.pf_field.insert(0, salary_data[8])  # PF
                self.net_salary_field.delete(0, tk.END)
                self.net_salary_field.insert(0, salary_data[9])  # Net Salary
                
                display_text += "SALARY DETAILS\n"
                display_text += "-" * 30 + "\n"
                display_text += f"Month                 : {salary_data[1]}\n"
                display_text += f"Year                  : {salary_data[2]}\n"
                display_text += f"Total Salary          : Rs.{salary_data[3]}\n"
                display_text += f"Total Working Days    : {salary_data[4]}\n"
                display_text += f"Absents               : {salary_data[5]}\n"
                display_text += f"Medical Allowance     : Rs.{salary_data[6]}\n"
                display_text += f"Conveyance Allowance  : Rs.{salary_data[7]}\n"
                display_text += f"Provident Fund        : Rs.{salary_data[8]}\n"
                display_text += f"Net Salary            : Rs.{salary_data[9]}\n"
            else:
                # If no salary data is found for the employee
                messagebox.showinfo("Info", "No salary data found for this Employee Code.")
            
        else:
            messagebox.showerror("Error", "No data found for the provided Employee Code.")
        
        self.display_text_area.insert(tk.END, display_text)
        self.display_text_area.config(state='disabled')  

    def create_salary_details(self, container):
              # Frame for Salary Details (Right side)
        salary_frame = ttk.LabelFrame(container, text="Salary Details", padding="20")
        salary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Grid in right column
        
        # Month (Dropdown)
        ttk.Label(salary_frame, text="Month*").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.month_field = ttk.Combobox(salary_frame, width=27, 
            values=["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"])
        self.month_field.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.month_field.set("Select Month")
        
        # Year (Current Year as Default)
        ttk.Label(salary_frame, text="Year*").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        current_year = datetime.now().year
        self.year_field = ttk.Combobox(salary_frame, width=27, 
            values=[str(year) for year in range(current_year-5, current_year+2)])
        self.year_field.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.year_field.set(str(current_year))
        
        # Salary
        ttk.Label(salary_frame, text="Base Salary*").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.salary_field = ttk.Entry(salary_frame, width=30)
        self.salary_field.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.salary_field.insert(0, "Enter Base Salary")
        self.salary_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.salary_field, "Enter Base Salary"))
        self.salary_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.salary_field, "Enter Base Salary"))
        
        # Total Days
        ttk.Label(salary_frame, text="Total Working Days*").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.total_days_field = ttk.Entry(salary_frame, width=30)
        self.total_days_field.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.total_days_field.insert(0, "0-31")
        self.total_days_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.total_days_field, "0-31"))
        self.total_days_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.total_days_field, "0-31"))
        
        # Absents
        ttk.Label(salary_frame, text="Absent Days").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.absents_field = ttk.Entry(salary_frame, width=30)
        self.absents_field.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.absents_field.insert(0, "0")
        self.absents_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.absents_field, "0"))
        self.absents_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.absents_field, "0"))
        
        # Medical Allowance
        ttk.Label(salary_frame, text="Medical Allowance").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.medical_field = ttk.Entry(salary_frame, width=30)
        self.medical_field.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.medical_field.insert(0, "Medical Allowance")
        self.medical_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.medical_field, "Medical Allowance"))
        self.medical_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.medical_field, "Medical Allowance"))
        
        # Conveyance Allowance
        ttk.Label(salary_frame, text="Conveyance Allowance").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.convence_field = ttk.Entry(salary_frame, width=30)
        self.convence_field.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.convence_field.insert(0, "Conveyance Allowance")
        self.convence_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.convence_field, "Conveyance Allowance"))
        self.convence_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.convence_field, "Conveyance Allowance"))
        
        # Provident Fund (PF)
        ttk.Label(salary_frame, text="Provident Fund (%)").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.pf_field = ttk.Entry(salary_frame, width=30)
        self.pf_field.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        self.pf_field.insert(0, "PF Percentage")
        self.pf_field.bind('<FocusIn>', lambda e: self.on_entry_click(self.pf_field, "PF Percentage"))
        self.pf_field.bind('<FocusOut>', lambda e: self.on_focus_out(self.pf_field, "PF Percentage"))
        
        # Net Salary (Calculated)
        ttk.Label(salary_frame, text="Net Salary").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.net_salary_field = ttk.Entry(salary_frame, width=30, state="readonly")
        self.net_salary_field.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        # Calculate Net Salary Button
        calculate_button = ttk.Button(salary_frame, text="Calculate Net Salary", command=self.calculate_net_salary)
        calculate_button.grid(row=9, column=1, padx=5, pady=5, sticky="e")
        
          # Buttons: Calculate Salary, Save Salary, Clear Salary Form
        button_frame = ttk.Frame(salary_frame)
        button_frame.grid(row=9, column=1, pady=10, sticky="e")
        
        calc_button = ttk.Button(button_frame, text="Calculate Salary", command=self.calculate_salary)
        calc_button.grid(row=0, column=0, padx=5, pady=5)
        
        save_salary_button = ttk.Button(button_frame, text="Save Salary", command=self.save_salary_data)
        save_salary_button.grid(row=0, column=1, padx=5, pady=5)
        
        clear_salary_button = ttk.Button(button_frame, text="Clear Salary Form", command=self.clear_salary_form)
        clear_salary_button.grid(row=0, column=2, padx=5, pady=5)
        
        button_frame = ttk.Frame(salary_frame)
        button_frame.grid(row=9, column=1, pady=10, sticky="e")
        
        calc_button = ttk.Button(button_frame, text="Calculate Salary", command=self.calculate_salary)
        calc_button.grid(row=0, column=0, padx=5, pady=5)
        
        save_salary_button = ttk.Button(button_frame, text="Save Salary", command=self.save_salary_data)
        save_salary_button.grid(row=0, column=1, padx=5, pady=5)
        
        clear_salary_button = ttk.Button(button_frame, text="Clear Salary Form", command=self.clear_salary_form)
        clear_salary_button.grid(row=0, column=2, padx=5, pady=5)
        
        # New Print PDF button
        print_pdf_button = ttk.Button(button_frame, text="Print PDF", command=self.generate_pdf_report)
        print_pdf_button.grid(row=1, column=0, padx=5, pady=5)
        
        
        # Display Text Area
        ttk.Label(salary_frame, text="Employee Details", font=('Helvetica', 10, 'bold')).grid(row=10, column=0, columnspan=2, pady=(10,5), sticky='w')
        
        self.display_text_area = tk.Text(salary_frame, height=10, width=50, state='disabled', wrap=tk.WORD)
        self.display_text_area.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        
        # Add scrollbar to text area
        scrollbar = ttk.Scrollbar(salary_frame, orient='vertical', command=self.display_text_area.yview)
        scrollbar.grid(row=11, column=2, sticky='ns')
        self.display_text_area.configure(yscrollcommand=scrollbar.set)
        self.display_text_area.config(state='disabled')  


    def on_entry_click(self, entry, placeholder):
        """Handle focus in for Entry widgets"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground='black')

    def on_focus_out(self, entry, placeholder):
        """Handle focus out for Entry widgets"""
        if entry.get().strip() == '':
            entry.insert(0, placeholder)
            entry.config(foreground='gray')

    def calculate_net_salary(self):
        """
        Calculate Net Salary based on input fields
        This is a basic calculation and should be customized based on specific requirements
        """
        try:
            # Convert inputs to numeric values
            base_salary = float(self.salary_field.get() if self.salary_field.get() != "Enter Base Salary" else 0)
            total_days = float(self.total_days_field.get() if self.total_days_field.get() != "0-31" else 0)
            absents = float(self.absents_field.get() if self.absents_field.get() != "0" else 0)
            medical = float(self.medical_field.get() if self.medical_field.get() != "Medical Allowance" else 0)
            conveyance = float(self.convence_field.get() if self.convence_field.get() != "Conveyance Allowance" else 0)
            pf_percentage = float(self.pf_field.get() if self.pf_field.get() != "PF Percentage" else 0)

            # Calculate days worked
            days_worked = total_days - absents

            # Pro-rata salary based on days worked
            pro_rata_salary = base_salary * (days_worked / total_days) if total_days > 0 else base_salary

            # Calculate PF deduction
            pf_deduction = pro_rata_salary * (pf_percentage / 100)

            # Calculate net salary
            net_salary = pro_rata_salary + medical + conveyance - pf_deduction

            # Update net salary field
            self.net_salary_field.config(state='normal')
            self.net_salary_field.delete(0, tk.END)
            self.net_salary_field.insert(0, f"{net_salary:.2f}")
            self.net_salary_field.config(state='readonly')

        except ValueError:
            # Handle invalid input
            tk.messagebox.showerror("Calculation Error", "Please enter valid numeric values")

    def clear_salary_form(self):
        """Clear all salary form fields"""
        # Reset Entry fields
        fields_to_reset = [
            (self.salary_field, "Enter Base Salary"),
            (self.total_days_field, "0-31"),
            (self.absents_field, "0"),
            (self.medical_field, "Medical Allowance"),
            (self.convence_field, "Conveyance Allowance"),
            (self.pf_field, "PF Percentage")
        ]
        
        for field, placeholder in fields_to_reset:
            field.delete(0, tk.END)
            field.insert(0, placeholder)
            field.config(foreground='gray')
        
        # Reset Comboboxes
        self.month_field.set("Select Month")
        self.year_field.set(str(datetime.now().year))
        
        # Clear Net Salary
        self.net_salary_field.config(state='normal')
        self.net_salary_field.delete(0, tk.END)
        self.net_salary_field.config(state='readonly')
        
      
    def validate_employee_data(self):
        # Check for empty required fields
        required_fields = [
            (self.emp_code_entry, "Employee Code"),
            (self.name_field, "Name"),
            (self.designation_field, "Designation"),
            (self.contact_field, "Contact Number")
        ]
        
        for field, field_name in required_fields:
            if not field.get().strip():
                messagebox.showerror("Validation Error", f"{field_name} cannot be empty")
                return False
        
        # Name validation
        name = self.name_field.get().strip()
        if not re.match(r'^[A-Za-z\s]{2,50}$', name):
            messagebox.showerror("Validation Error", "Invalid name. Use only alphabets (2-50 characters)")
            return False
        
        # Age validation
        try:
            age = int(self.age_field.get())
            if age < 18 or age > 100:
                messagebox.showerror("Validation Error", "Age must be between 18 and 100")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid number")
            return False
        
            # Email validation
        email = self.email_field.get().strip()
        if email:  # Check if the email field is not empty
            # Remove the regex validation, allowing any input
            if not email:  # This check is redundant now but can be kept for clarity
                messagebox.showerror("Validation Error", "Email cannot be empty")
                return False
        
        # Contact number validation
        contact = self.contact_field.get().strip()
        if not re.match(r'^\+?[1-9]\d{9,14}$', contact):
            messagebox.showerror("Validation Error", "Invalid contact number (10-15 digits)")
            return False
        
        # Date of Birth (DOB) validation
        dob = self.dob_field.get().strip()
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            # Check if DOB is not in the future
            if dob_date > datetime.now():
                messagebox.showerror("Validation Error", "Date of Birth cannot be in the future")
                return False
            # Check if person is at least 18 years old
            min_dob = datetime.now().replace(year=datetime.now().year - 100)
            if dob_date < min_dob:
                messagebox.showerror("Validation Error", "Invalid Date of Birth")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid Date of Birth. Use YYYY-MM-DD format")
            return False
        
        # Date of Joining (DOJ) validation
        doj = self.doj_field.get().strip()
        try:
            doj_date = datetime.strptime(doj, '%Y-%m-%d')
            # Check if DOJ is not in the future
            if doj_date > datetime.now():
                messagebox.showerror("Validation Error", "Date of Joining cannot be in the future")
                return False
            # Check if DOJ is after DOB
            if doj_date < dob_date:
                messagebox.showerror("Validation Error", "Date of Joining cannot be before Date of Birth")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid Date of Joining. Use YYYY-MM-DD format")
            return False
        
        # Experience validation
        try:
            experience = float(self.experience_field.get())
            if experience < 0 or experience > 50:
                messagebox.showerror("Validation Error", "Experience must be between 0 and 50 years")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Experience must be a valid number")
            return False
        
        # Proof ID validation
        proof_id = self.proof_id_field.get().strip()
        if not proof_id:
            messagebox.showerror("Validation Error", "Proof ID cannot be empty")
            return False
        
        # Address validation
        address = self.address_text.get(1.0, tk.END).strip()
        if len(address) < 10 or len(address) > 500:
            messagebox.showerror("Validation Error", "Address must be between 10 and 500 characters")
            return False
        
        return True

    def save_employee_data(self):
        # Validate fields before saving
        if not self.emp_code_entry.get() or not self.name_field.get():
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        if not self.validate_employee_data():
            return  

        emp_code = self.emp_code_entry.get()

        # Check if employee data already exists for the provided emp_code
        self.cursor.execute('''SELECT * FROM employee WHERE emp_code = ?''', (emp_code,))
        existing_employee = self.cursor.fetchone()

        if existing_employee:
            # Update existing employee data
            self.cursor.execute('''
            UPDATE employee
            SET name = ?, age = ?, designation = ?, gender = ?, email = ?, dob = ?, doj = ?, experience = ?, proof_id = ?, contact = ?, status = ?, address = ?
            WHERE emp_code = ?
            ''', (
                self.name_field.get(),
                self.age_field.get(),
                self.designation_field.get(),
                self.gender_field.get(),
                self.email_field.get(),
                self.dob_field.get(),
                self.doj_field.get(),
                self.experience_field.get(),
                self.proof_id_field.get(),
                self.contact_field.get(),
                self.status_field.get(),
                self.address_text.get(1.0, tk.END),
                emp_code
            ))
            
            messagebox.showinfo("Success", "Employee data updated successfully!")
        else:
            # Insert new employee data
            self.cursor.execute(''' 
            INSERT INTO employee (emp_code,  name, age,designation, gender, email,  dob, doj, experience, proof_id, contact, status, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (
                self.emp_code_entry.get(),
                self.name_field.get(),
                self.age_field.get(),
                self.designation_field.get(),
                self.gender_field.get(),
                self.email_field.get(),
                self.dob_field.get(),
                self.doj_field.get(),
                self.experience_field.get(),
                self.proof_id_field.get(),
                self.contact_field.get(),
                self.status_field.get(),
                self.address_text.get(1.0, tk.END)
            ))
            
            messagebox.showinfo("Success", "Employee data saved successfully!")

        self.conn.commit()  # Commit the changes

    def save_salary_data(self):
        # Validate that salary is calculated
        if not self.net_salary_field.get():
            messagebox.showerror("Error", "Please calculate salary first!")
            return

        emp_code = self.emp_code_entry.get()

        # Check if salary data already exists for the provided emp_code
        self.cursor.execute('''SELECT * FROM salary_details WHERE emp_code = ? AND month = ? AND year = ?''', 
                            (emp_code, self.month_field.get(), self.year_field.get()))
        existing_salary = self.cursor.fetchone()

        if existing_salary:
            # Update existing salary data
            self.cursor.execute('''
            UPDATE salary_details
            SET salary = ?, total_days = ?, absents = ?, medical = ?, convence = ?, pf = ?, net_salary = ?
            WHERE emp_code = ? AND month = ? AND year = ?
            ''', (
                self.salary_field.get(),
                self.total_days_field.get(),
                self.absents_field.get(),
                self.medical_field.get(),
                self.convence_field.get(),
                self.pf_field.get(),
                self.net_salary_field.get(),
                emp_code,
                self.month_field.get(),
                self.year_field.get()
            ))
            
            messagebox.showinfo("Success", "Salary data updated successfully!")
        else:
            # Insert new salary data
            self.cursor.execute(''' 
            INSERT INTO salary_details (emp_code, month, year, salary, total_days, absents, medical, convence, pf, net_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                emp_code,
                self.month_field.get(),
                self.year_field.get(),
                self.salary_field.get(),
                self.total_days_field.get(),
                self.absents_field.get(),
                self.medical_field.get(),
                self.convence_field.get(),
                self.pf_field.get(),
                self.net_salary_field.get()
            ))

            messagebox.showinfo("Success", "Salary data saved successfully!")

        self.conn.commit()  # Commit the changes

    def calculate_salary(self):
        # Dummy salary calculation logic (you can replace this with real calculation)
        try:
            basic_salary = float(self.salary_field.get())
            total_days = int(self.total_days_field.get())
            absents = int(self.absents_field.get())
            medical = float(self.medical_field.get())
            convence = float(self.convence_field.get())
            pf = float(self.pf_field.get())
            
            # Simple net salary calculation (adjust as needed)
            net_salary = basic_salary - (absents * 10) + medical + convence - pf
            self.net_salary_field.config(state="normal")
            self.net_salary_field.delete(0, tk.END)
            self.net_salary_field.insert(0, f"{net_salary:.2f}")
            self.net_salary_field.config(state="readonly")
        except ValueError:
            messagebox.showerror("Error", "Invalid input data for salary calculation.")

    def clear_employee_form(self):
        # Clear all employee detail fields
        self.emp_code_entry.delete(0, tk.END)
        self.name_field.delete(0, tk.END)
        self.designation_field.delete(0, tk.END)
        self.age_field.delete(0, tk.END)
        self.gender_field.set('')
        self.email_field.delete(0, tk.END)
        self.dob_field.delete(0, tk.END)
        self.doj_field.delete(0, tk.END)
        self.experience_field.delete(0, tk.END)
        self.proof_id_field.delete(0, tk.END)
        self.contact_field.delete(0, tk.END)
        self.status_field.set('')
        self.address_text.delete(1.0, tk.END)

    def clear_salary_form(self):
        # Clear all salary detail fields
        self.month_field.delete(0, tk.END)
        self.year_field.delete(0, tk.END)
        self.salary_field.delete(0, tk.END)
        self.total_days_field.delete(0, tk.END)
        self.absents_field.delete(0, tk.END)
        self.medical_field.delete(0, tk.END)
        self.convence_field.delete(0, tk.END)
        self.pf_field.delete(0, tk.END)
        self.net_salary_field.config(state="normal")
        self.net_salary_field.delete(0, tk.END)
        self.net_salary_field.config(state="readonly")

#----------------------------------------------------------------------------------PDF Generate-----------------------------------------------------------------------

    def generate_pdf_report(self):
        # Check if Employee Code is provided
        emp_code = self.emp_code_entry.get()
        if not emp_code:
            messagebox.showerror("Error", "Please enter Employee Code to generate report.")
            return

        # Fetch employee details
        self.cursor.execute('''SELECT * FROM employee WHERE emp_code = ?''', (emp_code,))
        employee_data = self.cursor.fetchone()

        # Fetch salary details
        self.cursor.execute('''SELECT * FROM salary_details WHERE emp_code = ?''', (emp_code,))
        salary_data = self.cursor.fetchone()

        if not employee_data or not salary_data:
            messagebox.showerror("Error", "No data found for the provided Employee Code.")
            return

        try:
            # Generate PDF filename with employee code and current timestamp
            timestamp1 = datetime.now().strftime("%d_%m_%Y")
            timestamp2 = datetime.now().strftime("%H_%M")
            pdf_filename = f"ID_{emp_code}_Employee_Report_Date_{timestamp1}_Time_{timestamp2}.pdf"

            # Create PDF
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter

            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width/2, height - 50, "Employee Performance Management System")
            c.setFont("Helvetica", 12)
            c.drawCentredString(width/2, height - 70, "Employee Comprehensive Report")

            # Employee Details Section
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 120, "Employee Details")
            c.line(50, height - 125, 550, height - 125)

            # Employee Details Content
            y_position = height - 150
            employee_details = [
                f"Employee Code: {employee_data[0]}",
                f"Name: {employee_data[2]}",
                f"Designation: {employee_data[1]}",
                f"Age: {employee_data[3]}",
                f"Gender: {employee_data[4]}",
                f"Email: {employee_data[5]}",
                f"Date of Birth: {employee_data[6]}",
                f"Date of Joining: {employee_data[7]}",
                f"Experience: {employee_data[8]}",
                f"Proof ID: {employee_data[9]}",
                f"Contact: {employee_data[10]}",
                f"Status: {employee_data[11]}",
                f"Address: {employee_data[12].strip()}"
            ]

            c.setFont("Helvetica", 10)
            for detail in employee_details:
                c.drawString(50, y_position, detail)
                y_position -= 15

            # Salary Details Section
            y_position -= 20
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, "Salary Details")
            c.line(50, y_position - 5, 550, y_position - 5)

            y_position -= 30
            salary_details = [
                f"Month: {salary_data[1]}",
                f"Year: {salary_data[2]}",
                f"Total Salary: Rs.{salary_data[3]}",
                f"Total Working Days: {salary_data[4]}",
                f"Absents: {salary_data[5]}",
                f"Medical Allowance: Rs.{salary_data[6]}",
                f"Conveyance Allowance: Rs.{salary_data[7]}",
                f"Provident Fund (PF): Rs.{salary_data[8]}",
                f"Net Salary: Rs.{salary_data[9]}"
            ]

            c.setFont("Helvetica", 10)
            for detail in salary_details:
                c.drawString(50, y_position, detail)
                y_position -= 15

            # Footer
            c.setFont("Helvetica", 8)
            c.drawString(50, 50, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            c.save()

            messagebox.showinfo("Success", f"Report generated successfully!\nFile saved as {pdf_filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeePMS(root)
    root.mainloop()
