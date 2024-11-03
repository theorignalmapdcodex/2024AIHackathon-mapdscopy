from mm_rag.data_storage.google_storage import GoogleStorage
from mm_rag.multi_modal_data import MultiModalData


def test_main(shared_datadir):
    # Test the main function of the script
    gs = GoogleStorage()

    result = gs.upload_video(local_data_path=shared_datadir / "Welcome back to Planet Earth.mp4")

    assert type(result) == MultiModalData
    assert result.data_uri.startswith("gs://")
    assert result.data_uri.endswith(".mp4")