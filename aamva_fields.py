import datetime
import pdb
import ansi_d20

EMPTY_KEY = "NONE"

# ----- HELPER METHODS -----
def parse_date(mmddyyyy_date) -> datetime.datetime:

    month, day, year = mmddyyyy_date[0:2], mmddyyyy_date[2:4], mmddyyyy_date[4:8]
    return datetime.datetime(year=int(year), month=int(month), day=int(day))


def parse_truncation(truncation_flag) -> str:
    if truncation_flag == "T":
        return "Truncated"

    elif truncation_flag == "N":
        return "Not truncated"

    elif truncation_flag == "U":
        return "Unknown if truncated"

    else:
        return ""

# --------------------


class DataElement:
    code = ""
    min_length = 0
    max_length = 0
    key_name = ""
    value = ""

    def get_regex(self):
        return fr"{self.code}(.{{{self.min_length},{self.max_length}}})"

    def parse(self):
        return self.value


class JurisdictionSpecificVehicleClass(DataElement):

    def __init__(self):
        self.code = "DCA"
        self.key_name = "Jurisdiction-specific vehicle class"
        self.min_length = 1
        self.max_length = 6

    def parse(self):

        # TODO: How does this work for commercial licenses?
        if self.value == "A":
            return "Travel trailer/fifth wheel (noncommercial)"

        elif self.value == "B":
            return "Housecar/motorhome (noncommercial)"

        elif self.value == "C":
            return "[CA-only] Standard vehicle"

        elif self.value == "D":
            return "[Other states besides CA] Standard vehicle"

        elif self.value == "M1":
            return "Motorcycle license"

        elif self.value == "M2":
            return "Limited motorcycle license (moped/scooter only)"

        else:
            raise ValueError(
                f"'{self.value}' is not a recognized license type")


class JurisdictionSpecificRestrictionCodes(DataElement):

    def __init__(self):
        self.code = "DCB"
        self.key_name = "Jurisdiction-specific restriction codes"
        self.min_length = 4
        self.max_length = 12


class JurisdictionSpecificEndorsementCodes(DataElement):

    def __init__(self):
        self.code = "DCD"
        self.key_name = "Jurisdiction-specific endorsement codes"
        self.min_length = 4
        self.max_length = 5


class DocumentExpirationDate(DataElement):

    def __init__(self):
        self.code = "DBA"
        self.key_name = "Document Expiration Date"
        self.min_length = 8
        self.max_length = self.min_length

    def parse(self):

        def get_expired_or_expiration_string(timestamp, current):

            difference_timestamp = timestamp - current

            if (timestamp > current):
                return f"Expires in {difference_timestamp.days} days"

            elif (current > timestamp):
                return f"Expired {abs(difference_timestamp.days)} days ago"

            else:
                raise ValueError(
                    "Timestamp of expiration matches current timestamp -- verify data was correctly parsed")

        # month, day, year = self.value[0:2], self.value[2:4], self.value[4:8]

        # timestamp = datetime.datetime(year=int(year), month=int(month), day=int(day))
        timestamp = parse_date(self.value)
        now = datetime.datetime.now()

        return f"{timestamp.isoformat()} | {get_expired_or_expiration_string(timestamp, now)}"


class CustomerFamilyName(DataElement):

    def __init__(self):
        self.code = "DCS"
        self.key_name = "Customer Family Name"
        self.min_length = 3
        self.max_length = 40


class CustomerFirstName(DataElement):

    def __init__(self):
        self.code = "DAC"
        self.key_name = "Customer First Name"
        self.min_length = 3
        self.max_length = 40


class CustomerMiddleName(DataElement):

    def __init__(self):
        self.code = "DAD"
        self.key_name = "Customer Middle Name(s)"
        self.min_length = 3
        self.max_length = 40

    def parse(self):

        if self.value == EMPTY_KEY:
            return ""

        else:
            return self.value


class DocumentIssueDate(DataElement):

    def __init__(self):
        self.code = "DBD"
        self.key_name = "Document Issue Date"
        self.min_length = 8
        self.max_length = self.min_length

    def parse(self):

        # month, day, year = self.value[0:2], self.value[2:4], self.value[4:8]
        # timestamp = datetime.datetime(year=int(year), month=int(month), day=int(day))
        timestamp = parse_date(self.value)
        return timestamp.isoformat()


class DateOfBirth(DataElement):

    def __init__(self):
        self.code = "DBB"
        self.key_name = "Date of Birth"
        self.min_length = 8
        self.max_length = self.min_length

    def parse(self):

        # month, day, year = self.value[0:2], self.value[2:4], self.value[4:8]
        # timestamp = datetime.datetime(year=int(year), month=int(month), day=int(day))
        timestamp = parse_date(self.value)
        now = datetime.datetime.now()

        return f"{timestamp.isoformat()} | Approx age: {now.year - timestamp.year}"


