import os
from typing import List
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(
    project=os.environ["GCP_PROJECT_ID"],
    location="us-central1",
    staging_bucket="gs://reasoning_engines",
)

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Part,
)
from vertexai.generative_models import GenerativeModel

# multimodal_model = GenerativeModel("gemini-1.5-flash-001")
multimodal_model = GenerativeModel("gemini-1.5-pro-001")


def vertex_query(query: str, video_uri_list: List[str]) -> str:

    video_list = []
    for video_uri in video_uri_list:
        video_1 = Part.from_uri(video_uri, mime_type="video/mp4")
        video_list.append(video_1)

    prompt = f"""
    Please have a look at the video and answer the following
    question.

    Question:
    {query}
    """

    content = [*video_list, prompt]

    generation_config = GenerationConfig(
        temperature=0.0,
    )

    responses = multimodal_model.generate_content(
        content, generation_config=generation_config, stream=False
    )

    return responses.text


if __name__ == "__main__":
    video_uri_1 = [
        "gs://mmrag/90_welcome-back-to-planet-earth.mp4",
    ]

    question = "What is the name of the first leading astronaut?"

    result = vertex_query(question, video_uri_1)

    print(result)
