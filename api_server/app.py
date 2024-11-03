from query_video import main as query_video
from vertex_query import vertex_query


def main(query: str):
    query_result = query_video(query)

    # get top 1 piece
    video_uri = query_result[0]["id"]

    # parse to get the video uri
    video_uri = "_".join(video_uri.split("_")[:2])

    # parse start_time and end_time
    start_time, end_time = query_result[0]["id"].split("_")[-2:]

    # turn video uri to the url
    parts = video_uri.split("/")
    bucket_name = parts[2]
    video_name = parts[-1]

    video_url = f"https://storage.googleapis.com/{bucket_name}/{video_name}"

    result = vertex_query(query, video_uri)

    return result, {
        "start_time": start_time,
        "end_time": end_time,
        "video_uri": video_url,
    }


if __name__ == "__main__":
    query = "What is the first astronaut's says?"
    result = main(query)
    print(result)
