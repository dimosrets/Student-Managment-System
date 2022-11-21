#import everything that program needs from tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#import the database
from Database import StudentsDatabase

#import module webbrowser to be able open a URL 
import webbrowser as web

#import fpdf to be able to extract students information in pdf
from fpdf import FPDF


#some global configurations for text and color
text_font = ( "Arial", 12 ,"bold")
background_color = "#24d186"

#############################
### DECLARE ALL FUNCTIONS ###
#############################

	############################
	### FOR COPYRIGHTS FRAME ###
	############################
def findme():
	web.open("https://linktr.ee/_rets",new = "new")
	#####################################
	### END OF COPYRIGHTS FRAME       ###
	#####################################

    ######################
	### FOR LEFT FRAME ###
    ######################

def calculate_lessons(row):
	return_value = row.strip().split("\n")
	if return_value != ['']:
		print(len(row.strip().split("\n")))
		print(row.strip().split("\n"))
		return len(row.strip().split("\n"))
	return 0
	#r2 = [i.split()[2] for i in r[:len(r)]]
	#print(r2)

def calculate_hours(row):
	try :
		r = row.strip().split("\n")
		hours_string = [i.split()[2] for i in r[:len(r)]]
		#ta exoume etsi ['13:00-14:00', '13:00-14:00', '13:00-14:00', '13:00-14:00', '13:00-14:00', '19:30-20:00', '16:00-18:10']
		hours_list_string = [ i.split("-") for i in hours_string]
		#ta exoume etsi [['13:00', '14:00'], ['13:00', '14:00'], ['13:00', '14:00'], ['13:00', '14:00'], ['13:00', '14:00'], ['19:30', '20:00'], ['16:00', '18:10']]

		hours = 0
		minutes = 0
		for time in hours_list_string :
			ap_hour = 0
			ap_min = 0
			
			first = time[0]
			second = time[1]

			first_hour = int(first.split(":")[0])
			first_min = int(first.split(":")[1])

			second_hour = int(second.split(":")[0])
			second_min = int(second.split(":")[1])
			if second_min == first_min == 0 :
				ap_hour = second_hour - first_hour
			elif first_min == second_min and first_min != 0:
				ap_hour += 1
			elif first_min != second_min and second_min == 0 :
				ap_min = 60-first_min 
				if first_hour +1 < second_hour:
					ap_hour += second_hour-first_hour-1
			elif second_min != first_min and first_min == 0:
				ap_hour += second_hour - first_hour
				ap_min = second_min
			elif second_min != first_min != 0:
				ap_min = 60 - first_min + second_min
				if first_hour+1 < second_hour :
					ap_hour = second_hour - first_hour-1

			hours += ap_hour
			minutes += ap_min
			print("{} {}".format(ap_hour,ap_min))
		hours += minutes // 60 
		minutes = minutes %60
		print("total : {} {} ".format(hours,minutes))
		if minutes == 0 :
			return hours
	except :
		return 0
	return str(hours) +" "+str(minutes)

def calculate_unpaid(ppH , h , pai):
	print(f"""
		{ppH}
		{h}
		{pai}
		""")
		
	try :
		unpaid = h*ppH -  pai
	except (TypeError,ValueError):
		print("mplasasa" ,h.split())
		unpaid = int(h.split()[0])*ppH + ( int(h.split()[1])/60 * ppH) -  pai
			
	return unpaid

def add_student():
    if name.get() == "" or phone.get() == "" or pricePerHour.get() == "" or LessonsText.get(1.0, END) == "":
        messagebox.showerror("Wronk", "You should fill all fields")
        return
    db.add(name.get(),phone.get(),pricePerHour.get(), paid.get() ,LessonsText.get(1.0,END) , CommentsText.get(1.0, END))
    messagebox.showinfo("Success", "Registration successed")
    clearAll()
    dispalyAll()

def update_student():
    if name.get() == "" or phone.get() == "" or pricePerHour.get() == '' or LessonsText.get(1.0, END) == "" or paid.get() == "":
        messagebox.showerror("Wronk", "You should fill all fields")
        return
    # id, name, phone_num, lessons_dates, paid,comments
    db.update(row[0],name.get(),phone.get(),pricePerHour.get(), paid.get()   ,LessonsText.get(1.0,END),CommentsText.get(1.0, END))
    messagebox.showinfo("Success", "Update successed")
    clearAll()
    dispalyAll()


