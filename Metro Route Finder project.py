import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------
# Metro Network
# ---------------------------

metro = {
    "Central": {"Park": 2, "Museum": 4},
    "Park": {"Central": 2, "CityHall": 3},
    "Museum": {"Central": 4, "Harbor": 5},
    "CityHall": {"Park": 3, "Harbor": 2},
    "Harbor": {"Museum": 5, "CityHall": 2, "Airport": 6},
    "Airport": {"Harbor": 6}
}

# ---------------------------
# Dijkstra Simulation
# ---------------------------

def dijkstra(graph, start, end):

    pq = [(0, start)]

    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    previous = {node: None for node in graph}

    visited = set()

    print("\n==============================")
    print("DIJKSTRA ALGORITHM SIMULATION")
    print("==============================\n")

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        print(f"\nVisited Station: {current_node}")
        print(f"Current Distance: {current_distance} km")

        time.sleep(1)

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            print(
                f"Checking Route: "
                f"{current_node} → {neighbor}"
                f" = {distance} km"
            )

            time.sleep(0.7)

            if distance < distances[neighbor]:

                distances[neighbor] = distance
                previous[neighbor] = current_node

                heapq.heappush(
                    pq,
                    (distance, neighbor)
                )

                print(
                    f"Updated Distance of "
                    f"{neighbor}: {distance} km"
                )

        print("--------------------------------")

        if current_node == end:
            break

    path = []
    current = end

    while current:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end]

# ---------------------------
# User Input
# ---------------------------

print("\nAvailable Stations:\n")

for station in metro:
    print(station)

source = input("\nEnter Source Station: ")
destination = input("Enter Destination Station: ")

if source not in metro or destination not in metro:
    print("Invalid Station Name!")
    exit()

# ---------------------------
# Find Shortest Path
# ---------------------------

path, distance = dijkstra(
    metro,
    source,
    destination
)

print("\n================================")
print("SHORTEST ROUTE FOUND")
print("================================")

print("Route:")
print(" → ".join(path))

print(f"\nTotal Distance: {distance} km")
print(f"Stations Covered: {len(path)}")

# ---------------------------
# Graph Visualization
# ---------------------------

G = nx.Graph()

for station in metro:
    for neighbor, weight in metro[station].items():
        G.add_edge(
            station,
            neighbor,
            weight=weight
        )

plt.figure(figsize=(10, 7))

pos = nx.spring_layout(
    G,
    seed=42
)

# Draw Nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_color="lightblue",
    node_size=2500
)

# Draw Labels
nx.draw_networkx_labels(
    G,
    pos,
    font_size=10,
    font_weight="bold"
)

# Draw Normal Edges
nx.draw_networkx_edges(
    G,
    pos,
    edge_color="gray",
    width=2
)

# Edge Labels
edge_labels = nx.get_edge_attributes(
    G,
    'weight'
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels
)

# ---------------------------
# Animate Shortest Path
# ---------------------------

path_edges = list(
    zip(path, path[1:])
)

plt.title(
    "Metro Route Finder Simulation",
    fontsize=14
)

plt.pause(1)

for edge in path_edges:

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[edge],
        edge_color="red",
        width=5
    )

    plt.pause(1)

# Highlight Source and Destination

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[source],
    node_color="green",
    node_size=2800
)

nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=[destination],
    node_color="orange",
    node_size=2800
)

plt.title(
    f"Shortest Route:\n{' → '.join(path)}\nDistance = {distance} km",
    fontsize=12
)

plt.axis("off")
plt.show()