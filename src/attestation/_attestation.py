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
    name: str,
    recipients: list,
    genre: str,
    day: int = None,
    smtp_server: str = None,
    smtp_port: int = 587,
    smtp_username: str = None,
    send: bool = True,
    keep: bool = False,
    pdf_file: str = "",
) -> None:
    """
    Create and send an "attestation de présence".

    Args:
        name (str): the first and last name of the intern
        reciptients (list[str]): list of email addresses
        genre (["m", "f"]): wheter to put an "e" at the end of etudiant(e)
            "m" for male, "f" for female
        day (int): last day of the current month the intern is working
            if None then it is the last day of the current month
        smtp_server (str): address of the smtp mail to send the email (default: None)
            if kept to None the email will not be sent
        smpt_port (int): port from which to send the email (default: 587)
        smtp_username (str): username for the smtp address (default: None)
            if kept to None the email will not be sent
        send (bool): whether to send or not the email (default True)
        keep (bool): whether to keep or not the pdf (default False)
        pdf_file (str): path to the saved pdf file
            (default: "". If kept to "" it will be save in the current
            directory as `attestation firstname lastname.pdf`
    """
    if not day:
        current_date = datetime.date.today()
        year = current_date.year
        month = current_date.month
        day = calendar.monthrange(year, month)[1]
    if send:
        print(
            f"Please input the {smtp_server} account password for the user {smtp_username}."
        )
        smtp_password = getpass("Password: ")
    temp_dir = Path(tempfile.mkdtemp())
    tex_file = template.format(name=name, day=day, end=genre)
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
        stdout=subprocess.DEVNULL,
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
        stdout=subprocess.DEVNULL,
    )

    if send:
        sender = f"{smtp_username}@{smtp_server.removeprefix('smtp.')}"
        subject = f"Attestation présence {name}"
        body = (
            "Bonjour!\nVeuillez trouver attaché l'attestation"
            f" de présence de {name}.\nBonne journée,\nLéo Guignard\n\n"
        )

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
            smtp_connection.sendmail(
                sender, recipients + [sender], msg.as_string()
            )
            smtp_connection.quit()
        except Exception as e:
            print(e)
    if keep or not send:
        if not pdf_file:
            pdf_file = f"attestation {name}.pdf"
        created = f"attestation {name}.pdf"
        (temp_dir / created).rename(pdf_file)
    shutil.rmtree(temp_dir)


def script_run():
    description = """Building and sending an "attestation de présence" """
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
        help="email where to send the letter "
        "(default jasmina.STAMENOVA@univ-amu.fr & marlene.SALOM@univ-amu.fr)",
    )
    parser.add_argument(
        "-ld",
        "--last-day",
        default=None,
        type=int,
        help="Last day of the stay",
    )
    parser.add_argument(
        "-ns",
        "--no-send",
        action="store_true",
        help="Add this flag to not send the email",
    )
    parser.add_argument(
        "-k",
        "--keep-pdf",
        action="store_true",
        help="Add this flag to keep the generated pdf",
    )
    parser.add_argument(
        "-pdf",
        "--pdf-file",
        default="",
        type=str,
        help="Path and name of the generate pdf file if kept (ignore if the flag kept-pdf is not present)",
    )

    args = parser.parse_args()
    recipients = args.recipients
    if len(args.name) == 0:
        first_name = input("Please enter the first name: ")
        last_name = input("Please enter the last name: ")
        name = first_name + " " + last_name
    else:
        name = " ".join(args.name)
    genre = "" if args.genre == "m" else "e"
    keep = args.keep_pdf
    pdf_file = args.pdf_file
    send = not args.no_send
    print(send, keep, pdf_file)

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
        name,
        recipients,
        genre,
        day,
        smtp_server,
        smtp_port,
        smtp_username,
        send,
        keep,
        pdf_file,
    )
