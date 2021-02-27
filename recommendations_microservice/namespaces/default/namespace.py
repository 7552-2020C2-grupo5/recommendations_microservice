"""Default namespace module."""

from flask_restx import Namespace, Resource

from .models import recommendation_model
from .parsers import recommendation_parser

ns = Namespace("Recommendations", description="BookBNB recommendations")

ns.models[recommendation_model.name] = recommendation_model


@ns.route('')
class RecommendationResource(Resource):
    @ns.doc('get_recommendations')
    @ns.expect(recommendation_parser)
    @ns.marshal_with(recommendation_model)
    def get(self):
        """Get recommendations."""
        args = recommendation_parser.parse_args()
        return {"User": args.id}
