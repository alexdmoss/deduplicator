import sys
import os
import click

from deduplicator.logger import log


@click.command()
@click.option("--file", "-f", help="Input file with duplicates", type=str, required=True)
@click.option("--dry-run", help="Dry-run mode - print what would do only", flag_value=True)
def main(file, dry_run):
    if dry_run:
        log.info("Running in dry-run mode")
    log.info(f"Parsing input file [{file}]")

    duplicate_count = 0

    with open(file, "r") as f:
        lines = f.readlines()

        for line in lines:

            found_files = line.strip().split(",")
            log.info(f"Found {len(found_files) - 1} duplicate files for {found_files[0]}")

            # remove the duplicate files
            found_files.pop(0)

            for duplicates in found_files:

                file_to_delete = duplicates.strip()
                duplicate_count += 1

                try: 
                    os.stat(file_to_delete)

                    if dry_run:
                        log.info(f"[dry-run] Would delete {file_to_delete}")
                    else:
                        log.info(f"Deleting {file_to_delete}")
                        os.remove(file_to_delete)

                except OSError as e:
                    log.error(f"File {file_to_delete} does not exist or cannot be read")



    log.info(f"Found [{len(lines)}] lines")
    log.info(f"[{duplicate_count}] duplicate files removed")


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
