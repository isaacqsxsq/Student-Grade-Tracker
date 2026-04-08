import sys, csv, math
from tabulate import tabulate
import os

def initialize_files():
    os.makedirs('./Data', exist_ok=True)
    
    # Create categories file with defaults if missing
    if not os.path.exists('./Data/.categories.csv'):
        with open('./Data/.categories.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name','weight','mode'])
            writer.writeheader()
            writer.writerows([
                {'name': 'homework',   'weight': 0.3, 'mode': 'list'},
                {'name': 'test',       'weight': 0.5, 'mode': 'list'},
                {'name': 'attendance', 'weight': 0.2, 'mode': 'single'},
            ])
    
    # Create student file with headers if missing
    if not os.path.exists('./Data/.student.csv'):
        categories = []
        with open('./Data/.categories.csv') as f:
            categories = list(csv.DictReader(f))
        with open('./Data/.student.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name'] + [c['name'] for c in categories])
            writer.writeheader()
def display_menu():
    menu = "1. View All Student\n2. Add Student\n3. Add Student With Grade\n4. Update Student Grade\n5. Delete Student\n6. Update Category\n press q to quit\n---------------------------\nPress Number: "
    while True:
        try:
            inpu = input(menu)
            if inpu == 'q':
                sys.exit('Program Exited')
            elif 1 <= int(inpu) <= 6:
                match int(inpu):
                    case 1:
                        view_students()
                    case 2:
                        add_student()
                    case 3:
                        add_student_plus_grade()
                    case 4:
                        update_student_grade()
                    case 5:
                        delete_student()
                    case 6:
                        update_category()
            else:
                print("Invalid Number")
        except ValueError:
            print("Invalid Input")
def view_student(name): 
    # TODO valid print with different data 
    with open("./Data/.student.csv", "r") as file, open("./Data/.categories.csv", "r") as wFile:
        reader = csv.DictReader(file)
        rows = list(reader)
        fields = reader.fieldnames
        wreader = csv.DictReader(wFile)
        wRows = list(wreader)
        weights = [float(x['weight']) for x in wRows]
        ans = []
        average = [{'name': 'Average'}]
        avg_list = []
        final = 'N/A'
        for student in rows:
            if student['name'] == name:
                ans.append(student)
                break
        for field in fields[1:]:
            temp = calculate_average(name, field)
            if temp != "N/A":
                temp = round(temp, 2)  
            avg_list.append(temp)
            average[0] = average[0] | {field: temp}
        final = compute_final(avg_list, weights)
        average[0] = average[0] | {'final': final}
        print(tabulate(ans + average, headers= "keys", tablefmt="rounded_outline"))
def view_students(): 
    #TODO valid print with different data
    with open("./Data/.student.csv", "r") as file, open("./Data/.categories.csv", "r") as wFile:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        rows = list(reader)
        wreader = csv.DictReader(wFile)
        wRows = list(wreader)
        weights = [float(x['weight']) for x in wRows]
        ans = []
        if rows == []:
            print("List is now empty.")
            return
        final = 'N/A'
        
        for row in rows:
            average = [{'name': 'Average'}]
            avg_list = []
            for field in fields[1:]:
                temp = calculate_average(row['name'], field)
                if temp != "N/A":
                    temp = round(temp, 2)  
                avg_list.append(temp)
                average[0] = average[0] | {field: temp}
            final = compute_final(avg_list, weights)
            ans.append(row)
            ans.append(average[0] | {'final': final})
        print(tabulate(ans, headers= "keys", tablefmt="rounded_outline"))
def add_student():
    #TODO add default value corretly
    name = check_name()
    
    with open('./Data/.student.csv', 'a', newline = '') as file, open('./Data/.student.csv', 'r') as read:
        reader = csv.DictReader(read)
        fields = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fields)
        d = dict()
        for field in fields:
            if field == 'name':
                d[field] = name
            else:
                d[field] = ""
        writer.writerow(d)
    print(f'Sucessfully added')
def add_student_plus_grade():
    categories = []
    name = check_name()
    d = {'name': name}
    with open('./Data/.student.csv', 'a', newline = '') as file, open('./Data/.categories.csv', 'r') as read:
        reader = csv.DictReader(read)
        for row in reader:
            categories.append(row)
        writer = csv.DictWriter(file, fieldnames=["name"] + [x['name'] for x in categories])
        
        for category in categories:
            if category['mode'] == 'single':
                temp = check_valid_int(f"Type {category['name']} grade in a single number: ")
            else:
                temp = check_valid_int_array(f"Type {category['name']} grade with a numbers seaprated by commas: ")
            d[category['name']] = temp
        writer.writerow(d)
    print(f'Sucessfully added')
