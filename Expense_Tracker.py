# Default packages
import random as rnd #Generate ID for expense
import datetime as dt #Save expense date
import re #Validate user input format
import math #For certain calculation purpose
import os #Check is "user.csv" exist
import subprocess #Install package purpose
import sys #Check for module
from time import sleep #To stop program at some point for user to read prompted text


#REMEMBER TO DELETE AFTER FINISH
import pandas as pd
import matplotlib.pyplot as plt
import docx
import openpyxl

#Import when exist, install when not ✅
def importInstall(package_name, import_name=None):
    import_name = import_name or package_name
    try:
        return __import__(import_name)
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return __import__(import_name)

# Non-default packages ✅
pd = importInstall("pandas")
plt = importInstall("matplotlib")
import matplotlib.pyplot as plt
docx = importInstall("python-docx", "docx")
openpyxl = importInstall("openpyxl")

# Sets up dataframe template ✅
def createNewDF():
    return pd.DataFrame({
        "ID": [],
        "name": [],
        "amount": [],
        "category": [],
        "date": [],
        "notes": []
    })

# Deal with CSV presaved data ✅
def initialize():
    global df
    if not os.path.exists("user.csv"):
        print("user.csv does not exist.")
        print('Creating "user.csv" at current directory...')
        sleep(2)
        with open("user.csv", "x") as file:
            pass
    try:
        df = pd.read_csv("user.csv")

        # if frame is setted up but data is empty
        if df.empty:
            print("The original data is empty, creating new dataframe...")
            sleep(1.5)
            df = createNewDF()
            updateCSV()

        # framework with data
        else: 
            print("There is something in the data. Do you want to overwrite(Y/n)")
            overwrite = input("> ")
            while overwrite not in ["Y","n"]:
                overwrite = input("Please enter Y or n:  ")
            if overwrite == "Y":
                df = createNewDF()
                updateCSV()
                print("CSV overwritten with blank data.")
                sleep(1)
            else: 
                df["date"] = pd.to_datetime(df["date"])
                print("The original data will be used.")
                sleep(1)
                
    # totaly empty file
    except pd.errors.EmptyDataError:
        print("The CSV is totaly blank. Creating new template...")
        sleep(1)
        df = createNewDF()
        updateCSV()

#Display the starting menu ✅
def displayMenu():
    """Displays the starting menu with title"""
    print()
    print("*"*143)
    #graffi text "Expense tracker"
    print("""
$$$$$$$$\                                                                   $$$$$$$$\                           $$\                           
$$  _____|                                                                  \__$$  __|                          $$ |                          
$$ |      $$\   $$\  $$$$$$\   $$$$$$\  $$$$$$$\   $$$$$$$\  $$$$$$\           $$ | $$$$$$\  $$$$$$\   $$$$$$$\ $$ |  $$\  $$$$$$\   $$$$$$\  
$$$$$\    \$$\ $$  |$$  __$$\ $$  __$$\ $$  __$$\ $$  _____|$$  __$$\          $$ |$$  __$$\ \____$$\ $$  _____|$$ | $$  |$$  __$$\ $$  __$$\ 
$$  __|    \$$$$  / $$ /  $$ |$$$$$$$$ |$$ |  $$ |\$$$$$$\  $$$$$$$$ |         $$ |$$ |  \__|$$$$$$$ |$$ /      $$$$$$  / $$$$$$$$ |$$ |  \__|
$$ |       $$  $$<  $$ |  $$ |$$   ____|$$ |  $$ | \____$$\ $$   ____|         $$ |$$ |     $$  __$$ |$$ |      $$  _$$<  $$   ____|$$ |      
$$$$$$$$\ $$  /\$$\ $$$$$$$  |\$$$$$$$\ $$ |  $$ |$$$$$$$  |\$$$$$$$\          $$ |$$ |     \$$$$$$$ |\$$$$$$$\ $$ | \$$\ \$$$$$$$\ $$ |      
\________|\__/  \__|$$  ____/  \_______|\__|  \__|\_______/  \_______|         \__|\__|      \_______| \_______|\__|  \__| \_______|\__|      
                    $$ |                                                                                                                      
                    $$ |                                                                                                                      
                    \__|                                                                                                                      
          """)
    author = "by Yee Tng-37289632"
    print(f"{author:>142}")
    print("*"*143)
    print("Welcome to the Expense Tracker Program")
    print("What do you like to do today?")
    print("1. View expenses")
    print("2. Add new expense")
    print("3. Edit past expense")
    print("4. Delete expense")
    print("5. Search for expense")
    print("6. View summary")
    print("7. Load CSV data")
    print("8. Clear CSV data")
    print("9. Export data")
    print("h for Help")
    print("Exit (q to exit)")
    print()
    print()

