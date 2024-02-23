from tkinter import *
from tkinter import messagebox, END
from datetime import datetime
import pygame
from tkinter import Toplevel, Label, Entry, Button
from tkcalendar import *
import time

pygame.mixer.init()

# audio
audio_path_add = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/audios/audio.mp3"
audio_path_remove = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/audios/remove.mp3"
audio_path_pick_theme = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/audios/pick_theme.mp3"
audio_path_edit = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/audios/edit.mp3"
audio_path_select = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/audios/select.mp3"

# image
edit_image_path = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/pen25x25.png"
remove_image_path = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/trash25x25.png"
add_in_image_path = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/add25x25.png"
refresh_deadline_path = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/calendar.png"
menu_image_path = "/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/menu25x25.png"


def edit_task():
    selected_task_index = task_listbox.curselection()
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()

    if not selected_task_index:
        messagebox.showinfo("Error", "No task selected.")
        return

    task_info = task_listbox.get(selected_task_index[0])

    if ' | Due: ' in task_info:
        task, due_date_str = task_info.split(' | Due: ')
    elif ' | due: ' in task_info:
        task, due_date_str = task_info.split(' | due: ')
    else:
        messagebox.showinfo("Error", "Unexpected task format.")
        return

    try:
        due_date = datetime.strptime(due_date_str, "%m/%d/%y")

        if deadline_has_passed(due_date):
            messagebox.showinfo("Task Edit", f"The deadline for '{task}' has passed. Editing not allowed.")
            return

        edit_top = Toplevel()
        edit_top.title("Edit Task")
        edit_top.geometry("300x150")

        task_entry_edit = Entry(edit_top, font=('Helvetica', 14), relief=SOLID)
        task_entry_edit.insert(0, task)
        task_entry_edit.pack(pady=10)

        def update_task():
            new_task = task_entry_edit.get()
            pygame.mixer.music.load(audio_path_add)
            pygame.mixer.music.play()
            if new_task:
                task_listbox.delete(selected_task_index)
                task_listbox.insert(selected_task_index, f"{new_task} | Due: {due_date_str}")
                edit_top.destroy()
            else:
                messagebox.showinfo("Error", "Task cannot be empty.")

        confirm_button = Button(edit_top, text="Confirm Edit", command=update_task)
        confirm_button.pack(pady=10)

    except ValueError:
        messagebox.showinfo("Invalid Due Date", "Error parsing due date.")


def edit_deadline():
    selected_task_index = task_listbox.curselection()
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()

    if not selected_task_index:
        messagebox.showinfo("Error", "No task selected.")
        return

    try:
        refresh_top = Toplevel()
        refresh_top.title("Refresh Deadline")
        refresh_top.geometry("300x150")

        def refresh_deadline():
            pygame.mixer.music.load(audio_path_add)
            pygame.mixer.music.play()
            new_due_date_str = select_due_date()

            try:
                new_due_date = datetime.strptime(new_due_date_str, "%m/%d/%y")
                current_date = datetime.now()

                if new_due_date <= current_date:
                    messagebox.showinfo("Invalid Due Date", "The due date has already passed.")
                else:
                    task_info = task_listbox.get(selected_task_index[0])
                    task_listbox.delete(selected_task_index)
                    task_listbox.insert(selected_task_index, f"{task_info.split(' | Due: ')[0]} | Due: {new_due_date_str}")
                    refresh_top.destroy()

            except ValueError:
                messagebox.showinfo("Invalid Due Date", "Error parsing due date.")

        refresh_button = Button(refresh_top, text="change deadline", command=refresh_deadline)
        refresh_button.pack(pady=10)

    except ValueError:
        messagebox.showinfo("Invalid Due Date", "Error parsing due date.")


def add_task():
    task = task_entry.get()
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()
    if not task:
        messagebox.showinfo("Error", "write down the task")
        return

    due_date_str = select_due_date()

    if task and due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%m/%d/%y")
            current_date = datetime.now()

            if due_date <= current_date:
                messagebox.showinfo("Invalid Due Date", f"The due date for '{task}' has already passed.")
            else:
                task_listbox.insert(END, f"{task} | Due: {due_date_str}")
                task_entry.delete(0, END)
                pygame.mixer.music.load(audio_path_add)
                pygame.mixer.music.play()

        except ValueError:
            messagebox.showinfo("invalid Due Date", "please select a valid date format (MM/DD/YY).")


