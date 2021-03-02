"""Default namespace module."""

from flask_restx import Namespace, Resource

from recommendations_microservice.exceptions import RecommendationsUnavailable
from recommendations_microservice.recsys import (
    latest_publications,
    most_popular,
    reviews_cf,
    similar_publications,
    stars_cf,
)

from .models import recommendation_model, user_recommendations_model
from .parsers import (
    base_recommendation_parser,
    similarity_parser,
    user_recommendation_parser,
)

ns = Namespace("Recommendations", description="BookBNB recommendations")

ns.models[recommendation_model.name] = recommendation_model
ns.models[user_recommendations_model.name] = user_recommendations_model


@ns.route('/publications')
class PublicationsRecommendationResource(Resource):
    @ns.doc('get_publication_recommendations')
    @ns.expect(similarity_parser)
    @ns.marshal_with(user_recommendations_model)
    @ns.response(204, "No recommendations available")
    def get(self):
        """Get recommendations based on publications similarity."""
        args = similarity_parser.parse_args()
        try:
            recommendations = similar_publications(args.publication_id, args.max)
        except RecommendationsUnavailable:
            return {"No data was found for requested user"}, 204
        return {"recommendations": recommendations}


@ns.route('/popular')
class PopularRecommendationResource(Resource):
    @ns.doc('get_popular_recommendations')
    @ns.expect(base_recommendation_parser)
    @ns.marshal_with(user_recommendations_model)
    @ns.response(204, "No recommendations available")
    def get(self):
        """Get most popular publications recommended."""
        args = base_recommendation_parser.parse_args()
        try:
            recommendations = most_popular(args.max)
        except RecommendationsUnavailable:
            return {"No data was found for requested user"}, 204
        return {"recommendations": recommendations}


@ns.route('/latest')
class LatestRecommendationResource(Resource):
    @ns.doc('get_latest_recommendations')
    @ns.expect(base_recommendation_parser)
    @ns.marshal_with(user_recommendations_model)
    @ns.response(204, "No recommendations available")
    def get(self):
        """Get latest publications recommended."""
        args = base_recommendation_parser.parse_args()
        try:
            recommendations = latest_publications(args.max)
        except RecommendationsUnavailable:
            return {"No data was found for requested user"}, 204
        return {"recommendations": recommendations}


@ns.route('/reviews')
class CFRecommendationResource(Resource):
    @ns.doc('get_reviews_recommendations')
    @ns.expect(user_recommendation_parser)
    @ns.marshal_with(user_recommendations_model)
    @ns.response(204, "No recommendations available")
    def get(self):
        """Get CF recommendations based on reviews scores."""
        args = user_recommendation_parser.parse_args()
        try:
            recommendations = reviews_cf(args.user_id, args.max)
        except RecommendationsUnavailable:
            return {"No data was found for requested user"}, 204

        return {"recommendations": recommendations}


@ns.route('/stars')
class StarsCFRecommendationResource(Resource):
    @ns.doc('get_stars_recommendations')
    @ns.expect(user_recommendation_parser)
    @ns.marshal_with(user_recommendations_model)
    @ns.response(204, "No recommendations available")
    def get(self):
        """Get CF recommendations based on starred publications."""
        args = user_recommendation_parser.parse_args()
        try:
            recommendations = stars_cf(args.user_id, args.max)
        except RecommendationsUnavailable:
            return {"No data was found for requested user"}, 204

        return {"recommendations": recommendations}
