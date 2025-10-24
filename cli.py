import argparse
import time

from chrome import launch_chrome
from follow_random import follow_random
from logger import setup_logger
from unfollow_all import main as unfollow_all_main

logger = setup_logger()


def cmd_unfollow(args):
    logger.info("Starting unfollow all process...")
    launch_chrome(url="https://example.com", incognito=False)
    time.sleep(3)
    unfollow_all_main()


def cmd_follow(args):
    count = args.count
    logger.info(f"Starting follow process for {count} users...")
    launch_chrome(url="https://example.com", incognito=False)
    time.sleep(3)
    follow_random(count=count)


def main():
    parser = argparse.ArgumentParser(
        description="Twitter Unfollower/Follower CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    unfollow_parser = subparsers.add_parser(
        "unfollow",
        help="Unfollow all users"
    )
    unfollow_parser.set_defaults(func=cmd_unfollow)

    follow_parser = subparsers.add_parser(
        "follow",
        help="Follow random users from target profiles"
    )
    follow_parser.add_argument(
        "count",
        type=int,
        help="Number of users to follow"
    )
    follow_parser.set_defaults(func=cmd_follow)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
