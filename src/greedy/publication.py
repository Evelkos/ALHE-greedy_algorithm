class Publication:
    def __init__(
        self, publication_id: str, is_mono: bool, points: float, contribution: float
    ):
        self.id = publication_id
        self.is_mono = is_mono
        self.points = points
        self.contribution = contribution

    def __str__(self):
        return f"{self.id} {self.is_mono} {self.points} {self.contribution} {self.get_rate()}"

    def is_monograph(self):
        return self.is_mono

    def get_contribution(self):
        return self.contribution

    def get_id(self):
        return self.id

    def get_points(self):
        return self.points

    def get_rate(self):
        return self.points / self.contribution
