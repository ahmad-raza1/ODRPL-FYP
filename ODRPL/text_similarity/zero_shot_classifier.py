from transformers import pipeline

global classifier
classifier = pipeline("zero-shot-classification")

def compute_relevance_scores(sequence, candidate_labels):
    print("\n\nComputing relevance...\n\n")
    result = classifier(sequence, candidate_labels, multi_class=True)
    return result

if __name__ == "__main__":

    sequence = "TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems"
    candidate_labels = ["machine learning", "public health", "economics", "elections"]

    res = compute_relevance_scores(sequence, candidate_labels)
    print(res)