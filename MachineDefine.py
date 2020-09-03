

class Machine(object):
    def __init__(self, name, run_speed, setupTime):
        self.run_speed = run_speed
        self.setup_time = setupTime
        self.name = name
        self.running = True
        self.queue = []
        self.wait_time = 0


class Printing(Machine):
    def __init__(self, name, run_speed, setupTime, perf, color, rolls, max_roll_size):
        super().__init__(name, run_speed, setupTime)
        self.perf = perf
        self.rolls = rolls
        self.max_roll_size = max_roll_size
        self.color = color
        self.previous_roll = ""
        self.previous_color = ""


class Bindery(Machine):
    def __init__(self, name, run_speed, setupTime, cover_feeder, binderytype, max_rolls, inserts, max_roll_size):
        super().__init__(name, run_speed, setupTime)
        self.cover_feeder = cover_feeder
        self.type = binderytype
        self.rolls = max_rolls
        self.num_pockets = inserts
        self.max_roll_size = max_roll_size
        self.previous_roll = ""


class Inserter(Machine):
    def __init__(self, name, run_speed, setupTime, typeInsert, pockets, match, rolls, flat, max_roll_size):
        super().__init__(name, run_speed, setupTime)
        self.type = typeInsert
        self.num_pockets = pockets
        self.match = match
        self.rolls = rolls
        self.flat = flat
        self.max_roll_size = max_roll_size
        self.previous_foldtype = ""


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = float("inf")
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True


class Graph(object):
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=1):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)

    def add_edge_from(self, edge_list):
        for item in edge_list:
            if len(item) == 2:
                self.add_edge(item[0], item[1])
            elif len(item) == 3:
                self.add_edge(item[0], item[1], item[2])
            else:
                print('Not correct format')

    def get_vertices(self):
        return self.vert_dict.keys()

    def get_distance_dict(self):
        distance = {}
        for item in list(self.get_vertices()):
            distance[item] = self.vert_dict[item].distance
        return distance

    def dijkstra(self, start, target):
        start.set_distance(0)
        distances = self.get_distance_dict()
        while distances:
            current_val = min(distances, key=distances.get)
            current_vertex = self.vert_dict[current_val]
            current_vertex.set_visited()
            for next_node in current_vertex.adjacent:
                if next_node.visited:
                    continue
                #new_dist = current_vertex.get_weight(next_node) + current_vertex.get_distance()
                if type(next_node.id) != str:
                    new_dist = current_vertex.get_weight(next_node) + max(next_node.id.wait_time - current_vertex.get_distance(),0)
                else:
                    new_dist = current_vertex.get_weight(next_node) + current_vertex.get_distance()
                if new_dist < next_node.get_distance():
                    next_node.set_distance(new_dist)
                    next_node.set_previous(current_vertex)
            distances.pop(current_val)
        current_vertex = target
        path = [current_vertex]
        while current_vertex.previous:
            path.append(current_vertex.previous)
            current_vertex = current_vertex.previous
        return path[::-1]

    def length_of_path(self, start, target):
        path = self.dijkstra(start, target)
        distance = 0
        for i in path:
            if type(i.id) != str:
                distance += i.distance
        return distance


def printer_define():
    xp251 = Printing('XP251', 4224000, 30, True, ["Color", "Mono"], 2, 40)
    xp13B = Printing('XP13', 4224000, 30, False, ["Color", "Mono"], 2, 40)
    wp01 = Printing('WP01', 2112000, 30, False, ["Color", "Mono"], 1, 30)
    jm01 = Printing('JM01', 1056000, 30, True, ["Color", "Mono"], 1, 20)
    indigo = Printing('Indigo', 132, 30, True, ["Color"], 0, 0)
    oce = Printing('OCE', 132, 30, True, ["Mono"], 0, 0)
    printers = [xp251, xp13B, wp01, jm01, oce, indigo]
    return printers


