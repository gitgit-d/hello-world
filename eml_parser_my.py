import datetime
import json
import eml_parser
import os

# 遍历文件夹
def walkFile(filepath):
	maillist = []
	for root, dirs, files in os.walk(filepath):
		for f in files:
			maillist.append(os.path.join(root, f))
	return maillist
			
def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

filepath = "./mails"
maillist = walkFile(filepath)

f_out = open("edges.csv","a")
f_out.write("source,target\n")

for mail in maillist:
	print(mail)
	with open(mail, 'rb') as fhdl:
		raw_email = fhdl.read()
	parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

	body = json.loads(json.dumps(parsed_eml, default=json_serial))
	header = body["header"]
	sender_info = header["from"]
	receiver_info = header["to"]
	for item in receiver_info:
		writeStr = sender_info+","+item+"\n"
		f_out.write(writeStr)
		
	try:	
		cc_info = header["Cc"]
		for item in cc_info:
			writeStr = sender_info+","+item+"\n"
			f_out.write(writeStr)
	except:
		pass
f_out.close()
