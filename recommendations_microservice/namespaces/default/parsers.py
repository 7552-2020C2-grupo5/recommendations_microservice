"""Default namespace parsers module."""

from flask_restx import reqparse

recommendation_parser = reqparse.RequestParser()
recommendation_parser.add_argument(
    "id", help="The user id to get recommendations for", type=int
)
