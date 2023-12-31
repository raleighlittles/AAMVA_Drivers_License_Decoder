import argparse
import typing

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

    with open("examples/test_va.txt", "r") as f:
        
        id_card_results = decode_aamva_fields(f.readlines())
        
        print(id_card_results)