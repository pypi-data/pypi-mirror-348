from .node import Node

class Edge:
    def __init__(self, data, parent_group=None):
        self.raw = data
        self.start = Node(data.get("start"))
        self.end = Node(data.get("end"))
        self.relation = self._extract_relation(data.get("rel"))
        self.weight = data.get("weight", 0)
        self.surface_text = data.get("surfaceText")
        self.source = data.get("sources", [])
        self.parent_group = parent_group

    @staticmethod
    def _extract_relation(rel_obj):
        return rel_obj.get("label") if rel_obj else ""

    @staticmethod
    def _extract_source(sources):
        if sources:
            s = sources[0]
            return s.get("contributor", "").split("/")[-1]  # e.g. 'wordnet' or 'wiktionary'
        return ""

    @staticmethod
    def _term_to_label(term):
        if not term:
            return ""
        return term.split("/")[-1].replace("_", " ")

    def __str__(self):
        out = f"{self.start.label} [{self.relation}] {self.end.label} (weight={self.weight})"
        if self.surface_text:
            out += f"\n  ↳ {self.surface_text}"
        return out

    def to_dict(self):
        return {
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "relation": self.relation,
            "weight": self.weight,
            "surface_text": self.surface_text,
            "source": self.source
        }
