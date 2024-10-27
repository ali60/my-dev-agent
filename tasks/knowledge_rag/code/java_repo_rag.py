import argparse
import os
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer, models
import openai
import javalang
from dotenv import load_dotenv

load_dotenv()


# Load environment variables for OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
os_password = os.getenv("OPENSEARCH_PASSWORD")
os_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
os_port = os.getenv("OPENSEARCH_PORT")

# Initialize OpenSearch client
client = OpenSearch(
    hosts=[{"host": os_endpoint, "port": os_port}],
    http_auth=("admin", os_password),
    use_ssl=True,
)


# Specify the pre-trained model name
model_name = "microsoft/codebert-base"

# Initialize the transformer model and tokenizer
word_embedding_model = models.Transformer(model_name)

# Add a pooling layer to generate sentence embeddings
pooling_model = models.Pooling(
    word_embedding_model.get_word_embedding_dimension(),
    pooling_mode_mean_tokens=True,
    pooling_mode_cls_token=False,
    pooling_mode_max_tokens=False,
)

# Create the SentenceTransformer model
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])


def create_index():
    """Create an OpenSearch index with knn_vector mapping and fields for lexical search."""
    index_name = "source-code-index"
    try:
        if client.indices.exists(index=index_name):
            print(f"Index '{index_name}' already exists, skipping index creation.")

        else:
            client.indices.create(
                index=index_name,
                body={
                    "settings": {
                        "index": {"knn": True},
                        "analysis": {
                            "analyzer": {
                                "code_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "pattern",  # Splits on non-word characters
                                    "pattern": r"[^a-zA-Z0-9_]+",
                                    "filter": ["lowercase"],
                                }
                            }
                        },
                    },
                    "mappings": {
                        "properties": {
                            "code_vector": {
                                "type": "knn_vector",
                                "dimension": 768,  # Update according to the embedding dimension
                            },
                            "source_code": {
                                "type": "text",
                                "analyzer": "code_analyzer",
                            },
                            "file_path": {"type": "keyword"},
                            "class_name": {"type": "keyword"},
                            "method_name": {"type": "keyword"},
                            "code_type": {"type": "keyword"},
                        }
                    },
                },
            )
            print(f"Index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error creating index '{index_name}': {e}")


def index_source_code(file_path):
    """Index a Java source code file at function and class level with embeddings in OpenSearch."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        # Split source code into lines for easier extraction
        source_lines = source_code.split("\n")

        # Parse the source code using javalang
        tree = javalang.parse.parse(source_code)

        # Collect class declarations
        classes = []
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            classes.append(node)

        # Index classes and their methods
        for cls in classes:
            class_name = cls.name
            # Get start line of the class
            class_start_line = cls.position.line - 1 if cls.position else 0

            # For class end line, we can take the start line of the next class or end of file
            next_class_start_line = None
            cls_index = classes.index(cls)
            if cls_index + 1 < len(classes):
                next_class = classes[cls_index + 1]
                next_class_start_line = next_class.position.line - 1
            else:
                next_class_start_line = len(source_lines)

            class_code_lines = source_lines[class_start_line:next_class_start_line]
            class_source_code = "\n".join(class_code_lines)

            # Generate embedding for class
            embedding = model.encode(class_source_code).tolist()

            client.index(
                index="source-code-index",
                body={
                    "file_path": file_path,
                    "source_code": class_source_code,
                    "code_type": "class",
                    "class_name": class_name,
                    "method_name": None,
                    "code_vector": embedding,
                },
            )
            print(f"Indexed class '{class_name}' from file: {file_path}")

            # Index methods in the class
            methods = list(cls.methods)
            for idx, method in enumerate(methods):
                method_name = method.name
                method_start_line = method.position.line - 1 if method.position else 0

                # For method end line, we can take the start line of the next method or end of class
                if idx + 1 < len(methods):
                    next_method = methods[idx + 1]
                    method_end_line = next_method.position.line - 1
                else:
                    method_end_line = next_class_start_line

                method_code_lines = source_lines[method_start_line:method_end_line]
                method_source_code = "\n".join(method_code_lines)

                # Generate embedding for method
                embedding = model.encode(method_source_code).tolist()

                client.index(
                    index="source-code-index",
                    body={
                        "file_path": file_path,
                        "source_code": method_source_code,
                        "code_type": "method",
                        "class_name": class_name,
                        "method_name": method_name,
                        "code_vector": embedding,
                    },
                )
                print(
                    f"Indexed method '{method_name}' in class '{class_name}' from file: {file_path}"
                )

    except Exception as e:
        print(f"Error indexing source code from {file_path}: {e}")


def index_directory(directory):
    """Recursively find and index all Java files in a given directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                index_source_code(file_path)


