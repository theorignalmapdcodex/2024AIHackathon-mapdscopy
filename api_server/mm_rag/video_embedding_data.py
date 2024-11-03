class VideoEmbeddingData:
    def __init__(self, video_id, embedding, start_offset_sec, end_offset_sec):
        self.video_id = video_id
        self.embedding = embedding
        self.start_offset_sec = start_offset_sec
        self.end_offset_sec = end_offset_sec