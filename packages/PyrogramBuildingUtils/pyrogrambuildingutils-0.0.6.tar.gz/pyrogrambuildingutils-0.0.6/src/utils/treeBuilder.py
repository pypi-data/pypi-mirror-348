import argparse
import sys
from pathlib import Path


class TreeBuilder:
    """
    It is builder for your project tree
    """

    # ANSI-цвета (можно отключить через --no-color)
    CSI = "\033["
    RESET = CSI + "0m"
    BOLD = CSI + "1m"
    BLUE = CSI + "34m"
    GREEN = CSI + "32m"
    YELLOW = CSI + "33m"

    DEFAULT_IGNORES = {".git", "__pycache__"}

    def is_ignored(self, name: str, ignore_patterns):
        return any(
            name == pat or name.startswith(pat.rstrip("*")) for pat in ignore_patterns
        )

    def walk_tree(
        self,
        base_path: Path,
        prefix: str,
        max_depth: int,
        current_depth: int,
        ignore_patterns: set,
        show_files: bool,
        stats: dict,
        use_color: bool,
    ):
        try:
            entries = sorted(
                base_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())
            )
        except PermissionError:
            print(prefix + self.YELLOW + "[Permission Denied]" + self.RESET)
            return

        entries = [e for e in entries if not self.is_ignored(e.name, ignore_patterns)]
        total = len(entries)
        for idx, entry in enumerate(entries, 1):
            connector = "└── " if idx == total else "├── "
            name = entry.name + ("/" if entry.is_dir() else "")
            if use_color:
                name = (self.BLUE if entry.is_dir() else self.GREEN) + name + self.RESET

            print(prefix + connector + name)

            # статистика
            if entry.is_dir():
                stats["dirs"] += 1
            else:
                stats["files"] += 1

            # рекурсия
            if entry.is_dir() and (max_depth < 0 or current_depth < max_depth):
                extension = "    " if idx == total else "│   "
                self.walk_tree(
                    entry,
                    prefix + extension,
                    max_depth,
                    current_depth + 1,
                    ignore_patterns,
                    show_files,
                    stats,
                    use_color,
                )
            elif (
                entry.is_dir()
                and not show_files
                and (max_depth < 0 or current_depth < max_depth)
            ):
                # если скрываем файлы, но хотим спуститься в папки
                extension = "    " if idx == total else "│   "
                self.walk_tree(
                    entry,
                    prefix + extension,
                    max_depth,
                    current_depth + 1,
                    ignore_patterns,
                    show_files,
                    stats,
                    use_color,
                )

    def run(self):
        parser = argparse.ArgumentParser(
            description="🪴 SuperTree — максимальное дерево вашего проекта"
        )
        parser.add_argument(
            "path",
            nargs="?",
            default=".",
            help="Корневая папка (по умолчанию: текущая)",
        )
        parser.add_argument(
            "-d",
            "--max-depth",
            type=int,
            default=-1,
            help="Максимальная глубина (по умолчанию: неограничено)",
        )
        parser.add_argument(
            "-i",
            "--ignore",
            action="append",
            default=[],
            help="Паттерн для игнорирования (можно несколько). Поддерживается '*' на конце",
        )
        parser.add_argument(
            "-f",
            "--files",
            action="store_true",
            help="Показывать файлы (по умолчанию показываются и папки, и файлы). Без — только папки",
        )
        parser.add_argument(
            "-o", "--output", type=Path, help="Записать результат в файл вместо консоли"
        )
        parser.add_argument(
            "--no-color", action="store_true", help="Отключить ANSI-цвета"
        )
        args = parser.parse_args()

        root = Path(args.path).resolve()
        if not root.exists():
            print(f"❌ Путь не найден: {root}", file=sys.stderr)
            sys.exit(1)

        ignore_patterns = set(self.DEFAULT_IGNORES) | set(args.ignore)
        stats = {"dirs": 0, "files": 0}

        # Перенаправление вывода
        if args.output:
            out_stream = open(args.output, "w", encoding="utf-8")
        else:
            out_stream = sys.stdout

        # Виртуально «меняем» stdout, чтобы print писал либо в файл, либо в консоль
        old_stdout = sys.stdout
        sys.stdout = out_stream

        # Прелюдия
        header = f"{self.BOLD if not args.no_color else ''}{root}{self.RESET if not args.no_color else ''}"
        print(header)

        # Стартуем
        self.walk_tree(
            base_path=root,
            prefix="",
            max_depth=args.max_depth,
            current_depth=0,
            ignore_patterns=ignore_patterns,
            show_files=args.files,
            stats=stats,
            use_color=not args.no_color,
        )

        # Итоги
        summary = f"\nВсего папок: {stats['dirs']}, файлов: {stats['files']}"
        if not args.no_color:
            summary = self.YELLOW + summary + self.RESET
        print(summary)

        # Восстанавливаем stdout
        sys.stdout = old_stdout
        if args.output:
            out_stream.close()
            print(f"✅ Древо сохранено в {args.output}")


def run():
    TreeBuilder().run()
