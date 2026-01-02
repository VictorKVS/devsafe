import argparse

from cli.commands import (
    cmd_init,
    cmd_project_add,
    cmd_project_list,
    cmd_project_activate,
    cmd_start,
    cmd_stop,
    cmd_status,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devsafe",
        description="DevSafe — fail-safe developer runtime",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # init
    sub.add_parser("init", help="Initialize DevSafe runtime")

    # project add
    p_add = sub.add_parser("project-add", help="Register new project")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--path", required=True)
    p_add.add_argument("--backup", required=True)

    # project list
    sub.add_parser("project-list", help="List registered projects")

    # project activate
    p_act = sub.add_parser("project-activate", help="Activate project")
    p_act.add_argument("--name", required=True)

    # runtime control
    sub.add_parser("start", help="Start automation")
    sub.add_parser("stop", help="Stop automation")

    # status
    sub.add_parser("status", help="Show runtime status")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "project-add":
        cmd_project_add(args)
    elif args.command == "project-list":
        cmd_project_list()
    elif args.command == "project-activate":
        cmd_project_activate(args)
    elif args.command == "start":
        cmd_start()
    elif args.command == "stop":
        cmd_stop()
    elif args.command == "status":
        cmd_status()


if __name__ == "__main__":
    main()
