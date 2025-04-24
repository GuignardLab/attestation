## Your name
PI_name = "Léo Guignard"

## Your role
role = "Chef d'équipe CenTuri \`{{a}} l'IBDM"
## It will come out as:
## Je soussigné <PI_name>, <role>, certifie que ...


## Keep the line breaks or the LaTeX file will no compile
address = """
	IBDM UMR 7288 CNRS / AMU,\\\\
	Case 907 - Parc Scientifique de Luminy 13288\\\\
	163 avenue de Luminy\\\\
	13288 MARSEILLE cedex 09
"""

## Path to a signature image.
## Leave it as an empty string if you don't want to put it
# signature_path = ""
signature_path = "/Users/leo.guignard/Production/Students/Paperwork/Intern-presence/signature.pdf"

## Path to a logo image.
## Leave it as an empty string if you don't want to put it
# logo_path = ""
logo_path = "/Users/leo.guignard/Production/Students/Paperwork/Intern-presence/logo-ibdm.png"

## Body of the email that will be sent along with the pdf
email_body = (
    """Bonjour!
Veuillez trouver attaché l'attestation de présence de {name:s}.

Bonne journée,
"""
    + PI_name
    + """

"""
)

template = (
    """
\\documentclass[a4paper, 10pt]{{letter}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}
\\usepackage[french]{{babel}}
\\usepackage{{datetime}}
\\usepackage{{graphicx}}

% Address of sender
\\address{{ """
    + (
        ("""\\includegraphics[scale=.5]{{""" + logo_path + """}}\\\\""")
        if logo_path
        else ""
    )
    + address
    + """}}
\\newcommand{{\\studentname}}{{{name:s}}}
\\newcommand{{\\lastday}}{{{day:d}}}
\\newcommand{{\\student}}{{\\'etudiant{end:s}}}

\\newdateformat{{monthyeardate}}{{\\monthname[\\THEMONTH] \\THEYEAR}}
%\\newcommand{{\\month}}{{Juin}}
%\\newcommand{{\\year}}{{2022}}
%\\newcommand{{\\year}}{{2022}}

\\begin{{document}}

% Name and address of receiver
\\begin{{letter}}{{}}
% Opening statement
\\opening{{Sujet: Attestation de présence de \\studentname}}

% Letter body
A Qui de Droit,\\\\
Je soussigné """
    + PI_name
    + """, """
    + role
    + """, certifie que
l'\\student~\\studentname~a effectu\\'{{e}} du 1 \\monthyeardate\\today~ au \\lastday~\\monthyeardate\\today~ son
stage au sein de notre \\'{{e}}quipe.\\\\
\\\\

% Closing statement
\\closing{{Cordialement,\\\\"""
    + (
        (
            """
\\fromsig{{\\includegraphics[scale=.07]{{"""
            + signature_path
            + """}}}} \\\\"""
        )
        if signature_path
        else ""
    )
    + """
\\fromname{{"""
    + PI_name
    + """}}}}

\\end{{letter}}
\\end{{document}}
"""
)