def delete_student():
    db.remove(row[0])
    messagebox.showinfo("Success", "Deletion successed")
    clearAll()
    dispalyAll()

def print_student():
	if name.get() == "" or phone.get() == "" or pricePerHour.get() == "" or LessonsText.get(1.0, END) == "":
		messagebox.showerror("Wronk", "You should fill all fields")
		return
	
	pdf = FPDF()
	pdf.add_page()

	pdf.set_fill_color(255, 255, 250.0) # color for outer rectangle
	pdf.rect(3.0, 3.0, 205.0,292.0,'DF')
	
	pdf.set_fill_color(255, 255, 255) # color for inner rectangle
	pdf.rect(5.0, 5.0, 201.0,288.0,'FD')
	
	pdf.add_font('Arial', '', 'c:/windows/fonts/arial.ttf', uni=True)
	pdf.set_font("Arial", size = 25 )

	pdf.cell(200, 10, txt = "Ονοματεπώνυμο: "+name.get(),
	         ln = 1, align = 'L')
	pdf.cell(200, 10, txt = "Τηλέφωνο: "+phone.get(),
	         ln = 2, align = 'L')
	pdf.cell(200, 10, txt = "Τιμή Ανά Ώρα: "+str(pricePerHour.get())+"€",
	         ln = 3, align = 'L')
	pdf.cell(200, 10, txt = "Εξόφληση: "+str(paid.get())+"€",
	         ln = 4, align = 'L')
	if len(totalHours.get().split()) > 1:
		unpaid = int(totalHours.get().split()[0])*pricePerHour.get() + ( int(totalHours.get().split()[1])/60 * pricePerHour.get()) -  paid.get()
		if unpaid < 0 :
			pdf.cell(200,10,txt = "Πλεόνασμα: "+str(abs(unpaid))+"€",ln = 4, align = 'L')
		else :
			pdf.cell(200,10,txt = "Υπόλοιπο: "+str(unpaid)+"€",ln = 4, align = 'L')
	else :
		unpaid = int(totalHours.get())*pricePerHour.get() -  paid.get()
		if unpaid < 0 :
			pdf.cell(200,10,txt = "Πλεόνασμα: "+str(abs(unpaid))+"€",ln = 4, align = 'L')
		else :
			pdf.cell(200,10,txt = "Υπόλοιπο: "+str(unpaid)+"€",ln = 4, align = 'L')
	pdf.cell(200, 10, txt = "Μαθήματα",
	         ln = 5, align = 'C')
	lessons = LessonsText.get(1.0,END).strip().split("\n")
	for i in lessons:
		pdf.cell(200, 10, txt = i,ln = 1, align = 'L')
	pdf.cell(200, 10, txt = "",ln = 1, align = 'L')
	pdf.cell(200 , 10, txt = "Μαθήματα "+str(totalLessons.get())+" Ώρες "+str(totalHours.get()),ln = 6, align = 'L')
	pdf.cell(200, 10, txt = "Σχόλια",
	         ln = 6, align = 'C')
	Comments = CommentsText.get(1.0,END).strip().split("\n")
	for i in Comments:
		pdf.cell(200, 10, txt = i,ln = 1, align = 'L')
	
	messagebox.showinfo("Επιτυχία", "Το Έγγραφο βρίσκεται στον φάκελο Students")
	pdf.output( "Students\\"+name.get()+".pdf","F")
	
	clearAll()
	#Malakies TORA
	"""
	print("Ονοματεπώνυμο: "+name.get())
	print("Τηλέφωνο: "+phone.get())
	print("Τιμή Ανά Ώρα: "+str(pricePerHour.get())+"€")
	print("Εξόφληση: "+str(paid.get())+"€")
	if len(totalHours.get().split()) > 1:
		unpaid = int(totalHours.get().split()[0])*pricePerHour.get() + ( int(totalHours.get().split()[1])/60 * pricePerHour.get()) -  paid.get()
		if unpaid < 0 :
			print("Πλεόνασμα: "+str(abs(unpaid))+"€")
		else :
			print("Υπόλοιπο: "+str(unpaid)+"€")
	else :
		unpaid = int(totalHours.get())*pricePerHour.get() -  paid.get()
		if unpaid < 0 :
			print("Πλεόνασμα: "+str(abs(unpaid))+"€")	
		else :
			print("Υπόλοιπο: "+str(unpaid)+"€")
	print("Μαθήματα")
	lessons = LessonsText.get(1.0,END).strip().split("\n")
	for i in lessons:
		print(i)
	print("Μαθήματα "+str(totalLessons.get())+" Ώρες "+str(totalHours.get()))
	print("Σχόλια")
	Comments = CommentsText.get(1.0,END).strip().split("\n")
	for i in Comments:
		print(i)
	
	messagebox.showinfo("Επιτυχία", "Το Έγγραφο βρίσκεται στον φάκελο Students")
	print("pdf.output('Students\\"+name.get()+".pdf', F )")
	"""
	clearAll()

