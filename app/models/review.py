from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import validates

from app.extensions import db


class Review(db.Model):
    __tablename__ = "reviews"
    __table_args__ = (
        db.UniqueConstraint("user_id", "game_id", name="uq_reviews_user_game"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = db.relationship("User", back_populates="reviews")
    game = db.relationship("Game", back_populates="reviews")

    @validates("rating")
    def validate_rating(self, _key, rating: int) -> int:
        if type(rating) is not int or not 1 <= rating <= 5:
            raise ValueError("La valoración debe estar entre 1 y 5.")

        return rating

    @validates("text")
    def validate_text(self, _key, text: str) -> str:
        if not isinstance(text, str):
            raise ValueError("La reseña debe ser un string.")

        normalized_text = text.strip()
        if not 10 <= len(normalized_text) <= 1000:
            raise ValueError("La reseña debe tener entre 10 y 1000 caracteres.")

        return normalized_text

    def __repr__(self) -> str:
        return (
            f"<Review id={self.id} user_id={self.user_id} game_id={self.game_id} "
            f"rating={self.rating}>"
        )
