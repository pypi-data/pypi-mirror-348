# cli.py
import argparse
from typing import List, Any
from pubmed_paper_fetcher.fetcher import (
    fetch_pubmed_ids, fetch_paper_details, extract_data, save_to_csv, print_to_console
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with non-academic authors.")
    parser.add_argument("query", type=str, help="Query to search for papers.")
    parser.add_argument("-f", "--file", type=str, help="Specify the filename to save the results.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print detailed information.")
    args: argparse.Namespace = parser.parse_args()

    pubmed_ids: List[str] = fetch_pubmed_ids(args.query, args.debug)
    results: List[Any] = []

    for pubmed_id in pubmed_ids:
        details: str = fetch_paper_details(pubmed_id, args.debug)
        result: Any = extract_data(pubmed_id, details, args.debug)
        results.append(result)

    if args.file:
        save_to_csv(results, args.file)
        print(f"Results saved to {args.file}")
    else:
        print_to_console(results)

if __name__ == "__main__":
    main()