def update_student_grade():
    
    with open("./Data/.categories.csv", 'r') as read:
        reader = csv.DictReader(read)
        temp = list(reader)
        length = len(temp)
        categories = []
        for row in temp:
            categories.append(row)
    if length < 1:
        print('no categories')
        return
    name = check_name_not()
    view_student(name)
    while True:
        changing = input("Type category you want to change: ")
        if changing in [item['name'] for item in categories]:
            break
        else:
            print('Invalid category')
    option = 'single'
    for category in categories:
            if category['name'] == changing:
                if category['mode'] == 'single':
                    new_val = check_valid_int(f"Type new grade for {category['name']}: ")
                else:
                    while True:
                        option = input("1.Add\n2.update\nType option you want: ")
                        match option:
                            case '1':
                                new_val = check_valid_int("Type new grade: ")
                                break
                            case '2':
                                new_val = check_valid_int_array(f"Type {category['name']} grade with a numbers seaprated by commas: ")
                                break
                            case _:
                                print("invalid input")
                break
    with open("./Data/.student.csv", 'r') as read:
        reader = csv.DictReader(read)
        rows = []
        for row in reader:
            rows.append(row)
    
    for row in rows:
        if row['name'] == name:
            if option == "1":
                if row[changing]:
                    row[changing] += "," + str(new_val)
                else:
                    row[changing] = str(new_val)
            elif option == '2':
                row[changing] = str(new_val)
            elif option == 'single':
                row[changing] = str(new_val)
            break
    with open("./Data/.student.csv", 'w', newline='') as write:
        writer = csv.DictWriter(write, fieldnames=["name"] + [x['name'] for x in categories])
        writer.writeheader()
        writer.writerows(rows)
    print('Updated succesfully')
