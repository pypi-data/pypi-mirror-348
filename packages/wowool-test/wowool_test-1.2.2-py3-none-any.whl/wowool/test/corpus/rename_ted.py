from pathlib import Path
import shutil

root = Path(__file__).parent
print(root)

prefixx = "https__www.ted.com_talks_"
postfixx = "_transcript_language_xx.txt"

files = [fn for fn in root.glob("**/*.txt") if fn.name.startswith(prefixx)]

end_offset = 0 - len(postfixx)

for fn in files:
    language = fn.parent.name
    ted_folder = fn.parent / "ted_talks"
    ted_folder.mkdir(parents=True, exist_ok=True)
    target_fn = ted_folder / f"{fn.name[len(prefixx):end_offset]}.txt"
    print(f"{fn}--->{target_fn}")
    shutil.move(fn, target_fn)
