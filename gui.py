from tkinter import *
import tkinter.messagebox
import csv 
import requests
import os 

# 4260 is the code for Summer Quarter 2021.
# 4300 is the code for Fall Quarter 2021.
# 4320 is the code for Winter Quarter 2022
# 4340 is the code for Spring Quarter 2022.
# 4360 is the code for Summer Quarter 2022.
# 4400 is the code for Fall Quarter 2022.
# 4420 is the code for Winter Quarter 2023.
# 4430 is the code for Spring Quarter 2023.

"""

1. We first define a dictionary called quarterMap which maps the academic quarter to the quarter code.
2. We then define a function called get_courses which takes in the core code and the quarter code.
3. We then use the requests library to make a POST request to the SCU website.
4. We then use the json library to parse the response.
5. We then return the data from the response.
6. We then define a function called validateInput which takes in the user input.

"""

quarterMap = {
    "Spring 2023": "4440",
    "Winter 2023": "4420",
    "Fall 2022": "4400",
    "Summer 2022": "4360",
    "Spring 2022": "4340",
    "Winter 2022": "4320",
    "Fall 2021": "4300",
    "Summer 2021": "4260" 
}

quarterNameMap = {
    "Spring 2023": "spring2023",
    "Winter 2023": "winter2023",
    "Fall 2022": "fall2022",
    "Summer 2022": "summer2022",
    "Spring 2022": "spring2022",
    "Winter 2022": "winter2022",
    "Fall 2021": "fall2021",
    "Summer 2021": "summer2021"
}
  
def get_courses(core, quarterCode):  
    payload = f"newcore={core}&maxRes=10000"
    headers = {
        "authority": "www.scu.edu",
        "accept": "*/*",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": os.getenv("USER_AGENT"),
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-gpc": "1",
        "origin": "https://www.scu.edu",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-language": "en-US,en;q=0.9",
    }

    response = requests.request("POST", f"https://www.scu.edu/apps/ws/courseavail/search/{quarterCode}/ugrad", headers=headers, data=payload)
    data = response.json()
    return data

