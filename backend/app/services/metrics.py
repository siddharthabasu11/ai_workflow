from pathlib import Path


def analyze_repository(repo_path: Path) -> dict:
    file_count = 0
    total_loc = 0
    language_breakdown = {}
    file_line_counts = []

    for file_path in repo_path.rglob("*"):
        if not file_path.is_file():
            continue
        if ".git" in file_path.parts:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f)
        except (UnicodeDecodeError, OSError):
            continue

        file_count += 1
        total_loc += line_count

        ext = file_path.suffix or "no_extension"
        language_breakdown[ext] = language_breakdown.get(ext, 0) + line_count

        file_line_counts.append((file_path.name, line_count))

    file_line_counts.sort(key=lambda x: x[1], reverse=True)
    largest_files = [
        {"name": name, "lines": lines} for name, lines in file_line_counts[:5]
    ]

    return {
        "file_count": file_count,
        "total_loc": total_loc,
        "language_breakdown": language_breakdown,
        "largest_files": largest_files,
    }

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".c", ".cpp", ".h", ".hpp",
    ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".cs", ".scala", ".sh",
    ".cu", ".cuh",
}


def get_code_sample(repo_path: Path, max_chars: int = 2000, num_files: int = 2) -> str:
    code_files = []

    for file_path in repo_path.rglob("*"):
        if not file_path.is_file():
            continue
        if ".git" in file_path.parts:
            continue
        if file_path.suffix not in CODE_EXTENSIONS:
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            continue

        code_files.append((file_path.name, len(content), content))

    if not code_files:
        return ""

    code_files.sort(key=lambda x: x[1], reverse=True)

    chars_per_file = max_chars // min(num_files, len(code_files))
    samples = [
        f"--- {name} ---\n{content[:chars_per_file]}"
        for name, _, content in code_files[:num_files]
    ]
    return "\n\n".join(samples)