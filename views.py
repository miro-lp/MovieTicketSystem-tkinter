import os
from tkinter import Button, Label, Entry, Frame

from PIL import Image, ImageTk

from helper import clean_screen, check_entries_value
from manager import ManagerDB

from canvas import tk
from models.hall import Hall
from models.movie import Movie
from models.program import ProgramHour
from models.theater import MovieTheater

manager_user = ManagerDB()
manager_theater = ManagerDB('theaters.txt')
manager_movie = ManagerDB('movies.txt')
manager_hall = ManagerDB('halls.txt')
manager_program = ManagerDB('programs.txt')

base_folder = os.path.dirname(__file__)


def login_view():
    clean_screen()
    Label(text="Username", bg='blue', fg="white").grid(row=0, column=0, pady=2)
    user_name = Entry(tk, text="username")
    user_name.grid(row=0, column=1)
    Label(text="Password", bg='blue', fg="white").grid(row=1, column=0)
    password = Entry(tk, show="*")
    password.grid(row=1, column=1)
    login_btn = Button(tk, text="Login", bg="green", fg="white", height=2, width=15,
                       command=lambda: loged_view(username=user_name.get(), password=password.get()))
    login_btn.grid(row=2, column=3, padx=20, pady=20)


user = {}
classes_dict = {
    'theater': [MovieTheater, 2],
    'movie': [Movie, 4],
    'hall': [Hall, 4],
    'program': [ProgramHour, 5],
}


def loged_view(username, password):
    global user
    try:
        user = manager_user.login(username, password)
        all_theater_view()
    except ValueError as err:
        # print(err)
        Label(text=f'{err}', bg='#dece7e', fg="red", height=2, width=50, font=('Bold', 15)).grid(row=3, column=4,
                                                                                                 pady=10)


def all_theater_view():
    clean_screen()
    frame1 = Frame(tk, height=50, width=150)
    frame1.grid(row=0, column=0, pady=(20, 50))
    navPanel(frame1, login_view)
    frame2 = Frame(tk, height=200, width=1400)
    frame2.grid(row=1, column=2, pady=50, padx=(70, 150))

    theaters = manager_theater.get_all_items()
    counter = 0
    for t in theaters:
        img1 = Image.open(os.path.join(base_folder, t["img_path"]))
        bg = ImageTk.PhotoImage(img1)
        button = Button(frame2, text=f'{t["name"]}', compound='top', image=bg, font=('Bold', 15), bg='purple',
                        fg="white",
                        height=150, width=200,
                        command=lambda id=t['id']: theater_all_options(id))
        button.pack(side='left', expand=True)
        button.image = bg
        counter += 1
    if user['role'] == 'admin':
        frame3 = Frame(tk, height=50, width=1200)
        frame3.grid(row=2, column=2, padx=(70, 150))
        button_create = Button(frame3, text='Admin panel', bg='green', fg="white", height=2, width=30,
                               command=lambda: admin_control_options())
        button_create.pack(side='bottom')


def admin_control_options():
    clean_screen()
    options = {'Theater': lambda: crud_operation_view(manager_theater, 'theater'),
               'Movie': lambda: crud_operation_view(manager_movie, 'movie'),
               'Hall': lambda: crud_operation_view(manager_hall, 'hall'),
               'Program': lambda: crud_operation_view(manager_program, 'program')}

    for o in options:
        button = Button(tk, text=f'{o}', bg='green', font=(20), fg="white", height=12, width=24,
                        command=options[o])
        button.pack(side='left', expand=True)
        button.bind('<Enter>', lambda e, b=button: b.configure(bg="#5bc777"))
        button.bind('<Leave>', lambda e, b=button: b.configure(bg="green"))


