import os
import csv
import random
from shapely.wkt import loads
from magic_cost import magic_cost


list = []


class Area:

    def __init__(self, id, name, points):
        self.id = id
        self.name = name
        self.polygon = polygon_from_string(points)
        self.cost_to_areas = {}

    def serialize(self):
        magic_cost_to_areas = dict((k, round(v + magic_cost() / 2)) for (k, v) in self.cost_to_areas.items())
        return {
            'id': self.id,
            'name': self.name,
            'polygon': self.polygon.to_wkt(),
            'costToAreas': magic_cost_to_areas
        }


def load():
    path = os.path.dirname(os.path.abspath(__file__)) + '/data.csv'
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            a = Area(row[0], row[1], row[2])
            list.append(a)
    init_costs()


def init_costs():
    total = len(list)
    for fromIdx, fromArea in enumerate(list):
        for toIdx in range(0, total):
            if toIdx != fromIdx:
                cost = random.randint(80, 120)
                fromArea.cost_to_areas[list[toIdx].id] = cost
                list[toIdx].cost_to_areas[fromArea.id] = cost


def polygon_from_string(points_string):
    points_string = points_string.replace('(', '').replace(')', '').replace(',', ' ')
    points = points_string.split(';')
    points.append(points[0])
    return loads('POLYGON ((' + ', '.join(points) + '))')