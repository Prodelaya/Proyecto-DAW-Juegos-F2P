from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import validates

from app.extensions import db


class Game(db.Model):
    __tablename__ = "games"
    __table_args__ = (db.UniqueConstraint("api_id", name="uq_games_api_id"),)

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(500), nullable=True)
    short_description = db.Column(db.Text, nullable=True)
    game_url = db.Column(db.String(500), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(255), nullable=True)
    developer = db.Column(db.String(255), nullable=True)
    release_date = db.Column(db.String(50), nullable=True)
    freetogame_profile_url = db.Column(db.String(500), nullable=True)

    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=True)

    req_os = db.Column(db.String(255), nullable=True)
    req_processor = db.Column(db.String(255), nullable=True)
    req_memory = db.Column(db.String(255), nullable=True)
    req_graphics = db.Column(db.String(255), nullable=True)
    req_storage = db.Column(db.String(255), nullable=True)

    screenshots = db.Column(db.JSON, nullable=False, default=list)
    cached_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    reviews = db.relationship(
        "Review",
        back_populates="game",
        cascade="all, delete-orphan",
    )
    library_entries = db.relationship(
        "UserLibrary",
        back_populates="game",
        cascade="all, delete-orphan",
    )

    @validates("description")
    def validate_description(self, _key, description: str) -> str:
        if not isinstance(description, str) or not description.strip():
            raise ValueError("La descripción del juego es obligatoria.")

        return description.strip()

    @validates("screenshots")
    def validate_screenshots(self, _key, screenshots):
        if screenshots is None:
            return []

        if not isinstance(screenshots, list):
            raise ValueError("Las screenshots deben almacenarse como una lista JSON.")

        return screenshots

    def __repr__(self) -> str:
        return f"<Game id={self.id} api_id={self.api_id} title='{self.title}'>"
