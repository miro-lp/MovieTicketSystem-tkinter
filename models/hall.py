class Hall:
    def __init__(self, name, capacity, theater_id, program_id):
        self.id = ''
        self.name = name
        self.capacity = int(capacity)
        self.theater_id = theater_id
        self.program_id = program_id
        self.seats = self.arrange_seats(capacity)

    @staticmethod
    def arrange_seats(capacity):
        seats = []
        rows = int(capacity) // 10
        for i in range(1, rows+1):
            for j in range(10):
                seats.append({'name': str(i) + chr(65 + j), 'is_reserve': False})
        return seats



