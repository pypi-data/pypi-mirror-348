from pathlib import Path

name = "movies"
this_folder = Path(__file__).parent.resolve()
fn_wopr = this_folder / f"{name}.wopr"
fn_lnk = this_folder / f"{name}.lnk"
fn_lnk_with_topics = this_folder / f"{name}_with_topics.lnk"
