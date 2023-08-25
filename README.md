# attestation

Automatically send your attestation letters.

----------------------------------

## Installation

To install, clone this repository:

```shell
git pull https://github.com/GuignardLab/attestation.git
```

and then run:

```shell
cd attestation
pip install -e .
```

**Warning: You have to have install `pdflatex` as a command line**

## Usage

After installation you need to modify the first lines of the file `src/attestation/_template.py`.
You will want to modify `PI_name`, `role`, `address`, and you might want to inform `signature_path` and `logo_path` as **absolute** paths.

Setting `signature_path` or `logo_path` to the empty string will ignore them.

Once you have modified these variables you can ran the script as follow:

```shell
send-attestation --name Name Surname
```

with `Name` and `Surname` being the ones of the student you want to send the attestation for.

By default, the email is sent to the two concerned HR people (Marlène & Jasmina).
You can change that with the following command line:

```shell
send-attestation --name student_name student_surname --recipients LC1@institute.com LC2@institute.com
```

Few other parameters can be changed, running 

```shell
send-attestation --help
```

which will give you the following:

```text
usage: send-attestation [-h] [-n NAME [NAME ...]] [-g {m,f}] [-t SMTP] [-p PORT] [-u USERNAME]
                        [-r RECIPIENTS [RECIPIENTS ...]] [-ld LAST_DAY] [-ns] [-k] [-pdf PDF_FILE]

Building and sending an "attestation de présence"

optional arguments:
  -h, --help            show this help message and exit
  -n NAME [NAME ...], --name NAME [NAME ...]
  -g {m,f}, --genre {m,f}
  -t SMTP, --smtp SMTP  smtp (default LIS)
  -p PORT, --port PORT  port for email (default 587)
  -u USERNAME, --username USERNAME
                        account for email (default leo.guignard)
  -r RECIPIENTS [RECIPIENTS ...], --recipients RECIPIENTS [RECIPIENTS ...]
                        email where to send the letter (default jasmina.STAMENOVA@univ-amu.fr & marlene.SALOM@univ-amu.fr)
  -ld LAST_DAY, --last-day LAST_DAY
                        Last day of the stay
  -ns, --no-send        Add this flag to not send the email
  -k, --keep-pdf        Add this flag to keep the generated pdf
  -pdf PDF_FILE, --pdf-file PDF_FILE
                        Path and name of the generate pdf file if kept (ignore if the flag kept-pdf is not present)
```

should inform you about the possibilities.

The whole script can also be ran programatically the following way:

```python
from attestation import send_attestation

send_attestation(
    name, # Name of the student as a string
    recipients, # List of email addresses
    genre, # Wheter you need "étudiant" or "étudiante"
    day, # Last day of the stay of the student if it is not the end of the month
    smtp_server, # Smtp server to send (optional, default LIS)
    smtp_port, # Smtp port to send (optional)
    smtp_username, # Username for the smtp server
    send, # Bool whether to send or not the email
    keep, # bool whether to keep or not the generated pdf
    pdf_file, # where to save the pdf if saved
)
```

Typing `send_attestation?` should also give you a bit more information.

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"attestation" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

----------------------------------

This library was generated using [Cookiecutter] and a custom made template based on [@napari]'s [cookiecutter-napari-plugin] template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin
[tox]: https://tox.readthedocs.io/en/latest/

[file an issue]: https://github.com/GuignardLab/attestation/issues
