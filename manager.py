import json

from models.hall import Hall
from models.movie import Movie
from models.program import ProgramHour
from models.theater import MovieTheater
from models.users import User


class ManagerDB:
    db_path = 'db/'

    def __init__(self, filename=''):
        self.filename = filename

    def get_all_items(self):
        with open(self.db_path + self.filename, "r") as f:
            lines = f.readlines()
            result = []
            for l in lines:
                item = json.loads(l.strip())
                result.append(item)
        return result

    def get_item_by_id(self, id):
        with open(self.db_path + self.filename, "r") as f:
            lines = f.readlines()
            result = {}
            for l in lines:
                item = json.loads(l.strip())
                if item['id'] == id:
                    result = item
        return result

    def post_items(self, item):
        item = item.__dict__
        item.update({'id': ManagerDB.next_id()})
        with open(self.db_path + self.filename, "a") as f:
            f.write(json.dumps(item))
            f.write("\n")

    def delete_item(self, id):
        with open(self.db_path + self.filename, "r") as f:
            lines = f.readlines()
            result = []
            for l in lines:
                item = json.loads(l.strip())
                if item['id'] != id:
                    result.append(item)
        with open(self.db_path + self.filename, "w") as f:
            for item in result:
                f.write(json.dumps(item))
                f.write("\n")

    def edit_item(self, id, edit_item):
        with open(self.db_path + self.filename, "r") as f:
            lines = f.readlines()
            result = []
            for l in lines:
                item = json.loads(l.strip())
                if item['id'] == id:
                    for k in edit_item:
                        item[k] = edit_item[k]
                result.append(item)
        with open(self.db_path + self.filename, "w") as f:
            for item in result:
                f.write(json.dumps(item))
                f.write("\n")

    @staticmethod
    def next_id():
        with open("db/next_id.txt", "r+") as f:
            next_id = int(f.readlines()[0].strip()) + 1
            # print(next_id)
            f.seek(0)
            f.write(str(next_id))
            return str(next_id)

    def login(self, username, password):
        with open("db/users.txt", "r") as f:
            lines = f.readlines()
            for l in lines:
                user = json.loads(l.strip())
                if user['username'] == username and user['password'] == password:
                    with open("db/current_user.txt", "w") as f:
                        f.write(str(user))
                    return user
            raise ValueError('Invalid username or password')

    def register(self, user):
        user = user.__dict__
        user.update({'id': ManagerDB.next_id()})
        with open("db/users.txt", "a") as f:
            f.write(json.dumps(user))
            f.write("\n")


# # ManagerDB.next_id()
# # user = User('miro', '123456', 'miro', 'miro', 'admin')
# manager = ManagerDB('theaters.txt')
# # manager.register(user)
# # print(manager.login('miro', '123456'))


# theater = MovieTheater('sofia', '/imgs/background1.jpg')
# #
# manager.post_items(theater)
# #
# # print(manager.get_all_items())
# # # manager.edit_item('1013', {'name': 'Plovdiv'})
# # # print(manager.get_item_by_id('1013'))
# #
# hall = Hall('1', 60, '1010','1001')
# print(hall.__dict__)
# manager_halls = ManagerDB('halls.txt')
# # # manager_movie = ManagerDB('movies.txt')
# manager_halls.post_items(hall)
#
# # #
# # movie = Movie('Dune', '/imgs/background1.jpg', 'Very nice movie', 16)
# # manager_movie.post_items(movie)
# manager_program = ManagerDB('programs.txt')
# hour_program = ProgramHour('12:00', '14:00', '1012', '1020','1010')
#
# manager_program.post_items(hour_program)
