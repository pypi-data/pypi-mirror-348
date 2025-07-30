import os
from itertools import groupby
from pathlib import Path

import numpy as np
from moviepy import VideoClip, VideoFileClip
from numpy.typing import NDArray


def open_video(path: Path) -> VideoFileClip:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    clip = VideoFileClip(
        filename=path.as_posix(),
        has_mask=False,
        audio=False,
        target_resolution=(1920, None),
        fps_source="tbr",
    )

    return clip


def calculate_difference(
    current_frame: NDArray[np.float32],
    previous_frame: NDArray[np.float32],
) -> np.float32:
    cols, rows = 16, 9

    height, width, _ = current_frame.shape
    block_height = height // rows
    block_width = width // cols

    cropped_current = current_frame[: block_height * rows, : block_width * cols, :]
    cropped_prev = previous_frame[: block_height * rows, : block_width * cols, :]

    current_blocks = cropped_current.reshape(rows, block_height, cols, block_width, 3)
    prev_blocks = cropped_prev.reshape(rows, block_height, cols, block_width, 3)

    block_diff = np.abs(
        current_blocks.astype(np.float32) - prev_blocks.astype(np.float32)
    )

    mean_block_diff = (block_diff.mean(axis=(1, 3, 4))) / 255.0  # shape: (rows, cols)
    max_diff = np.max(mean_block_diff)

    return max_diff


type frame_time = float
type frame_difference = float


def compare_every_frame(
    clip: VideoClip,
    comparison_offset: int = 3,
) -> list[tuple[frame_time, frame_difference]]:
    if clip.n_frames <= comparison_offset:
        raise ValueError("`frame_offset` is lower than amount of frames")

    times_and_frames = clip.iter_frames(with_times=True, logger="bar")

    previous_frames = []
    differences = []

    for current_time, current_frame in times_and_frames:
        if len(previous_frames) < comparison_offset:
            previous_frames.append(current_frame)
            differences.append((float(current_time), 0.0))
            continue

        previous_frame = previous_frames[-comparison_offset]
        previous_frames.append(current_frame)

        difference = calculate_difference(current_frame, previous_frame)
        differences.append((float(current_time), float(difference)))

    return differences


def get_where_to_cut(
    differences: list[tuple[frame_time, frame_difference]],
    difference_threshold: float = 0.01,
) -> list[tuple[frame_time, frame_time]]:
    grouped_differences = [
        list(group)
        for _, group in groupby(
            differences,
            key=lambda x: x[1] > difference_threshold,
        )
    ]

    where_to_cut = [(group[0][0], group[-1][0]) for group in grouped_differences]

    return where_to_cut


def cut_on_scene_change(
    video_clip: VideoClip,
    comparison_offset: int = 3,
    difference_threshold: float = 0.01,
) -> list[VideoClip]:
    """
    Splits a video clip into multiple subclips at points where a scene change is detected.

    Args:
        video_clip (VideoClip): The input video clip to be analyzed and split.
        comparison_offset (int, optional): The n-th frame to compare the current frame against. Defaults to 3.
        difference_threshold (float, optional): The difference between frames to consider a scene change. Defaults to 0.01.

    Returns:
        list[VideoClip]: A list of subclips, each corresponding to a segment between detected scene changes.
    """

    differences = compare_every_frame(video_clip, comparison_offset)
    where_to_cut = get_where_to_cut(differences, difference_threshold)
    new_clips = [video_clip.subclipped(start, end) for start, end in where_to_cut]

    return new_clips


def save_cut_clips(
    cuts: list[VideoClip],
    output_dir: Path,
    video_name: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    threads = os.cpu_count() or 1

    for i, cut in enumerate(cuts):
        output_path = output_dir / f"{video_name}_{i + 1}.mp4"
        cut.write_videofile(
            output_path.as_posix(),
            fps=30,
            codec="libx264",
            audio=False,
            preset="ultrafast",
            threads=threads,
            logger="bar",
        )