# Display expense list ✅
def displayExpense():
    print("""
    Do you want to see:
    1. All past expenses
    2. Latest 5 expenses
    3. All expenses in month
    (q to leave)
          """)
    choice = input("> ")
    while choice not in ["1", "2", "3","q","Q"]:
        choice = input("The choice is invalid:  ")
    match choice:
        case "1":
            df.sort_values(by="date", inplace=True) 
            df.reset_index(drop=True, inplace=True)
            print("*"*130)
            print(df)
            print("*"*130)
        case "2":
            df.sort_values(by="date", inplace=True) 
            df.reset_index(drop=True, inplace=True)
            print("*"*130)
            print(df.tail(5))
            print("*"*130)
        case "3":
            # Make sure date column is datetime
            df["date"] = pd.to_datetime(df["date"])

            Year = input("What is the year you would like to look for? ")
            validYear = df["date"].dt.year.unique().tolist()
            while not Year.isdigit() or int(Year) not in validYear:
                Year = input("The year is not valid, try again: ")
            Year = int(Year)

            Month = input("What is the month you would like to look for? ")
            validMonth = df["date"].dt.month.unique().tolist()
            while not Month.isdigit() or int(Month) not in validMonth:
                Month = input("The month is not valid, try again: ")
            Month = int(Month)

            filtered = df[(df["date"].dt.year == Year) & (df["date"].dt.month == Month)]
            print("*"*130)
            print(filtered)
            print("*"*130)
            

        case "q" | "Q":
            return
    
# Add new expense ✅
def addExpense():
    # Name
    def name():
        x = input("Enter the name for the expense (q to quit):  ")
        if x == "q" or x == "Q":
            return None
        return x
        
    # Amount
    def amount():
        amount = input("Enter the amount for the expense (r to redo / q to quit):  ")
        amountPattern = r"^\d+(\.\d{2})$"
        if amount == "r" or amount == "R":
            return "redo"
        elif amount == "q" or amount == "Q":
            return None
        while not re.match(amountPattern, amount):
            amount = input("The input is not valid (Add .00 for whole value):  ")
        return float(amount)

    # Category
    def category():
        print("""Choose the category of the expense:
    1. Food and Drinks
    2. Commute
    3. Utilities
    4. Entertainment / Shopping
    5. Social Life
    (r to redo / q to quit)
        """)
        validCategory = ["1","2","3","4","5","r","R","q","Q"]
        category = input("> ")
        while category not in validCategory:
            category = input("The category is not valid. Try Again: ")
        match category:
            case "1":
                category = "Food and Drinks"
            case "2":
                category = "Commute"
            case "3":
                category = "Utilities"
            case "4":
                category = "Entertaiment / Shopping"
            case "5":
                category = "Social Life"
            case "r" | "R":
                return "redo"
            case "q" | "Q":
                return None
        return category

    # Date
    def date():
        Year = input("Enter the year of the expense : ")
        while not re.match(r"^\d{4}$", Year):
            Year = input("Enter only 4 digit number: ")
        Year = int(Year)

        Month = input("Enter the month of the expense in number: ")
        while not (re.match(r"^\d{1,2}$", Month) and 1 <= int(Month) <= 12):
            Month = input("Please enter a valid month in number: ")
        Month = int(Month)

        Day = input("Enter the day of the expense in number: ")
        if Month in [1,3,5,7,8,10,12]:
            while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 31):
                Day = input("Please enter a valid day in number: ")
        elif Month in [4,6,9,11]:
            while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 30):
                Day = input("Please enter a valid day in number: ")
        elif Month == 2 and Year % 4 == 0:
            while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 29):
                Day = input("Please enter a valid day in number: ")
        elif Month == 2 and Year % 4 > 0:
            while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 28):
                Day = input("Please enter a valid day in number: ")
        Day = int(Day)

        return dt.datetime(Year, Month, Day)

    # Main Logic
    while True:
        Name = name()
        if Name == None:
            return
        
        Amount = amount()
        if Amount == "redo":
            continue
        elif Amount is None:
            return

        Category = category()
        if Category == "redo":
            continue
        elif Category is None:
            return

        Date = date()

        # Note
        notes = input("Enter any extra notes. (If no, press Enter):  ")

        # ID generation
        id = genID(Category, Date.month, Date.day, Amount)

        df.loc[len(df)] = {"ID": id,
                        "name": Name,
                        "amount": Amount, 
                        "category": Category,
                        "date": Date,
                        "notes": notes}
        updateCSV()
        return
    