def query_source_code_combined(query, top_k=3):
    """Combine semantic and lexical search to retrieve relevant source code snippets."""
    try:
        query_embedding = model.encode(query).tolist()
        response = client.search(
            index="source-code-index",
            body={
                "size": top_k,
                "query": {
                    "bool": {
                        "should": [
                            {
                                "knn": {
                                    "code_vector": {
                                        "vector": query_embedding,
                                        "k": top_k,
                                    }
                                }
                            },
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "method_name^5",
                                        "class_name^3",
                                        "source_code",
                                    ],
                                    "analyzer": "code_analyzer",
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                },
            },
        )

        hits = response["hits"]["hits"]
        retrieved_snippets = [hit["_source"]["source_code"] for hit in hits]

        print("Retrieved Code Snippets:")
        for hit in hits:
            print(
                f"File: {hit['_source']['file_path']}, Code Type: {hit['_source']['code_type']}, Class: {hit['_source'].get('class_name')}, Method: {hit['_source'].get('method_name')}, Score: {hit['_score']}\nCode:\n{hit['_source']['source_code'][:500]}\n"
            )

        return retrieved_snippets
    except Exception as e:
        print(f"Error retrieving source code: {e}")
        return []


def delete_index():
    """Delete the OpenSearch index."""
    index_name = "source-code-index"
    try:
        if client.indices.exists(index=index_name):
            client.indices.delete(index=index_name)
            print(f"Index '{index_name}' deleted successfully.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"Error deleting index '{index_name}': {e}")


def generate_answer(query, context):
    """Generate an answer using GPT-4 based on retrieved code snippets."""
    try:
        prompt = f"Context:\n{context}\n\nQuestion:\n{query}\nAnswer the question based on the above context."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that answers programming-related questions.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )

        answer = response.choices[0]["message"]["content"].strip()
        print(f"\nGenerated Answer: {answer}")
        return answer

    except Exception as e:
        print(f"Error generating answer: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="RAG System for Java Source Code with OpenSearch and GPT"
    )

    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        help="Mode to run the script: 'index', 'query', 'answer'",
    )
    parser.add_argument(
        "--file_path", type=str, help="File path of the Java source code to index"
    )
    parser.add_argument(
        "--directory", type=str, help="Directory path to index all Java files"
    )
    parser.add_argument(
        "--query", type=str, help="Query text for retrieval and question answering"
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=3,
        help="Number of top-k code snippets to retrieve for the query",
    )

    args = parser.parse_args()

    if args.mode == "delete_index":
        # Delete the index
        delete_index()
    elif args.mode == "index":
        if args.directory:
            # Index all files in the directory
            create_index()
            index_directory(args.directory)
        elif args.file_path:
            # Index a single file
            create_index()
            index_source_code(args.file_path)
        else:
            print("Please provide a file path or directory to index.")

    elif args.mode == "query":
        if args.query:
            # Query the indexed code
            query_source_code_combined(args.query, args.top_k)
        else:
            print("Please provide a query with --query.")

    elif args.mode == "answer":
        if args.query:
            # Query the code and generate an answer
            retrieved_snippets = query_source_code_combined(args.query, args.top_k)
            if retrieved_snippets:
                context = "\n".join(retrieved_snippets)
                generate_answer(args.query, context)
        else:
            print("Please provide a query with --query.")

    else:
        print("Invalid mode. Choose 'index', 'query', or 'answer'.")
