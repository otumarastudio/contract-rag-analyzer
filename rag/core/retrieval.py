
# core/retrieval.py
def create_retriever(db, search_type="similarity", **kwargs):
    return db.as_retriever(search_type=search_type, search_kwargs=kwargs)

