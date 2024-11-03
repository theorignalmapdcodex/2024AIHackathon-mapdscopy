from mm_rag.data_storage.clip_video import clip_video


def test_clip_video(shared_datadir, tmp_path):
    video_file = shared_datadir / "Welcome back to Planet Earth.mp4"

    output_file = tmp_path / "output.mp4"

    clip_video(video_file, 0, 1, output_file)

    assert output_file.exists()