def theater_all_options(id):
    clean_screen()
    frame = Frame(tk)
    frame.grid(row=0, column=0, pady=(20, 50))
    navPanel(frame, all_theater_view)

    program = filter(lambda x: x['theater_id'] == id, manager_program.get_all_items())
    program = sorted(program, key=lambda x: x['start'])
    # print(program)
    counter = 1

    for item in program:
        frame = Frame(tk)
        frame.grid(row=counter, column=1, padx=(70, 150), pady=(0, 10))
        movie = list(filter(lambda x: x['id'] == item['movie_id'], manager_movie.get_all_items()))[0]
        hall = list(filter(lambda x: x['id'] == item['hall_id'], manager_hall.get_all_items()))[0]
        data = {'time': [f'{item["start"]} -{item["end"]}', ''],
                'movie_name': [movie['title'], ''],
                'hall_name': [f'Hall name\n{hall["name"]}', lambda: reserve_seats(movie, hall)],
                'sold_tickets': [item['tickets'], '']}
        # print(item)
        counter += 1
        for i in data:
            button = Button(frame, text=f'{data[i][0]}', bg='purple', font=(25), fg="white", height=3, width=24,
                            command=data[i][1])
            button.pack(side='left', expand=True)

        # print(movie, hall)


# def theater_crud_operation():
#     clean_screen()
#     theaters = manager_theater.get_all_items()
#     rows = []
#     titles = []
#     counter = 0
#     for i in theaters[0].keys():
#         e = Label(relief='ridge', text=i)
#         e.grid(row=0, column=counter, sticky='nsew')
#         counter += 1
#         titles.append(e)
#     counter += 1
#     e_a = Label(relief='ridge', text='action')
#     e_a.grid(row=0, column=counter, sticky='nsew')
#     titles.append(e_a)
#     counter += 1
#     d_a = Label(relief='ridge', text='action')
#     d_a.grid(row=0, column=counter, sticky='nsew')
#     titles.append(d_a)
#     rows.append(titles)
#     for i in range(len(theaters)):
#         cols = []
#         e = Label(relief='ridge', text=theaters[i]['id'])
#         e.grid(row=i + 1, column=0, sticky='nsew')
#         cols.append(e)
#         for j in range(1, 3):
#             e = Entry(relief='ridge')
#             e.grid(row=i + 1, column=j, sticky='nsew')
#             e.insert('end', list(theaters[i].values())[j])
#             cols.append(e)
#
#         e_b = Button(text=f'Edit', bg='yellow', command=lambda c=i, id=theaters[i]['id']: on_edit(id, c))
#         e_b.grid(row=i + 1, column=4, sticky='nsew')
#         cols.append(e_b)
#         d_b = Button(relief='ridge', text='Delete', bg='red', command=lambda id=theaters[i]['id']: on_delete(id))
#         d_b.grid(row=i + 1, column=5, sticky='nsew')
#         cols.append(d_b)
#         rows.append(cols)
#
#     Label(text="Name theater", bg='blue', fg="white").grid(row=len(theaters) + 1, column=0, pady=20)
#     theater_name = Entry(tk, text="name")
#     theater_name.grid(row=len(theaters) + 1, column=1, padx=10)
#     Label(text="Img_path of theater", bg='blue', fg="white").grid(row=len(theaters) + 2, column=0)
#     img_path = Entry(tk, text="img_path")
#     img_path.grid(row=len(theaters) + 2, column=1, padx=10)
#     create_btn = Button(tk, text="Create", bg="green", fg="white", height=2, width=15,
#                         command=lambda: [manager_theater.post_items(
#                             MovieTheater(check_entries_value(theater_name.get()), check_entries_value(img_path.get()))),
#                             all_theater_view()])
#     create_btn.grid(row=len(theaters) + 3, column=2, padx=20, pady=0)
#     back_btn = Button(tk, text="Back", bg="green", fg="white", height=2, width=15,
#                       command=lambda: admin_control_options())
#     back_btn.grid(row=len(theaters) + 3, column=11, padx=20, pady=20)
#
#     def on_edit(id, i):
#         result = {'name': rows[int(i) + 1][1].get(), 'img_path': rows[int(i) + 1][2].get()}
#         manager_theater.edit_item(id, result)
#         theater_crud_operation()
#
#     def on_delete(id):
#         manager_theater.delete_item(id)
#         theater_crud_operation()


