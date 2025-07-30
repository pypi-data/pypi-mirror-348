class Node:
    def __init__(self, data: dict):
        self.id = data.get("@id")
        self.label = data.get("label")
        self.language = data.get("language")
        self.term = data.get("term")
        self.sense_label = data.get("sense_label")

    def to_dict(self):
        return {
            "@id": self.id,
            "label": self.label,
            "language": self.language,
            "term": self.term,
            "sense_label": self.sense_label,
        }
