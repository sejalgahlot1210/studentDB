import psycopg2
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def run_query(query,parameters=()):
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="123456789",host="localhost",port="5432")
    cur = conn.cursor()
    query_results = None
    try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):
            query_results = cur.fetchall()
        conn.commit()
    
    except psycopg2.Error as e:
        messagebox.showerror("Database Failed",str(e))

    finally:
        cur.close()
        conn.close()

    return query_results

def refresh_treeview():
    for item in tree.get_children():
        tree.delete(item)
    records = run_query("select * from students;")
    for record in records:
        tree.insert('',END, values=record)

def insert_data():
    query = "insert into students(name,address,age,phonenum) values (%s,%s,%s,%s)"
    parameters = (name_entry.get(), addr_entry.get(),age_entry.get(),phone_entry.get())
    run_query(query, parameters)
    messagebox.showinfo("Information","Data Inserted!")
    refresh_treeview()

def delete_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "delete from students where id=%s"
    parameters = (student_id, )
    run_query(query,parameters)
    messagebox.showinfo("Information","Data deleted successfully!")
    refresh_treeview()

def update_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "update students set name=%s, address=%s, age=%s, phonenum=%s where id=%s"
    parameters = (name_entry.get(), addr_entry.get(),age_entry.get(),phone_entry.get(),student_id)
    run_query(query,parameters)
    messagebox.showinfo("Information","Data updated successfully!")
    refresh_treeview()

root = Tk()
root.title("STUDENT DBMS")

#labelFrame helps you to place labels on the top of frame 
frame = LabelFrame(root, text="Student Data")
#sticky sets the alignment of frame to ew, ew: east west i.e stratched the frame along east west i.e horizontally
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

Label(frame, text="Name: ").grid(row=0, column=0, padx=5,sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, pady=5, sticky="ew")

Label(frame, text="Address: ").grid(row=1, column=0, padx=5,sticky="w")
addr_entry= Entry(frame)
addr_entry.grid(row=1,column=1, pady=5, sticky="ew")

Label(frame, text="Age: ").grid(row=2, column=0, padx=5, sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1, pady=5, sticky="ew")

Label(frame, text="Phone number: ").grid(row=3, column=0, padx=5, sticky="w")
phone_entry = Entry(frame)
phone_entry.grid(row=3, column=1, pady=5, sticky="ew")

#seperate frame to create buttons
button_frame = Frame(root)
button_frame.grid(row=1, column=0, pady=5, sticky= "ew")
Button(button_frame, text="Create Data", padx=8, command=insert_data).grid(row=0, column=0, padx=5, pady=5, sticky="w")
Button(button_frame, text="Add Data", padx=8,command=insert_data).grid(row=0, column=1, padx=5, pady=5, sticky="w")
Button(button_frame, text="Update Data",command=update_data).grid(row=0, column=2, padx=5, pady=5, sticky="w")
Button(button_frame, text="Delete Data", padx=8,command=delete_data).grid(row=0, column=3, padx=5, pady=5, sticky="w")

#tree frame to display data
tree_frame = Frame(root)
tree_frame.grid(row=2, column= 0, padx=10, sticky= "nsew")

#scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

#browse is used to select one entry at a time
#yscrollcommand connects scrollbar to treeview and updates scroller position when scrolled
#yview updates the tree view entries when scrolled
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode= "browse")
tree.pack()
tree_scroll.config(command=tree.yview)

#create column names in tree view
tree['columns'] = ("student_id","name","address","age","phone number")
tree.column("#0",width=0, stretch=NO)
tree.column("student_id", anchor=CENTER, width=80)
tree.column("name", anchor=CENTER, width=120)
tree.column("address", anchor=CENTER, width=120)
tree.column("age", anchor=CENTER, width=50)
tree.column("phone number", anchor=CENTER, width=120)

tree.heading("student_id",text="ID",anchor=CENTER)
tree.heading("name",text="Name",anchor=CENTER)
tree.heading("address",text="Address",anchor=CENTER)
tree.heading("age",text="Age",anchor=CENTER)
tree.heading("phone number",text="Phone Number",anchor=CENTER)

refresh_treeview()
root.mainloop() 