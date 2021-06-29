from transformers import pipeline

def compute_relevance_scores(sequence, candidate_labels):
    classifier = pipeline("zero-shot-classification")
    result = classifier(sequence, candidate_labels, multi_class=True)
    return result

if __name__ == "__main__":

    sequence = "TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems"
    candidate_labels = ["machine learning", "public health", "economics", "elections"]

    res = compute_relevance_scores(sequence, candidate_labels)
    print(res)