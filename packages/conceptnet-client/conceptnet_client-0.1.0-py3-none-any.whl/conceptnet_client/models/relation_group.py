class RelationGroup:
    def __init__(self, relation, edges, parent_group=None):
        self.relation = relation
        self.edges = edges
        self.parent_group = parent_group  # reference to EdgeGroup

    def __len__(self):
        return len(self.edges)

    def __iter__(self):
        return iter(self.edges)

    def __str__(self):
        lines = [f"[{self.relation}] ({len(self.edges)} items)"]
        for edge in self.edges:
            lines.append(str(edge))
        return "\n".join(lines)

    def to_dict(self):
        return {
            "relation": self.relation,
            "edges": [e.to_dict() for e in self.edges]
        }
