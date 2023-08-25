## Your name
PI_name = "FirstName LastName"

## Your role
role = "Chef d'équipe CenTuri au LIS"
## It will come out as:
## Je soussigné <PI_name>, <role>, certifie que ...


## Keep the line breaks or the LaTeX file will no compile
address = """
	LIS UMR 7020 CNRS / AMU / UTLN,\\\\
	Campus universitaire de Luminy\\\\
	Bat. TPR2, 5ème étage, Bloc 1\\\\
	163 avenue de Luminy\\\\
	13288 MARSEILLE cedex 09 	   
"""

## Path to a signature image.
## Leave it as an empty string if you don't want to put it
# signature_path = ""
signature_path = (
    "/Users/leo.guignard/Production/Students/Intern-presence/signature.pdf"
)

## Path to a logo image.
## Leave it as an empty string if you don't want to put it
# logo_path = ""
logo_path = "/Users/leo.guignard/Production/Students/Intern-presence/logo_LIS_color.png"


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
        ("""\\includegraphics[scale=.1]{{""" + logo_path + """}}\\\\""")
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
l'\\student~\\studentname~a travaillé sur son projet en présentiel ou en
télétravail du 1 \\monthyeardate\\today~ jusqu'au \\lastday~\\monthyeardate\\today~.\\\\
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
