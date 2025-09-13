#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
# ]
# ///
"""
Specify CLI - Setup tool for Specify projects

Usage:
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init --here

Or install globally:
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar

# Constants
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI"
}

# Language support
LANG = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "project_setup": "Specify Project Setup",
        "initializing_here": "Initializing in current directory:",
        "creating_new_project": "Creating new project:",
        "warning_dir_not_empty": "Warning: Current directory is not empty ({count} items)",
        "warning_template_overwrite": "Template files will be merged with existing content and may overwrite existing files",
        "prompt_continue": "Do you want to continue?",
        "ai_prompt": "Choose your AI assistant:",
        "git_not_found": "Git not found - will skip repository initialization",
        "error_invalid_lang": "Error: Invalid language '{lang}'. Choose 'en' or 'ja'",
        "error_both_project_and_here": "Error: Cannot specify both project name and --here flag",
        "error_missing_project_or_here": "Error: Must specify either a project name or use --here flag",
        "error_invalid_ai": "Error: Invalid AI assistant '{ai}'",
        "error_dir_exists": "Error: Directory '{project_name}' already exists",
        "tracker_title": "Initialize Specify Project",
        "step_precheck": "Check required tools",
        "step_ai_select": "Select AI assistant",
        "step_copy": "Copy template",
        "step_extract": "Extract template",
        "step_zip_list": "Archive contents",
        "step_extracted_summary": "Extraction summary",
        "step_cleanup": "Cleanup",
        "step_git": "Initialize git repository",
        "step_final": "Finalize",
        "step_flatten": "Flatten nested directory",
        "project_ready": "Project ready.",
        "next_steps_title": "Next steps",
        "next_step_here": "1. You're already in the project directory!",
        "next_step_cd": "1. [bold green]cd {project_name}[/bold green]",
        "next_step_update_constitution": "{step_num}. Update [bold magenta]CONSTITUTION.md[/bold magenta] with your project's non-negotiable principles",
        "selection_hint": "Use ↑/↓ to navigate, Enter to select, Esc to cancel",
        "selection_cancelled": "Selection cancelled",
        "selection_failed": "Selection failed.",
        "help_usage_hint": "Run 'specify --help' for usage information",
        "operation_cancelled": "Operation cancelled",
        "checking_requirements": "Checking Specify requirements...",
        "checking_internet": "Checking internet connectivity...",
        "internet_ok": "Internet connection available",
        "internet_ng": "No internet connection - required for downloading templates",
        "check_connection": "Please check your internet connection",
        "optional_tools": "Optional tools:",
        "optional_ai_tools": "Optional AI tools:",
        "cli_ready": "✓ Specify CLI is ready to use!",
        "consider_git": "Consider installing git for repository management",
        "consider_ai": "Consider installing an AI assistant for the best experience",
    },
    "ja": {
        "project_setup": "Specifyプロジェクトのセットアップ",
        "initializing_here": "現在のディレクトリに初期化:",
        "creating_new_project": "新しいプロジェクトを作成:",
        "warning_dir_not_empty": "警告: 現在のディレクトリは空ではありません ({count} 件)",
        "warning_template_overwrite": "テンプレートは既存の内容とマージされ、既存ファイルを上書きする可能性があります",
        "prompt_continue": "続行しますか？",
        "ai_prompt": "AIアシスタントを選択してください:",
        "git_not_found": "Gitが見つかりません - リポジトリの初期化をスキップします",
        "error_invalid_lang": "エラー: 無効な言語 '{lang}' です。'en' または 'ja' を指定してください",
        "error_both_project_and_here": "エラー: プロジェクト名と --here を同時に指定できません",
        "error_missing_project_or_here": "エラー: プロジェクト名を指定するか --here を使用してください",
        "error_invalid_ai": "エラー: 無効なAIアシスタント '{ai}'",
        "error_dir_exists": "エラー: ディレクトリ '{project_name}' は既に存在します",
        "tracker_title": "Specifyプロジェクトを初期化",
        "step_precheck": "必要なツールを確認",
        "step_ai_select": "AIアシスタントの選択",
        "step_copy": "テンプレートをコピー",
        "step_extract": "テンプレートを展開",
        "step_zip_list": "アーカイブ内容",
        "step_extracted_summary": "展開結果",
        "step_cleanup": "クリーンアップ",
        "step_git": "gitリポジトリを初期化",
        "step_final": "完了",
        "step_flatten": "ネストされたディレクトリを平坦化",
        "project_ready": "プロジェクトの準備ができました。",
        "next_steps_title": "次のステップ",
        "next_step_here": "1. すでにプロジェクトディレクトリ内にいます！",
        "next_step_cd": "1. [bold green]cd {project_name}[/bold green]",
        "next_step_update_constitution": "{step_num}. [bold magenta]CONSTITUTION.md[/bold magenta] を更新する",
        "selection_hint": "↑/↓ で移動、Enter で決定、Esc でキャンセル",
        "selection_cancelled": "選択をキャンセルしました",
        "selection_failed": "選択に失敗しました。",
        "help_usage_hint": "'specify --help' で使い方を表示",
        "operation_cancelled": "操作をキャンセルしました",
        "checking_requirements": "Specify の要件を確認中...",
        "checking_internet": "インターネット接続を確認中...",
        "internet_ok": "インターネット接続があります",
        "internet_ng": "インターネットに接続できません（テンプレートのダウンロードに必要）",
        "check_connection": "インターネット接続を確認してください",
        "optional_tools": "オプションのツール:",
        "optional_ai_tools": "オプションのAIツール:",
        "cli_ready": "✓ Specify CLI を利用できます！",
        "consider_git": "リポジトリ管理のために git のインストールを検討してください",
        "consider_ai": "最適な体験のためにAIアシスタントの導入を検討してください",
    },
}


def t(key: str, **kwargs) -> str:
    """Return translated string for current language."""
    return TRANSLATIONS.get(LANG, TRANSLATIONS["en"]).get(key, key).format(**kwargs)

# ASCII Art Banner
BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝
███████║██║     ███████╗╚██████╗██║██║        ██║
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝
"""

