import heapq

type NodeConnections[T] = list[tuple[T, int]]
type AdjacenyList[T] = dict[T, NodeConnections[T]]

class Graph[T]():
    def __init__(self):
        self._adjaceny_list: AdjacenyList[T] = {}
    
    def __repr__(self):
        rep = ""
        for key in self._adjaceny_list:
            rep += f"\nK:{key} neighbors: {self._adjaceny_list[key]}"
        return rep
    
    def addNode(self, key: T):
        if key in self._adjaceny_list:
            print("node already exists")
            return
        
        self._adjaceny_list[key] = [];

    def addConnection(self, a: T, b: T, weight: int):
        if a not in self._adjaceny_list or b not in self._adjaceny_list:
            print("invalid connection either node a or node b does not exist")
            return
        
        self._adjaceny_list[a].append([b, weight])
        self._adjaceny_list[b].append([a, weight])
    
    def getConnections(self, key: T) -> NodeConnections | None:
        if key not in self._adjaceny_list:
            print("failed to retrieve connections invalid node")
            return None
        return self._adjaceny_list[key]
    
    
    # Finds the shortest path from start to goal using A* algorithm.
    # Returns a list of positions representing the path, or None if no path exists.
    def find_path(self, start: T, goal: T) -> list[T] | None:
        # Make sure that the start and goal are both present
        if (start not in self._adjaceny_list or 
            goal not in self._adjaceny_list):
            print(f"invalid start or end positions {start}, {goal}")
            return None
        
        # Heuristic function (Manhattan distance)
        def heuristic(pos):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        # Priority queue for A* algorithm
        # Format: (f_score, position)
        open_set = []
        heapq.heappush(open_set, ((heuristic(start), start)))
        
        # Dictionary to store the g_score (actual distance) to each position
        g_score = {start: 0}
        
        # Dictionary to store the f_score (g_score + heuristic) for each position
        f_score = {start: heuristic(start)}
        
        # Dictionary to store the previous position for each position
        previous = {}
        
        # Set to track positions in the open set
        open_set_hash = {start}

        # Set to track already processed positions
        closed_set = set()
        
        while open_set:
            # Get the position with the lowest f_score
            _, current_position = heapq.heappop(open_set)
            open_set_hash.remove(current_position)
            
            # Add to closed set
            closed_set.add(current_position)
            
            # Check if we've reached the goal
            if current_position == goal:
                # Reconstruct the path
                path = []
                while current_position != start:
                    path.append(current_position)
                    current_position = previous[current_position]
                path.append(start)
                path.reverse()
                return path
            
            # Check if position exists in graph
            if current_position not in self._adjaceny_list:
                continue
                
            # Explore neighbors
            for neighbor, cost in self._adjaceny_list[current_position]:
                # Skip if in closed set
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_score
                tentative_g_score = g_score[current_position] + cost
                
                # Update if we've found a better path
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Update path info
                    previous[neighbor] = current_position
                    g_score[neighbor] = tentative_g_score
                    f_score_value = tentative_g_score + heuristic(neighbor)
                    f_score[neighbor] = f_score_value
                    
                    # Add to open set if not already there
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score_value, neighbor))
                        open_set_hash.add(neighbor)
        
        # No path found
        return None
