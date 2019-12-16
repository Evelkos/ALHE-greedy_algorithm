class Publication:
    def __init__(self, publication_id: str, is_monograph: bool, points: float, contribution: float):
        self.id = publication_id
        self.is_monograph = is_monograph
        self.points = points
        self.contribution = contribution

    def get_is_monograph(self):
        return self.is_monograph

    def get_contribution(self):
        return self.contribution

    def get_rate(self):
        return self.points / self.contribution