def clearAll():
	global row
	row = []
	name.set("")
	phone.set("")
	LessonsText.delete(1.0, END)
	paid.set("0")
	unpaid.set("0")
	pricePerHour.set("0")
	totalLessons.set("0")
	totalHours.set("0")
	CommentsText.delete(1.0, END)

    #########################
    ### END OF LEFT FRAME ###
    #########################

    #######################
	### FOR RIGHT FRAME ###
    #######################

def get_student(event):
	selected_row = tv.focus()
	data = tv.item(selected_row)
	global row
	row = data["values"]
	name.set(row[1])
	phone.set(row[2])
	pricePerHour.set(row[3])
	paid.set(row[4])
	unpaid.set(calculate_unpaid(row[3], calculate_hours(row[5]) , row[4]))
	LessonsText.delete(1.0, END)
	totalLessons.set(calculate_lessons(row[5]))
	totalHours.set(calculate_hours(row[5]))
	LessonsText.insert(END, row[5])
	CommentsText.delete(1.0, END)
	CommentsText.insert(END,row[6])
	
   

def dispalyAll():
	tv.delete(*tv.get_children())

	for row in db.all_students():
		#print(row)
		tv.insert("", END, values=row)


    ##########################
	### END OF RIGHT FRAME ###
    ##########################


###################################
### END DECLARING ALL FUNCTIONS ###
###################################


#########################
###    INIT THE APP   ###
#########################
#connect to the database
db = StudentsDatabase("Students.db")

#general settings to make the tkinter app
app = Tk()
app.title("Students Managment System for a Τutoring Τeacher")
app.geometry("1000x800")
app.minsize( height= 700 ,  width = 1000)

name = StringVar()
phone = StringVar()
pricePerHour = IntVar()
paid = IntVar()
totalHours = StringVar()
totalLessons = IntVar()
unpaid = IntVar()
#############################
###  END OF INIT THE APP  ###
#############################

########################
###  GUI LEFT FRAME  ###
########################
Left = Frame(app , bg = background_color)

NameLabel = Label( Left , bg = background_color , text = "Full Name" , font = text_font)
NameEntry = Entry( Left, font = text_font, textvariable = name)

PhoneLabel = Label( Left , bg = background_color , text = "Phone" , font = text_font)
PhoneEntry = Entry( Left , font = text_font , textvariable = phone)

PriceLabel = Label( Left , bg = background_color , text = "Price per hour" ,font = text_font)
PriceEntry = Entry( Left , bg = background_color , textvariable = pricePerHour , font = text_font)

PaidLabel = Label( Left , bg = background_color , text = "Paid" ,font = text_font)
PaidEntry = Entry( Left , bg = background_color , textvariable = paid , font = text_font)

UnpaidLabel = Label( Left , bg = background_color , text = "Unpaid" ,font = text_font)
UnpaidINTLabel = Label( Left , bg = background_color , textvariable = unpaid ,font = text_font)

LessonsTextLabel = Label(Left , text = "Lessons", font = text_font , bg = background_color)
LessonsText = Text( Left , height = 10 , width = 40)

HoursLabel = Label( Left , bg = background_color , text = "Total Hours" , font = text_font)
HoursVarLabel = Label( Left , bg = background_color , textvariable = totalHours , font = text_font)

LessonsLabel = Label( Left , bg = background_color , text = "Total Lessons" , font = text_font)
LessonsVarLabel = Label( Left , bg = background_color , textvariable = totalLessons , font = text_font)

