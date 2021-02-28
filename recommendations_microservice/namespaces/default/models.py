"""Default namespace models module."""

from flask_restx import Model, fields

recommendation_model = Model(
    "Recommendations",
    {
        "publication_id": fields.String(
            description="The id for the recommended publication."
        ),
        "score": fields.Float(description="The score assigned"),
    },
)

user_recommendations_model = Model(
    "User recommendations",
    {
        "recommendations": fields.List(
            fields.Nested(recommendation_model),
            description="Recommendations offered according to method.",
        ),
    },
)
