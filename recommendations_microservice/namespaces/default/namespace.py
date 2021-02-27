"""Default namespace module."""

from flask_restx import Namespace, Resource

from recommendations_microservice.recsys import make_recommendations

from .models import recommendation_model, user_recommendations_model
from .parsers import recommendation_parser

ns = Namespace("Recommendations", description="BookBNB recommendations")

ns.models[recommendation_model.name] = recommendation_model
ns.models[user_recommendations_model.name] = user_recommendations_model


@ns.route('')
class RecommendationResource(Resource):
    @ns.doc('get_recommendations')
    @ns.expect(recommendation_parser)
    @ns.marshal_with(user_recommendations_model)
    def get(self):
        """Get recommendations."""
        args = recommendation_parser.parse_args()
        recommendations = make_recommendations(args.user_id)
        return {"user_id": args.user_id, "recommendations": recommendations}
