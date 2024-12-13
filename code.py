import os
import numpy as np

def read_transportation_problem():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'transportation_problem.txt')
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    supply_nodes = {}
    demand_nodes = {}
    cost_matrix = []
    
    section = None
    for line in lines:
        line = line.strip()
        if line == "Supply Nodes:":
            section = "supply"
        elif line == "Demand Nodes:":
            section = "demand"
        elif line == "Cost Matrix:":
            section = "cost"
        elif section == "supply" and line:
            node, supply = line.split(': ')
            supply_nodes[node] = int(supply)
        elif section == "demand" and line:
            node, demand = line.split(': ')
            demand_nodes[node] = int(demand)
        elif section == "cost" and line:
            costs = list(map(int, line.split()))
            cost_matrix.append(costs)
    
    return supply_nodes, demand_nodes, cost_matrix

def northwest_corner_rule(supply, demand, cost):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    i, j = 0, 0
    while i < m and j < n:
        allocation[i, j] = min(supply[i], demand[j])
        supply[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]
        if supply[i] == 0:
            i += 1
        else:
            j += 1
    return allocation

def minimum_cost_method(supply, demand, cost):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    supply = supply.copy()
    demand = demand.copy()
    
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        min_cost = np.inf
        min_i, min_j = -1, -1
        for i in range(m):
            for j in range(n):
                if supply[i] > 0 and demand[j] > 0 and cost[i, j] < min_cost:
                    min_cost = cost[i, j]
                    min_i, min_j = i, j
        alloc = min(supply[min_i], demand[min_j])
        allocation[min_i, min_j] = alloc
        supply[min_i] -= alloc
        demand[min_j] -= alloc
    return allocation

def minimum_row_cost_method(supply, demand, cost):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    supply = supply.copy()
    demand = demand.copy()
    
    for i in range(m):
        while supply[i] > 0:
            min_cost = np.inf
            min_j = -1
            for j in range(n):
                if demand[j] > 0 and cost[i, j] < min_cost:
                    min_cost = cost[i, j]
                    min_j = j
            alloc = min(supply[i], demand[min_j])
            allocation[i, min_j] = alloc
            supply[i] -= alloc
            demand[min_j] -= alloc
    return allocation

def vogels_method(supply, demand, cost):
    m, n = len(supply), len(demand)
    allocation = np.zeros((m, n))
    supply = supply.copy()
    demand = demand.copy()
    
    while np.sum(supply) > 0 and np.sum(demand) > 0:
        penalties = []
        for i in range(m):
            if supply[i] > 0:
                valid_costs = [cost[i, j] for j in range(n) if demand[j] > 0]
                if len(valid_costs) > 1:
                    penalties.append((sorted(valid_costs)[1] - sorted(valid_costs)[0], i, 'row'))
                elif valid_costs:
                    penalties.append((valid_costs[0], i, 'row'))
        for j in range(n):
            if demand[j] > 0:
                valid_costs = [cost[i, j] for i in range(m) if supply[i] > 0]
                if len(valid_costs) > 1:
                    penalties.append((sorted(valid_costs)[1] - sorted(valid_costs)[0], j, 'col'))
                elif valid_costs:
                    penalties.append((valid_costs[0], j, 'col'))
        max_penalty = max(penalties, key=lambda x: x[0])
        
        if max_penalty[2] == 'row':
            i = max_penalty[1]
            min_cost = np.inf
            min_j = -1
            for j in range(n):
                if demand[j] > 0 and cost[i, j] < min_cost:
                    min_cost = cost[i, j]
                    min_j = j
            alloc = min(supply[i], demand[min_j])
            allocation[i, min_j] = alloc
            supply[i] -= alloc
            demand[min_j] -= alloc
        else:
            j = max_penalty[1]
            min_cost = np.inf
            min_i = -1
            for i in range(m):
                if supply[i] > 0 and cost[i, j] < min_cost:
                    min_cost = cost[i, j]
                    min_i = i
            alloc = min(supply[min_i], demand[j])
            allocation[min_i, j] = alloc
            supply[min_i] -= alloc
            demand[j] -= alloc
    return allocation

def calculate_total_cost(allocation, cost):
    return np.sum(allocation * cost)


if __name__ == "__main__":
    supply_nodes, demand_nodes, cost_matrix = read_transportation_problem()
    
    supply = list(supply_nodes.values())
    demand = list(demand_nodes.values())
    cost = np.array(cost_matrix)
    
    print("\nNorthwest corner rule:\n")
    nw_allocation = northwest_corner_rule(supply.copy(), demand.copy(), cost)
    print(nw_allocation)
    print("\nTotal Cost:", calculate_total_cost(nw_allocation, cost))
    
    print("\n\nMinimum cost method:\n")
    min_cost_allocation = minimum_cost_method(supply.copy(), demand.copy(), cost)
    print(min_cost_allocation)
    print("\nTotal Cost:", calculate_total_cost(min_cost_allocation, cost))
    
    print("\n\nMinimum row cost method:\n")
    min_row_allocation = minimum_row_cost_method(supply.copy(), demand.copy(), cost)
    print(min_row_allocation)
    print("\nTotal Cost:", calculate_total_cost(min_row_allocation, cost))
    
    print("\n\nVogel's method:\n")
    vogels_allocation = vogels_method(supply.copy(), demand.copy(), cost)
    print(vogels_allocation)
    print("\nTotal Cost:", calculate_total_cost(vogels_allocation, cost))

