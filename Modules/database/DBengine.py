from sqlalchemy import create_engine
from enum import Enum
from pathlib import Path
import os



class DBtype(Enum):
    sqlite: 'sqlite'

config = {'db_type': 'sqlite'}


class DBEngine:

    def __init__(self, config: dict):
        self.db_type = config['db_type']
        self.engine = None
        self.session = None
        self.start_engine()

    def start_engine(self):
        engine_type = {
            'sqlite': 'sqlite:////'+self._get_db_path()
        }

        self.engine = create_engine(engine_type[self.db_type], echo=True)

    @staticmethod
    def _get_db_path():
        BASE_DIR = Path(__file__).resolve().parent
        path = os.path.join(BASE_DIR, 'tournament.db')
        return path

tomek = DBEngine(config)
print(tomek.engine)