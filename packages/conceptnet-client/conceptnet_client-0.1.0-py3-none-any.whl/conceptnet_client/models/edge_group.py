from .edge import Edge
from .relation_group import RelationGroup

class EdgeGroup:
    def __init__(self, edge_data_list):
        self.edges = [Edge(data, parent_group=self) for data in edge_data_list]

    def __len__(self):
        return len(self.edges)

    def __iter__(self):
        return iter(self.edges)

    def __getitem__(self, index):
        return self.edges[index]

    def relations(self):
        return list(set(edge.relation for edge in self.edges))

    def group_by_relation(self):
        grouped = {}
        for edge in self.edges:
            grouped.setdefault(edge.relation, []).append(edge)
        return [RelationGroup(relation, edges, parent_group=self) for relation, edges in grouped.items()]

    def filter(self, func):
        return [edge for edge in self.edges if func(edge)]

    def to_dict(self):
        return [edge.to_dict() for edge in self.edges]
