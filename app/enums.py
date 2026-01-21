from enum import Enum

class LeadStatus(str, Enum):
    NEW = "NEW"
    HOT = "HOT"
    WARM = "WARM"
    COLD = "COLD"
