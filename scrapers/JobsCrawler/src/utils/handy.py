import smtplib
import sqlite3
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

""" LOAD THE ENVIRONMENT VARIABLES """

async def link_exists_in_db(link: str, cur: sqlite3.Cursor, test: bool = False) -> bool:
	"""
	Check if a link already exists in the database.

	Args:
		link: The job link to check
		cur: SQLite cursor
		test: Whether to check in test table (default: False)

	Returns:
		True if link exists, False otherwise
	"""
	table = "test" if test else "main_jobs"

	# SQLite uses ? for parameter placeholders instead of %s
	query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE link=?)"
	cur.execute(query, (link,))

	result = cur.fetchone()

	return bool(result[0]) if result else False


""" OTHER UTILS """


def send_email(log_file_path):
	fromaddr = "maddy@rolehounds.com"
	toaddr = "juancarlosrg1999@gmail.com"
	msg = MIMEMultipart()

	msg["From"] = fromaddr
	msg["To"] = toaddr
	msg["Subject"] = "Finished crawling & embedding! logs attached"

	with open(log_file_path, "rb") as f:
		part = MIMEBase("application", "octet-stream")
		part.set_payload(f.read())
		encoders.encode_base64(part)
		part.add_header("Content-Disposition", 'attachment; filename="log.txt"')
		msg.attach(part)

	server = smtplib.SMTP("smtp-mail.outlook.com", 587)
	server.starttls()
	server.login(fromaddr, "buttercuP339!")
	server.send_message(msg)
	server.quit()

