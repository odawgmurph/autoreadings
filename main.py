subdomain = ""
token = ""

import requests as rq, tkinter as tk, csv, tkinter.filedialog, datetime

root = tk.Tk()
root.title('Reading Assignment Schedule')
filepath = ""
rows = []
assignments = []
section = ""

def openfile():
    global filepath
    filepath = tkinter.filedialog.askopenfilename(
        initialdir = "/",
        title='File Select',
        filetypes=(("CSV Files", "*.csv"),)
    )
    if filepath:
        pass

def doubledate(date):
    first = int(date[:date.find('/')])
    second = int(date[date.find('/')+1:date.find('/', date.find('/')+1)])
    last = date[-4:]
    new = f"{first:02}/{second:02}/{last}"
    return new

def csvread():
    if filepath != "":
        with open(filepath, 'r') as csvfile:
            csreader = csv.reader(csvfile)
            for row in csreader:
                rows.append(row)
            length = len(rows)
            print(f"{length-1} assignments found.")
        for row in rows[1:]:
            date = row[0]
            realdate = doubledate(date)
            desc = row[1]
            abbr = row[2]
            assignments.append({
                'date': realdate,
                'description': desc,
                'abbr': abbr,
            })
        for assign in assignments:
            abbrev = assign['abbr']
            description = assign['description']
            datedue = assign['date']
            headers = {
                "AssignmentTypeId": "1114",
                "ShortDescription": assign["abbr"],
                "LongDescription": assign["description"],
                "IncGradeBook": False,
                "AbbrDescription": "CLS",
                "MaxPoints": "10",
                "Factor": "1",
                "ExtraCredit": False,
                "IncCumGrade": False,
                "PublishGrade": False,
                "DropboxInd": False,
                "DropboxNumFiles": "1",
                "DropboxTimeLate": "11:59 PM",
                "SectionLinks": [
                    {
                    "SectionId": section,
                    "DateAssigned": datetime.datetime.now().strftime("%m/%m/%Y"),
                    "AssignmentTime": "00:00:00",
                    "DateDue": assign["date"],
                    "DueTime": "8:30 AM",
                    "Section": None,
                    "PublishInd": True,
                    "PublishOnAssignedInd": False
                    }
                ],
                "LinkItems": [],
                "DownloadItems": [],
                "SendNotification": False,
                "Notifications": [],
                "HasGrades": False,
                "RubricId": 0,
                "Lti": []
            }
            # response = rq.post(f"{subdomain}.myschoolapp.com/api/academics/assignment?t={token}", json=headers)
            # print(response.text)
            print(f"this would publish {abbrev}")
        
select = tk.Button(root, text="Choose file", command=openfile)
select.pack(pady=(10))

boxlabel = tk.Label(root, text="Class ID")
boxlabel.pack()

idbox = tk.Entry()
idbox.pack()

def upstart():
    global section
    section = idbox.get()
    csvread()

upload = tk.Button(root, text="Upload files", command=upstart)
upload.pack(pady=10)

root.geometry("400x200")

root.mainloop()