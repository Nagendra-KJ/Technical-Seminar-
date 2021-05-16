class criticality_set:
    def __init__(self):
        self.node_list = []
        self.red_time = 0
        self.green_time = 0
        self.total_time = self.red_time + self.green_time
        self.wcrt = 0
    
    def add_node(self, node, color, weight):
        self.node_list.append(node)
        if color == 'green':
            self.green_time = self.green_time + weight
        else:
            self.red_time = self.red_time + weight
        self.total_time = self.green_time + self.red_time
    
    def print_list(self):
        print(self.node_list)

    def print_delays(self):
        print(self.green_time, self.red_time, self.total_time)
    
    def print_wcrt(self):
        print(self.wcrt)