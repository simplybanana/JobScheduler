import networkx as nx


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
        self.current_roll = ""
        self.current_color = ""


class Bindery(Machine):
    def __init__(self, name, run_speed, setupTime, cover_feeder, binderytype, max_rolls, inserts, max_roll_size):
        super().__init__(name, run_speed, setupTime)
        self.cover_feeder = cover_feeder
        self.type = binderytype
        self.rolls = max_rolls
        self.num_pockets = inserts
        self.max_roll_size = max_roll_size
        self.current_roll = ""


class Inserter(Machine):
    def __init__(self, name, run_speed, setupTime, typeInsert, pockets, match, rolls, flat, max_roll_size):
        super().__init__(name, run_speed, setupTime)
        self.type = typeInsert
        self.num_pockets = pockets
        self.match = match
        self.rolls = rolls
        self.flat = flat
        self.max_roll_size = max_roll_size
        self.current_foldtype = ""


def create_graph():
    xp251 = Printing('XP251', 4224000, 30, True, ["Color", "Mono"], 2, 40)
    xp13B = Printing('XP13', 4224000, 30, False, ["Color", "Mono"], 2, 40)
    wp01 = Printing('WP01', 2112000, 30, False, ["Color", "Mono"], 1, 30)
    jm01 = Printing('JM01', 1056000, 30, True, ["Color", "Mono"], 1, 20)
    indigo = Printing('Indigo', 132, 30, True, ["Color"], 0, 0)
    oce = Printing('OCE', 132, 30, True, ["Mono"], 0, 0)
    pf7 = Bindery('PF7', 2000, 20, 0, 'PB', 1, 0, 27)
    ibis2 = Bindery('IBIS2', 1500, 20, 1, 'SS', 1, 2, 18)
    ibis3 = Bindery('IBIS3', 1500, 20, 0, 'SS', 1, 2, 18)
    cmc401 = Inserter('CMC401', 8000, 60, 'Env', 4, 4, 1, False, 18)
    cmc402 = Inserter('CMC402', 8000, 60, 'Env', 4, 3, 2, False, 18)
    cmcevo1 = Inserter('CMCEVO1', 10000, 60, 'Env', 5, 3, 2, False, 18)
    cmcevo2 = Inserter('CMCEVO2', 10000, 60, 'Env', 5, 3, 2, False, 18)
    cmceasy = Inserter('CMCEASY', 8000, 60, 'Env', 7, 3, 1, True, 18)
    cmc250 = Inserter('CMC250', 4000, 60, 'Env', 5, 3, 0, False, 0)
    printers = [xp251, xp13B, wp01, jm01, oce, indigo]
    binders = [pf7, ibis2, ibis3]
    inserters = [cmc401, cmc402, cmcevo1, cmcevo2, cmceasy, cmc250]
    machineList = printers + binders +inserters
    G = nx.DiGraph()
    G.add_node("start")
    G.add_nodes_from(machineList)
    G.add_node("shipping")
    edgelist = []
    for k in printers:
        edgelist.append(("start",k))
    for i in printers:
        for j in inserters:
            if j.name == 'CMC250' and (i.name != 'OCE' and i.name != 'Indigo'):
                pass
            elif (i.name == 'OCE' or i.name == 'Indigo') and j.name != 'CMC250':
                pass
            else:
                edgelist.append((i, j))
    for i in printers:
        for j in binders:
            edgelist.append((i, j))
    for i in binders:
        for j in inserters:
            edgelist.append((i, j))
    for i in binders:
        edgelist.append((i, "shipping"))
    for j in inserters:
        edgelist.append((j,"shipping"))
    G.add_edges_from(edgelist)
    return G


def update_weights(graph, job):
    for parent, target in graph.edges:
        if type(target) == str:
            graph[parent][target]['weight'] = 0
        elif not target.running:
            graph[parent][target]['weight'] = float("inf")
        elif job.rolls > target.rolls:
            graph[parent][target]['weight'] = float("inf")
        elif type(target) == Printing:
            if job.perf and not target.perf:
                graph[parent][target]['weight'] = float("inf")
            elif job.colorsetup not in target.color:
                graph[parent][target]['weight'] = float("inf")
            elif job.roll_size > target.max_roll_size:
                graph[parent][target]['weight'] = float("inf")
            else:
                if job.colorsetup != target.current_color:
                    target.setup_time = 60
                elif job.rolls != target.current_roll:
                    target.setup_time = 60
                else:
                    target.setup_time = 5
                if job.rolls < target.rolls:
                    graph[parent][target]['weight'] = target.wait_time + (job.totalPages/target.run_speed/2)*60 + target.setup_time
                else:
                    graph[parent][target]['weight'] = target.wait_time + (
                                job.totalPages / target.run_speed) * 60 + target.setup_time
        elif type(target) == Bindery:
            if job.productType != target.type:
                graph[parent][target]['weight'] = float("inf")
            else:
                graph[parent][target]['weight'] = target.wait_time + (job.totalRecords/target.run_speed)*60 + target.setup_time
        elif type(target) == Inserter:
            if job.insertType != target.type:
                graph[parent][target]['weight'] = float("inf")
            elif job.collateral > target.num_pockets or job.matching > target.match:
                graph[parent][target]['weight'] = float("inf")
            else:
                if job.foldType == target.current_foldtype:
                    target.setup_time = 15
                else:
                    target.setup_time = 30
                graph[parent][target]['weight'] = target.wait_time + (job.totalRecords/target.run_speed)*60 + target.setup_time
    return graph


if __name__ == "__main__":
    a = 2
    print(a)
    a /=2
    print(a)