"""
Implementation of the AAMVA ANSI D20 codes.
"""

# Some drivers licenses commonly use "BRN" for 'Brown' even though officially that's not one of the official supported designations.
colors = {"BLK" : "Black", "BLU": "Blue", "BRO": "Brown", "DIC": "Dichromatic", "GRY": "Gray", "GRN": "Green", "HAZ": "Hazel", "MAR": "Maroon", "PNK": "Pink", "UNK": "Unknown"}

# See Appendix 9.8 Driver Race and Ethnicity (page 50)
races_and_ethnicities = {"AI": "Alaskan or American Indian", "AP": "Asian or Pacific Islander", "BK": "Black", 'H': "Hispanic Origin", 'O': "Non-hispanic", 'U': "Unknown", 'W': "White"}