# Generate expense ID ✅
def genID(category, month, day, amount):
    #Category + Date + Random Number
    base = rnd.randint(0,100)
    head = 0
    match category:
        case "Food and Drinks":
            head  = 1
        case "Commute":
            head  = 2
        case "Utilities":
            head  = 3
        case "Entertaiment / Shopping":
            head  = 4
        case "Social Life":
            head  = 5
    return int(str(head) + str(month) + str(day) + str(math.floor(amount)) + str(base))

# Edit expense ✅
def editExpense():
    target = input("Please enter the ID of the expense you would like to edit (q to quit):  ")
    while target not in df["ID"].astype(str).tolist() and target != "q":
        target = input("The ID is invalid. Try again:  ")
    if target == "q":
        return
    targetIndex = df.index[df["ID"].astype(str) == target][0]
    print("*"*130)
    print(f"The expense you would like to edit is: {df.at[targetIndex, 'name']} on {df.at[targetIndex, 'date']} with the amount {df.at[targetIndex, 'amount']} for {df.at[targetIndex, 'category']}. (Notes: {df.at[targetIndex, 'notes']})")
    print("""
    What is the data you would like to edit on this expense
    1. Name
    2. Date
    3. Amount
    4. Category
    5. Notes
    (q to quit)
          """)
    
    editTarget = input("> ")
    while editTarget not in ["1","2","3","4","5","q","Q"]:
        editTarget = input("The data is invalid. Try Again:  ")

    def confirm():
        confirm = input("Are you sure? (Y / n)  ")
        while confirm not in ["Y","n"]:
            confirm = input("Please enter Y(yes) or n(no):  ")
        if confirm == "Y":
            return True
        else:
            return False
        
    match editTarget:
        # Name
        case "1":
            name = input("Enter the name for the expense (q to quit):  ")
            if name == "q" or name == "Q":
                return
            if confirm():
                df.at[targetIndex, 'name'] = name
            else: 
                return

        # Date
        case "2":
            Year = input("Enter the year of the expense : ")
            while not re.match(r"^\d{4}$", Year):
                Year = input("Enter only 4 digit number: ")
            Year = int(Year)

            Month = input("Enter the month of the expense in number: ")
            while not (re.match(r"^\d{1,2}$", Month) and 1 <= int(Month) <= 12):
                Month = input("Please enter a valid month in number: ")
            Month = int(Month)

            Day = input("Enter the day of the expense in number: ")
            if Month in [1,3,5,7,8,10,12]:
                while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 31):
                    Day = input("Please enter a valid day in number: ")
            elif Month in [4,6,9,11]:
                while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 30):
                    Day = input("Please enter a valid day in number: ")
            elif Month == 2 and Year % 4 == 0:
                while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 29):
                    Day = input("Please enter a valid day in number: ")
            elif Month == 2 and Year % 4 > 0:
                while not (re.match(r"^\d{1,2}$", Day) and 1 <= int(Day) <= 28):
                    Day = input("Please enter a valid day in number: ")
            Day = int(Day)

            if confirm():
                df.at[targetIndex, 'date'] = dt.datetime(Year, Month, Day)
                df.at[targetIndex, 'ID'] = genID(df.at[targetIndex, 'category'], df.at[targetIndex, 'date'].month, df.at[targetIndex, 'date'].day, df.at[targetIndex, 'amount'])
            else:
                return

        # Amount
        case "3":
            amount = input("Enter the amount for the expense (q to quit):  ")
            amountPattern = r"^\d+(\.\d{2})$"
            if amount == "q" or amount == "Q":
                return 
            while not re.match(amountPattern, amount):
                amount = input("The input is not valid (Add .00 for whole value):  ")
            if confirm():
                df.at[targetIndex, 'amount'] = float(amount)
                df.at[targetIndex, 'ID'] = genID(df.at[targetIndex, 'category'], df.at[targetIndex, 'date'].month, df.at[targetIndex, 'date'].day, df.at[targetIndex, 'amount'])
            else: 
                return

        # Category
        case "4":
            print("""Choose the category of the expense:
    1. Food and Drinks
    2. Commute
    3. Utilities
    4. Entertainment / Shopping
    5. Social Life
    (q to quit)
        """)
            validCategory = ["1","2","3","4","5","q","Q"]
            category = input("> ")
            while category not in validCategory:
                category = input("The category is not valid. Try Again: ")
            match category:
                case "1":
                    category = "Food and Drinks"
                case "2":
                    category = "Commute"
                case "3":
                    category = "Utilities"
                case "4":
                    category = "Entertaiment / Shopping"
                case "5":
                    category = "Social Life"
                case "q" | "Q":
                    return
            if confirm():
                df.at[targetIndex, 'category'] = category
                df.at[targetIndex, 'ID'] = genID(df.at[targetIndex, 'category'], df.at[targetIndex, 'date'].month, df.at[targetIndex, 'date'].day, df.at[targetIndex, 'amount'])
            else: 
                return

        # Notes
        case "5":
            notes = input("Enter any extra notes. (If no, press Enter):  ")
            if confirm():
                df.at[targetIndex, 'notes'] = notes
            else:
                return

        #Quit
        case "q" | "Q":
            return
        
    sleep(0.5)
    print(f"The expense ({df.at[targetIndex, 'ID']}) is now: {df.at[targetIndex, 'name']} on {df.at[targetIndex, 'date']} with the amount {df.at[targetIndex, 'amount']} for {df.at[targetIndex, 'category']}. (Notes: {df.at[targetIndex, 'notes']})")
    updateCSV()

