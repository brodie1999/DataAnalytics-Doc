import subprocess
from collections import defaultdict


def generate_dot_file(input_document, readers, also_like_documents, output_path):
    """
    Generate the .dot file for the 'Also Likes' graph.

    :param input_document: The input document's UUID (last 4 hex digits).
    :param readers: Set of reader UUIDs (last 4 hex digits).
    :param also_like_documents: Dictionary mapping readers to the documents they "also like."
    :param output_path: Path to save the .dot file.
    """
    with open(output_path, "w") as f:
        f.write('digraph also_likes {\n')
        f.write(' ranksep=.75; ratio=compress; size = "15,22"; orientation=landscape; rotate=180;\n\n')
        f.write(' node [shape=plaintext, fontsize=16];\n\n')

        # Highlight input document and readers
        f.write(f' "{input_document}" [label="{input_document}", shape="circle", style=filled, color=".3 .9 .7"];\n')
        for reader in readers:
            f.write(f' "{reader}" [label="{reader}", shape="box", style=filled, color=".3 .9 .7"];\n')

        # Add all readers and documents
        for reader in readers:
            f.write(f' "{reader}" [label="{reader}", shape="box"];\n')
        for reader, docs in also_like_documents.items():
            for doc in docs:
                f.write(f' "{doc}" [label="{doc}", shape="circle"];\n')

        # Add connections (arrows for "has-read" relationships)
        for reader, docs in also_like_documents.items():
            for doc in docs:
                f.write(f' "{reader}" -> "{doc}";\n')
        f.write(f' "{list(readers)[0]}" -> "{input_document}";\n')

        f.write('}\n')


def create_graph(dot_file, output_file):
    """
    Run Graphviz to create the graph.

    :param dot_file: Path to the .dot file.
    :param output_file: Path to save the generated graph.
    """
    try:
        subprocess.run(["dot", "-Tps", "-o", output_file, dot_file], check=True)
        print(f"Graph created: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating graph: {e}")