# def movie_crud_operation():
#     clean_screen()
#     movies = manager_movie.get_all_items()
#     rows = []
#     titles = []
#     counter = 0
#     for i in movies[0].keys():
#         e = Label(relief='ridge', text=i)
#         e.grid(row=0, column=counter, sticky='nsew')
#         counter += 1
#         titles.append(e)
#     counter += 1
#     e_a = Label(relief='ridge', text='action')
#     e_a.grid(row=0, column=counter, sticky='nsew')
#     titles.append(e_a)
#     counter += 1
#     d_a = Label(relief='ridge', text='action')
#     d_a.grid(row=0, column=counter, sticky='nsew')
#     titles.append(d_a)
#     rows.append(titles)
#     for i in range(len(movies)):
#         cols = []
#         e = Label(relief='ridge', text=movies[i]['id'])
#         e.grid(row=i + 1, column=0, sticky='nsew')
#         cols.append(e)
#         for j in range(1, len(movies[0].keys())):
#             e = Entry(relief='ridge')
#             e.grid(row=i + 1, column=j, sticky='nsew')
#             e.insert('end', list(movies[i].values())[j])
#             cols.append(e)
#
#         e_b = Button(text=f'Edit', bg='yellow', command=lambda c=i, id=movies[i]['id']: on_edit(id, c))
#         e_b.grid(row=i + 1, column=len(movies[0].keys()) + 1, sticky='nsew')
#         cols.append(e_b)
#         d_b = Button(relief='ridge', text='Delete', bg='red', command=lambda id=movies[i]['id']: on_delete(id))
#         d_b.grid(row=i + 1, column=len(movies[0].keys()) + 2, sticky='nsew')
#         cols.append(d_b)
#         rows.append(cols)
#
#     Label(text="Title movie", bg='blue', fg="white").grid(row=len(movies) + 1, column=0, pady=20)
#     movie_name = Entry(tk, text="title")
#     movie_name.grid(row=len(movies) + 1, column=1, padx=10)
#     Label(text="Img_path movie", bg='blue', fg="white").grid(row=len(movies) + 2, column=0)
#     img_path = Entry(tk, text="img_path")
#     img_path.grid(row=len(movies) + 2, column=1, padx=10)
#     Label(text="Description movie", bg='blue', fg="white").grid(row=len(movies) + 3, column=0)
#     description = Entry(tk, text="description")
#     description.grid(row=len(movies) + 3, column=1, padx=10)
#     Label(text="Price movie", bg='blue', fg="white").grid(row=len(movies) + 4, column=0)
#     price = Entry(tk, text="price")
#     price.grid(row=len(movies) + 4, column=1, padx=10)
#
#     create_btn = Button(tk, text="Create", bg="green", fg="white", height=2, width=15,
#                         command=lambda: [manager_movie.post_items(
#                             Movie(check_entries_value(movie_name.get()), check_entries_value(img_path.get()),
#                                   check_entries_value(description.get()), check_entries_value(price.get()),
#                                   )),
#                             all_theater_view()])
#     create_btn.grid(row=len(movies) + 3, column=2, padx=20, pady=0)
#     back_btn = Button(tk, text="Back", bg="green", fg="white", height=2, width=15,
#                       command=lambda: admin_control_options())
#     back_btn.grid(row=len(movies) + 3, column=11, padx=20, pady=20)
#
#     def on_edit(id, i):
#         result = {'title': rows[int(i) + 1][1].get(),
#                   'img_path': rows[int(i) + 1][2].get(),
#                   'description': rows[int(i) + 1][3].get(),
#                   'price': rows[int(i) + 1][4].get(),
#                   'tickets': rows[int(i) + 1][5].get(),
#                   }
#         manager_movie.edit_item(id, result)
#         movie_crud_operation()
#
#     def on_delete(id):
#         manager_movie.delete_item(id)
#         movie_crud_operation()