def delete_student():
    
    with open('./Data/.student.csv', 'r') as file:
        reader = csv.DictReader(file)
        temp  = list(reader)
        length = len(temp)
        if length < 1:
            print('no student')
            return
        print("You can not revert the deletion.")
        name = check_name_not()
        view_student(name)
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled. ")
            return
       
        rows = []
        fields = reader.fieldnames
        for row in temp:
            if row['name'] != name:
                rows.append(row)
    
    with open('./Data/.student.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
def update_category():
    while True:
        option = input("1. Add category\n2. Delete category,\n3. Update weight\n'q' to quit\nType: ").lower()
        match option:
            case "1":
                add_category()
                print("Succefully updated")
                break
            case "2":
                delete_category()
                break
            case "3":
                update_weights()
                break
            case "q":
                return
            case _:
                print("Type valid number. ")
def add_category():
    with open("./Data/.categories.csv") as cfile, open("./Data/.student.csv") as sfile:
        creader = csv.DictReader(cfile)
        cRow = list(creader)
        cLength = len(cRow)
        sreader = csv.DictReader(sfile)
        sRow = list(sreader)
        sFields = sreader.fieldnames
    print(tabulate(cRow, headers= "keys", tablefmt="rounded_outline"))
    name = check_category()
    while True:
        mode = input("Type list or single for mode: ").lower()
        if mode == 'single' or mode == 'list':
            break
        else:
            print("Type valid mode")
    weights = check_valid_weight_array("\nType new weights for every cateogry.\nYour inputs must be separated by comma and have be an float: \n", cLength + 1)
    
    with open("./Data/.categories.csv", 'w', newline="") as cWrite, open("./Data/.student.csv", "w", newline="") as sWrite:
        cWriter = csv.DictWriter(cWrite, fieldnames=['name','weight','mode'])
        cWriter.writeheader()
        for i, c in enumerate(cRow):
            c['weight'] = weights[i]
        cWriter.writerows(cRow + [{"name": name, "weight":weights[-1], "mode": mode}])
        
        sWriter = csv.DictWriter(sWrite, fieldnames=sFields + [name])
        sWriter.writeheader()
        sWriter.writerows(row | {name: ''} for row in sRow)
def delete_category():
    with open("./Data/.categories.csv") as cfile, open("./Data/.student.csv") as sfile:
        creader = csv.DictReader(cfile)
        cRow = list(creader)
        cLength = len(cRow)
        sreader = csv.DictReader(sfile)
        sRow = list(sreader)
        sFields = sreader.fieldnames
    if cLength == 1:
        print("You can not have less than one category")
        return
    print(tabulate(cRow, headers= "keys", tablefmt="rounded_outline"))
    name = check_category_not()
    confirm = input("Are you sure? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled. ")
        return
    weights = check_valid_weight_array("\nType new weights for remaining category.\nYour inputs must be separated by comma and have be an float: \n", cLength - 1)
    
    with open("./Data/.categories.csv", 'w', newline="") as cWrite, open("./Data/.student.csv", "w", newline="") as sWrite:
        cWriter = csv.DictWriter(cWrite, fieldnames=['name','weight','mode'])
        cWriter.writeheader()
        cRow = [x for x in cRow if x['name'] != name]
        for i in range(cLength-1):
            cRow[i]['weight'] = weights[i]
        cWriter.writerows(cRow)
        
        newFields = [x for x in sFields if x != name]
        sWriter = csv.DictWriter(sWrite, fieldnames=newFields)
        sWriter.writeheader()
        for j in range(len(sRow)):
            del sRow[j][name]
        sWriter.writerows(sRow)
    print("Succefully updated")
def update_weights():
    with open("./Data/.categories.csv") as cfile:
        creader = csv.DictReader(cfile)
        cRow = list(creader)
        cLength = len(cRow)
        if cLength < 1:
            print('no category')
            return
    print(tabulate(cRow, headers= "keys", tablefmt="rounded_outline"))
    weights = check_valid_weight_array("\nType new weights for every category.\nYour inputs must be separated by comma and have be an float: \n", cLength)
    for i in range(cLength):
        cRow[i]['weight'] = weights[i]
        
    with open("./Data/.categories.csv", 'w', newline="") as cWrite:
        cWriter = csv.DictWriter(cWrite, fieldnames=['name','weight','mode'])
        cWriter.writeheader()
        cWriter.writerows(cRow)
    print("Succefully updated")
       
def compute_final(avg_scores, weights):
    length = len(avg_scores)
    if length == 0:
        return "N/A"
    final = 0
    divi = 0
    for i in range(length):
        if avg_scores[i] != "N/A":
            final += float(avg_scores[i]) * weights[i]
            divi += 1
    if divi == 0:
        return 'N/A'
    return round(final, 2)
        
        

def main():
    initialize_files()
    display_menu()
def check_name_not():
    while True:
        name = input("Student's name: ").title()
        if not check_exist(name):
            print("Student does not exist")
        else:
            break     
    return name
def check_exist(name): 
    with open("./Data/.student.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == name:
                return True
    return False
def check_exist_category(cate):
    with open("./Data/.categories.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == cate:
                return True
    return False
def check_category():
    while True:
        name = input("Cateogry name: ").lower()
        if check_exist_category(name):
            print("Category Already exist")
        else:
            break     
    return name
def check_category_not():
    while True:
        name = input("Type cateogry name you want to delete: ").lower()
        if not check_exist_category(name):
            print("Category does not exist")
        else:
            break     
    return name
def check_name():
    while True:
        name = input("Student's name: ").title()
        if check_exist(name):
            print("Student Already exist")
        else:
            break     
    return name
def check_valid_int(st):
    while True:
        try:
            num = int(input(st))
            if 0<=num<=100:
                return num
            else:
                print("type number in range of 0 to 100")
        except ValueError:
            print('Write valid integer')
def check_valid_int_array(st):
    while True:
        try:
            temp = input(st)
            arr = [int(num.strip()) for num in temp.split(',')]
            
            if all(0 <= n <= 100 for n in arr):
                    return temp
            else:
                print("All numbers must be between 0 and 100")
        except ValueError:
            print('Write valid integer')
def check_valid_weight_array(st, le):
    while True:
        try:
            temp = input(st)
            arr = [float(num.strip()) for num in temp.split(',')]
            
            if not all(0 < n <= 1 for n in arr) :
                print("All numbers must be between 0 and 1")
            elif not math.isclose(sum(arr), 1.0, abs_tol=1e-9):
                print("Weights need to be sum up to 1")
            elif len(arr) != le:
                print("Number of inputs should match number of weights.")
            else:
                return arr
        except ValueError:
            print('Write valid integer')
def calculate_average(name, cate):
    try:
        with open("./Data/.student.csv") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            val = ''
            for row in rows:
                if row['name'] == name:
                    val = row[cate]
                    break
            val = [int(num) for num in val.split(',')]
            length = len(val)
            summ = sum(val)
            avg = summ / length
            return avg
    except ValueError:
        return "N/A"
if __name__ == "__main__":
    main()



