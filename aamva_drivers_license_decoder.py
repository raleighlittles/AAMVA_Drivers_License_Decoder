import argparse
import typing
import os
import json

# locals
import aamva_2020


def decode_aamva_fields(pdf417_data_txt : typing.List[str]) -> dict:
    """
    pdf417_data_txt is a list of text lines consisting of the full PDF-417 data from the drivers license barcode
    """

    results = dict()

    header_only = aamva_2020.parse_header(pdf417_data_txt)
    body_results = aamva_2020.parse_pdf417_data(pdf417_data_txt)

    results["header"] = header_only
    results["body"] = body_results

    return results


if __name__ == "__main__":

    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-f", "--text-file", type=str, help="Input text file containing the decoded PDF-417 data, to read from", required=True)
    argparse_parser.add_argument("-o", "--output-file", type=str, help="Output text file to write results to")

    argparse_args = argparse_parser.parse_args()

    input_filename = argparse_args.text_file

    if os.path.exists(input_filename):

        with open(file=input_filename, mode="r", encoding="utf-8") as input_file:
            
            id_card_results = decode_aamva_fields([x for x in input_file.readlines() if x != ""])

            formatted_results_json = json.dumps(id_card_results, sort_keys=True, indent=4)

            if argparse_args.output_file is not None:
                with open(file=argparse_args.output_file, mode="w", encoding="utf-8") as output_file:
                    output_file.write(formatted_results_json)
                    output_file.flush()

            else:
                print("---------------------")
                print(formatted_results_json)

    else:
        raise FileNotFoundError(f"Error can't find input file '{input_filename}'")