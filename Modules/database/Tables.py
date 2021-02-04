from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

Base = declarative_base()


class ScoreDB(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True)
    points = Column(Integer)
    tiebreakers = Column(Integer)

    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship('PlayerDB', back_populates='score')


class PlayerDB(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nickname = Column(String)
    score = relationship('ScoreDB', uselist=False, back_populates='player')
    opponents_ids = Column(String)
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship('GameDB', back_populates='game_participants')

    def __repr__(self):
        return self.name


class GameDB(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    game_status = Column(String)
    game_participants = relationship('PlayerDB', back_populates='game')

    round_id = Column(Integer, ForeignKey('round.id'))
    round = relationship('RoundDB', back_populates='games_in_round')


class RoundDB(Base):
    __tablename__ = 'round'

    id = Column(Integer, primary_key=True)

    ts_start = Column(DATETIME)
    ts_end = Column(DATETIME, nullable=True)
    round_status = Column(String)
    games_in_round = relationship('GameDB', back_populates='round')


