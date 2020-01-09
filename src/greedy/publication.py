class Publication:
    def __init__(
        self,
        publication_id: str,
        is_mono: bool,
        points: float,
        contribution: float,
        author=None,
        accepted: bool = False,
    ):
        self.id = publication_id
        self.is_mono = is_mono
        self.points = round(points, 3)
        self.contribution = contribution
        self.author = author
        self.accepted = accepted

    def __str__(self):
        return f"id = {self.id} mono = {self.is_mono} points =  {self.points} contrib = {self.contribution} rate = {self.get_rate()} accepted = {self.accepted}"

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.is_mono == other.is_mono
            and self.points == other.points
            and self.contribution == other.contribution
        )

    def is_accepted(self):
        return self.accepted

    def is_monograph(self):
        return self.is_mono

    def get_author(self):
        return self.author

    def get_contribution(self):
        return self.contribution

    def get_id(self):
        return self.id

    def get_points(self):
        return round(self.points, 3)

    def get_rate(self):
        return self.points / self.contribution

    def set_author(self, author):
        self.author = author

    def set_is_accepted(self, is_accepted: bool):
        self.accepted = is_accepted
