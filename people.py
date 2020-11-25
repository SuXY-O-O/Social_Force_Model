import random
import math


class People:
    def __init__(self, _id, _type, _loc_x, _loc_y):
        self.id = _id  # ID of the people
        self.type = _type  # Direction
        self.dt = 0.02 + random.randint(0, 6) / 100  # t_i of the people
        self.weight = 50 + random.randint(0, 20)  # Weight
        self.radius = (35 + random.randint(0, 5)) / 2  # Size of the people
        self.target_v = (60 + random.randint(0, 60)) / 100  # Target speed
        self.location = (_loc_x, _loc_y)  # Position
        self.v = (0, 0)  # Present speed
        self.a = (0, 0)  # Present acceleration
        self.target_location = (0, 0)  # Target end position
        if _type == 1:
            self.target_location = (1080, random.randint(60, 600))
        else:
            self.target_location = (0, random.randint(60, 600))


class PeopleList:
    def __init__(self, type1_num, type2_num):
        self.list = []
        count = 0
        tmp = type1_num // 3 + 1
        delta = 560 // (tmp - 1)
        for i in range(0, tmp):
            if count < type1_num:
                self.list.append(People("o" + str(count), 1, 140, 60 + i * delta))
                count = count + 1
            if count < type1_num:
                self.list.append(People("o" + str(count), 1, 100, 60 + i * delta))
                count = count + 1
            if count < type1_num:
                self.list.append(People("o" + str(count), 1, 60, 60 + i * delta))
                count = count + 1
        tmp = type2_num // 3 + 1
        delta = 560 // (tmp - 1)
        for i in range(0, tmp):
            if count - type1_num < type2_num:
                self.list.append(People("o" + str(count), 2, 940, 60 + i * delta))
                count = count + 1
            if count - type1_num < type2_num:
                self.list.append(People("o" + str(count), 2, 980, 60 + i * delta))
                count = count + 1
            if count - type1_num < type2_num:
                self.list.append(People("o" + str(count), 2, 1020, 60 + i * delta))
                count = count + 1

    def calculate(self, arg_A, arg_B):
        for people in self.list:
            # Calculate target force
            e = ((people.target_location[0] - people.location[0]) / 100,
                 (people.target_location[1] - people.location[1]) / 100)
            tmp = math.sqrt(math.pow(e[0], 2) + math.pow(e[1], 2))
            e = (e[0] / tmp, e[1] / tmp)
            e = (e[0] * people.target_v, e[1] * people.target_v)
            e = (e[0] - people.v[0], e[1] - people.v[1])
            arg_self = (e[0] * people.weight / people.dt, e[1] * people.weight / people.dt)
            # Calculate people force
            arg_people = (0, 0)
            for p in self.list:
                if p.id == people.id:
                    continue
                d = ((people.location[0] - p.location[0]) / 100, (people.location[1] - p.location[1]) / 100)
                dis = math.sqrt(math.pow(d[0], 2) + math.pow(d[1], 2))
                d = (d[0] / dis, d[1] / dis)
                dis = (dis * 100 - p.radius - people.radius) / 100
                a = arg_A * math.exp(dis / arg_B)
                d = (d[0] * a, d[1] * a)
                arg_people = (arg_people[0] + d[0], arg_people[1] + d[1])
            # Calculate edge force
            arg_edge = (0, 0)
            if people.location[1] < 200:
                a = arg_A * math.exp((people.location[1] - 40) / 100 / arg_B)
                arg_edge = (0, a)
            elif people.location[1] > 480:
                a = arg_A * math.exp((640 - people.location[1]) / 100 / arg_B)
                arg_edge = (0, -a)
            # Calculate new acceleration
            out_x = (arg_self[0] + arg_people[0] + arg_edge[0]) / people.weight
            out_y = (arg_self[1] + arg_people[1] + arg_edge[1]) / people.weight
            people.a = (out_x, out_y)

    def move(self, delta_time):
        for people in self.list:
            new_vx = people.v[0] + people.a[0] * delta_time
            new_vy = people.v[1] + people.a[1] * delta_time
            l_x = (people.v[0] + new_vx) / 2 * delta_time * 100
            l_y = (people.v[1] + new_vy) / 2 * delta_time * 100
            people.location = (people.location[0] + l_x, people.location[1] + l_y)
            people.v = (new_vx, new_vy)
            if people.location[0] > 1040 or people.location[0] < 40:
                self.list.remove(people)

    def count_size_and_v(self):
        total_num = 0
        total_v = 0
        for people in self.list:
            if 200 <= people.location[0] <= 900:
                total_num += 1
                total_v += math.sqrt(people.v[0] ** 2 + people.v[1] ** 2)
        if total_num != 0:
            total_v /= total_num
        return total_num, total_v
