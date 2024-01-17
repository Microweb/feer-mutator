import asyncio
import argparse
import logging

from .consts import ROOT, ORGANIZATION_NAME, VERSION
from .hubstaff import create_hubstaff_api
from .renders import render_html_organization
from .time import get_period
from .storage import save_result_in_file


logger = logging.getLogger(__name__)


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mutator")
    parser.add_argument("--version", action="version", version=VERSION)

    group = parser.add_argument_group("Framework options")
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="set loggers to debug level",
    )
    group.add_argument(
        "--day",
        action="store",
        type=int,
        help="generate summary for specific relative day",
    )
    return parser.parse_args()


async def main():
    args = get_arguments()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    period = get_period(args.day)

    logger.info(
        "Generating summary for organization: %s period: %s", ORGANIZATION_NAME, period
    )
    api = create_hubstaff_api()
    organization = await api.get_organization_activities(ORGANIZATION_NAME, period)
    result = render_html_organization(organization, period)

    file_name = f"{organization.name}_{period}.html"
    file_path = ROOT / file_name
    await save_result_in_file(file_path, result)

    logger.info("Summary generated to file: %s", file_path)


def cli():
    asyncio.run(main())
