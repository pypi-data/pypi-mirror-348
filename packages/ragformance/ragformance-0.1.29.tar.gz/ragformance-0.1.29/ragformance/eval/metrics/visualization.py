from sentence_transformers import SentenceTransformer
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def find_in_corpus(corpus, doc_id, field):
    for doc in corpus:
        if doc["_id"] == doc_id:
            return doc[field]
    return None


def visualize_semantic_F1(
    corpus,
    answers,
    output_file="visualization.html",
    write_to_file=False,
    f1_threshold=0.5,
    semantic_threshold=0.5,
):
    quadrants = {
        "Difficult and missed": 0,  # Top-left (orange)
        "Difficult and success": 0,  # Top-right (green)
        "Simple but missed": 0,  # Bottom-left (red)
        "Simple and success": 0,  # Bottom-right (blue)
    }

    qrels = {}
    run = {}
    data = []

    for a in answers:
        query_id = a["query"]["_id"]
        qrels[query_id] = [doc["corpus_id"] for doc in a["query"]["references"]]
        run[query_id] = a["relevant_documents_ids"]

    for idx, query_id in enumerate(qrels):
        relevant_docs = set(qrels[query_id])
        retrieved_docs = set(run.get(query_id, []))

        precision = (
            len(relevant_docs & retrieved_docs) / len(retrieved_docs)
            if retrieved_docs
            else 0
        )
        recall = (
            len(relevant_docs & retrieved_docs) / len(relevant_docs)
            if relevant_docs
            else 0
        )
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall)
            else 0
        )

        # TODO : allow to replace the f1 score  and semantic scores with other metrics

        found = len(relevant_docs & retrieved_docs)
        not_found = len(relevant_docs - retrieved_docs)
        found_but_not_relevant = len(retrieved_docs - relevant_docs)

        query_text = answers[idx]["query"]["text"]
        query_embedding = embedding_model.encode(query_text, show_progress_bar=False)

        document_texts = [
            find_in_corpus(corpus, doc_id, "text") for doc_id in relevant_docs
        ]
        if not document_texts:
            continue  # Skip if no documents found

        doc_embeddings = embedding_model.encode(document_texts, show_progress_bar=False)
        semantic_score = 0
        for doc_embedding in doc_embeddings:
            similarity = (query_embedding @ doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            # clip similarity to [0, 1]
            similarity = max(0, min(1, similarity))
            semantic_score += similarity
        semantic_score /= len(doc_embeddings)

        # Determine quadrant
        is_simple = semantic_score > semantic_threshold
        is_success = f1 > f1_threshold

        if not is_simple and not is_success:
            quadrants["Difficult and missed"] += 1
        elif not is_simple and is_success:
            quadrants["Difficult and success"] += 1
        elif is_simple and not is_success:
            quadrants["Simple but missed"] += 1
        elif is_simple and is_success:
            quadrants["Simple and success"] += 1

        data.append(
            {
                "query": query_id,
                "f1_score": f1,
                "semantic_score": semantic_score,
                "stats": f"{len(relevant_docs)} expected / {found} found <br>{not_found} not found / {found_but_not_relevant} found but not relevant",
                "color": len(retrieved_docs),
            }
        )

    # Plot using Plotly
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[d["f1_score"] for d in data],
            y=[d["semantic_score"] for d in data],
            mode="markers",
            marker=dict(
                size=10,
                color=[d["color"] for d in data],
                colorscale="Viridis",
                showscale=True,
            ),
            text=[
                f"Query ID: {d['query']}<br>F1: {d['f1_score']:.2f}<br>Semantic Similarity Score: {d['semantic_score']:.2f}<br>{d['stats']}"
                for d in data
            ],
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title="Semantic Similarity of queries, number of documents retrieved as color",
        xaxis_title="F1 Score (Right is better)",
        yaxis_title="Semantic Similarity Score <br>(Axis Reversed : Difficult queries are on the top)",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        shapes=[
            dict(
                type="line",
                x0=f1_threshold,
                x1=f1_threshold,
                y0=0,
                y1=1,
                line=dict(dash="dot", color="grey"),
            ),
            dict(
                type="line",
                x0=0,
                x1=1,
                y0=semantic_threshold,
                y1=semantic_threshold,
                line=dict(dash="dot", color="grey"),
            ),
        ],
    )
    fig.update_yaxes(autorange="reversed")

    # Save as self-contained HTML
    if write_to_file:
        plot(
            fig, filename=output_file, auto_open=False, include_plotlyjs="cdn"
        )  # use 'cdn' or 'directory' for smaller files

    fig.show()

    return quadrants


def display_semantic_quadrants(
    quadrants, output_file="semantic_quadrants.html", write_to_file=False
):
    # Order matters here
    labels = [
        ["Difficult and missed", "Difficult and success"],
        ["Simple but missed", "Simple and success"],
    ]

    z = [
        [quadrants["Difficult and missed"], quadrants["Difficult and success"]],
        [quadrants["Simple but missed"], quadrants["Simple and success"]],
    ]

    # Corresponding colors (flat 2D z is used for shape placement)
    custom_colors = {
        "Difficult and missed": "#ffd6a5",  #  orange
        "Difficult and success": "#caffbf",  #  green
        "Simple but missed": "#ffadad",  #  red
        "Simple and success": "#9bf6ff",  #  blue
    }

    # Draw colored rectangles manually with annotations
    shapes = []
    annotations = []
    total = sum([sum(row) for row in z])
    for i in range(2):
        for j in range(2):
            label = labels[i][j]
            count = z[i][j]
            percent = count / total * 100 if total > 0 else 0
            x0, x1 = j, j + 1
            y0, y1 = 1 - i, 2 - i
            shapes.append(
                dict(
                    type="rect",
                    x0=x0,
                    x1=x1,
                    y0=y0,
                    y1=y1,
                    fillcolor=custom_colors[label],
                    line=dict(width=2),
                )
            )
            annotations.append(
                dict(
                    x=(x0 + x1) / 2,
                    y=(y0 + y1) / 2,
                    text=f"<b>{count} ({percent:.1f}%)</b><br>{label}",
                    showarrow=False,
                    font=dict(color="black", size=16),
                )
            )

    fig = go.Figure()
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        xaxis=dict(showgrid=False, zeroline=False, tickvals=[], range=[0, 2]),
        yaxis=dict(showgrid=False, zeroline=False, tickvals=[], range=[0, 2]),
        width=600,
        height=500,
    )

    # Hide axes lines
    fig.update_xaxes(
        showticklabels=True, showline=False, showgrid=False, zeroline=False
    )
    fig.update_yaxes(
        showticklabels=True, showline=False, showgrid=False, zeroline=False
    )
    if write_to_file:
        plot(fig, filename=output_file, auto_open=False, include_plotlyjs="cdn")
    fig.show()
