from sqlalchemy.orm import Session
from sqlalchemy import text
from . import model

def get_texts_by_embedding(db: Session, query_embedding: list[float], chat_id: int) -> list[str]:
    vector_str = f"[{','.join(str(x) for x in query_embedding)}]"

    query = text("""
    SELECT
        se.index,
        se.title,
        se.texto,
        (1 - (se.embeddings <=> (:embedding)::vector)) AS cosine_similarity,
        se.rating,
        (0.5 * (1 - (se.embeddings <=> (:embedding)::vector)) + 0.5 * (se.rating / 5.0)) AS combined_score
    FROM
        vectorial.session_embeddings se
    ORDER BY
        combined_score DESC
    LIMIT 10
    """)

    most_similar_results = db.execute(
        query,
        {
            "embedding": vector_str,
        }
    ).fetchall()

    if not most_similar_results:
        return []

    final_formatted_texts = []
    for res in most_similar_results:
        final_formatted_texts.append(
            f"titulo: {res.title} "
            f"resumen: {res.texto} "
            f"score_total: {res.combined_score:.4f} "
            f"score_similaridad_coseno: {res.cosine_similarity:.4f} "
            f"score_rating: {res.rating:.2f}" 
        )

    return final_formatted_texts