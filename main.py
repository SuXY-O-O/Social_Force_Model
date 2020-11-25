from gui import GUI
from people import PeopleList
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ARGs
left_to_right = 20
right_to_left = 31
arg_A = 2000
arg_B = -0.08
delta_time = 0.005

left_to_right = min(left_to_right, 42)
left_to_right = max(left_to_right, 4)
right_to_left = min(right_to_left, 42)
right_to_left = max(right_to_left, 4)


if __name__ == '__main__':
    gui = GUI()
    gui.add_barrier()
    gui.update_gui()

    people_list = PeopleList(left_to_right, right_to_left)
    time = 0
    for p in people_list.list:
        gui.add_oval(p.location[0], p.location[1], p.radius, p.id, p.type)
    gui.update_gui()

    tmp_time = 0
    array_t_n_v = [(0, 0, 0)]
    while people_list.list:
        people_list.calculate(arg_A, arg_B)
        i = 0
        while i < len(people_list.list):
            gui.del_oval(people_list.list[i].id)
            i = i + 1
        people_list.move(delta_time)
        for p in people_list.list:
            gui.add_oval(p.location[0], p.location[1], p.radius, p.id, p.type)
        time = time + delta_time
        if time - tmp_time > 0.25:
            tmp_time += 0.25
            n, v = people_list.count_size_and_v()
            array_t_n_v.append((tmp_time, n, v))
        gui.update_time(str(round(time, 3)))
        gui.update_gui()

    gui.start()
    print(array_t_n_v)

    fig = plt.figure(1)
    ax = Axes3D(fig)
    for t_n_v in array_t_n_v:
        if t_n_v[1] >= 3:
            ax.scatter(t_n_v[0], t_n_v[1], t_n_v[2], c='r')
    ax.set_zlabel('Average speed')  # 坐标轴
    ax.set_ylabel('Number of people')
    ax.set_xlabel('Time')
    plt.show()


