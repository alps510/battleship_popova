import random


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Координаты от 0 до 5!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Повтор выстрела...'

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, orient, l):
        self.bow = bow
        self.orient = orient
        self.l = l
        self.lives = l

    def __repr__(self):
        return f"Ship{self.bow}, {self.orient}, {self.l}"

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orient == 0:
                cur_y += i
            else:
                cur_x += i
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots


class Board:
    def __init__(self, hid=False, size = 6):
        self.size = size
        self.field = [['0'] * size for i in range(size)]
        self.shipes = []
        self.count = 0
        self.busy = []
        self.hid = hid

    def __str__(self):
        res = ' ' \
              '|0|1|2|3|4|5|'
        for i, value in enumerate(self.field):
            res += f"\n{i}|" + "|".join(value) + "|"
            if self.hid:
                res = res.replace('◆', '0')
        return res

    def add_ship(self, ship):
        for d in ship.dots:
            self.field[d.x][d.y] = "◆"

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.shipes:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'

                if ship.lives == 0:
                    self.count += 1
                    print('Корабль уничтожен!')
                    self.contour(ship)
                    return True
                else:
                    print('Корабль ранен!')
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def contour(self, ship):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if not self.hid:
                        self.busy.append(cur)
                    if self.hid:
                        self.field[cur.x][cur.y] = '.'

    def remover(self, t, i, j):
        try:
            t[i].remove(j)
        except IndexError:
            pass
        except ValueError:
            pass

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    @property
    def ship_list(self):
        r = [0, 1]
        while True:
            T = [[i for i in range(6)] for i in range(6)]
            T1 = [Ship(Dot(0, 0), 0, 1) for i in range(7)]
            z = random.choice(r)
            if z == 0:
                x = random.randint(0, len(T) - 1)
                y = random.randint(0, len(T[x]) - 3)
                T1[0] = Ship(Dot(x, y), z, 3)
                for i in range(x - 1, x + 2):
                    if i >= 0:
                        for j in range(y - 1, y + 4):
                            self.remover(T, i, j)
            else:
                x = random.randint(0, len(T) - 3)
                y = random.randint(0, len(T[x]) - 1)
                T1[0] = Ship(Dot(x, y), z, 3)
                for i in range(x - 1, x + 4):
                    if i >= 0:
                        for j in range(y - 1, y + 2):
                            self.remover(T, i, j)
            for k in range(0, 2):
                z = random.choice(r)
                if z == 0:
                    while True:
                        x = random.randint(0, len(T) - 1)
                        if len(T[x]) > 0:
                            y = random.choice(T[x])
                            try:
                                if (T[x][T[x].index(y) + 1] - T[x][T[x].index(y)]) == 1:
                                    T1[k + 1] = Ship(Dot(x, y), z, 2)
                                    break
                            except IndexError as e:
                                pass
                        else:
                            pass
                    for i in range(x - 1, x + 2):
                        if i >= 0:
                            for j in range(y - 1, y + 3):
                                self.remover(T, i, j)
                else:
                    while True:
                        x = random.randint(0, len(T) - 2)
                        if len(T[x]) > 0:
                            y = random.choice(T[x])
                            if y in T[x + 1]:
                                T1[k + 1] = Ship(Dot(x, y), z, 2)
                                break
                        else:
                            pass
                    for i in range(x - 1, x + 3):
                        if i >= 0:
                            for j in range(y - 1, y + 2):
                                self.remover(T, i, j)
            for k in range(4):
                while True:
                    x = random.randint(0, len(T) - 1)
                    if len(T[x]) > 0:
                        y = random.choice(T[x])
                        T1[k + 3] = Ship(Dot(x, y), z, 1)
                        break
                    else:
                        pass
                for i in range(x - 1, x + 2):
                    if i >= 0:
                        for j in range(y - 1, y + 2):
                            self.remover(T, i, j)
                n = 0
                for p in range(0, 6):
                    if len(T[p]) > 0:
                        n += 1
                if n == 0:
                    break
            if k == 3:
                break
            else:
                pass
        self.shipes = T1
        return T1


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                res = self.enemy.shot(target)
                return res
            except BoardException as e:
                print(e)


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите координаты: ').split(' ')
            try:
                x, y = cords
                x, y = int(x), int(y)

            except ValueError:
                print('Некорректный ввод!')
                continue
            else:
                break
        return Dot(x, y)


class AI(Player):
    def ask(self):
        while True:
            d = Dot(random.randint(0, 5), random.randint(0, 5))
            if d in self.enemy.busy:
                continue
            else:
                print(f"Ход компьютера: {d.x}, {d.y}")
                return d


class Game:
    def __init__(self, size=6):
        self.size = size
        self.co = self.random_board()
        self.pl = self.random_board()
        self.co.hid = True
        self.us = User(self.pl, self.co)
        self.ai = AI(self.co, self.pl)

    def random_board(self):
        board = Board()
        T2 = board.ship_list
        for i in range(7):
            board.add_ship(T2[i])
        return board

    def greet(self):
        print('-' * 15,'Морской бой', '-'*15)
        print('Ввод двух координат от 0 до 5, через пробел')
        print('-' * 43)

    def loop(self):
        num = 0
        while True:
            print('Доска пользователя: ')
            print(self.us.board)
            print('-'*14)
            print('Доска компьютера: ')
            print(self.ai.board)

            if num % 2 == 0:
                print('-' * 14)
                print('Ход пользователя: ')
                repeat = self.us.move()
            else:
                print('Ход компьютера: ')
                repeat = self.ai.move()

            if self.us.board.count == 7:
                print('Компьютер выиграл!')
                break
            if self.ai.board.count == 7:
                print('Пользователь выиграл!')
                break
            num += 1
            if repeat:
                num -= 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
