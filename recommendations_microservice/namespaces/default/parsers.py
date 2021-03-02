"""Default namespace parsers module."""

from flask_restx import reqparse

base_recommendation_parser = reqparse.RequestParser()
base_recommendation_parser.add_argument(
    "max", help="Max recommendations to fetch", type=int, default=10
)

user_recommendation_parser = reqparse.RequestParser()
user_recommendation_parser.add_argument(
    "user_id", help="The user id to get recommendations for", type=int
)
user_recommendation_parser.add_argument(
    "max", help="Max recommendations to fetch", type=int, default=10
)

similarity_parser = reqparse.RequestParser()
similarity_parser.add_argument(
    "publication_id", help="The publication_id id to get recommendations for", type=int
)
similarity_parser.add_argument(
    "max", help="Max recommendations to fetch", type=int, default=10
)
