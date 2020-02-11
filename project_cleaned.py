import warnings
warnings.filterwarnings("ignore")

import random as random
import math as math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y= y
    def move(self, change):
        return Point2d(self.x + change.x, self.y + change.y)
    def scale(self, mult):
        return Point2d(self.x * mult, self.y * mult)
    def distance(self, point2):
        return math.sqrt((point2.x - self.x) ** 2 + (point2.y - self.y) ** 2)
    x = 0
    y = 0

point_zero = Point2d(0, 0)
target = Point2d(1, 1)
margin_pos = 0.01
margin_speed = 0.01

class Circle:
    def __init__(self, x, y, r):
        self.center = Point2d(x, y)
        self.r = r
    center = point_zero
    r = 0
    def isPointInCircle(self, point):
        return self.center.distance(point) < self.r

class Step:
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
    pos = point_zero
    speed = point_zero

class Attempt:
    def __init__(self, circles, time_delta, forces):
        self.forces = forces
        self.path = calculate_path(forces, time_delta)
        self.error = error(circles, self.path)
    forces = []
    path = []
    error = 0

def calculate_path(forces, time_delta):
    res = [Step(point_zero, point_zero)]
    speed = point_zero
    for force in forces:
        speed_scaled = speed.scale(time_delta)
        last_step = res[len(res) - 1]
        new_step = Step(last_step.pos.move(speed), speed)
        res.append(new_step)
        speed = speed.move(force.scale(time_delta))
    return res

def error(circles, path):
    res = 0
    end_error = 10000000000000000
    arrived_at = len(path)
    for i in range(len(path)):
        step = path[i]
        if(arrived_at == len(path) and step.pos.distance(target) < margin_pos):
            if(abs(step.speed.x) < margin_speed and abs(step.speed.y) < margin_speed):
                arrived_at = i
                break
        pos_dist = step.pos.distance(target)
        speed_len = step.speed.distance(point_zero)
        new_end_error = round(pos_dist * 10000) * 10 + round(speed_len * 10000) * 100
        if(new_end_error < end_error):
            end_error = new_end_error
        if(step.pos.x > 1 or step.pos.y > 1):
            res += 1000000 / len(path)
        if(step.pos.x < 0 or step.pos.y < 0):
            res += 100000000 / len(path)
        for circle in circles:
            if(circle.isPointInCircle(step.pos)):
                res += 10000000 / len(path)
    if(arrived_at == len(path)):
        res += end_error
    else:
        res += (arrived_at + 1) / len(path)
    return res

def random_forces(n, max_force, time_delta):
    random_forces = []
    speed = point_zero
    pos = point_zero
    for i in range(n):
        force_length = random.uniform(0, max_force)
        force_angle = random.uniform(0, math.pi * 2)
        force_x = force_length * math.sin(force_angle)
        force_y = force_length * math.cos(force_angle)
        random_forces.append(Point2d(force_x, force_y))
        speed_scaled = speed.scale(time_delta)
        pos = pos.move(speed_scaled)
        speed = speed.move(random_forces[len(random_forces) - 1].scale(time_delta))
    return random_forces

def random_circles(n, max_radius):
    random_circles = []
    for i in range(n):
        circle_x = random.uniform(0, 1)
        circle_y = random.uniform(0, 1)
        circle_r = random.uniform(0, max_radius)
        random_circles.append(Circle(circle_x, circle_y, circle_r))
    return random_circles

def mutated_forces(forces, max_force, max_deviation, max_angle, time_delta):
    new_forces = []
    angle = 0
    speed = point_zero
    pos = point_zero
    for force in forces:
        speed_scaled = speed.scale(time_delta)
        pos = pos.move(speed_scaled)
        if(pos.distance(target) < margin_pos):
            new_force = speed.scale(-1 / time_delta)
            new_force_length = new_force.distance(point_zero)
            if(new_force_length > max_force):
                new_force.scale(max_force / new_force_length)
            new_forces.append(new_force)
        elif(random.random() > 0.9):
            length = random.uniform(0, max_force)
            angle = random.uniform(0, math.pi * 2)
            new_forces.append(Point2d(length * math.cos(angle), length * math.sin(angle)))
        else:
            new_forces.append(force)
        speed = speed.move(new_forces[len(new_forces) - 1].scale(time_delta))
    return new_forces

