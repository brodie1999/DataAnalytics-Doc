import json
from collections import defaultdict, Counter

# (a) Retrieve all visitors of a document
def get_visitors_by_document(json_file_path, subject_doc_id):
    """
    Retrieves the UUIDs of all visitors who read a specified document.

    :param json_file_path: Path to the JSON file containing the event data.
    :param subject_doc_id: UUID of the document whose visitors need to be retrieved.
    :return: A set of visitor UUIDs who read the document.
    """
    visitors = set()
    try:
        with open(json_file_path, 'r') as file:
            for line in file:
                try:
                    event = json.loads(line)
                    if event.get("subject_doc_id") == subject_doc_id and event.get("env_type") == "reader":
                        visitors.add(event.get("visitor_uuid"))
                except json.JSONDecodeError:
                    continue  # Skip any invalid lines that cannot be parsed as JSON
    except FileNotFoundError:
        print(f"Error: File not found - {json_file_path}")
    return visitors

# (b) Retrieve all documents read by a visitor
def get_documents_by_visitor(json_file_path, visitor_uuid):
    """
    Retrieves the UUIDs of all documents read by a specified visitor.

    :param json_file_path: Path to the JSON file containing the event data.
    :param visitor_uuid: UUID of the visitor whose document reading history is to be retrieved.
    :return: A set of document UUIDs that the visitor has read.
    """
    documents = set()
    try:
        with open(json_file_path, 'r') as file:
            for line in file:
                try:
                    event = json.loads(line)
                    if event.get("visitor_uuid") == visitor_uuid and event.get("env_type") == "reader":
                        documents.add(event.get("subject_doc_id"))
                except json.JSONDecodeError:
                    continue  # Skip any invalid lines that cannot be parsed as JSON
    except FileNotFoundError:
        print(f"Error: File not found - {json_file_path}")
    return documents

# (c) Implement "Also Likes" functionality
def also_likes(json_file_path, subject_doc_id, sorting_function):
    """
    Implements the "Also Likes" functionality, which recommends documents that were read by
    the same visitors who read the specified document, sorted by a given sorting function.

    :param json_file_path: Path to the JSON file containing the event data.
    :param subject_doc_id: UUID of the document for which to find similar documents.
    :param sorting_function: A function that sorts the documents based on specific criteria.
    :return: A list of related document UUIDs, sorted by the provided sorting function.
    """
    # Step 1: Retrieve all visitors who read the input document
    visitors = get_visitors_by_document(json_file_path, subject_doc_id)

    # Step 2: Retrieve all documents read by those visitors
    related_documents = Counter()
    for visitor in visitors:
        documents = get_documents_by_visitor(json_file_path, visitor)
        for doc in documents:
            if doc != subject_doc_id:  # Exclude the input document from the results
                related_documents[doc] += 1

    # Step 3: Sort the documents using the provided sorting function
    sorted_documents = sorting_function(related_documents)
    return sorted_documents

# (d) Example Sorting Function: Sort by Number of Readers
def sort_by_readers(document_counts):
    """
    Sorts documents based on the number of readers, from most to least popular.

    :param document_counts: A Counter object containing the number of readers for each document.
    :return: A list of the top 10 most-read documents, sorted by reader count.
    """
    return [doc for doc, _ in document_counts.most_common(10)]