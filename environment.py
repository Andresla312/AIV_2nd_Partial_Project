import pygame
import string

class Environment:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dijkstra's Algorithm Visualizer")
        self.clock = pygame.time.Clock()

        self.nodes = []
        self.node_labels = []  # ['A', 'B', ...]
        self.edges = []  # (start_index, end_index, weight)

        self.node_radius = 20
        self.running = True

        self.phase = "Add Nodes"  # 'Add Nodes', 'Connect Nodes', 'Assign Weights'
        self.font = pygame.font.SysFont(None, 24)

        self.selected_node = None
        self.selected_edge = None
        self.typing_weight = ""


    '''
    Add a new node at the specified position if user hasn't exceeded 26 nodes.
    Nodes are automatically labeled with uppercase letters (A-Z).
    '''
    def add_node(self, pos):
        if len(self.node_labels) < 26:  # Up to 26 nodes (A-Z)
            self.nodes.append(pos)
            self.node_labels.append(string.ascii_uppercase[len(self.nodes) - 1])


    '''
    Add an edge between two nodes if it doesn't already exist.
    Args:
        start: Index of starting node
        end: Index of ending node
    '''
    def add_edge(self, start, end):
        if start != end and not self.edge_exists(start, end):
            self.edges.append((start, end, 1))  # Default temporary weight of 1


    '''
    Check if an edge already exists between two nodes.
        Args:
            u: First node index
            v: Second node index
        Returns:
            True if edge exists, False otherwise
    '''
    def edge_exists(self, u, v):
        return any((a == u and b == v) for a, b, _ in self.edges)


    '''
    Find the node at a given screen position.
        Args:
            pos: (x,y) screen coordinates
        Returns:
            Index of node if found, None otherwise
    '''
    def get_node_at_pos(self, pos):
        for i, node_pos in enumerate(self.nodes):
            if (pos[0] - node_pos[0]) ** 2 + (pos[1] - node_pos[1]) ** 2 <= self.node_radius ** 2:
                return i
        return None
    

    '''
    Find the edge at a given screen position.
        Args:
            pos: (x,y) screen coordinates
        Returns:
            Index of edge if found, None otherwise
    '''
    def get_edge_at_pos(self, pos):
        for i, (a, b, _) in enumerate(self.edges):
            ax, ay = self.nodes[a]
            bx, by = self.nodes[b]
            mid_x = (ax + bx) // 2
            mid_y = (ay + by) // 2
            if (pos[0] - mid_x) ** 2 + (pos[1] - mid_y) ** 2 <= 15**2:
                return i
        return None


    '''
    Update the weight of the selected edge with the typed value.
    '''
    def update_weight(self):
        if self.selected_edge is not None and self.typing_weight:
            try:
                new_weight = int(self.typing_weight)
                a, b, _ = self.edges[self.selected_edge]
                self.edges[self.selected_edge] = (a, b, new_weight)
            except ValueError:
                pass
            self.typing_weight = ""
            self.selected_edge = None


    '''
    Draw all visual elements on the screen.
    This includes nodes, edges, and the current phase of the editor.
    '''
    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw edges
        for i, (a, b, w) in enumerate(self.edges):
            start = self.nodes[a]
            end = self.nodes[b]

            # Calculate direction vector
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            ux, uy = dx / dist, dy / dist  # Uniatry vector

            # Adjust start and end positions to avoid overlap with nodes
            offset = self.node_radius
            start_pos = (start[0] + ux * offset, start[1] + uy * offset)
            end_pos = (end[0] - ux * offset, end[1] - uy * offset)

            # Main line
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)

            # Arrowhead
            arrow_size = 12  # Size of the arrowhead
            left = (end_pos[0] - ux * arrow_size - uy * arrow_size / 2,
                    end_pos[1] - uy * arrow_size + ux * arrow_size / 2)
            right = (end_pos[0] - ux * arrow_size + uy * arrow_size / 2,
                    end_pos[1] - uy * arrow_size - ux * arrow_size / 2)

            pygame.draw.polygon(self.screen, (0, 0, 0), [end_pos, left, right])

            # Weight label
            mid_x = (start[0] + end[0]) // 2
            mid_y = (start[1] + end[1]) // 2
            color = (255, 0, 0) if i == self.selected_edge else (0, 0, 0)
            text = self.font.render(str(w), True, color)
            self.screen.blit(text, (mid_x, mid_y))

        # Draw nodes
        for i, pos in enumerate(self.nodes):
            pygame.draw.circle(self.screen, (0, 0, 255), pos, self.node_radius)
            label = self.font.render(self.node_labels[i], True, (255, 255, 255))
            label_rect = label.get_rect(center=pos)
            self.screen.blit(label, label_rect)

        # Show current phase
        phase_text = self.font.render(f"Phase: {self.phase}", True, (0, 128, 0))
        self.screen.blit(phase_text, (10, 10))

        instructions = {
            "Add Nodes": "1. Click to add nodes.\n2. Press SPACE to continue.",
            "Connect Nodes": "1. Click on two nodes to connect them.\n2. Press SPACE to continue.",
            "Assign Weights": "1. Click on an edge to assign a weight and press ENTER.\n2. Press SPACE to finish.\n3. Continue on console.",
        }

        instruction_lines = instructions.get(self.phase, "").split("\n")
        for i, line in enumerate(instruction_lines):
            rendered_line = self.font.render(line, True, (50, 50, 50))
            self.screen.blit(rendered_line, (10, 40 + i * 25))  # 25px spacing between lines
        pygame.display.flip()


    '''
    Run the main loop of the editor.
    This handles events, updates the display, and manages the current phase.
    ''' 
    def run_editor(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.phase == "Add Nodes":
                            self.phase = "Connect Nodes"
                        elif self.phase == "Connect Nodes":
                            self.phase = "Assign Weights"
                        elif self.phase == "Assign Weights":
                            self.running = False

                    elif self.phase == "Assign Weights":
                        if event.key == pygame.K_RETURN:
                            self.update_weight()
                        elif event.key == pygame.K_BACKSPACE:
                            self.typing_weight = self.typing_weight[:-1]
                        elif event.unicode.isdigit():
                            self.typing_weight += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.phase == "Add Nodes":
                        self.add_node(pos)

                    elif self.phase == "Connect Nodes": # first node selected is the start node
                        node_index = self.get_node_at_pos(pos)
                        if node_index is not None:
                            if self.selected_node is None:
                                self.selected_node = node_index
                            else:
                                self.add_edge(self.selected_node, node_index)
                                self.selected_node = None

                    elif self.phase == "Assign Weights":
                        self.selected_edge = self.get_edge_at_pos(pos)
                        self.typing_weight = ""

            self.draw()


    '''
    Get the current graph data including nodes, edges, and labels.
    Returns:
        nodes: List of node positions
    '''
    def get_graph_data(self):
        return self.nodes, self.edges, self.node_labels
    

    '''
    Highlight the path found by Dijkstra's algorithm.
    '''
    def highlight_path(self, path):
        running = True

        for i in range(len(path) - 1, 0, -1):  # Backwards
            a = self.nodes[path[i]]
            b = self.nodes[path[i - 1]]

            # Direction vector (from a to b)
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            ux, uy = dx / dist, dy / dist
            
            offset = self.node_radius
            start_pos = (a[0] + ux * offset, a[1] + uy * offset)
            end_pos = (b[0] - ux * offset, b[1] - uy * offset)

            # Green line
            pygame.draw.line(self.screen, (0, 255, 0), start_pos, end_pos, 4)

            # Green arrow
            arrow_size = 14
            left = (end_pos[0] - ux * arrow_size - uy * arrow_size / 2,
                    end_pos[1] - uy * arrow_size + ux * arrow_size / 2)
            right = (end_pos[0] - ux * arrow_size + uy * arrow_size / 2,
                    end_pos[1] - uy * arrow_size - ux * arrow_size / 2)
            pygame.draw.polygon(self.screen, (0, 255, 0), [end_pos, left, right])

        pygame.display.flip()
        print("Check out Dijkstra's Algorithm Visualizer.\nClose the window to finish.")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()