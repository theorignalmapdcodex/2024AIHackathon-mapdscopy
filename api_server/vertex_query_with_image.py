import os
import pathlib
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
    Image,
)
from vertexai.generative_models import GenerativeModel

# multimodal_model = GenerativeModel("gemini-1.5-flash-001")
multimodal_model = GenerativeModel("gemini-1.5-pro-001")


def vertex_query_with_image(query: str, video_uri_list: str, image_uri: str) -> str:
    video_parts = []
    for video_uri in video_uri_list:
        video_1 = Part.from_uri(video_uri, mime_type="video/mp4")
        video_parts.append(video_1)

    image_1 = Image.load_from_file(image_uri)

    role = """
You are specialized in analyzing videos and finding \
a needle in a haystack.
"""

    instruction = """
Here are three videos that record by user.
Your answers are only based on the videos.
"""

    prompt = f"""
    Please have a look at the videos and answer the following
    question.

    Question:
    {query}

    The image that along with the question is:
    """

    content = [role, instruction, *video_parts, prompt, image_1]

    generation_config = GenerationConfig(
        temperature=0.0,
    )

    responses = multimodal_model.generate_content(
        content, generation_config=generation_config, stream=False
    )

    return responses.text


if __name__ == "__main__":
    CURRENT_DIR = pathlib.Path(__file__).resolve().parent


    video_uri_1 = "gs://mmrag/90_welcome-back-to-planet-earth.mp4"

    # question = "What is the name of the leading astronaut?"
    question = "Who is this person? I think I met him before. But I don't remember his name and what he does."

    image = str(CURRENT_DIR / "mm_rag/data_storage/data/Robert_Behnken.jpg")

    result = vertex_query_with_image(question, video_uri_1, image)

    print(result)
