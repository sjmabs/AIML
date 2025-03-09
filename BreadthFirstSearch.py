# coded based on pseudocode similar to the book Artificial Intelligence Modern Approach Fourth Edition

def BreadthFirstSearch(graph, start, end):
    frontier = [start] # set initial start node
    reached = {start}  # to store nodes that have been reached
    iteration_count = 1
    while frontier:
        print(f"Frontier at start of iteration {iteration_count}: ", frontier)
        node = frontier.pop(0)
        print("Looking at node: ", node)
        if node == end:
            print(f"Solution found after exploring {len(reached)} nodes")
            return True
        for child in graph[node]:
            if child not in reached: # only add child to frontier if not already been reached
                frontier.append(child)
                reached.add(child)
                print(reached)
                print("Added child node as it has not already been explored: ", child)
            else:
                print("Already reached this child so no need to add again: ", child)
        iteration_count += 1
    return False

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E', 'A'],
    'C': ['F', 'A'],
    'D': ['B'],
    'E': ['B', 'C', 'F'],
    'F': ['C']
}

print(BreadthFirstSearch(graph, 'A', 'F'))  # Expected: True
print(BreadthFirstSearch(graph, 'A', 'G'))  # Expected: False (G is not in the graph)
