from pathlib import Path
from subprocess import run
import sys


def samples(repo: Path):
    """
    Check the samples
    """
    from pathlib import Path
    import difflib
    from wowool.native.core.engine import Engine
    from wowool.native.core.engine import default_engine

    sys.path.append(str(repo))
    engine: Engine = default_engine()
    language_info = engine.language_info
    if not language_info:
        raise RuntimeError("No language information available")

    def get_language(fn: Path):
        return str(fn.name).split("-")[0]

    samples_dir = repo / "samples"

    for fn in samples_dir.glob("*.py"):
        language = get_language(fn)
        if language not in language_info:
            print(f"Warning: Skipping '{fn.name}': language '{language}' not available")
            continue

        print(f"Running sample: {fn}")
        result = run(f"python {fn}", capture_output=True, shell=True, cwd=fn.parent)
        if result.returncode != 0:
            print(f"Error running {fn}: {result.stderr.decode()}")
            continue
        fn_ref = Path(str(fn).replace(".py", "-output.txt"))
        if fn_ref.exists():
            lines = [line for line in difflib.unified_diff(fn_ref.read_text(), result.stdout.decode())]
            if 0 != len(lines):
                print("Unexpected output:")
                print(result.stdout.decode())
        else:
            print(f"Reference file {fn_ref} does not exist, skipping comparison")
            print(f"stdout: {result.stdout.decode()}")
            fn_ref = Path(str(fn).replace(".py", "-output-result.txt"))
            fn_ref.write_text(result.stdout.decode())
