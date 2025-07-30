from pathlib import Path

import typer

from apresenta.cortar import cut_on_scene_change, open_video, save_cut_clips

app = typer.Typer(
    name="apresenta",
    no_args_is_help=True,
    help=(
        "Apresenta is a command-line toolkit for automatic narration of presentation videos."
    ),
    add_completion=False,
    add_help_option=True,
)


@app.command("cut")
def cut(
    video: Path = typer.Argument(..., help="Path to the video to be cut"),
    output: Path = typer.Option(
        None, help="Directory to save the cuts (default: same as video)"
    ),
    offset: int = typer.Option(
        3, help="Offset for comparison, i.e., comparing f[n] with f[n-offset]"
    ),
    threshold: float = typer.Option(0.01, help="Difference threshold for scene cut"),
):
    """
    Cuts the video into scenes, saving each segment as a new file.
    """
    if not video.exists():
        typer.echo(f"File not found: {video}")
        raise typer.Exit(code=1)

    clip = None
    try:
        typer.echo(f"Opening video: {video}")
        clip = open_video(video)
        typer.echo("Detecting scene cuts...")
        typer.echo(f"Using offset {offset} and difference threshold {threshold}")
        cuts = cut_on_scene_change(
            clip, comparison_offset=offset, difference_threshold=threshold
        )
        if not cuts:
            typer.echo("No scene cuts detected.")
            return

        output_dir = output or video.parent
        video_name = video.stem
        typer.echo(f"Saving cuts to: {output_dir}")
        save_cut_clips(cuts, output_dir, video_name)
        typer.echo(f"Done! {len(cuts)} cuts saved in {output_dir}")
    except Exception as e:
        typer.echo(f"Error processing video: {e}")
        raise typer.Exit(code=1)
    finally:
        if clip is not None:
            clip.close()


@app.command("narrate")
def narrate():
    """
    Generates narration audio for each cut (not yet implemented).
    """
    typer.echo("The 'narrate' command is not yet implemented.")


@app.command("sync")
def sync():
    """
    Combines video cuts and narration into one final video (not yet implemented).
    """
    typer.echo("The 'sync' command is not yet implemented.")


@app.command("info")
def info():
    """
    Explains the app workflow.
    """
    typer.echo(
        "Workflow:\n"
        "1. Export your presentation as a video from PowerPoint.\n"
        "2. Use the 'cut' command to split the video into smaller parts (scenes).\n"
        "3. Write narration for each cut in an automatically generated CSV file (feature not yet implemented).\n"
        "4. Use the 'narrate' command to generate narration audio files for each cut (feature not yet implemented).\n"
        "5. All files will be saved in the same output folder.\n"
        "6. Use the 'sync' command to automatically edit and export the final narrated presentation video (feature not yet implemented)."
    )


if __name__ == "__main__":
    app()