def validateInput():   
    quarter = input.get()  
    
    if (quarter == "Select academic quarter:"):
        tkinter.messagebox.showinfo("Invalid Message Alert", "The field cannot be left empty!")

    else:
        tkinter.messagebox.showinfo("Success Message", "Successfully downloaded!")  
        
        courses = {}

        # Core Codes
        coreDict = {
            "I_PTHAMS": "American Studies (Pathway)",
            "I_PTHAE": "Applied Ethics (Pathway)",
            "I_PTHB": "Beauty (Pathway)",
            "I_PTHCHD": "Children, Family, & Society (Pathway)",
            "I_PTHCINST": "Cinema Studies (Pathway)",
            "I_PTHDEM": "Democracy (Pathway)",
            "I_PTHDT": "Design Thinking (Pathway)",
            "I_PTHFHP": "Feeding the World (Pathway)",
            "I_PTHGGE": "Gender, Globalization & Empire (Pathway)",
            "I_PTHGSB": "Gender, Sexuality & the Body (Pathway)",
            "I_PTHGB": "Global Health (Pathway)",
            "I_PTHHR": "Human Rights (Pathway)", 
            "I_PTHIS": "Islamic Studies (Pathway)",
            "I_PTHJA": "Justice and the Arts (Pathway)",
            "I_PTHLSJ": "Law & Social Justice (Pathway)",
            "I_PTHLPOSC": "Leading People, Org & Soc Chng (Pathway)",
            "I_PTHPS": "Paradigm Shifts (Pathway)",
            "I_PTHPR": "Politics & Religion (Pathway)",
            "I_PTHRPSI": "Race Place & Soc Inequalities (Pathway)",
            "I_PTHS": "Sustainability (Pathway)",
            "I_PTHDA": "The Digital Age (Pathway)",
            "I_PTHVST": "Values Science Technology (Pathway)",
            "I_PTHV": "Vocation (Pathway)",
            "I_AW": "Advanced Writing",
            "E_ARTS": "Arts",
            "E_CE": "Civic Engagement",
            "F_CTW1": "Critical Thinking and Writing 1",
            "F_CTW2": "Critical Thinking and Writing 2",
            "F_CI1": "Cultures and Ideas 1",
            "F_CI2": "Cultures and Ideas 2",
            "E_CI3": "Cultures and Ideas 3",
            "E_DV": "Diversity",
            "E_ETH": "Ethics",
            "I_EL": "Experiential Learning for Social Justice",
            "F_RTC1": "Religion Theology & Culture 1",
            "E_RTC2": "Religion Theology & Culture 2",
            "E_RTC3": "Religion Theology & Culture 3",
            "E_STS": "Science Technology & Society",
            "E_SOSC": "Social Science",
            "E_ARTSPAR": "Partial Credit Arts",
            "E_CEPAR": "Partial Credit Civic Engagement",
            "E_STSPAR": "Partial Credit Engineering, Math, CS"
        }

        for core in coreDict:
            print(f"Fetching {coreDict[core]} . . .")

            # Fetch course data and add it to dict
            data = get_courses(core, quarterMap.get(quarter))
            for info in data["results"]:
                if info["class_nbr"] in courses:
                    newCore = f"{courses.get(info['class_nbr']).get('core')}, {coreDict[core]}"
                    courses.get(info["class_nbr"]).update({"core": newCore})
                else:
                    newCourse = {
                        "class": f"{info['subject']} {info['catalog_nbr']} ({info['class_nbr']})",
                        "description": info["class_descr"],
                        "core": coreDict[core],
                        "days-times": f"{info['mtg_days_1']} {info['mtg_time_beg_1']} - {info['mtg_time_end_1']}" if info["mtg_time_end_1"] != "" else "TBA",
                        "room": f"{info['mtg_facility_1'] or 'TBA' }",
                        "instructor": f"{info['instr_1'] or 'TBA' }",
                        "units": info["units_minimum"],
                        "seats": info["seats_remaining"] if int(info["seats_remaining"]) > 0 else "None",
                    }

                    courses.update({info["class_nbr"]: newCourse})

        rows = ["CLASS", "DESCRIPTION", "CORES SATISFIED", "DAYS/TIMES", "ROOM", "INSTRUCTOR", "UNITS", "SEATS REMAINING"] 
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"scu_double_dips-{quarterNameMap.get(quarter)}.csv"
        file_path = os.path.join(script_dir, filename)
    
        with open(file_path, "w") as csv_file: 
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(rows) # write header

            for course in courses:

                # Checking if there are multiple cores for a course.
                if "," in courses.get(course).get("core"):   

                    course_data = []

                    for data_point in courses.get(course):
                        course_data.append(courses.get(course)[data_point])

                    csv_writer.writerow([data_point for data_point in course_data]) # write each item

            print(f"\n\n=== Finished fetching core requirements for {quarter}! ===\n\n")

if __name__ == "__main__":  
    root = Tk()
    root.resizable(0,0)
    root.geometry("500x350")
    root.title("SCU Double Dip Courses Retriever") 

    label_0 = Label(root, text="SCU Core Double Dips", bg="#FF7C80", fg="white", width=20, font=("bold", 20))
    label_0.place(x=90,y=53) 

    label_1 = Label(root, text="Quarter", width=20, font=("bold", 10))
    label_1.place(x=70, y=180)

    list1 = quarterMap.keys()
    input = StringVar()
    droplist = OptionMenu(root, input, *list1)
    droplist.config(width=22)
    input.set("Select academic quarter:") 
    droplist.place(x=240, y=180) 

    Button(root, text="Download", width=20, bg="#FF7C80", fg="white", command = validateInput).place(x=180,y=280)
 
    root.mainloop()