# Delete expense ✅
def delExpense():
    target = input("Please enter the ID of the expense you would like to delete (q to quit):  ")
    while target not in df["ID"].astype(str).tolist() and target != "q":
        target = input("The ID is invalid. Try again:  ")
    if target == "q":
        return
    targetIndex = df.index[df["ID"].astype(str) == target][0]
    print(f"The expense you would like to delete is: {df.at[targetIndex, 'name']} on {df.at[targetIndex, 'date']} with the amount {df.at[targetIndex, 'amount']}")

    # Confirmation 
    confirm = input("Are you confirm to delete the expense? (Y / n):  ")
    while confirm not in ["Y", "n"]:
        confirm = input("Please type Y (yes) or n (no)")
    if confirm == "Y":
        df.drop(targetIndex, inplace=True)
        updateCSV()
        print("Expense deleted successfully!")

# Search for expense (name, amount range, category, date range)
def searchExpense():
    print("""
What parameter would you like to search with?
1. Name
2. Amount Range
3. Category
4. Date Range
(q to quit)
""")
    userInput = input("Choose the function or quit:  ")
    while userInput not in ["1","2","3","4","q","Q"]:
            userInput = input("The function is not available, choose again:  ")
    if userInput == "q" or userInput == "q":
        return
    
    match userInput:
        # Keyword search name
        case '1':
            target = input("Enter the name of the expense that you would like to search:  ").strip().lower()
            search = df[df["name"].str.lower().str.contains(target)]
            while search.empty:
                target = input("The name is not available. Try Again:  ")
                search = df[df["name"].str.lower().str.contains(target)]
            print("*"*130)
            print("This is the search results:  ")
            print(search)
            print("*"*130)

        # Amount Range
        case '2':
            target = input("Enter the amount range that you would like to search (minimum,maximum):  ")
            # \s* space, \d+ multiple digit, (\.\d+)? optional decimal
            while not re.match(r"^\s*\d+(\.\d+)?\s*,\s*\d+(\.\d+)?\s*$", target):
                target = input("The format is incorrect. Try again (minimum,maximum):  ")
            min,max = target.split(",")
            min = float(min)
            max = float(max)
            if min > max:
                min, max = max, min
            
            if min == max:    
                search = df[df["amount"] == min]
            else: 
                search = df[(df["amount"] >= min) & (df["amount"] <= max)]
            if search.empty:
                print("*"*130)
                print("There is no data for the amount range.")
                print("*"*130)
            else:
                search = search.sort_values(by="amount")
                print("*"*130)
                print("This is the search results:  ")
                print(search) 
                print("*"*130)

        # Category
        case '3':
            print("""Choose the category of the expense:
    1. Food and Drinks
    2. Commute
    3. Utilities
    4. Entertainment / Shopping
    5. Social Life
    (q to quit)
        """)
            validCategory = ["1","2","3","4","5","q","Q"]
            category = input("> ")
            while category not in validCategory:
                category = input("The category is not valid. Try Again: ")
            if category == "q" or category == "Q":
                return
            match category:
                case "1":
                    category = "Food and Drinks"
                case "2":
                    category = "Commute"
                case "3": 
                    category = "Utilities"
                case "4":
                    category = "Entertaiment / Shopping"
                case "5":
                    category = "Social Life"

            search = df[df["category"] == category]
            
            if search.empty:
                print("There is no expense in this category")
            else:
                search = search.sort_values(by="date")
                sleep(1)
                print("*"*130)
                print("This is the search results:  ")
                print(search) 
                print("*"*130)
        
        # Date range
        case '4':
            while True:
                startDate = input("Please enter the start date as YYYY-MM-DD (q to quit): ")
                if startDate.lower() == "q":
                    break
                
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", startDate):
                    print("Invalid format. Use YYYY-MM-DD.")
                    continue
                
                try:
                    year, month, day = map(int, startDate.split("-"))
                    dt.date(year, month, day)
                    break
                except ValueError:
                    print("Invalid date. Try again in YYYY-MM-DD")
            year, month, day = map(int, startDate.split("-"))
            startDate = dt.date(year, month, day)
            

            while True:
                endDate = input("Please enter the end date as YYYY-MM-DD (q to quit): ")
                if endDate.lower() == "q":
                    break
                
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", endDate):
                    print("Invalid format. Use YYYY-MM-DD.")
                    continue
                
                try:
                    year, month, day = map(int, endDate.split("-"))
                    dt.date(year, month, day)
                    break
                except ValueError:
                    print("Invalid date. Try again in YYYY-MM-DD")
            year, month, day = map(int, endDate.split("-"))
            endDate = dt.date(year, month, day)

            if startDate > endDate:
                startDate, endDate = endDate, startDate
            
            if startDate == endDate:    
                search = df[df["date"] == startDate]
            else: 
                search = df[(df["date"] >= startDate) & (df["date"] <= endDate)]
            if search.empty:
                print("*"*130)
                print("There is no data for the amount range.")
                print("*"*130)
            else:
                search = search.sort_values(by="category")
                print("*"*130)
                print("This is the search results:  ")
                print(search)
                print("*"*130)
    