class PhysicalDescriptionSex(DataElement):

    def __init__(self):

        self.code = "DBC"
        self.key_name = "Physical Description - Sex"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):

        if str(self.value) == "1":
            return "Male"

        elif str(self.value) == "2":
            return "Female"

        elif str(self.value) == "9":
            return "Not specified"

        else:
            raise ValueError(f"'{self.value}' is not a valid value")


class PhysicalDescriptionEyeColor(DataElement):

    def __init__(self):

        self.code = "DAY"
        self.key_name = "Physical Description - Eye Color"
        self.min_length = 3
        self.max_length = self.min_length

    def parse(self):
        return ansi_d20.colors.get(self.value)


class PhysicalDescriptionHeight(DataElement):

    def __init__(self):

        self.code = "DAU"
        self.key_name = "Physical Description - Height"
        self.min_length = 6
        self.max_length = self.min_length

    def parse(self):
        """
        This value can be in both centimeters or inches. e.g.
        '073 IN' or '181 CM'
        Start first by separating the units from the value themselves
        """
        value, units = self.value.split(" ")

        if units.lower() == "in":
            # Convert the # of inches to a height in feet and inches
            # eg 73 inches is 6'1
            inches = int(value)
            inches_to_feet = 12
            return f"{inches // inches_to_feet}'{inches % inches_to_feet} ({inches} inches)"

        elif units.lower() == "cm":
            # metric, no conversion needed :)
            return f"{int(value)} centimeters"


class AddressStreet1(DataElement):

    def __init__(self):
        self.code = "DAG"
        self.key_name = "Address - Street 1"
        self.min_length = 8
        self.max_length = 35


class AddressCity(DataElement):

    def __init__(self):

        self.code = "DAI"
        self.key_name = "Address - City"
        self.min_length = 4
        self.max_length = 20


class AddressJurisdictionCode(DataElement):

    def __init__(self):

        self.code = "DAJ"
        self.key_name = "Address - Jurisdiction Code"
        self.min_length = 2
        self.max_length = 2


class AddressPostalCode(DataElement):

    def __init__(self):

        self.code = "DAK"
        self.key_name = "Address - Postal Code"
        self.min_length = 5
        self.max_length = 11


class CustomerIDNumber(DataElement):

    def __init__(self):

        self.code = "DAQ"
        self.key_name = "Customer ID Number"
        self.min_length = 8
        self.max_length = self.min_length


class DocumentDiscriminator(DataElement):

    def __init__(self):

        self.code = "DCF"
        self.key_name = "Document Discriminator"
        self.min_length = 25
        self.max_length = self.min_length


class CountryIdentification(DataElement):

    def __init__(self):

        self.code = "DCG"
        self.key_name = "Country Identification"
        self.min_length = 3
        self.max_length = self.min_length


class FamilyNameTruncation(DataElement):

    def __init__(self):

        self.code = "DDE"
        self.key_name = "Family name truncation"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):
        return parse_truncation(self.value)


class FirstNameTruncation(DataElement):

    def __init__(self):

        self.code = "DDF"
        self.key_name = "First name truncation"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):
        return parse_truncation(self.value)


class MiddleNameTruncation(DataElement):

    def __init__(self):

        self.code = "DDG"
        self.key_name = "Middle name truncation"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):
        return parse_truncation(self.value)


### OPTIONAL ELEMENTS ###

class AddressStreet2(DataElement):

    def __init__(self):

        self.code = "DAH"
        self.min_length = 2
        self.max_length = self.min_length
        self.key_name = "Address - Street 2"


class HairColor(DataElement):

    def __init__(self):

        self.code = "DAZ"
        self.key_name = "Hair color"
        self.min_length = 3
        self.max_length = 12

    def parse(self):
        return ansi_d20.colors.get(self.value)


class PlaceOfBirth(DataElement):

    def __init__(self):

        self.code = "DCI"
        self.key_name = "Place of birth"
        self.min_length = 5
        self.max_length = 33


class AuditInformation(DataElement):

    def __init__(self):

        self.code = "DCJ"
        self.key_name = "Audit Information"
        self.min_length = 3
        self.max_length = 25


class InventoryControlNumber(DataElement):

    def __init__(self):
        self.code = "DCK"
        self.key_name = "Inventory control number"
        self.min_length = 10
        self.max_length = 25


class AliasFamilyName(DataElement):

    def __init__(self):
        self.code = "DBN"
        self.key_name = "Alias / AKA Family Name"
        self.min_length = 2
        self.max_length = 10


class AliasGivenName(DataElement):

    def __init__(self):
        self.code = "DBG"
        self.key_name = "Alias / AKA Given Name"
        self.min_length = 2
        self.max_length = 15


class AliasSuffixName(DataElement):

    def __init__(self):

        self.code = "DBS"
        self.key_name = "Alias / AKA Suffix Name"
        self.min_length = 1
        self.max_length = 5


class NameSuffix(DataElement):

    def __init__(self):

        self.code = "DCU"
        self.key_name = "Name Suffix"
        self.min_length = 1
        self.max_length = 5


