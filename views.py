import json
import os

from tkinter import Button, Label, Entry, Frame, Canvas, Text, Scrollbar

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
    Label(text="Username", bg='#1F036A', font=('', 12, ''), fg="white").grid(row=0, column=0, pady=3)
    user_name = Entry(tk, text="username", bg='#D6D8D8')
    user_name.grid(row=0, column=1)
    Label(text="Password", bg='#1F036A', fg="white", font=('', 12, '')).grid(row=1, column=0)
    password = Entry(tk, show="*", bg='#D6D8D8')
    password.grid(row=1, column=1)
    login_btn = Button(tk, text="Login", bg="green", fg="white", font=('', 12, ''), height=2, width=15,
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
    frame.grid(row=0, column=0, pady=(20, 20))
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
        data = {'time': [f'Start - End:\n{item["start"]} -{item["end"]}', '',
                         f'Start - End:\n{item["start"]} -{item["end"]}'],
                'movie_name': [f'Movie name:\n{movie["title"]}', lambda m=movie: details_movie(m, id),
                               'Movies\nDetails'],
                'hall_name': [f'Hall name:\n{hall["name"]}', lambda m=movie, h=hall, p=item: reserve_seats(m, h, p),
                              'Reserve\nTickets'],
                'sold_tickets': [f'Sold tickets:\n{item["tickets"]}', '',
                                 f'Seats left:\n{int(hall["capacity"]) - int(item["tickets"])}']}
        # print(item)
        counter += 1
        for i in data:
            button = Button(frame, text=f'{data[i][0]}', bg='purple', font=(25), fg="white", height=3, width=24,
                            command=data[i][1])
            button.pack(side='left', expand=True)
            button.bind('<Enter>', lambda e, b=button, d=data[i][2]: b.configure(bg="#320E65", text=d))
            button.bind('<Leave>', lambda e, b=button, d=data[i][0]: b.configure(bg="purple", text=d))

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
            e.insert('end', str(list(items[i].values())[j]))
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
        print(result)
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


def reserve_seats(movie, hall, program):
    clean_screen()
    frame1 = Frame(tk, height=50, width=150)
    frame1.grid(row=0, column=0, pady=(20, 20))
    navPanel(frame1, lambda: theater_all_options(hall['theater_id']))
    frame2 = Frame(tk, height=700, width=700)
    frame2.grid(row=1, column=1, pady=(20, 20), padx=(70, 20), columnspan=3)
    counter = 0
    row = 0
    print(hall["seats"])
    seats = sorted(hall["seats"], key=lambda a: a['name'], reverse=True)
    reserved_seats = []

    frame4 = Frame(tk, height=60, width=500)
    frame4.grid(row=0, column=2, pady=(10, 5))

    def ticket_text_change():
        nonlocal reserved_seats
        return f'Tickets: {len(reserved_seats)} x {float(movie["price"]):.1f} lv.= {len(reserved_seats) * float(movie["price"]):.1f} lv.     \n' \
               f'Seats: {", ".join(map(lambda s: s["name"], reserved_seats))}      '

    img1 = Image.open(os.path.join(base_folder, "imgs/ticket.png"))

    bg1 = ImageTk.PhotoImage(img1)
    bg1.resize = ("50x500")

    ticket = Label(frame4, image=bg1, text=ticket_text_change(), font=('Ariel', 16, 'bold'), bg="#B867F0",
                   fg='black', compound='center')
    ticket.image = bg1

    ticket.pack()
    frame5 = Frame(tk, height=50, width=30)
    frame5.grid(row=0, column=1, pady=(10, 5), padx=(50, 1))
    frame6 = Frame(tk, height=60, width=30)
    frame6.grid(row=0, column=3, pady=(10, 5))

    back_btn2 = Button(frame5, text="Cancel", bg="green", fg="white", height=2, width=10,
                       command=lambda: reserve_seats(movie, hall, program))
    back_btn2.pack(anchor='w')

    back_btn3 = Button(frame6, text="Buy", bg="green", fg="white", height=2, width=10,
                       command=lambda: buy_tickets(movie, hall, reserved_seats, program))
    back_btn3.pack(anchor='e')

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
                        command=lambda a=s : [reserved_seats.append(a), ticket.configure(text=ticket_text_change())])
        button.pack(side='right')

        button.bind('<Button-1>', lambda e, b=button: b.configure(bg='red', ))

        counter += 1

    frame3 = Frame(tk, height=100, width=700)
    frame3.grid(row=2, column=1, pady=(20, 5), padx=(70, 20), columnspan=3)
    img = Image.open(os.path.join(base_folder, "imgs/cinema_strip.png"))

    bg = ImageTk.PhotoImage(img)
    bg.resize = ("80x700")
    lable = Label(frame3, image=bg, bg="black", text=f"{movie['title']}", font=('Comic Sans MS', 20, 'bold'),
                  fg='white', compound='center', height=78, width=340)
    lable.image = bg
    lable.pack()


