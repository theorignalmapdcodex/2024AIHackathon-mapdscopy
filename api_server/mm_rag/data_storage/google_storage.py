import pathlib
from typing import Optional
from mm_rag.data_storage.data_storage_base import DataStorageBase
from mm_rag.multi_modal_data import MultiModalData
from mm_rag.data_storage.get_video_info import get_video_info
import math

from google.cloud import storage

from slugify import slugify


class GoogleStorage(DataStorageBase):
    def __init__(self, bucket_name="mmrag"):
        self.bucket_name = bucket_name

        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def upload_video(self, local_data_path: str) -> MultiModalData:
        video_info = get_video_info(local_data_path)
        if video_info["duration"] == 0:
            raise ValueError("Video duration is 0")
        video_duration = video_info["duration"]

        data_path = pathlib.Path(local_data_path)
        target_name = (
            str(math.ceil(video_duration))
            + "_"
            + slugify(data_path.stem)
            + data_path.suffix
        )

        blob = self.bucket.blob(target_name)

        blob.upload_from_filename(local_data_path, if_generation_match=None)

        # link = blob.path_helper(self.bucket_name, target_name)
        link = f"{self.bucket_name}/{target_name}"

        return MultiModalData("gs://" + link, video_duration)

    def upload_image(self, local_data_path: str) -> MultiModalData:
        data_path = pathlib.Path(local_data_path)
        target_name = slugify(data_path.stem) + data_path.suffix

        blob = self.bucket.blob(target_name)

        blob.upload_from_filename(local_data_path, if_generation_match=None)

        # link = blob.path_helper(self.bucket_name, target_name)
        link = f"{self.bucket_name}/{target_name}"

        return MultiModalData("gs://" + link)
