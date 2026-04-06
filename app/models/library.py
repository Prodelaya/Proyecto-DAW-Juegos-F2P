from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import validates

from app.extensions import db


VALID_STATUSES = ("want_to_play", "playing", "played")


class UserLibrary(db.Model):
    __tablename__ = "user_library"
    __table_args__ = (
        db.UniqueConstraint("user_id", "game_id", name="uq_user_library_user_game"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="want_to_play")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="library_entries")
    game = db.relationship("Game", back_populates="library_entries")

    @validates("status")
    def validate_status(self, _key, status: str) -> str:
        if not isinstance(status, str):
            raise ValueError("El estado de biblioteca debe ser un string.")

        normalized_status = status.strip()
        if normalized_status not in VALID_STATUSES:
            raise ValueError(
                "El estado de biblioteca debe ser want_to_play, playing o played."
            )

        return normalized_status

    def __repr__(self) -> str:
        return (
            f"<UserLibrary id={self.id} user_id={self.user_id} "
            f"game_id={self.game_id} status='{self.status}'>"
        )
