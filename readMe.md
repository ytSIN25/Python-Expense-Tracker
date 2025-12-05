# Python Expense Tracker Program

This is a lab work project for Python. The program provides functions such as adding, editing, and summarizing expense records. This program works best on Windows.

---

## Special Feature

This program runs with multiple Python modules. However, if the modules are not installed, the program will attempt to install them automatically, as long as *pip* and *Python* are already installed on your Windows device.

A CSV file will be generated automatically to store the data. You can export the data using the export function, or simply use the built-in storage system.

---

## Viewing Expenses

The **View Expense** function provides three options:

1. View all expenses  
2. View the latest 5 expenses  
3. View expenses by month  
   - (This displays all expenses in the selected month)

---

## Add, Edit, and Delete

The program supports adding new expense records with parameters such as:
- name  
- category  
- amount  
- notes  

Each expense will have an automatically generated **ID**, which can be viewed using the view function.

For **editing** and **deleting**, the **ID** of the expense is required to locate the record.

---

## Search for Expense

You can search for expenses using multiple filters:
- keyword  
- amount range  
- date range  
- categories  

Both the amount range and date range features also support searching for a **specific value** only.

---

## Export

One of the key features of this program is the **export function**, which allows you to export your data as:

- CSV  
- DOCX  
- XLSX  
- PDF  
- TXT  
- HTML  

**CSV, Excel, and HTML** exports are done using *pandas*.  
**DOCX** is created using *python-docx*.  
**PDF** is generated using *Matplotlib*.

All exported files will appear in the same directory as this program. You may also name the exported file to avoid confusion.

---

## Dealing with CSV

The program stores, reads, and writes data using a CSV file named **ExpenseTrackerRecord.csv**.

- If you edit the CSV manually *while the program is running*, you can use function 7 to reload the CSV.  
- If the program is not running, it will load the latest CSV automatically upon start.  
- If you want to reset the CSV (useful for testing), you can use the **Clear CSV** function to create a blank file.

---

### Created by **YT Sin**  
**5 February 2025**
