# Importar todos los modelos para que SQLAlchemy los descubra al hacer db.create_all()
from .user import User  # noqa: F401
from .game import Game  # noqa: F401
from .review import Review  # noqa: F401
from .library import UserLibrary  # noqa: F401