CommentsTextLabel = Label( Left ,  bg = background_color , text = "Comments" , font = text_font)
CommentsText = Text( Left , height = 10 , width = 40 )

AddButton = Button( Left , bg = background_color , text = "Add Student", font = text_font , command = add_student)
DeleteButton = Button( Left , bg = background_color , text = "Delete", font = text_font, command = delete_student)
UpdateButton = Button( Left , bg = background_color , text = "Update", font = text_font, command = update_student)
ClearAllButton = Button( Left , bg = background_color , text = "Clear", font = text_font , command = clearAll)
PrintButton = Button( Left ,  bg = background_color , text = "Print", font = text_font , command = print_student)
#grid all widgets of left frame 
NameLabel.grid(row = 0 , column = 0 , columnspan = 3)
NameEntry.grid(row = 0 , column = 3 , columnspan = 3)

PhoneLabel.grid(row = 1 , column = 0 , columnspan = 3)
PhoneEntry.grid(row = 1 , column = 3 , columnspan = 3)

PriceLabel.grid(row = 2 , column = 0 , columnspan = 3)
PriceEntry.grid(row = 2 , column = 3 , columnspan = 3)

PaidLabel.grid(row = 3 , column = 0 , columnspan = 3)
PaidEntry.grid(row = 3 , column = 3 , columnspan = 3)

UnpaidLabel.grid(row = 4 , column = 0 , columnspan = 3)
UnpaidINTLabel.grid(row = 4 , column = 3 , columnspan = 3)

LessonsTextLabel.grid(row = 5 , column = 0 , columnspan = 6)
LessonsText.grid(row = 6 , column = 0 , columnspan = 6)

HoursLabel.grid(row = 7 , column = 0 , columnspan = 3)
HoursVarLabel.grid(row = 7 , column = 3 , columnspan = 3)

LessonsLabel.grid(row = 8 , column = 0 , columnspan = 3) 
LessonsVarLabel.grid(row = 8 , column = 3 , columnspan = 3)

CommentsTextLabel.grid(row =  9, column = 0 , columnspan = 6)
CommentsText.grid(row = 10, column = 0 , columnspan = 6)

AddButton.grid(row = 12 , column = 0 , columnspan = 3)
DeleteButton.grid(row = 12 , column = 3 , columnspan = 3)
UpdateButton.grid(row = 13 , column = 0 , columnspan = 3, pady = 5)
ClearAllButton.grid(row = 13 , column = 3 , columnspan = 3, pady = 5)
PrintButton.grid(row = 14 , column = 0 , columnspan = 6, pady = 5)

###############################
### END OF  GUI LEFT FRAME  ###
###############################

#######################
### GUI RIGHT FRAME ###
#######################
Right = Frame( app , bg = background_color)

StudentsLabel = Label(Right , text = "Students", font = text_font , bg = background_color)
s = ttk.Style()
s.configure("mystyle.Treeview",
                rowheight=17) 
s.configure("mystyle.Treeview.Heading", font = text_font, background = background_color, fieldbackground =  background_color)
tv = ttk.Treeview(Right, columns=(1, 2), style="mystyle.Treeview",height = 10)

tv.column('#0',anchor= "center", stretch=YES )
tv.heading("1",anchor= "center", text="ID")
tv.column("1",anchor= "center", width = 75)
tv.heading("2",anchor= "center", text="Full Name")
tv.column("2",anchor= "center", width = 125)
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", get_student)

StudentsLabel.pack(side = TOP , fill = X)
tv.pack(side = BOTTOM , fill = BOTH , expand = 1)
##############################
### END OF GUI RIGHT FRAME ###
##############################


############################
### GUI COPYRIGHTS FRAME ###
############################
CopyRights = Frame(app , bg = background_color )
Label(CopyRights , text = "Made By Rets. All Rights Reserved(lefts  too)", background = background_color , font = text_font ).pack()
Button( CopyRights , text = "Find Rets on Social", background = background_color , font = text_font , command = findme).pack()
###################################
### END OF GUI COPYRIGHTS FRAME ###
###################################

################################
### DISPLAY THE APP'S FRAMES ###
################################

CopyRights.pack(side = BOTTOM , fill = BOTH)
Right.pack(side = RIGHT , fill = BOTH , expand = 1)
Left.pack(side = LEFT , fill = BOTH, expand = 1)



dispalyAll()

app.mainloop()