class PhysicalDescriptionWeightRange(DataElement):

    def __init__(self):

        self.code = "DCE"
        self.key_name = "Physical Description - Weight Range"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):

        weight_ranges = dict({'0': "up to 31 kg (up to 70 lbs)", '1': "32 - 45 kg (71 - 100 lbs)", '2': "46 - 59 kg (101 – 130 lbs)", '3': "60 - 70 kg (131 – 160 lbs)", '4': "71 - 86 kg (161 – 190 lbs) ",
                             '5': "87 - 100 kg (191 – 220 lbs) ", '6': "101 - 113 kg (221 – 250 lbs) ", '7': "114 - 127 kg (251 – 280 lbs)", '8': " 128 – 145 kg (281 – 320 lbs)", '9': "146+ kg (321+ lbs)"})

        return weight_ranges.get(str(self.value))


class RaceEthnicity(DataElement):

    def __init__(self):

        self.code = "DCL"
        self.key_name = "Race / ethnicity"
        self.min_length = 3
        self.max_length = self.min_length

    def parse(self):
        return ansi_d20.races_and_ethnicities.get(self.value)


class StandardVehicleClassification(DataElement):

    def __init__(self):

        self.code = "DCM"
        self.key_name = "Standard vehicle classification"
        self.min_length = 4
        self.max_length = self.min_length


class StandardEndorsementCode(DataElement):

    def __init__(self):

        self.code = "DCN"
        self.key_name = "Standard endorsement code"
        self.min_length = 5
        self.max_length = self.min_length


class StandardRestrictionCode(DataElement):

    def __init__(self):

        self.code = "DCO"
        self.key_name = "Standard restriction code"
        self.min_length = 10
        self.max_length = 12


class JurisdictionSpecificVehicleClassificationDescription(DataElement):

    def __init__(self):

        self.code = "DCP"
        self.key_name = "Jurisdiction-specific vehicle classification description"
        self.min_length = 10
        self.max_length = 50


class JurisdictionSpecificEndorsementCodeDescription(DataElement):

    def __init__(self):

        self.code = "DCQ"
        self.key_name = "Jurisdiction-specific endorsement code description"
        self.min_length = 10
        self.max_length = 50


class JurisdictionSpecificRestrictionCodeDescription(DataElement):

    def __init__(self):

        self.code = "DCR"
        self.key_name = "Jurisdiction-specific restriction code description"
        self.min_length = 10
        self.max_length = 50


class ComplianceType(DataElement):

    def __init__(self):

        self.code = "DDA"
        self.key_name = "Compliance Type"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):

        if self.value == "F":
            return "Compliant ✅"

        elif self.value == "N":
            return "Non-compliant"

        else:
            raise ValueError("Can't determine compliance type")


class CardRevisionDate(DataElement):

    def __init__(self):

        self.code = "DDB"
        self.key_name = "Card Revision Date"
        self.min_length = 8
        self.max_length = self.min_length

    def parse(self):
        return parse_date(self.value).isoformat()


class HAZMAT_Endorsement_Expiration_Date(DataElement):

    def __init__(self):

        self.code = "DDC"
        self.key_name = "HAZMAT Endorsement Expiration Date"
        self.min_length = 8
        self.max_length = self.min_length

    def parse(self):

        return parse_date(self.value).isoformat()


class LimitedDurationDocumentIndicator(DataElement):

    def __init__(self):

        self.code = "DDD"
        self.key_name = "Limited Duration Document Indicator"
        self.min_length = 1
        self.max_length = self.min_length


class WeightPounds(DataElement):

    def __init__(self):
        self.code = "DAW"
        self.key_name = "Weight (pounds)"
        self.min_length = 3
        self.max_length = self.min_length


class WeightKilograms(DataElement):

    def __init__(self):
        self.code = "DAX"
        self.key_name = "Weight (kilograms)"
        self.min_length = 3
        self.max_length = 3


class Under18Until(DataElement):

    def __init__(self):
        self.code = "DDH"
        self.key_name = "Under 18 Until"
        self.min_length = 8
        self.max_length = self.min_length


class Under19Until(DataElement):

    def __init__(self):
        self.code = "DDI"
        self.key_name = "Under 19 Until"
        self.min_length = 8
        self.max_length = self.min_length


class Under21Until(DataElement):

    def __init__(self):
        self.code = "DDJ"
        self.key_name = "Under 21 Until"
        self.min_length = 8
        self.max_length = self.min_length


class OrganDonorIndicator(DataElement):

    def __init__(self):
        self.code = "DDK"
        self.key_name = "Organ Donor Indicator"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):
        return "Organ Donor" if self.value == "1" else "Not an organ donor"


class VeteranIndicator(DataElement):

    def __init__(self):
        self.code = "DDL"
        self.key_name = "Veteran Indicator"
        self.min_length = 1
        self.max_length = self.min_length

    def parse(self):
        return "Veteran" if self.value == "1" else "Not a veteran"
