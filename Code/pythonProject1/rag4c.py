import os
import numpy as np
import re
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt


def combine_sentences(sentences, buffer_size=1):
    combined_sentences = [
        ' '.join(sentences[j]['sentence'] for j in range(max(i - buffer_size, 0), min(i + buffer_size + 1, len(sentences))))
        for i in range(len(sentences))
    ]
    for i, combined_sentence in enumerate(combined_sentences):
        sentences[i]['combined_sentence'] = combined_sentence

    return sentences


def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def calculate_cosine_distances(sentences):
    distances = []
    for i in range(len(sentences) - 1):
        embedding_current = sentences[i]['combined_sentence_embedding']
        embedding_next = sentences[i + 1]['combined_sentence_embedding']

        similarity = cosine_similarity(embedding_current, embedding_next)

        distance = 1 - similarity
        distances.append(distance)

        sentences[i]['distance_to_next'] = distance
    return distances, sentences


if __name__ == '__main__':
    folder_path = './supporting_document_c'
    files = os.listdir(folder_path)
    for file_name in files:
        print(file_name)
        file_path = os.path.join(folder_path, file_name)
        text = ""
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text += file.read() + "\n"
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='gbk') as file:
                    text += file.read() + "\n"

    single_sentences_list = re.split(r'[。；？！\n]+', text)  # Split text
    sentences = [{'sentence': x, 'index': i} for i, x in enumerate(single_sentences_list)]
    sentences = combine_sentences(sentences)

    model = SentenceTransformer(model_name_or_path='moka-ai/m3e-base')
    embeddings = model.encode([x['combined_sentence'] for x in sentences])
    for i, sentence in enumerate(sentences):
        sentence['combined_sentence_embedding'] = embeddings[i]
    distances, sentences = calculate_cosine_distances(sentences)

    breakpoint_percentile_threshold = 90
    breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)  # If want more chunks, lower the percentile cutoff
    num_distances_above_theshold = len([x for x in distances if x > breakpoint_distance_threshold])  # The amount of distances above threshold
    indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]

    start_index = 0
    chunks = []
    for index in indices_above_thresh:
        end_index = index
        group = sentences[start_index:end_index + 1]
        combined_text = ' '.join([d['sentence'] for d in group])
        chunks.append(combined_text)
        start_index = index + 1
    if start_index < len(sentences):
        combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
        chunks.append(combined_text)