def crossover_forces(forces1, forces2):
    new_forces = []
    for i in range(len(forces1)):
        if(random.random() >= 0.5):
            new_forces.append(forces1[i])
        else:
            new_forces.append(forces2[i])
        #new_forces.append(forces1[i].scale(0.5).move(forces2[i].scale(0.5)))
    return new_forces



random.seed()

max_force = 0.1
time_delta = 1
circles = [Circle(0.05, 0.25, 0.05),
           Circle(0.25, 0.25, 0.05),
           Circle(0.35, 0.35, 0.15),
           Circle(0.15, 0.85, 0.05),
           Circle(0.6, 0.2, 0.1),
           Circle(0.5, 0.6, 0.1),
           Circle(0.85, 0.35, 0.05),
           Circle(0.8, 0.8, 0.1)]

max_length = 50

angle_deviation = math.pi / 2
attempts_list = []
population = 300
iterations_num = 300
for iteration in range(iterations_num):
    if((iteration + 1) % (iterations_num / 5) == 0):
        print((iteration + 1) / iterations_num * 100, '%')
    new_attempts_list = []
    angle_deviation = math.pi / 8
    parents = []
    if(iteration > 0):
        probability = []
        for attempt in attempts_list:
            probability.append(1 / attempt.error)
        parents = np.random.choice(attempts_list, population * 2, probability)
    for k in range(population // 10):
        if(iteration == 0):
            forces = random_forces(max_length, max_force, time_delta)
        else:
            forces = mutated_forces(attempts_list[k].forces, max_force, max_force * 0.2, angle_deviation, time_delta)
        new_attempts_list.append(Attempt(circles, time_delta, forces))
    for k in range(population // 10, population):
        if(iteration == 0):
            forces = random_forces(max_length, max_force, time_delta)
        else:
            forces = mutated_forces(crossover_forces(parents[k * 2].forces, parents[k * 2 + 1].forces), max_force, max_force * 0.2, angle_deviation, time_delta)
        new_attempts_list.append(Attempt(circles, time_delta, forces))
    attempts_list = sorted(new_attempts_list, key = lambda attempt: attempt.error)
    if((iteration + 1) % (iterations_num / 5) == 0):
        fig = plt.figure()
        for circle in circles:
            ax = fig.add_subplot(1, 1, 1)
            circ = plt.Circle((circle.center.x, circle.center.y), radius=circle.r, color='#000080')
            ax.add_patch(circ)
        square_df=pd.DataFrame({'x': [0, 1, 1, 0, 0], 'y': [0, 0, 1, 1, 0]})
        plt.plot('x', 'y', data = square_df, color='#000080', linewidth = 2)
        for k in range(1, population // 10):
            x = []
            y = []
            for i in range(len(attempts_list[k].path)):
                x.append(attempts_list[k].path[i].pos.x)
                y.append(attempts_list[k].path[i].pos.y)
            df=pd.DataFrame({'x': x, 'y': y})
            plt.plot('x', 'y', data = df, color='#f08000', linewidth = 1)
        x = []
        y = []
        for i in range(len(attempts_list[0].path)):
            x.append(attempts_list[0].path[i].pos.x)
            y.append(attempts_list[0].path[i].pos.y)
            if(attempts_list[0].path[i].speed.distance(point_zero) < 0.01):
                ax = fig.add_subplot(1, 1, 1)
                circ = plt.Circle((attempts_list[0].path[i].pos.x, attempts_list[0].path[i].pos.y), radius=0.015, color='#f00000')
                ax.add_patch(circ)
            else:
                ax = fig.add_subplot(1, 1, 1)
                circ = plt.Circle((attempts_list[0].path[i].pos.x, attempts_list[0].path[i].pos.y), radius=0.01, color='#f00000')
                ax.add_patch(circ)
        df=pd.DataFrame({'x': x, 'y': y})
        plt.plot('x', 'y', data = df, color='#f00000', linewidth = 2)
        plt.axes().set_aspect('equal', 'datalim')
        plt.show()
