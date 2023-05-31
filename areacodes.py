"""
Given a .vcf file of contact info, get area codes for all contacts
and export area code counts in CSV form.
"""
import argparse
from collections import defaultdict, Counter
import re
import vobject

TEL_KEY = "tel"
IGNORE_TELS = ["Mobile", "Other", "Home", "Work", "workFax"]


def read_file(filename):
    """read file using vobject"""
    with open(filename, "r") as f:
        card_reader = vobject.readComponents(f.read())

    file_cards = [card for card in card_reader]
    return file_cards


def parse_args():
    """Set up (and use) command line arguments for the script"""
    parser = argparse.ArgumentParser(
        prog="Get contact area code counts",
        description="Basically what it says on the tin",
    )
    parser.add_argument("filename", help="Contacts file to parse (vcf)")
    parser.add_argument(
        "-o",
        "--output-file",
        help="Where to dump area code counts (defaults to area_code_counts.csv)",
        default="area_code_counts.csv",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print extra debugging info"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Parse file
    print("Reading cards from file...")
    cards = read_file(args.filename)
    print("Finished reading cards")

    cards_by_number = defaultdict(set)
    for card in cards:
        if TEL_KEY in card.contents.keys():
            tels = [
                tel.value
                for tel in card.contents[TEL_KEY]
                if tel.value not in IGNORE_TELS
            ]
            # Remove weird characters
            tels = [re.sub("¬†|-|\(|\)| ", "", tel) for tel in tels]
            for tel in tels:
                cards_by_number[tel].add(card)

    area_codes = []
    for tel_number in sorted(cards_by_number.keys()):
        # Hacky way to get area codes, but here we are
        if len(tel_number) == 10:
            area_code = tel_number[:3]
        elif len(tel_number) == 11 and tel_number[0] == "1":
            area_code = tel_number[1:4]
        elif len(tel_number) == 12 and tel_number.startswith("+1"):
            area_code = tel_number[2:5]
        else:
            print(tel_number)
            area_code = ""
        area_codes.append(area_code)

    area_code_counter = Counter(area_codes).items()
    if args.verbose:
        print(f"All telephone numbers: {cards_by_number.keys()}")
    csv_lines = []
    csv_lines.append("Area code, Count")
    for k, v in area_code_counter:
        csv_line = f"{k}, {v}"
        csv_lines.append(csv_line)
        if args.verbose:
            print(csv_line)
    with open(args.output_file, "w") as f:
        csv_lines = [line + "\n" for line in csv_lines]
        f.writelines(csv_lines)