def buy_tickets(movie, hall, reserved_seats, program):
    movie["tickets"] = str(int(movie["tickets"]) + len(reserved_seats))
    manager_movie.edit_item(movie['id'], movie)
    program["tickets"] = str(int(program["tickets"]) + len(reserved_seats))
    manager_program.edit_item(program['id'], program)
    for s in reserved_seats:
        for i in hall['seats']:
            if i['name'] == s['name']:
                i['is_reserve'] = True
    manager_hall.edit_item(hall['id'], hall)
    theater_all_options(program['theater_id'])


def details_movie(movie, id):
    clean_screen()
    frame1 = Frame(tk, height=50, width=150)
    frame1.grid(row=0, column=0, pady=(20, 20), padx=(0, 50))
    navPanel(frame1, lambda: theater_all_options(id))
    frame2 = Frame(tk, height=400, width=600)
    frame2.grid(row=0, column=1, rowspan=3, pady=(20, 20), padx=(20, 50))

    img = Image.open(os.path.join(base_folder, movie['img_path']))

    bg = ImageTk.PhotoImage(img)
    bg.resize = ("500x600")
    lable = Label(frame2, image=bg)

    lable.image = bg
    lable.pack()

    frame3 = Frame(tk, height=140, width=300)
    frame3.grid(row=0, column=2, pady=(20, 20), padx=(20, 20))

    name = Label(frame3, text=movie["title"], fg="white", bg='black', font=('Comic Sans MS', 22, 'bold'),
                 compound='center')
    name.pack()

    frame4 = Frame(tk, height=90, width=300)
    frame4.grid(row=1, column=2, pady=(20, 20), padx=(20, 20))
    price = Label(frame4, text=f'Price: {movie["price"]} lv.', fg="white", bg='black', font=('Comic Sans MS', 18, 'bold'),
                 compound='center')
    price.pack(anchor='e')

    frame5 = Frame(tk, height=90, width=300)
    frame5.grid(row=2, column=2, pady=(20, 20), padx=(20, 20))
    total_income = Label(frame5, text=f'Box office: {float(movie["price"])*int(movie["tickets"])} lv.', fg="white", bg='black',
                  font=('Comic Sans MS', 18, 'bold'),
                  compound='center')
    total_income.pack(anchor='e')

    frame6 = Frame(tk, height=100, width=800)
    frame6.grid(row=3, column=1, columnspan=2, pady=(20, 20), padx=(20, 20))
    # description = Label(frame6, text=f'Description: {movie["description"]}', fg="white", bg='black',
    #               font=('Comic Sans MS', 12, 'bold'),  height=80, width=200,
    #               compound='center')
    # description.pack(anchor='e')

    text = Text(frame6, height=5, width=60)
    # scroll = Scrollbar(frame6)
    # text.configure(yscrollcommand=scroll.set)
    text.pack(side='left')

    # scroll.config(command=text.yview)
    # scroll.pack(side='left', fill=tk.Y)

    text.insert('end', f'Description: {movie["description"]}')

    print(movie)
