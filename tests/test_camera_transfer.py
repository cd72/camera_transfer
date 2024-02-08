import logging
from datetime import datetime
from pathlib import Path

import pytest

from cameratransfer import app
from cameratransfer.camera_file_getter import CameraFileGetter
from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings
from cameratransfer.hash_store import HashStore
from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter

logger = logging.getLogger(__name__)


@pytest.fixture
def base_test_settings(tmp_path: Path) -> Settings:
    return Settings(
        camera_folder=tmp_path,
        main_photos_folder=tmp_path,
        main_videos_folder=tmp_path,
        sqlite_database=None,
        dry_run=False,
        camera_model_short_names={"COOLPIX S9700": "S9700"},
    )


@pytest.fixture
def single_image_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/single_image"
    return base_test_settings

@pytest.fixture
def duplicate_image_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/duplicate_image"
    return base_test_settings

@pytest.fixture
def single_video_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/single_video"
    return base_test_settings

@pytest.fixture
def duplicate_video_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/duplicate_video"
    return base_test_settings


def test_app_load_dotenv() -> None:
    settings = app.load_settings_from_dotenv(Path(__file__).parent / "test.env")

    assert settings.dry_run == False
    assert settings.camera_model_short_names == {"COOLPIX S9700": "S9700"}
    assert settings.main_photos_folder == Path("/tmp")
    assert settings.main_videos_folder == Path("/tmp")
    assert settings.camera_folder == Path("/tmp")
    assert settings.sqlite_database is None
    assert settings.image_formats == {".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"}
    assert settings.video_formats == {".mov", ".MOV", ".mp4", ".MP4"}



##########################################################################################


def test_camera_transfer(single_image_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(single_image_test_settings)
    camera_transfer.run()
    assert len(list(single_image_test_settings.main_photos_folder.iterdir())) == 1

    expected_output_file = (
        Path(single_image_test_settings.main_photos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217


def test_camera_transfer_duplicate(duplicate_image_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(duplicate_image_test_settings)
    camera_transfer.run()
    assert len(list(duplicate_image_test_settings.main_photos_folder.iterdir())) == 1

    expected_output_file = (
        Path(duplicate_image_test_settings.main_photos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217

def test_video_transfer(single_video_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(single_video_test_settings)
    camera_transfer.run()
    assert len(list(single_video_test_settings.main_videos_folder.iterdir())) == 1

    expected_output_file = (
        Path(single_video_test_settings.main_videos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047


def test_video_transfer_duplicate(duplicate_video_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(duplicate_video_test_settings)
    camera_transfer.run()
    assert len(list(duplicate_video_test_settings.main_videos_folder.iterdir())) == 1

    expected_output_file = (
        Path(duplicate_video_test_settings.main_videos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047

