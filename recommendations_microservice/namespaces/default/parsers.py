"""Default namespace parsers module."""

from flask_restx import reqparse

recommendation_parser = reqparse.RequestParser()
recommendation_parser.add_argument(
    "user_id", help="The user id to get recommendations for", type=int
)
recommendation_parser.add_argument(
    "max", help="Max recommendations to fetch", type=int, default=10
)
