"""Recsys module"""
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine
from surprise import NMF, Dataset, Reader

from recommendations_microservice.cfg import config
from recommendations_microservice.exceptions import RecommendationsUnavailable


def similar_publications(publication_id, max_recommendations):
    publications_url = config.publications.db()
    publications_engine = create_engine(publications_url)
    all_publications = pd.read_sql(
        "select id, rooms, beds, bathrooms, price_per_night from public.publication where blocked = false and blockchain_status = 'CONFIRMED'",
        publications_engine,
    )
    if all_publications.empty or publication_id not in all_publications["id"]:
        raise RecommendationsUnavailable

    all_publications.set_index("id", inplace=True)
    norm_data = MinMaxScaler().fit_transform(all_publications)

    scores, idxs = cKDTree(norm_data).query(
        all_publications.loc[publication_id], k=max_recommendations + 1, p=2
    )
    return sorted(
        [
            {"publication_id": all_publications.index[idx], "score": score}
            for idx, score in zip(idxs, scores)
            if np.isfinite(score)
            and score > 0
            and all_publications.index[idx] != publication_id
        ],
        key=lambda x: x.get("score"),
        reverse=False,
    )


def most_popular(max_recommendations):
    url = config.bookings.db()
    engine = create_engine(url)
    df = pd.read_sql(
        "select id, publication_id, booking_date from public.booking", engine
    )
    if df.empty:
        raise RecommendationsUnavailable

    df['days'] = (datetime.utcnow() - df.booking_date).dt.days
    df['exp'] = 1 / (1 + df.days)
    df['exp_score'] = np.exp(df.exp) / np.e
    return (
        df.groupby("publication_id")
        .agg({"exp_score": "sum"})
        .reset_index()
        .rename(columns={"exp_score": "score"})
        .sort_values("score", ascending=False)
        .head(max_recommendations)
        .to_dict(orient="records")
    )


def latest_publications(max_recommendations):
    url = config.publications.db()
    engine = create_engine(url)
    all_publications = pd.read_sql(
        f"""select id as publication_id, publication_date
    from public.publication
    where blocked = false and blockchain_status = 'CONFIRMED'
    order by publication_date desc
    limit {max_recommendations}""",
        engine,
    )
    all_publications['days'] = (
        datetime.utcnow() - all_publications.publication_date
    ).dt.total_seconds() / 86400
    all_publications["score"] = 1 / all_publications.days
    return all_publications[['publication_id', 'score']].to_dict(orient="records")


def reviews_cf(user_id, max_recommendations):
    reviews_url = config.reviews.db()
    reviews_engine = create_engine(reviews_url)
    all_reviews = pd.read_sql(
        "select publication_id, reviewer_id, score from public.publication_review",
        reviews_engine,
    )
    if user_id not in all_reviews["reviewer_id"]:
        raise RecommendationsUnavailable

    reader = Reader(rating_scale=(1, 4))
    data = Dataset.load_from_df(all_reviews, reader)
    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()
    testset = [x for x in testset if x[0] == user_id]
    algo = NMF()
    algo.fit(trainset)
    retval = [{"publication_id": x.iid, "score": x.est} for x in algo.test(testset)]
    retval = sorted(retval, key=lambda x: x.get("score"), reverse=True)
    return retval[:max_recommendations]


def stars_cf(user_id, max_recommendations):
    publications_url = config.publications.db()
    publications_engine = create_engine(publications_url)
    all_stars = pd.read_sql(
        "select user_id, publication_id, 1 from public.publication_star",
        publications_engine,
    )
    if all_stars.empty or user_id not in all_stars["user_id"]:
        raise RecommendationsUnavailable

    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(all_stars, reader)
    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()
    testset = [x for x in testset if x[0] == 0]
    algo = NMF()
    algo.fit(trainset)
    retval = [{"publication_id": x.iid, "score": x.est} for x in algo.test(testset)]
    retval = sorted(retval, key=lambda x: x.get("score"), reverse=True)
    return retval[:max_recommendations]
