from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ScoreBase(ABC):

    def __init__(self, points=0):
        self.points = points

    @abstractmethod
    def points_addition(self, points: int):
        pass

    @abstractmethod
    def points_subtraction(self, points: int):
        pass


class WTCScoreSystem(ScoreBase):

    def __init__(self, points=0, tiebreakers=0):
        super().__init__(points=points)
        self.tiebreakers = tiebreakers

    def __repr__(self):
        return f'Points: {self.points}, tiebreakers: {self.tiebreakers}'

    def comparison_points(self):
        return float(f'{self.points}.{self.tiebreakers}')

    def points_addition(self, points: int):
        self.points = self.points + points

    def points_subtraction(self, points: int):
        self.points = self.points - points

    def points_manual_change(self, points: int):
        self.points = points

    def tiebreakers_addition(self, tiebreakers: int):
        self.tiebreakers = self.tiebreakers + tiebreakers

    def tiebreakers_subtraction(self, tiebreakers: int):
        self.tiebreakers = self.tiebreakers - tiebreakers


if __name__ == '__main__':
    s = WTCScoreSystem(points=5, tiebreakers=50)
    print(s.comp_points)
    s.points_addition(5)
    print(s.points)
    s.tiebreakers_addition(52)
    print(s.comp_points)
