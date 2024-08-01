
# core/retrieval.py
def create_retriever(db, search_type="similarity", **kwargs):
    if search_type == "similarity_search_with_score":
        return db.as_retriever(
            search_type="similarity_search_with_score",
            search_kwargs={"score_threshold": 0.1, **kwargs}
        )
    return db.as_retriever(search_type=search_type, search_kwargs=kwargs)
