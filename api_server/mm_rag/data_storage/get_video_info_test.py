from mm_rag.data_storage.get_video_info import get_video_info

def test_main(shared_datadir):
    video_file = shared_datadir / "Welcome back to Planet Earth.mp4"

    video_info = get_video_info(video_file)

    assert video_info["duration"] > 0