def binder_define():
    pf7 = Bindery('PF7', 2000, 20, 0, 'PB', 1, 0, 27)
    ibis2 = Bindery('IBIS2', 1500, 20, 1, 'SS', 1, 2, 18)
    ibis3 = Bindery('IBIS3', 1500, 20, 0, 'SS', 1, 2, 18)
    binders = [pf7, ibis2, ibis3]
    return binders


def inserter_define():
    cmc401 = Inserter('CMC401', 8000, 60, 'Env', 4, 4, 1, False, 18)
    cmc402 = Inserter('CMC402', 8000, 60, 'Env', 4, 3, 2, False, 18)
    cmcevo1 = Inserter('CMCEVO1', 10000, 60, 'Env', 5, 3, 2, False, 18)
    cmcevo2 = Inserter('CMCEVO2', 10000, 60, 'Env', 5, 3, 2, False, 18)
    cmceasy = Inserter('CMCEASY', 8000, 60, 'Env', 7, 3, 1, True, 18)
    cmc250 = Inserter('CMC250', 4000, 60, 'Env', 5, 3, 0, False, 0)
    inserters = [cmc401, cmc402, cmcevo1, cmcevo2, cmceasy, cmc250]
    return inserters


def create_graph():
    printers = printer_define()
    binders = binder_define()
    inserters = inserter_define()
    G = Graph()
    edgelist = []
    for i in printers:
        edgelist.append(("start", i))
        for j in inserters:
            if j.name == 'CMC250' and (i.name != 'OCE' and i.name != 'Indigo'):
                pass
            elif (i.name == 'OCE' or i.name == 'Indigo') and j.name != 'CMC250':
                pass
            else:
                edgelist.append((i, j))
        for k in binders:
            edgelist.append((i, k))
    for i in binders:
        for j in inserters:
            edgelist.append((i, j))
        edgelist.append((i, "shipping"))
    for j in inserters:
        edgelist.append((j,"shipping"))
    G.add_edge_from(edgelist)
    return G


def update_weights(graph, order):
    job_level = order.jobs[0]
    if job_level.productType != "Perfect Bind":
        if order.totalPages > 90000:
            order.rolls = 2
        elif order.totalPages > 4000:
            order.rolls = 1
        else:
            order.rolls = 0
        order.roll_size = int(job_level.paperProfile[:2]) * order.rolls
    for vertex in graph:
        for edge in vertex.adjacent:
            target = edge.id
            if type(target) == str:
                weight = 0
            elif not target.running:
                weight = float("inf")
            elif order.rolls > target.rolls:
                weight = float("inf")
            elif type(target) == Printing:
                if job_level.perf and not target.perf:
                    weight = float("inf")
                elif job_level.colorsetup not in target.color:
                    weight = float("inf")
                elif order.roll_size > target.max_roll_size:
                    weight = float("inf")
                elif order.rolls == 0 and target.rolls != 0:
                    weight = float("inf")
                else:
                    if job_level.colorsetup != target.previous_color:
                        target.setup_time = 60
                    else:
                        target.setup_time = 5
                    weight = (order.totalPages / target.run_speed) * 60 + target.setup_time
            elif type(target) == Bindery:
                if job_level.productType != target.type:
                    weight = float("inf")
                elif int(job_level.paperProfile[:2]) > target.max_roll_size:
                    weight = float("inf")
                else:
                    weight = (order.totalRecords / target.run_speed) * 60 + target.setup_time
            elif type(target) == Inserter:
                if job_level.insertType != target.type:
                    weight = float("inf")
                elif target.name not in order.insertGroup:
                    weight = float("inf")
                elif order.rolls == 0 and target.flat is False:
                    weight = float("inf")
                else:
                    if job_level.foldType == target.previous_foldtype:
                        target.setup_time = 15
                    else:
                        target.setup_time = 30
                    weight = (order.totalRecords / target.run_speed) * 60 + target.setup_time
            else:
                print('fail')
                weight = 0
            vertex.adjacent[edge] = weight
    return graph


def update_queue(path):
    for i in path:
        if type(i.id) != str:
            machine = i.id
            machine.wait_time += i.get_distance()


if __name__ == "__main__":
    pass