def crud_operation_view(manager, class_name):
    clean_screen()
    items = manager.get_all_items()
    rows = []
    titles = []
    counter = 0
    list_labels = list(items[0].keys())
    for label in list_labels:
        e = Label(relief='ridge', text=label)
        e.grid(row=0, column=counter, sticky='nsew')
        counter += 1
        titles.append(e)
    counter += 1
    e_a = Label(relief='ridge', text='action')
    e_a.grid(row=0, column=counter, sticky='nsew')
    titles.append(e_a)
    counter += 1
    d_a = Label(relief='ridge', text='action')
    d_a.grid(row=0, column=counter, sticky='nsew')
    titles.append(d_a)
    rows.append(titles)
    for i in range(len(items)):
        cols = []
        e = Label(relief='ridge', text=items[i]['id'])
        e.grid(row=i + 1, column=0, sticky='nsew')
        cols.append(e)
        for j in range(1, len(list_labels)):
            e = Entry(relief='ridge')
            e.grid(row=i + 1, column=j, sticky='nsew')
            e.insert('end', list(items[i].values())[j])
            cols.append(e)

        e_b = Button(text=f'Edit', bg='yellow', command=lambda c=i, id=items[i]['id']: on_edit(id, c))
        e_b.grid(row=i + 1, column=len(items[0].keys()) + 1, sticky='nsew')
        cols.append(e_b)
        d_b = Button(relief='ridge', text='Delete', bg='red', command=lambda id=items[i]['id']: on_delete(id))
        d_b.grid(row=i + 1, column=len(items[0].keys()) + 2, sticky='nsew')
        cols.append(d_b)
        rows.append(cols)

    rows_create = []

    for index in range(classes_dict[class_name][1]):
        label = list_labels[index + 1]
        Label(text=f"{label}", bg='blue', fg="white").grid(row=len(items) + 1 + index, column=0, pady=20)
        c = Entry(tk, text=f"{label}")
        c.grid(row=len(items) + 1 + index, column=1, padx=10)
        rows_create.append(c)

    def on_press():
        result = []
        for el in rows_create:
            result.append(check_entries_value(el.get()))
        return result

    create_btn = Button(tk, text="Create", bg="green", fg="white", height=2, width=15,
                        command=lambda: [manager.post_items(
                            classes_dict[class_name][0](*on_press())),
                            admin_control_options()])
    create_btn.grid(row=len(items) + 3, column=2, padx=20, pady=0)
    back_btn = Button(tk, text="Back", bg="green", fg="white", height=2, width=15,
                      command=lambda: admin_control_options())
    back_btn.grid(row=len(items) + 3, column=11, padx=20, pady=20)

    def on_edit(id, i):
        result = {}
        for index, label in enumerate(list_labels[1:]):
            result[label] = rows[int(i) + 1][index + 1].get()

        manager.edit_item(id, result)
        crud_operation_view(manager, class_name)

    def on_delete(id):
        manager.delete_item(id)
        crud_operation_view(manager, class_name)


def navPanel(frame, view):
    back_btn = Button(frame, text="Back", bg="green", fg="white", height=2, width=15,
                      command=lambda: view())
    back_btn.pack()


def greeting(frame):
    pass


def reserve_seats(movie, hall):
    clean_screen()
    frame1 = Frame(tk, height=50, width=150)
    frame1.grid(row=0, column=0, pady=(20, 20))
    navPanel(frame1, lambda: theater_all_options(hall['theater_id']))
    frame2 = Frame(tk, height=700, width=700)
    frame2.grid(row=1, column=1, pady=(20, 20), padx=(70, 20))
    counter = 0
    row = 0
    seats = sorted(hall["seats"], key=lambda a: a['name'], reverse=True)
    for s in seats:
        if counter % 10 == 0:
            frame = Frame(frame2)
            frame.grid(row=row, column=0)
            row += 1
        if s["is_reserve"] == True:

            color = 'red'
        else:
            color = 'blue'

        button = Button(frame, text=f'{s["name"]}', bg=color, font=(25), fg="white", height=2, width=7,
                        command=lambda a=f'{s["name"]}': print(a))
        button.pack(side='right')

        button.bind('<Button-1>', lambda e, b=button: b.configure(bg='red'))
        counter += 1

        # print(hall)
