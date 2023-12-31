import argparse
import typing

# locals
import aamva_2020

def decode_aamva_fields(pdf417_data_txt : typing.List[str]) -> dict:
    """
    pdf417_data_txt is a list of text lines consisting of the full PDF-417 data from the drivers license barcode
    """

    aamva_2020.parse_header(pdf417_data_txt)
    aamva_2020.parse_pdf417_data(pdf417_data_txt)


if __name__ == "__main__":

    with open("new_ca.txt", "r") as f:
        
        decode_aamva_fields(f.readlines())