def create_graph(n, edges):
   
    graph = [[] for _ in range(n)]  # Initialize an empty adjacency list

    for u, v in edges:
        graph[u].append(v)  # Add edge u -> v
        graph[v].append(u)  # Add edge v -> u (since it's undirected)

    return graph

def main():
        n_vertices = int(input())
        n_edges = int(input())
        cost = int(input())

        edge_list = []
        for _ in range(n_edges):
            u, v = map(int, input().split())
            edge_list.append((u, v))
        graph = create_graph(n_vertices, edge_list)

        count = 0
        
        for i, neighbors in enumerate(graph):
            if len(neighbors) > 1:
                 count += 1

        
        return cost * count



print(main())
        