def select_due_date():
    def grab_date():
        due_date_str = cal.get_date()
        pygame.mixer.music.load(audio_path_add)
        pygame.mixer.music.play()
        my_label.config(text="Due date is " + due_date_str)
        top.after(500, lambda: top.destroy())
        top.due_date_str = due_date_str

    top = Toplevel()
    top.title("Calendar")
    top.geometry("300x280")
    top.resizable(False, False)

    cal = Calendar(top, selectmode='day', year=time.localtime().tm_year, month=time.localtime().tm_mon, day=time.localtime().tm_mday)
    cal.pack(pady=10)

    my_button = Button(top, text="Set Date", command=grab_date)
    my_button.pack(pady=10)
    my_label = Label(top, text='')
    my_label.pack(pady=10)

    top.wait_window(top)

    return getattr(top, 'due_date_str', None)


def remove_task():
    selected_task_index = task_listbox.curselection()
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()

    if not selected_task_index:
        messagebox.showinfo("Error", "no task selected.")
        return

    task_info = task_listbox.get(selected_task_index[0])

    if ' | Due: ' in task_info:
        task, due_date_str = task_info.split(' | Due: ')
    else:
        messagebox.showinfo("Error", "Unexpected task format.")
        return

    try:
        due_date = datetime.strptime(due_date_str, "%m/%d/%y")

        if deadline_has_passed(due_date):
            confirmation = messagebox.askyesno('Task Removal',
                                               f"The deadline for '{task}' has passed. Do you still want to delete it?")
            if confirmation:
                task_listbox.delete(selected_task_index[0])
                messagebox.showinfo("Task", f"'{task}' deleted")
                pygame.mixer.music.load(audio_path_remove)
                pygame.mixer.music.play()
            else:
                messagebox.showinfo("Task Removal", f"Deletion of '{task}' canceled.")
        else:
            confirmation = messagebox.askyesno('Alert', f"Do you really want to delete task: {task} ?")
            if confirmation:
                task_listbox.delete(selected_task_index)
                messagebox.showinfo("Task", f"'{task}' deleting")
                pygame.mixer.music.load(audio_path_remove)
                pygame.mixer.music.play()
            else:
                messagebox.showinfo("Task Removal", f"Deletion of '{task}' canceled.")

    except ValueError:
            messagebox.showinfo("Invalid Due Date", "Error parsing due date.")


def deadline_has_passed(due_date):
    current_date = datetime.now()
    return due_date < current_date


def on_enter_key(event):
    add_task()


def on_delete_key(event):
    remove_task()

def open_theme_popup(selected_theme_var):
    theme_popup = Toplevel(root)
    theme_popup.title("Select Theme")
    theme_popup.config(width=100, height=100)
    theme_popup.geometry("165x120")
    theme_popup.resizable(True, True)

    theme_label = Label(theme_popup, text='Select Theme:', font=('Helvetica', 12))
    theme_label.pack(pady=5)

    themes = ['Blue', 'Green', 'Pink', 'Purple', 'Red']

    theme_dropdown = OptionMenu(theme_popup, selected_theme_var, *themes)
    theme_dropdown.pack(pady=5)

    apply_button = Button(theme_popup, text="Apply", command=lambda: apply_theme(selected_theme_var.get(), theme_popup))
    apply_button.pack(pady=10)
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()
    if not selected_theme_var:
        root.destroy()


def apply_theme(selected_theme, theme_popup):
    if selected_theme == 'Blue':
        apply_blue_theme()
    elif selected_theme == 'Green':
        apply_green_theme()
    elif selected_theme == 'Pink':
        apply_pink_theme()
    elif selected_theme == 'Purple':
        apply_purple_theme()
    elif selected_theme == 'Red':
        apply_red_theme()
    pygame.mixer.music.load(audio_path_pick_theme)
    pygame.mixer.music.play()

    theme_popup.destroy()


def change_theme():
    selected_theme_var = StringVar(root)
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()
    selected_theme_var.set('Purple')
    open_theme_popup(selected_theme_var)
    pygame.mixer.music.load(audio_path_add)
    pygame.mixer.music.play()


