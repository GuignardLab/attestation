import argparse
from pathlib import Path
import smtplib
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import subprocess
import tempfile
import shutil
from ._template import template
import datetime
import calendar


def send_attestation(
    name, recipients, end, day, smtp_server, smtp_port, smtp_username
):
    print(
        f"Please input the {smtp_server} account password for the user {smtp_username}."
    )
    smtp_password = getpass("Password: ")
    temp_dir = Path(tempfile.mkdtemp())
    tex_file = template.format(name=name, day=day, end=end)
    with open(temp_dir / "tmp.tex", "w") as f:
        f.write(tex_file)
    subprocess.run(
        [
            "pdflatex",
            "-output-directory",
            temp_dir,
            "-jobname",
            f"attestation {name}",
            "tmp.tex",
        ],
        # stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "pdflatex",
            "-output-directory",
            temp_dir,
            "-jobname",
            f"attestation {name}",
            "tmp.tex",
        ],
        # stdout=subprocess.DEVNULL,
    )

    sender = f"{smtp_username}@{smtp_server.removeprefix('smtp.')}"
    subject = f"Attestation présence {name}"
    body = ( "Bonjour!\nVeuillez trouver attaché l'attestation"
            f" de présence de {name}.\nBonne journée,\nLéo Guignard\n\n")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(
        recipients
    )  # Join recipient emails with a comma and space
    msg["Subject"] = subject
    msg["Bcc"] = sender

    # Attach the body of the email
    msg.attach(MIMEText(body, "plain"))

    # Attach the PDF file
    pdf_filename = temp_dir / f"attestation {name}.pdf"
    with open(pdf_filename, "rb") as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition", f"attachment; filename={pdf_filename}"
        )
        msg.attach(pdf_attachment)

    try:
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()  # enable TLS encryption
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(sender, recipients + [sender], msg.as_string())
        smtp_connection.quit()
    except Exception as e:
        print(e)
    shutil.rmtree(temp_dir)


def script_run():
    description = """Sending """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-n", "--name", nargs="+", default=[], type=str)
    parser.add_argument(
        "-g", "--genre", choices=["m", "f"], nargs=1, default="m"
    )
    parser.add_argument(
        "-t",
        "--smtp",
        default="smtp.lis-lab.fr",
        type=str,
        help="smtp (default LIS)",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=587,
        type=int,
        help="port for email (default 587)",
    )
    parser.add_argument(
        "-u",
        "--username",
        default="leo.guignard",
        type=str,
        help="account for email (default leo.guignard)",
    )
    parser.add_argument(
        "-r",
        "--recipients",
        default=["jasmina.STAMENOVA@univ-amu.fr", "marlene.SALOM@univ-amu.fr"],
        nargs="+",
        type=str,
        help="email where to send the letter"
        "(default jasmina.STAMENOVA@univ-amu.fr & marlene.SALOM@univ-amu.fr",
    )
    parser.add_argument(
        "-ld",
        "--last-day",
        default=None,
        type=int,
        help="Last day of the stay",
    )

    args = parser.parse_args()
    recipients = args.recipients
    if len(args.name) == 0:
        first_name = input("Please enter the first name: ")
        last_name = input("Please enter the last name: ")
        name = first_name + " " + last_name
    else:
        name = " ".join(args.name)
    end = "" if args.genre == "m" else "e"

    # Get the current year and month
    if args.last_day:
        day = args.last_day
    else:
        current_date = datetime.date.today()
        year = current_date.year
        month = current_date.month
        day = calendar.monthrange(year, month)[1]
    smtp_server = args.smtp
    smtp_port = args.port
    smtp_username = args.username
    send_attestation(
        name, recipients, end, day, smtp_server, smtp_port, smtp_username
    )