# View summary
def viewSummary():
    pass

# Export data ✅
def export():
    global df
    def create(name,format):
        global df
        if os.path.exists(f"{name}.{format}"):
            print(f"The file with the name '{name}' already exist. please delete and try again.")
            sleep(0.5)
            return
        print(f"Exporting to {name}.{format}...")

        if format == "xlsx":
            df.to_excel(f"{name}.{format}",index=False)

        elif format == "csv":
            df.to_csv(f"{name}.{format}",index=False)

        elif format == "html":
            df.to_html(f"{name}.{format}",index=False)

        elif format == "pdf":
            fig, ax = plt.subplots(figsize=(12, len(df)*0.5))
            ax.axis('off')
            table = ax.table(cellText = df.values, colLabels = df.columns, cellLoc = 'center', loc = 'center')
            plt.savefig(f"{name}.pdf")

        elif format == "docx":
            doc = docx.Document()
            doc.add_heading(name, 1)
            table = doc.add_table(rows=1, cols=len(df.columns))
            for i, column in enumerate(df.columns):
                table.rows[0].cells[i].text = column
            
            for row in df.values:
                cells = table.add_row().cells
                for i, value in enumerate(row):
                    cells[i].text = str(value)
            
            doc.save(f"{name}.docx")
            
        elif format == "txt":
            with open(f"{name}.txt", "w") as f:
                f.write(df.to_string(index=False))
        sleep(1)
        print("The data has been exported! ")

    # Main
    print("""
What file format do you want to export your data to?
1. Excel(xlsx)
2. CSV
3. HTML
4. PDF
5. Word(docx)
6. txt
(q to quit)
          """)
    select = input("> ")
    while select not in ["1","2","3","4","5","6","q","Q"]:
        select = input("Please select a valid option:  ")
    if select == "q" or select ==  "Q":
        return
    name = input("Enter the name you would like to have: ")
    name = name.replace(" ", "_")
    match select:
        case "1":
            create(name, "xlsx")
        case "2":
            create(name, "csv")
        case "3":
            create(name, "html")
        case "4":
            create(name, "pdf")
        case "5":
            create(name, "docx")
        case "6":
            create(name, "txt")

