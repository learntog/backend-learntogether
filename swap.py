import networkx as nx
from firebase  import firebase

firebase = firebase.FirebaseApplication('https://learntogether-a250b.firebaseio.com/')
swaps = firebase.get("", "/swaps/unitcode/typeofactivity/")

edgesindex = {}
listofgraphtuple = []

for each in swaps:
    edgekeys = []
    edgekey = ""
    currentedge = swaps[each][0] 
    for i in range(1,len(swaps[each])):
        edgekey = currentedge + swaps[each][i]
        listofgraphtuple.append((currentedge, swaps[each][i]))
        edgekeys.append(edgekey)
        edgekey = ""
    for key in edgekeys:
        edgesindex[key] = each
    #print (edgekeys)

print(edgesindex)
print(listofgraphtuple)

G = nx.DiGraph(listofgraphtuple)
solution = list(nx.simple_cycles(G))

for x in solution:
    x+=[x[0]]
print(solution)

useraction = []
for solutionz in solution:
    actions = []
    for i in range(len(solutionz) - 1):
        actions.append(edgesindex[solutionz[i]+solutionz[i+1]])
    useraction.append(actions)
print(useraction)

"""
OUTPUT:
{'8pm4pm': 'uid', '4pm8pm': 'uid1', '4pm6pm': 'uid2', '6pm8pm': 'uid3', '6pm4pm': 'uid3', '6pm10am': 'uid3'}
[('8pm', '4pm'), ('4pm', '8pm'), ('4pm', '6pm'), ('6pm', '8pm'), ('6pm', '4pm'), ('6pm', '10am')]
[['6pm', '4pm', '6pm'], ['6pm', '8pm', '4pm', '6pm'], ['4pm', '8pm', '4pm']]
[['uid3', 'uid2'], ['uid3', 'uid', 'uid2'], ['uid1', 'uid']]
"""

