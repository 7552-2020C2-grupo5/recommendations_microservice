"""Default namespace models module."""

from flask_restx import Model, fields

recommendation_model = Model(
    "Recommendations",
    {
        "publication_id": fields.String(
            description="The id for the recommended publication"
        ),
        "score": fields.Float(description="The score assigned"),
    },
)

user_recommendations_model = Model(
    "User recommendations",
    {
        "user_id": fields.Integer(description="The user id"),
        "recommendations": fields.List(
            fields.Nested(recommendation_model),
            description="Recommendations for the user",
        ),
    },
)
