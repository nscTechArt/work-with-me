"""Static hygiene checker template for living docs, markdown links, .scratch/ leaks, and module pointers."""

from __future__ import annotations

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure source directories and extensions for this repository.
CODE_DIRS: tuple[str, ...] = ("src",)
CODE_EXTS: tuple[str, ...] = (".py", ".ts", ".tsx", ".js", ".jsx", ".cs", ".go", ".rs", ".cpp", ".h", ".hpp")

# Set True on mature repositories where every module file must carry a top-of-file pointer.
REQUIRE_HEADER_POINTER = False
POINTER_HEADER_LINES = 25
UNOWNED_CODE_FILES: frozenset[str] = frozenset()

MAX_ARCH_DOC_WORDS = 1500

MODULE_POINTER_RE = re.compile(r"(?://|#)\s*Contract and decisions:\s*(\S+)")
SCRATCH_REF_RE = re.compile(r"\.scratch[/\\]", re.IGNORECASE)
# Policy/entry docs may mention generic ".scratch/" or ".scratch/<slug>/" conventions,
# so only concrete draft paths (e.g. ".scratch/my-task/spec.md") are flagged there.
SCRATCH_CONCRETE_REF_RE = re.compile(r"\.scratch[/\\][A-Za-z0-9._-]", re.IGNORECASE)
SCRATCH_CONVENTION_DOCS = frozenset({"AGENTS.md", "docs/evidence-model.md"})
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\r\n]+)`")
MD_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")


def build_repo_path_re() -> re.Pattern[str]:
    prefixes = ["docs/", r"\.agents/"] + [re.escape(d.rstrip("/")) + "/" for d in CODE_DIRS]
    joined = "|".join(prefixes)
    return re.compile(rf"^(?:{joined})[^\s<>]*$|^AGENTS\.md$|^GLOSSARY\.md$")


REPO_PATH_RE = build_repo_path_re()


def rel_posix(path: str) -> str:
    return os.path.relpath(path, REPO_ROOT).replace("\\", "/")


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def iter_code_files() -> list[str]:
    results: list[str] = []
    for folder in CODE_DIRS:
        base = os.path.join(REPO_ROOT, folder)
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                if fn.endswith(CODE_EXTS):
                    results.append(os.path.join(dirpath, fn))
    results.sort()
    return results


def iter_markdown_files() -> list[str]:
    results: list[str] = []
    for top in ("AGENTS.md", "GLOSSARY.md"):
        p = os.path.join(REPO_ROOT, top)
        if os.path.isfile(p):
            results.append(p)
    for folder in ("docs", os.path.join(".agents", "skills")):
        base = os.path.join(REPO_ROOT, folder)
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                if fn.endswith(".md"):
                    results.append(os.path.join(dirpath, fn))
    results.sort()
    return results


def check_code_files(errors: list[str]) -> int:
    files = iter_code_files()
    for path in files:
        rel = rel_posix(path)
        lines = read_text(path).splitlines()

        found_header_pointer = False
        for idx, line in enumerate(lines, 1):
            if SCRATCH_REF_RE.search(line):
                errors.append(f"{rel}:{idx}: references .scratch/ draft")

            m = MODULE_POINTER_RE.search(line)
            if m:
                raw_target = m.group(1).rstrip(").,;")
                if "#" in raw_target:
                    errors.append(f"{rel}:{idx}: module pointer must not include #section fragment ({raw_target})")
                elif not raw_target.startswith("docs/architecture/") or not raw_target.endswith(".md"):
                    errors.append(f"{rel}:{idx}: module pointer must target docs/architecture/<module>.md ({raw_target})")
                else:
                    target_abs = os.path.join(REPO_ROOT, raw_target.replace("/", os.sep))
                    if not os.path.isfile(target_abs):
                        errors.append(f"{rel}:{idx}: broken module pointer ({raw_target})")
                    elif idx <= POINTER_HEADER_LINES:
                        found_header_pointer = True

        if REQUIRE_HEADER_POINTER and rel not in UNOWNED_CODE_FILES and not found_header_pointer:
            errors.append(f"{rel}:1: missing top-of-file module pointer (Contract and decisions: docs/architecture/<module>.md)")

    return len(files)


def github_heading_slugs(path: str, cache: dict[str, set[str]]) -> set[str]:
    if path in cache:
        return cache[path]
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in read_text(path).splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = MD_HEADING_RE.match(line)
        if not m:
            continue
        heading = m.group(1).strip()
        heading = re.sub(r"`([^`]*)`", r"\1", heading)
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = heading.lower()
        slug = re.sub(r"[^\w\s-]", "", heading)
        slug = re.sub(r"\s+", "-", slug).strip("-")
        if not slug:
            continue
        if slug in counts:
            counts[slug] += 1
            slugs.add(f"{slug}-{counts[slug]}")
        else:
            counts[slug] = 0
            slugs.add(slug)
    cache[path] = slugs
    return slugs


def resolve_doc_target(source_file: str, target_file: str) -> str | None:
    if not target_file:
        return source_file
    rel_resolved = os.path.normpath(os.path.join(os.path.dirname(source_file), target_file))
    return rel_resolved if os.path.exists(rel_resolved) else None


def check_markdown_files(errors: list[str]) -> int:
    files = iter_markdown_files()
    slug_cache: dict[str, set[str]] = {}

    for path in files:
        rel = rel_posix(path)
        text = read_text(path)
        lines = text.splitlines()

        if rel.startswith("docs/architecture/"):
            words = len(text.split())
            if words > MAX_ARCH_DOC_WORDS:
                errors.append(f"{rel}:1: architecture doc has {words} words (limit {MAX_ARCH_DOC_WORDS})")

        scratch_re = SCRATCH_CONCRETE_REF_RE if rel in SCRATCH_CONVENTION_DOCS else SCRATCH_REF_RE
        for idx, line in enumerate(lines, 1):
            if scratch_re.search(line):
                errors.append(f"{rel}:{idx}: living doc references .scratch/ draft")

        in_fence = False
        for idx, line in enumerate(lines, 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            line_no_code = INLINE_CODE_RE.sub("", line)
            for m in MD_LINK_RE.finditer(line_no_code):
                raw_expr = m.group(1).strip()
                if not raw_expr:
                    continue
                raw_target = raw_expr.split()[0].strip("<>")
                if raw_target.startswith(("http://", "https://", "mailto:", "file://")):
                    continue
                if "#" in raw_target:
                    target_file, anchor = raw_target.split("#", 1)
                else:
                    target_file, anchor = raw_target, ""
                if "<" in target_file or ">" in target_file or "*" in target_file:
                    continue
                resolved = resolve_doc_target(path, target_file)
                if resolved is None:
                    errors.append(f"{rel}:{idx}: broken markdown link ({raw_target})")
                    continue
                if anchor and os.path.isfile(resolved) and resolved.endswith(".md"):
                    if anchor.lower() not in github_heading_slugs(resolved, slug_cache):
                        errors.append(f"{rel}:{idx}: broken markdown heading anchor ({raw_target})")

            for m in INLINE_CODE_RE.finditer(line):
                token = m.group(1).strip()
                if not REPO_PATH_RE.match(token):
                    continue
                if any(ch in token for ch in ("<", ">", "*", "{", "}")):
                    continue
                if "#" in token:
                    target_file, anchor = token.split("#", 1)
                else:
                    target_file, anchor = token, ""
                target_clean = target_file.rstrip("/")
                resolved = os.path.normpath(os.path.join(REPO_ROOT, target_clean))
                if not os.path.exists(resolved):
                    errors.append(f"{rel}:{idx}: broken backticked repo path ({token})")
                elif anchor and os.path.isfile(resolved) and resolved.endswith(".md"):
                    if anchor.lower() not in github_heading_slugs(resolved, slug_cache):
                        errors.append(f"{rel}:{idx}: broken backticked heading anchor ({token})")

    return len(files)


def main() -> int:
    errors: list[str] = []
    code_count = check_code_files(errors)
    doc_count = check_markdown_files(errors)

    if errors:
        print(f"Hygiene check FAILED ({len(errors)} issue(s) across {code_count} code files, {doc_count} docs):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Hygiene check PASSED ({code_count} code files, {doc_count} docs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
