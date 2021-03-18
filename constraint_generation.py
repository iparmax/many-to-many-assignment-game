from collections import defaultdict
from itertools import combinations
import networkx as nx 

def get_routes(r,O,D):
    range_routes = list(r)[-1]
    count = 1
    routes = defaultdict(lambda: [])
    for i in range(1,range_routes):
        if r[i] == r[i+1]:
            continue
        routes[count].append(r[i])
        if r[i+1] in routes[count]:
            count +=1
    routes[count].append(r[i+1])
    
    q = 1
    routes_idx = defaultdict(lambda: [])
    for i in routes.keys():
        if (routes[i][0] == O[q]) and (routes[i][-1] == D[q]):
            routes_idx[(i,q)] = routes[i]
        else:
            q+=1
            routes_idx[(i,q)] = routes[i]
    return routes_idx

def feas_paths(links,O,D):
    G = nx.DiGraph()
    for i in links.keys():
        G.add_node(i[0])
        G.add_node(i[1])
        G.add_edge(i[0],i[1])

    r_feas = defaultdict(lambda: [])
    count = 1
    for i,j in zip(O.items(),D.items()): 
        for path in nx.all_simple_paths(G, source=i[1], target=j[1]):
            r_feas[(count,i[0])] = path
            count+=1
    return r_feas

def write_to_file1(namefile,string,flag,dict):
    with open(f'{namefile}.dat', flag) as f:
        f.write(f'{string} : [ ')
        for item in range(1,len(dict.values())+1):
            f.write(str(item))
            f.write(' ')
        f.write(']\n')
        f.close

def write_to_file2(namefile,string,flag,dict):
    with open(f'{namefile}.dat', flag) as f:
        f.write(f'{string} : [ ')
        for item in dict.values():
            f.write(str(item))
            f.write(' ')
        f.write(']\n')
        f.close

def write_to_file3(namefile,string,flag,dict):
    with open(f'{namefile}.dat', flag) as f:
        f.write(f'{string} : [ ')
        for item in dict.items():
            txt = str(item[0])
            x = txt.replace(",", " ")
            f.write(x)
            f.write(' ')
            f.write(str(int(item[1])))
            f.write(' ')
        f.write(']\n')
        f.close

# Gather data from LP
r_star = get_routes(r,O,D)
links = {x:y for x,y in links_network.items() if y!=0}
operators_network = {x:y for x,y in operators_network.items() if y!=0}
operators = {x:y for x,y in operators_network.items() if x[1]==1}
r_feas = feas_paths(links,O,D)

A = defaultdict(lambda: [])
dual_m = {}
for i in links.items():
    for j in operators_network.items():
        if i[1] == j[1]:
            char = chr(j[0][0]+64)
            if char != 'G':
                A[(char,j[0][1])] = list(i[0])
                dual_m[(char,j[0][1])] = dual[(i[0])]
            else:
                A[('blank',j[0][1])] = list(i[0])
                dual_m[('blank',j[0][1])] = dual[(i[0])]

y_opt = {}
for k in A.items():
    y_opt[k[0]] = 0

flow_paths = {}
y_paths = {}
for i in flow.items():
    for j in links.items():
        for k in A.items():
            if set(k[1]) == set(j[0]) and i[1] > 0 and j[1] == i[0][0]:
                flow_paths[(k[0][0],i[0][1])] =  i[1]
                y_paths[(k[0][0],i[0][1])] =  j[1]
                y_opt[k[0]] = 1

gen_cost = {}
op_cost = {}
for j in links.items():
    for k in A.items():
        if set(k[1]) == set(j[0]):
            gen_cost[k[0]] = t[j[1]]
            op_cost[k[0]] = c[j[1]]

operators_best = defaultdict(lambda: [])
for i in r_star.items():
    for j in A.items():
        if (any(j[1] == i[1][k:k+2] for k in range(0,len(i[1]) - 1))) and j[0][0]!= 'blank':
            operators_best[(i[0][1])].append(j[0][0])