def apply_blue_theme():
    canvas.config(bg='#070F2B')
    title.config(bg='#1B1A55', fg='#FFFFFF')
    task_entry.config(bg='#9290C3')
    task_listbox.config(bg='#535C91', selectbackground='#3498DB')


def apply_green_theme():
    canvas.config(bg='#2ECC71')
    title.config(bg='#2ECC71', fg='#FFFFFF')
    task_entry.config(bg='#ECF0F1')
    task_listbox.config(bg='#ECF0F1', selectbackground='#2ECC71')


def apply_pink_theme():
    canvas.config(bg='#FF66B2')
    title.config(bg='#FF66B2', fg='#FFFFFF')
    task_entry.config(bg='#FFD9EB')
    task_listbox.config(bg='#FFD9EB', selectbackground='#FF66B2')


def apply_purple_theme():
    canvas.config(bg='#8E44AD')
    title.config(bg='#8E44AD', fg='#FFFFFF')
    task_entry.config(bg='#D2B4DE')
    task_listbox.config(bg='#D2B4DE', selectbackground='#8E44AD')


def apply_red_theme():
    canvas.config(bg='#E74C3C')
    title.config(bg='#E74C3C', fg='#FFFFFF')
    task_entry.config(bg='#FADBD8')
    task_listbox.config(bg='#FADBD8', selectbackground='#E74C3C')


def show_description(description):
    messagebox.showinfo("Button Description", description)



# description
add_description = "add new task"
remove_description = "delete selected task"
edit_description = "edit selected task"
refresh_description = "edit deadline"


root = Tk()
root.title("Task Manager")
root.geometry('420x600')
root.resizable(width=False, height=False)
# root.after(0, check_deadlines)


image_icon = PhotoImage(file="/Users/meruyertbauyrzhanqyzy/Documents/uni/pythonProject/TaskManager/images/icons8-task-50.png")
root.iconphoto(False, image_icon)

canvas = Canvas(root, height=600, width=420, bg='#3498DB')
canvas.pack()

frame = Frame(root, bg='#FFFFFF', bd=5)
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

title = Label(frame, text='Task Manager', bg='#3498DB', fg='#FFFFFF', font=('Helvetica', 18, 'bold'))
title.pack(pady=10)

task_entry = Entry(frame, bg='#ECF0F1', font=('Helvetica', 16), relief=SOLID)
task_entry.pack(pady=10, padx=10, ipady=5, fill=X)


# BUTTONS
add_image = PhotoImage(file=add_in_image_path)
add_button = Button(frame, image=add_image, command=add_task, cursor="hand")
add_button.place(x=10, y=100, width=40, height=40)
# add_button.bind("<Enter>", lambda event: show_description(add_description))

remove_image = PhotoImage(file=remove_image_path)
remove_button = Button(frame, image=remove_image, command=remove_task, cursor="hand2")
remove_button.place(x=276, y=100, width=40, height=40)
 # remove_button.bind("<Enter>", lambda event: show_description(remove_description))

edit_image = PhotoImage(file=edit_image_path)
edit_button = Button(frame, image=edit_image, command=edit_task, cursor="hand2")
edit_button.place(x=226, y=100, width=40, height=40)
# edit_button.bind("<Enter>", lambda event: show_description(edit_description))

calendar_image = PhotoImage(file=refresh_deadline_path)
refresh_button = Button(frame, image=calendar_image, command=edit_deadline, cursor="hand2")
refresh_button.place(x=60, y=100, width=40, height=40)
# refresh_button.bind("<Enter>", lambda event: show_description(refresh_description))

menu_image = PhotoImage(file=menu_image_path)


# List Box
task_listbox = Listbox(frame, bg='#ECF0F1', font=('Helvetica', 16), selectbackground='#3498DB', selectmode=SOLID, bd=0)
task_listbox.pack(pady=45, padx=10, fill=BOTH, expand=True)


menu_button = Menubutton(frame,image=menu_image,indicatoron=True,borderwidth=1,relief="raised")
menu_button.place(x=276,y=10,width=40,height=30)

course = Menu(menu_button,tearoff=0)
course.add_command(label="select theme",command=change_theme)

menu_button['menu']=course

# ONKEY
task_entry.bind('<Return>', on_enter_key)
remove_button.bind('<Delete>', on_delete_key)


apply_purple_theme()
root.mainloop()
