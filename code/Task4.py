import json
from collections import defaultdict

def calculate_top_readers(json_file_path):
    """
    Calculate the total reading time for each user and identify the top 10 readers.

    :param json_file_path: Path to the JSON file containing event data.
    :return: List of tuples with top 10 readers and their total reading time.
    """
    reader_times = defaultdict(int)

    try:
        # Read and process the JSON file
        with open(json_file_path, 'r') as file:
            for line in file:
                try:
                    event = json.loads(line)
                    user_id = event.get("visitor_uuid")
                    read_time = event.get("event_readtime", 0)

                    if user_id and isinstance(read_time, (int, float)):
                        reader_times[user_id] += read_time
                except json.JSONDecodeError:
                    # Skip invalid JSON lines
                    continue

        # Sort users by total reading time (descending order) and extract top 10
        top_readers = sorted(reader_times.items(), key=lambda x: x[1], reverse=True)[:10]
        #print("TASK 4 RESULT: ", top_readers) # CLI output
        return top_readers

    except FileNotFoundError:
        print(f"Error: File not found - {json_file_path}")
        return []
    except Exception as e:
        print(f"Error: Unexpected error - {e}")
        return []