operators_feas = defaultdict(lambda: [])
for i in r_feas.items():
    for j in A.items():
        if (any(j[1] == i[1][k:k+2] for k in range(0,len(i[1]) - 1))) and j[0][0]!= 'blank':
            if j[0][0] not in  operators_feas[(i[0][1])]:
                operators_feas[(i[0][1])].append(j[0][0])

route_combs = defaultdict(lambda: [])
for i in operators_best.items():
    combs = []
    count = 0
    for j in range(1,len(i)+2):
        comb = list(combinations(i[1], j))
        for k in comb:
            count+=1
            route_combs[count,i[0]] = k

omega_r = defaultdict(lambda: [])
idx_omega = defaultdict(lambda: [])
for i in r_feas.items():
    omega = 0 
    for j in range(0,len(i[1])-1):
        for k in A.items():
            if k[1] == (i[1][j:j+2]):
                omega += op_cost[k[0]]+dual_m[k[0]]+ gen_cost[k[0]]*(1-y_opt[k[0]])
                idx_omega[i[0]].append(k[0][0])
    omega_r[i[0]] = omega
    
route_operators = defaultdict(lambda: [])
for i in r_feas.items():
    for j in range(0,len(i[1])-1):
        for k in A.items():
            if k[1] == (i[1][j:j+2]):
                route_operators[i[0]].append(k[0][0])

route_operators_optimal = defaultdict(lambda: [])
for i in r_star.items():
    for j in range(0,len(i[1])-1):
        for k in A.items():
            if k[1] == (i[1][j:j+2]):
                route_operators_optimal[i[0]].append(k[0][0])

arg_min = defaultdict(lambda: [])
r_p = defaultdict(lambda: [])
for i in route_combs.items():
    for j in route_operators.items():
        if j[0][1] == i[0][1]:
            if (set(i[1]).intersection(set(j[1]))) != set():
               pass
            else:
                arg_min[i[1],i[0][1]].extend(j[1])
                count = 0 
                for k in route_operators_optimal.values():
                    if set(k).intersection(set(arg_min[i[1],i[0][1]]))!=set():
                        count +=1
                if count == 0:
                    r_p[i[1],i[0][1]] = arg_min[i[1],i[0][1]]

omega_rp = {}
for k in r_p.items():
    minimum = 999999999999999
    for i,j in zip(idx_omega.items(),omega_r.items()):
        if (any(i[1] == k[1][a:a+2] for a in range(0,len(k[1]) - 1))):
            if j[1] < minimum:
                omega_rp[k[0]] = j[1]
                minimum = j[1]
omega_i = {}
for i in O.keys():
    minimum = 999999999999999999
    for j in omega_rp.items():
        if j[0][1] == i:
            if j[1] <= minimum:
                minimum = j[1]
    if minimum !=  999999999999999999:
        omega_i[i] = minimum
    else:
        omega_i[i] = 0

f_star = {}
z_star = {}
y_star = {}
for i in route_operators.items():
    for j in route_operators_optimal.items():
        if i[1] == j[1]:
            for k in i[1]:
                if k != 'blank':
                    f_star[i[0][1],i[0][0],(ord(k.lower())-96)] = ord(k.lower())-96
                    z_star[i[0][1],i[0][0],(ord(k.lower())-96)] = flow_paths[(k,i[0][1])]
                    y_star[i[0][1],i[0][0],(ord(k.lower())-96)] = y_paths[(k,i[0][1])]
                elif k == 'blank':
                    y_star[i[0][1],i[0][0],7] = y_paths[(k,i[0][1])]

# Creating dat file
write_to_file1('stability','users','w',O)
write_to_file1('stability','paths','a',r_feas)
write_to_file1('stability','operators','a',operators)
write_to_file1('stability','links','a',links)
write_to_file2('stability','t','a',t)
write_to_file2('stability','c','a',c)
write_to_file2('stability','utility','a',utility)
write_to_file2('stability','u_stability','a',omega_i)
write_to_file3('stability','f_star','a',f_star)
write_to_file3('stability','z_star','a',z_star)
write_to_file3('stability','y_star','a',y_star)