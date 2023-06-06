def create_cpe(vendor: str, product: str, version: str, part:str = None):
	cpe = "cpe:2.3:"
	if part in ["a", "o", "h"]:
		cpe += part
	else:
		#cpe += "a:"
		cpe += "o:"
	cpe = cpe + vendor + ":"
	cpe = cpe + product + ":"
	cpe = cpe + version + ":"
	cpe += "*:*:*:*:*:*:*"
	return cpe


PORT_MAPPING = {
	"http": 80,
	"https": 443,
	"ftp": 21,
	"ssh": 22,
	"telnet": 23,
	"smtp": 25,
	"dns": 53,
	"kerberos": 88,
	"ldap": 389,
	"rpc": 530,
	"rtsp": 554  
}