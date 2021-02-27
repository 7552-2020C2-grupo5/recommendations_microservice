"""Default namespace models module."""

from flask_restx import Model, fields

recommendation_model = Model(
    "Recommendations", {"User": fields.String(description="The user id")}
)
