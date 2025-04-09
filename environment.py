import pygame
import string

class Environment:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Graph Editor")
        self.clock = pygame.time.Clock()

        self.nodes = []
        self.node_labels = []  # ['A', 'B', ...]
        self.edges = []  # (start_index, end_index, weight)

        self.node_radius = 20
        self.running = True

        self.phase = "add_nodes"  # 'add_nodes', 'connect_nodes', 'assign_weights'
        self.font = pygame.font.SysFont(None, 24)

        self.selected_node = None
        self.selected_edge = None
        self.typing_weight = ""
    
    def add_node(self, pos):
        if len(self.node_labels) < 26:  # Solo hasta Z
            self.nodes.append(pos)
            self.node_labels.append(string.ascii_uppercase[len(self.nodes) - 1])

    def add_edge(self, start, end):
        if start != end and not self.edge_exists(start, end):
            self.edges.append((start, end, 1))  # Peso temporal por defecto

    def edge_exists(self, u, v):
        return any((a == u and b == v) or (a == v and b == u) for a, b, _ in self.edges)

    def get_node_at_pos(self, pos):
        for i, node_pos in enumerate(self.nodes):
            if (pos[0] - node_pos[0]) ** 2 + (pos[1] - node_pos[1]) ** 2 <= self.node_radius ** 2:
                return i
        return None

    def get_edge_at_pos(self, pos):
        for i, (a, b, _) in enumerate(self.edges):
            ax, ay = self.nodes[a]
            bx, by = self.nodes[b]
            mid_x = (ax + bx) // 2
            mid_y = (ay + by) // 2
            if (pos[0] - mid_x) ** 2 + (pos[1] - mid_y) ** 2 <= 15**2:
                return i
        return None

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

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw edges
        for i, (a, b, w) in enumerate(self.edges):
            pygame.draw.line(self.screen, (0, 0, 0), self.nodes[a], self.nodes[b], 2)
            mid_x = (self.nodes[a][0] + self.nodes[b][0]) // 2
            mid_y = (self.nodes[a][1] + self.nodes[b][1]) // 2
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

        pygame.display.flip()

    def run_editor(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.phase == "add_nodes":
                            self.phase = "connect_nodes"
                        elif self.phase == "connect_nodes":
                            self.phase = "assign_weights"
                        elif self.phase == "assign_weights":
                            self.running = False

                    elif self.phase == "assign_weights":
                        if event.key == pygame.K_RETURN:
                            self.update_weight()
                        elif event.key == pygame.K_BACKSPACE:
                            self.typing_weight = self.typing_weight[:-1]
                        elif event.unicode.isdigit():
                            self.typing_weight += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.phase == "add_nodes":
                        self.add_node(pos)

                    elif self.phase == "connect_nodes":
                        node_index = self.get_node_at_pos(pos)
                        if node_index is not None:
                            if self.selected_node is None:
                                self.selected_node = node_index
                            else:
                                self.add_edge(self.selected_node, node_index)
                                self.selected_node = None

                    elif self.phase == "assign_weights":
                        self.selected_edge = self.get_edge_at_pos(pos)
                        self.typing_weight = ""

            self.draw()

    def get_graph_data(self):
        return self.nodes, self.edges, self.node_labels
    
    def highlight_path(self, path):
        running = True

        # Dibujar el camino en verde
        for i in range(len(path) - 1):
            start = self.nodes[path[i]]
            end = self.nodes[path[i + 1]]
            pygame.draw.line(self.screen, (0, 255, 0), start, end, 5)  # Verde brillante

        pygame.display.flip()

        print("Se muestra el camino más corto en pantalla. Cierra la ventana para terminar.")

        # Mantener la ventana abierta hasta que el usuario la cierre
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()