TAGLINE = {"en": "Spec-Driven Development Toolkit", "ja": "仕様駆動開発ツールキット"}
class StepTracker:
    """Track and render hierarchical steps without emojis, similar to Claude Code tree output.
    Supports live auto-refresh via an attached refresh callback.
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # If not present, add it
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[bold cyan]{self.title}[/bold cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # Circles (unchanged styling)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩
"""

def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    # Arrow keys
    if key == readchar.key.UP:
        return 'up'
    if key == readchar.key.DOWN:
        return 'down'

    # Enter/Return
    if key == readchar.key.ENTER:
        return 'enter'

    # Escape
    if key == readchar.key.ESC:
        return 'escape'

    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "Select an option", default_key: str = None) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="bright_cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[bright_cyan]{key}: {options[key]}[/bright_cyan]")
            else:
                table.add_row(" ", f"[white]{key}: {options[key]}[/white]")

        table.add_row("", "")
        table.add_row("", f"[dim]{t('selection_hint')}[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print(f"\n[yellow]{t('selection_cancelled')}[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print(f"\n[yellow]{t('selection_cancelled')}[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print(f"\n[red]{t('selection_failed')}[/red]")
        raise typer.Exit(1)

    # Suppress explicit selection print; tracker / later logic will report consolidated status
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Setup tool for Specify spec-driven development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner."""
    # Create gradient effect with different colors
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE.get(LANG, TAGLINE["en"]), style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(
    ctx: typer.Context,
    lang: str = typer.Option("en", "--lang", "-l", help="UI language: en or ja"),
):
    """Set language and show banner when no subcommand is provided."""
    global LANG
    if lang in TRANSLATIONS:
        LANG = lang
    else:
        console.print(f"[red]{t('error_invalid_lang', lang=lang)}[/red]")
        raise typer.Exit(1)
    # Show banner only when no subcommand and no help flag
    # (help is handled by BannerGroup)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center(f"[dim]{t('help_usage_hint')}[/dim]"))
        console.print()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, install_hint: str) -> bool:
    """Check if a tool is installed."""
    if shutil.which(tool):
        return True
    else:
        console.print(f"[yellow]⚠️  {tool} not found[/yellow]")
        console.print(f"   Install with: [cyan]{install_hint}[/cyan]")
        return False


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository in the specified path.
    quiet: if True suppress console output (tracker handles status)
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True

    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def apply_language_templates(project_path: Path) -> None:
    """Copy language-specific templates and README into the project.

    Primary source is packaged resources so installed users get JA files.
    Falls back to repo-root files for dev checkouts.
    """
    if LANG != "ja":
        return

    dest_templates = project_path / "templates"
    dest_templates.mkdir(parents=True, exist_ok=True)

    def copy_resource(src, dest: Path) -> None:
        with src.open("rb") as rf, open(dest, "wb") as wf:
            shutil.copyfileobj(rf, wf)

    # 1) Try packaged resources first
    copied_any = False
    try:
        from importlib.resources import files as ir_files  # Python 3.11+

        res_base = ir_files("specify_cli") / "resources" / "locales" / "ja"
        res_templates = res_base / "templates"
        if res_templates.exists():
            for src in res_templates.iterdir():
                name = getattr(src, "name", "")
                dest = dest_templates / name
                copy_resource(src, dest)
                copied_any = True

            readme_res = res_base / "README.md"
            if readme_res.exists():
                copy_resource(readme_res, project_path / "README.md")
    except Exception:
        # Ignore and fall back to repo-based copies below
        pass

    # 2) Fallback for local dev (repo checkout)
    if not copied_any:
        repo_root = Path(__file__).resolve().parents[2]
        src_templates = repo_root / "locales" / "ja" / "templates"
        if src_templates.exists():
            for src in src_templates.glob("*.md"):
                dest = dest_templates / src.name
                shutil.copy2(src, dest)
                copied_any = True

        ja_readme = repo_root / "locales" / "ja" / "README.md"
        if ja_readme.exists():
            shutil.copy2(ja_readme, project_path / "README.md")


def copy_and_extract_template_from_resources(project_path: Path, ai_assistant: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    """Copy templates and scripts from bundled resources into project_path.

    Source is unified (no per-OS duplication) under:
      specify_cli/resources/
        - templates/           (markdown templates)
        - templates/commands/  (command prompts for AI agents)
        - scripts/             (shell scripts common to all)
        - [optional] memory/   (constitution and related files)

    Destination layout mirrors the release workflow package base:
      - templates -> project_path/templates
      - scripts   -> project_path/scripts
      - memory    -> project_path/memory  (if available)
    """
    from importlib.resources import files as ir_files
    res_base = ir_files("specify_cli") / "resources"
    src_templates = res_base / "templates"
    src_scripts = res_base / "scripts"
    src_memory = res_base / "memory"

    if not is_current_dir:
        project_path.mkdir(parents=True, exist_ok=True)

    if tracker:
        tracker.start("copy", "resources")
    elif verbose:
        console.print(f"[cyan]Copying from resources: {res_base}[/cyan]")

    def copy_tree(src_path: Path, dst_path: Path, *, exclude_subpath: Path | None = None):
        for item in src_path.rglob("*"):
            if exclude_subpath is not None:
                try:
                    # Skip anything under exclude_subpath
                    item.relative_to(exclude_subpath)
                    continue
                except ValueError:
                    pass
            rel = item.relative_to(src_path)
            dest = dst_path / rel
            if item.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)

    try:
        # 1) Templates: copy from templates into project_path/templates (excluding templates/commands)
        if src_templates.exists():
            dest_templates = project_path / "templates"
            commands_sub = src_templates / "commands"
            copy_tree(Path(src_templates), dest_templates, exclude_subpath=Path(commands_sub))

        # 2) Scripts: copy to project_path/scripts (no OS branching to match release)
        if src_scripts.exists():
            dest_scripts = project_path / "scripts"
            copy_tree(Path(src_scripts), dest_scripts)

            # Make .sh executable on Unix-like platforms
            if not sys.platform.startswith("win"):
                for sh in dest_scripts.rglob("*.sh"):
                    try:
                        mode = sh.stat().st_mode
                        sh.chmod(mode | 0o111)
                    except Exception:
                        pass

        # 3) Memory: optional copy if available in resources, else fall back to repo root
        memory_copied = False
        if src_memory.exists():
            dest_memory = project_path / "memory"
            copy_tree(Path(src_memory), dest_memory)
            memory_copied = True
        if not memory_copied:
            # Fallback for local development environment (repo checkout)
            repo_root = Path(__file__).resolve().parents[2]
            local_memory = repo_root / "memory"
            if local_memory.exists():
                dest_memory = project_path / "memory"
                copy_tree(local_memory, dest_memory)

        if tracker:
            tracker.complete("copy")
    except Exception as e:
        if tracker:
            tracker.error("copy", str(e))
        else:
            if verbose:
                console.print(f"[red]Error copying template:[/red] {e}")
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)

    return project_path


def generate_agent_commands(project_path: Path, ai_assistant: str) -> None:
    """Generate agent-specific command files from templates/commands.

    Mirrors the release workflow behavior:
      - Claude:   write to `.claude/commands/*.md` (content only)
      - Gemini:   write to `.gemini/commands/*.toml` with description + prompt
      - Copilot:  write to `.github/prompts/*.prompt.md` with title + content
    """
    from importlib.resources import files as ir_files

    res_base = ir_files("specify_cli") / "resources"
    src_cmds = res_base / "templates" / "commands"
    if not src_cmds.exists():
        return

    # Determine output directory and formatting rules
    if ai_assistant == "claude":
        out_dir = project_path / ".claude" / "commands"
        mode = "claude"
    elif ai_assistant == "gemini":
        out_dir = project_path / ".gemini" / "commands"
        mode = "gemini"
    elif ai_assistant == "copilot":
        out_dir = project_path / ".github" / "prompts"
        mode = "copilot"
    else:
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    def parse_front_matter_and_body(text: str) -> tuple[dict, str]:
        """Very small YAML front matter parser for 'description' only."""
        lines = text.splitlines()
        meta: dict[str, str] = {}
        body_start = 0
        if len(lines) >= 3 and lines[0].strip() == "---":
            # find second '---'
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    body_start = i + 1
                    break
            # parse between 1..i-1
            for j in range(1, body_start - 1):
                line = lines[j]
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    meta[k] = v
        else:
            body_start = 0
        body = "\n".join(lines[body_start:]).lstrip("\n")
        return meta, body

    for entry in Path(src_cmds).glob("*.md"):
        with open(entry, "r", encoding="utf-8") as rf:
            raw = rf.read()
        meta, body = parse_front_matter_and_body(raw)

        if mode == "claude":
            # Replace placeholder with $ARGUMENTS
            content = body.replace("{ARGS}", "$ARGUMENTS")
            out_path = out_dir / f"{entry.stem}.md"
            out_path.write_text(content, encoding="utf-8")
        elif mode == "gemini":
            content = body.replace("{ARGS}", "{{args}}")
            lines = []
            desc = meta.get("description", "")
            lines.append(f"description = \"{desc}\"")
            lines.append("")
            lines.append("prompt = \"\"\"")
            lines.append(content)
            lines.append("\"\"\"")
            out_path = out_dir / f"{entry.stem}.toml"
            out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        elif mode == "copilot":
            content = body.replace("{ARGS}", "$ARGUMENTS")
            desc = meta.get("description", "").split(". ")[0].strip()
            title = f"# {desc}" if desc else "# Prompt"
            out_lines = [title, "", content]
            out_path = out_dir / f"{entry.stem}.prompt.md"
            out_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")

    # Optional: If Gemini, copy GEMINI.md if available in resources or repo
    if ai_assistant == "gemini":
        # Try packaged resources path first
        candidates: list[Path] = []
        try:
            gemini_md = (ir_files("specify_cli") / "resources" / "agent_templates" / "gemini" / "GEMINI.md")
            if gemini_md.exists():
                # type: ignore - importlib.resources Traversable has open(); we need a local Path for uniform handling
                tmp = project_path / "GEMINI.md"
                with gemini_md.open("rb") as rf, open(tmp, "wb") as wf:
                    shutil.copyfileobj(rf, wf)
                candidates.append(tmp)
        except Exception:
            pass
        if not candidates:
            repo_root = Path(__file__).resolve().parents[2]
            local = repo_root / "agent_templates" / "gemini" / "GEMINI.md"
            if local.exists():
                shutil.copy2(local, project_path / "GEMINI.md")

# Backward-compatibility shims (disable network path and route to resources)
def download_template_from_github(ai_assistant: str, download_dir: Path, *, verbose: bool = True, show_progress: bool = True):
    raise typer.Exit("Network downloads are disabled. Templates are bundled in resources.")


def download_and_extract_template(project_path: Path, ai_assistant: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    return copy_and_extract_template_from_resources(project_path, ai_assistant, is_current_dir, verbose=verbose, tracker=tracker)


@app.command()
def init(
    project_name: str = typer.Argument(None, help="Name for your new project directory (optional if using --here)"),
    ai_assistant: str = typer.Option(None, "--ai", help="AI assistant to use: claude, gemini, or copilot"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="Skip checks for AI agent tools like Claude Code"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    here: bool = typer.Option(False, "--here", help="Initialize project in the current directory instead of creating a new one"),
):
    """
    Initialize a new Specify project from the bundled template.

    This command will:
    1. Check that required tools are installed (git is optional)
    2. Let you choose your AI assistant (Claude Code, Gemini CLI, or GitHub Copilot)
    3. Copy the appropriate template from bundled resources
    4. Place it into a new project directory or current directory
    5. Initialize a fresh git repository (if not --no-git and no existing repo)
    6. Optionally set up AI assistant commands

    Examples:
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai gemini
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init --here --ai claude
        specify init --here
    """
    # Show banner first
    show_banner()

    # Validate arguments
    if here and project_name:
        console.print(f"[red]{t('error_both_project_and_here')}[/red]")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print(f"[red]{t('error_missing_project_or_here')}[/red]")
        raise typer.Exit(1)

    # Determine project directory
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        # Check if current directory has any files
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]{t('warning_dir_not_empty', count=len(existing_items))}[/yellow]")
            console.print(f"[yellow]{t('warning_template_overwrite')}[/yellow]")

            # Ask for confirmation
            response = typer.confirm(t('prompt_continue'))
            if not response:
                console.print(f"[yellow]{t('operation_cancelled')}[/yellow]")
                raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # Check if project directory already exists
        if project_path.exists():
            console.print(f"[red]{t('error_dir_exists', project_name=project_name)}[/red]")
            raise typer.Exit(1)

    console.print(Panel.fit(
        f"[bold cyan]{t('project_setup')}[/bold cyan]\n"
        f"{t('initializing_here') if here else t('creating_new_project')} [green]{project_path.name}[/green]"
        + (f"\n[dim]Path: {project_path}[/dim]" if here else ""),
        border_style="cyan"
    ))

    # Check git only if we might need it (not --no-git)
    git_available = True
    if not no_git:
        git_available = check_tool("git", "https://git-scm.com/downloads")
        if not git_available:
            console.print(f"[yellow]{t('git_not_found')}[/yellow]")

    # AI assistant selection
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]{t('error_invalid_ai', ai=ai_assistant)}[/red] Choose from: {', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # Use arrow-key selection interface
        selected_ai = select_with_arrows(
            AI_CHOICES,
            t('ai_prompt'),
            "copilot"
        )

    # Check agent tools unless ignored
    if not ignore_agent_tools:
        agent_tool_missing = False
        if selected_ai == "claude":
            if not check_tool("claude", "Install from: https://docs.anthropic.com/en/docs/claude-code/setup"):
                console.print("[red]Error:[/red] Claude CLI is required for Claude Code projects")
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "Install from: https://github.com/google-gemini/gemini-cli"):
                console.print("[red]Error:[/red] Gemini CLI is required for Gemini projects")
                agent_tool_missing = True
        # GitHub Copilot check is not needed as it's typically available in supported IDEs

        if agent_tool_missing:
            console.print("\n[red]Required AI tool is missing![/red]")
            console.print("[yellow]Tip:[/yellow] Use --ignore-agent-tools to skip this check")
            raise typer.Exit(1)

    # Download and set up project
    # New tree-based progress (no emojis); include earlier substeps
    tracker = StepTracker(t('tracker_title'))
    # Flag to allow suppressing legacy headings
    sys._specify_tracker_active = True
    # Pre steps recorded as completed before live rendering
    tracker.add("precheck", t('step_precheck'))
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", t('step_ai_select'))
    tracker.complete("ai-select", f"{selected_ai}")
    for key, label_key in [
        ("copy", "step_copy"),
        ("extract", "step_extract"),
        ("git", "step_git"),
        ("final", "step_final")
    ]:
        tracker.add(key, t(label_key))

    # Use transient so live tree is replaced by the final static render (avoids duplicate output)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            copy_and_extract_template_from_resources(project_path, selected_ai, here, verbose=False, tracker=tracker)
            apply_language_templates(project_path)

            # Generate agent-specific commands (mirrors release workflow)
            tracker.start("extract", "generate agent commands")
            generate_agent_commands(project_path, selected_ai)
            tracker.complete("extract", "commands ready")

            # Git step
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif git_available:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "project ready")
        except Exception as e:
            tracker.error("final", str(e))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # Force final render
            pass

    # Final static tree (ensures finished state visible after Live context ends)
    console.print(tracker.render())
    console.print(f"\n[bold green]{t('project_ready')}[/bold green]")

    # Boxed "Next steps" section
    steps_lines = []
    if not here:
        steps_lines.append(t('next_step_cd', project_name=project_name))
        step_num = 2
    else:
        steps_lines.append(t('next_step_here'))
        step_num = 2

    if selected_ai == "claude":
        steps_lines.append(f"{step_num}. Open in Visual Studio Code and start using / commands with Claude Code")
        steps_lines.append("   - Type / in any file to see available commands")
        steps_lines.append("   - Use /specify to create specifications")
        steps_lines.append("   - Use /plan to create implementation plans")
        steps_lines.append("   - Use /tasks to generate tasks")
    elif selected_ai == "gemini":
        steps_lines.append(f"{step_num}. Use / commands with Gemini CLI")
        steps_lines.append("   - Run gemini /specify to create specifications")
        steps_lines.append("   - Run gemini /plan to create implementation plans")
        steps_lines.append("   - See GEMINI.md for all available commands")
    elif selected_ai == "copilot":
        steps_lines.append(f"{step_num}. Open in Visual Studio Code and use [bold cyan]/specify[/], [bold cyan]/plan[/], [bold cyan]/tasks[/] commands with GitHub Copilot")

    step_num += 1
    steps_lines.append(t('next_step_update_constitution', step_num=step_num))

    steps_panel = Panel("\n".join(steps_lines), title=t('next_steps_title'), border_style="cyan", padding=(1,2))
    console.print()  # blank line
    console.print(steps_panel)

    # Removed farewell line per user request


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print(f"[bold]{t('checking_requirements')}[/bold]\n")

    console.print(f"\n[cyan]{t('optional_tools')}[/cyan]")
    git_ok = check_tool("git", "https://git-scm.com/downloads")

    console.print(f"\n[cyan]{t('optional_ai_tools')}[/cyan]")
    claude_ok = check_tool("claude", "Install from: https://docs.anthropic.com/en/docs/claude-code/setup")
    gemini_ok = check_tool("gemini", "Install from: https://github.com/google-gemini/gemini-cli")

    console.print(f"\n[green]{t('cli_ready')}[/green]")
    if not git_ok:
        console.print(f"[yellow]{t('consider_git')}[/yellow]")
    if not (claude_ok or gemini_ok):
        console.print(f"[yellow]{t('consider_ai')}[/yellow]")


def main():
    app()


if __name__ == "__main__":
    main()
