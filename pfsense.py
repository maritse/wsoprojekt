from config import PFSENSE_ADDRESS
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

PfsenseFauxapi = PfsenseFauxapi(PFSENSE_ADDRESS, '<fauxapi-key>', '<fauxapi-secret>')


print("test")