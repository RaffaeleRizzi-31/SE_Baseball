from dataclasses import dataclass

@dataclass
class Team:
    id : int
    year : int
    team_code : str
    name: str

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f"id: {self.id} | year: {self.year} | team_code: {self.team_code} | name: {self.name}"

    def __hash__(self):
        return hash(self.id)
