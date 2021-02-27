"""Recsys module"""
import pandas as pd
from sqlalchemy import create_engine

from recommendations_microservice.cfg import config


def most_popular(_user_id, max_recommendations):
    url = config.bookings.db()
    print(url)
    engine = create_engine(url)
    df = pd.read_sql("select id, publication_id from public.booking", engine)
    return (
        df.groupby("publication_id")
        .agg("count")
        .astype("float")
        .rename(columns={"id": "score"})
        .sort_values("score", ascending=False)
        .reset_index()
        .head(max_recommendations)
        .to_dict(orient="records")
    )
