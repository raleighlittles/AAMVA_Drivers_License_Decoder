

COMPLIANCE_INDICATOR = "@"
FILE_TYPE = "ANSI"

ISSUER_ID_NUM_LEN = 6

AAMVA_VERSION_NUMBER_LEN = 2
AAMVA_VERSION_NUMBER_START_OFFSET = 6
AAMVA_VERSION_NUMBER_END_OFFSET = AAMVA_VERSION_NUMBER_START_OFFSET + AAMVA_VERSION_NUMBER_LEN

JURISDICTION_VERSION_NUMBER_LEN = 2
JURISDICTION_VERSION_NUMBER_START_OFFSET = AAMVA_VERSION_NUMBER_END_OFFSET
JURISDICTION_VERSION_NUMBER_END_OFFSET = JURISDICTION_VERSION_NUMBER_START_OFFSET + JURISDICTION_VERSION_NUMBER_LEN

NUMBER_OF_ENTRIES_LEN = 2
NUMBER_OF_ENTRIES_START_OFFSET = JURISDICTION_VERSION_NUMBER_END_OFFSET
NUMBER_OF_ENTRIES_END_OFFSET = NUMBER_OF_ENTRIES_START_OFFSET + NUMBER_OF_ENTRIES_LEN

SUBFILE_1_TYPE_LEN = 2
SUBFILE_1_TYPE_START_OFFSET = NUMBER_OF_ENTRIES_END_OFFSET
SUBFILE_1_TYPE_END_OFFSET = SUBFILE_1_TYPE_START_OFFSET + SUBFILE_1_TYPE_LEN

OFFSET_1_FIELD_LEN = 4
OFFSET_1_FIELD_START_OFFSET = SUBFILE_1_TYPE_END_OFFSET
OFFSET_1_FIELD_END_OFFSET = OFFSET_1_FIELD_START_OFFSET + OFFSET_1_FIELD_LEN

LENGTH_1_FIELD_LEN = 4
LENGTH_1_FIELD_START_OFFSET = OFFSET_1_FIELD_END_OFFSET
LENGTH_1_FIELD_END_OFFSET = LENGTH_1_FIELD_START_OFFSET + LENGTH_1_FIELD_LEN

SUBFILE_2_TYPE_LEN = 2
SUBFILE_2_TYPE_START_OFFSET = LENGTH_1_FIELD_END_OFFSET
SUBFILE_2_TYPE_END_OFFSET = SUBFILE_2_TYPE_START_OFFSET + SUBFILE_2_TYPE_LEN

OFFSET_2_FIELD_LEN = 4
OFFSET_2_FIELD_START_OFFSET = SUBFILE_2_TYPE_END_OFFSET
OFFSET_2_FIELD_END_OFFSET = OFFSET_2_FIELD_START_OFFSET + OFFSET_2_FIELD_LEN

LENGTH_2_FIELD_LEN = 4
LENGTH_2_FIELD_START_OFFSET = OFFSET_2_FIELD_END_OFFSET
LENGTH_2_FIELD_END_OFFSET = LENGTH_2_FIELD_START_OFFSET + LENGTH_2_FIELD_LEN