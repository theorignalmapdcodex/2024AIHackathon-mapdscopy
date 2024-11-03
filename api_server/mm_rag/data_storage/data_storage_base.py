from mm_rag.multi_modal_data import MultiModalData

class DataStorageBase:
    def __init__(self) -> None:
        pass

    def upload_video(self, local_data_path: str, target_name: str) -> MultiModalData:
        raise NotImplementedError()