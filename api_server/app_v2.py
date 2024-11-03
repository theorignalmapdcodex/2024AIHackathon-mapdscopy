from query_video import main as query_video
from vertex_query_v2 import vertex_query


def main(query: str):
    query_result = query_video(query)

    # get topk pieces
    topk = 2
    video_uri_list = set()
    video_url_list = set()
    for i in range(topk):
        video_uri = query_result[i]["id"]

        # parse to get the video uri
        video_uri = "_".join(video_uri.split("_")[:2])

        video_uri_list.add(video_uri)

        # parse start_time and end_time
        start_time, end_time = query_result[0]["id"].split("_")[-2:]

        # turn video uri to the url
        parts = video_uri.split("/")
        bucket_name = parts[2]
        video_name = parts[-1]

        video_url = f"https://storage.googleapis.com/{bucket_name}/{video_name}"

        video_url_list.add(video_url)

    video_uri_list = list(video_uri_list)
    video_url_list = list(video_url_list)

    result = vertex_query(query, video_uri_list)

    return result, {
        "start_time": 0,
        "end_time": 0,
        "video_uri": video_url_list,
    }


if __name__ == "__main__":
    query = "how many astronauts are there in the space station"
    result = main(query)
    print(result)
