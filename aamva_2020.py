import typing

import pdb
import re

# locals
import constants
import fields

class AAMVA_Header_Exception(Exception):
    pass


def parse_pdf417_data(pdf_417_raw_data : typing.List[str]):

    parsed_data = list()

    data_elements = set([fields.JurisdictionSpecificVehicleClass(), fields.JurisdictionSpecificRestrictionCodes(), fields.JurisdictionSpecificEndorsementCodes(), fields.DocumentExpirationDate(), fields.CustomerFamilyName(), fields.CustomerFirstName(), fields.CustomerMiddleName(), fields.DocumentIssueDate(), fields.DateOfBirth(), fields.PhysicalDescriptionSex(), fields.PhysicalDescriptionEyeColor(), fields.PhysicalDescriptionHeight(), fields.AddressStreet1(), fields.AddressCity(), fields.AddressJurisdictionCode(), fields.AddressPostalCode(), fields.CustomerIDNumber(), fields.DocumentDiscriminator(), fields.CountryIdentification(), fields.FamilyNameTruncation(), fields.FirstNameTruncation(), fields.MiddleNameTruncation(), fields.AddressStreet2(), fields.HairColor(), fields.PlaceOfBirth(), fields.AuditInformation(), fields.InventoryControlNumber(), fields.AliasFamilyName(), fields.AliasGivenName(), fields.AliasSuffixName(), fields.NameSuffix(), fields.PhysicalDescriptionWeightRange(), fields.RaceEthnicity(), fields.StandardVehicleClassification(), fields.StandardEndorsementCode(), fields.StandardRestrictionCode(), fields.JurisdictionSpecificVehicleClassificationDescription(), fields.JurisdictionSpecificEndorsementCodeDescription(), fields.JurisdictionSpecificRestrictionCodeDescription(), fields.ComplianceType(), fields.CardRevisionDate(), fields.HAZMAT_Endorsement_Expiration_Date(), fields.LimitedDurationDocumentIndicator(), fields.WeightPounds(), fields.WeightKilograms(), fields.Under18Until(), fields.Under21Until(), fields.OrganDonorIndicator(), fields.VeteranIndicator()])

    for idx, data_element in enumerate(data_elements):

        field_data = dict()

        for line in pdf_417_raw_data:
            regex_matches = re.findall(data_element.get_regex(), line)
            if len(regex_matches) > 1:
                raise ValueError("Incorrect regex result, found too many values")
            
            elif len(regex_matches) == 1:
                data_element.value = regex_matches[0]
                print(f"Parsing field: '{data_element.key_name}'")
                parsed_value = data_element.parse()

                field_data["idx"] = idx
                field_data["key"] = data_element.code
                field_data["description"] = data_element.key_name
                field_data["value"] = data_element.value
                
                # Avoid adding the 'parsed' value field if its meaning is the same as the regular value
                if parsed_value != data_element.value:
                    field_data["parsed_value"] = parsed_value

                parsed_data.append(field_data)
                break

    print(f"Extracted {len(parsed_data)} elements from PDF 417 data")
    pdb.set_trace()
    return parsed_data





def parse_header(pdf_417_raw_data : typing.List[str]) -> dict:

    if not pdf_417_raw_data[0].startswith(constants.COMPLIANCE_INDICATOR):
        raise AAMVA_Header_Exception("Compliance indicator missing")
    
    if not pdf_417_raw_data[1].startswith(constants.FILE_TYPE):
        raise AAMVA_Header_Exception("File type missing")
        
    header_dict = parse_ansi_field(pdf_417_raw_data[1].split(" ")[1])

    return header_dict

    
def parse_ansi_field(ansi_field_txt : str) -> dict:
    """
    Example ANSI field: 
    "636000100002DL00410278ZV03190008DLDAQT64235789"

    The AAMVA specification defines a minimum number of fields that must be present in this string,
    but other states can add their own fields on top of that
    """

    issuer_id_num = ansi_field_txt[0 : constants.ISSUER_ID_NUM_LEN]
    aamva_version_number = ansi_field_txt[constants.AAMVA_VERSION_NUMBER_START_OFFSET : constants.AAMVA_VERSION_NUMBER_END_OFFSET]
    jurisdiction_version_number = ansi_field_txt[constants.JURISDICTION_VERSION_NUMBER_START_OFFSET : constants.JURISDICTION_VERSION_NUMBER_END_OFFSET]
    number_of_entries = ansi_field_txt[constants.NUMBER_OF_ENTRIES_START_OFFSET : constants.NUMBER_OF_ENTRIES_END_OFFSET]
    subfile_1_type = ansi_field_txt[constants.SUBFILE_1_TYPE_START_OFFSET : constants.SUBFILE_1_TYPE_END_OFFSET]
    offset_1_field = ansi_field_txt[constants.OFFSET_1_FIELD_START_OFFSET : constants.OFFSET_1_FIELD_END_OFFSET]
    length_1_field = ansi_field_txt[constants.LENGTH_1_FIELD_START_OFFSET : constants.LENGTH_1_FIELD_END_OFFSET]
    subfile_2_type = ansi_field_txt[constants.SUBFILE_2_TYPE_START_OFFSET : constants.SUBFILE_2_TYPE_END_OFFSET]
    offset_2_field = ansi_field_txt[constants.OFFSET_2_FIELD_START_OFFSET : constants.OFFSET_2_FIELD_END_OFFSET]
    length_2_field = ansi_field_txt[constants.LENGTH_2_FIELD_START_OFFSET : constants.LENGTH_2_FIELD_END_OFFSET]



    return dict({"issuer_id_num": issuer_id_num, "aamva_version_num" : aamva_version_number, "jurisdiction_version_number" : jurisdiction_version_number, "number_of_entries" : number_of_entries, "subfile_1_type" : subfile_1_type, "offset_1_field" : offset_1_field, "length_1" : length_1_field, "subfile_2_type" : subfile_2_type, "offset_2_field": offset_2_field, "length_2": length_2_field})