#help
def help():
    print("Welcome to help ")
    print("Which function do you want to query?")

#update csv to df ✅
def loadCSV():
    df = pd.read_csv("user.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

#update df to csv ✅
def updateCSV():
    df.sort_values(by="date", inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.to_csv("user.csv",index=False)

def main():
    global df
    isRunning = True
    #Initialize in case "user.csv" not exist
    initialize()

    #Main part
    while isRunning:
        displayMenu()
        userInput = input("Choose the function or quit:  ")
        while userInput not in ["1","2","3","4","5","6","7","8","9","h","H","q","Q"]:
                userInput = input("The function is not available, choose again:  ")

        match userInput:
            case '1':
                displayExpense()
                input("Press enter to go back to the menu")
            case '2':
                addExpense()
                input("Press enter to go back to the menu")
            case '3':
                editExpense()
                input("Press enter to go back to the menu")
            case '4':
                delExpense()
                input("Press enter to go back to the menu")
            case '5':
                searchExpense()
                input("Press enter to go back to the menu")
            case '6':
                viewSummary()
                input("Press enter to go back to the menu")
            case '7':
                df = loadCSV()
                df["date"] = pd.to_datetime(df["date"])
                print("The CSV from last time has been imported!")
                sleep(2)
            case '8':
                df = pd.DataFrame({"ID":[],
                   "name": [],
                   "amount": [],
                   "category": [],
                   "date": [],
                   "notes": []})
                updateCSV()
                input("Press enter to go back to the menu")
            case '9':
                export()
                input("Press enter to go back to the menu")
            # Help
            case 'h' | 'H':
                help()
                input("Press enter to go back to the menu")

            # Exit
            case 'q' | 'Q':
                print("Bye Bye!")
                isRunning = False
        
if __name__ == "__main__":
    main()