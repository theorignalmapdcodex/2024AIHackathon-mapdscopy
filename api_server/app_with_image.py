import pathlib
from query_video_with_image import main as query_video_with_image
from vertex_query_with_image import vertex_query_with_image


def uri_to_url(uri: str):
    # parse to get the video uri
    video_uri = "_".join(uri.split("_")[:2])

    return video_uri


def main(query: str, image_url: str):
    query_result = query_video_with_image(image_url)

    # get top 2 video
    topk = 1
    video_url_list = set()
    for i in range(topk):
        video_uri = query_result[i]["id"]
        url = uri_to_url(video_uri)
        video_url_list.add(url)

    video_url_list = list(video_url_list)

    print(video_url_list)

    result = vertex_query_with_image(query, video_url_list, image_url)

    return result, {"start_time": 0, "end_time": 0, "video_uri": video_url_list}


if __name__ == "__main__":
    CURRENT_DIR = pathlib.Path(__file__).resolve().parent
    
    query = "Who is this person? I think I met him before. But I don't remember his name and what he does."
    image_url = str(CURRENT_DIR / "mm_rag/data_storage/data/Robert_Behnken.jpg")
    result = main(query, image_url)
    print(result)
