DEPARTMENT = frozenset([
    'Section of', 'Section for', 'Division of', 'Department of', 'Departamento de',
    'Department for', 'Departments of', 'Departments for',
    'Faculty of', 'Unit ', 'Graduate School of', 'Research Unit',
    'Program in', 'Laboratorio', 'Laboratories',
    'Laboratory', 'Genomics Center', 'Haematological',
    'Environmental Engineering', 'Power Engineering', 'Biosystems Engineering',
    'Orthopaedic Department', 'Clinic for', 'Occupational Therapy Department',
    'Surgery Program'
])


INSTITUTE = frozenset([
    'college', 'university', 'universitat', 'universite',
    'unversiteit', 'universita', 'universidad', 'universiti', 'hospital', 'hopitaux de', 'unidade de',
    "ha'pital", 'istituti', 'istituto', 'institucio', 'institut', 'institutet', 'medical center', ' pharma',
    'riuniti', 'clinic', ' school of medicine', 'karolinska sjukhuset',
    'national institutes of health', 'cancer center', 'bioscience institute',
    'national institute for', 'national center for ', 'national centre for',
    'unilever research', 'national cardiovascular center',
    'centro operativo', 'animal research centre', 'nutrition research center',
    'national perinatal epidemiology unit', 'tanabe seiyaku', 'animal health trust',
    'marine biological laboratory', ' medical school', ' research laboratories',
    'baxter diagnostics', 'inserm', 'sylvius laboratory', 'broad institute', ' inra', '/inra',
    'health chemical laboratory', 'genecor, inc', 'infirmary',
    'national center for health', 'john innes centre', 'chru de la timone',
    'chu de bordeaux', 'ecole nationale ', 'cape technologies',
    'national chemical laboratory', ' national laboratory', 'department of research and development',
    'academy of sciences', 'centre chirurgical de la porte', 'international centre of ',
    'lawrence berkeley laboratory', 'albert einstein college', 'gedeon richter ltd',
    ' nih', 'ufrgs', 'national research centre', ' co.', ' ltd.', ' ltd', 'inc.', 'research limited',
    'clinic college of', 'center for', 'research center', 'research centre',
    'schon klinik', 'innovaderm research', 'novartis', 'aquarium', 'foundation',
    'permanente', 'healthcare system', 'national oncology institute',
    'global research and development', 'health service', 'national primate research center',
    'faculdade de ', ' urmc', ' pllc', ' pgimer', 'center for disease control',
    'london school of ', 'ggze', 'health service executive', 'council for scientific',
    'cnrs', 'eth zurich', 'johns hopkins', 'isconova', 'barts health', 'ceinge',
    'national jewish health', 'german institute', 'iqwig', 'federal joint committee'
    'nationale contre', 'cura villa maria', 'centre de psychologie', 'centro diagnostico',
    'international reference centre', 'complesso integrato', 'health care centre',
    'idiphim', 'cytogenetic laboratory', 'fondazione', 'facebook', 'google', 'association for',
    ' llc', 'national museum', 'national research council', 'rehabilitation center',
    'rehabilitation institute', 'oncology center', 'cancer centre', 'virginia tech',
    'ciberesp', 'department of food', 'rothamsted research', 'evangelisches',
    'ziekenhuizen', 'academy of ', 'chinese national ', 'pathology associates',
    'science magnet', 'ucla ', ' ucsd', 'uc berkeley', 'uc san diego', 'trial group',
    'acdi', 'specialty center', 'agemetra', 'national research institute', 'diabetes center',
    'rothamsted research', 'affichem', 'disease association', 'ministry of health',
    'incorporation', 'medical research council', 'develogen', 'innovation campus',
    'flemish government', "centre d'etudes", 'kaist', 'epfl', ' eth', 'ecole normale',
    'ecole polytechnique', 'mental health center', 'charite centrum', 'phc affairs',
    'afmc', 'cdsr', 'chu de ', 'harvard school', 'karnavati school', 'academic centre for',
    'school of public health', 'school of sport sciences', 'medical center', 'medical centre',
    'neocodex', 'umc utrecht', 'centers for disease', 'cardiac surgery center',
    'medical city', 'wisconsin department', "doctor's data", 'drug development office',
    'research unit', 'ecogen', 'international corporation', 'tourism agency',
    'naval research laboratory', 'infection research', 'health solutions',
    'us military', 'us department', 'human genome center', 'siemens', 'swiss institute',
    'usda', 'marine science center', 'u.s. geological', 'u.s. positive', 'u.s. Department',
    'botanical center', 'municipal centre', 'municipal health', 'research council',
    'national serology', 'national sexually', "d'aragona", 'metropolitan health',
    'rosa and company', 'laboratory of oncology', 'oncology r&d', 'assessment service',
    'cancer registry', 'technology agency', 'district health', 'irccs', 'pharmexa',
    'scientific service', 'limited company', 'health authority', 'biodiversity center',
    'national park', 'corporation', 'ucl ', 'escola nacional', 'va health system',
    'agri-food', 'agrotech', 'agroforestry', 'umr micalis', 'allan rosenfield',
    'allan wilson', 'allen institute', 'ameripath', 'biotechnologies', 'anaerobe systems',
    'nhs trust', 'danisco animal', 'dupont industrial', 'laboratory for'
])


EMAIL = frozenset([
    r'email:', r'e-mail:', r'[\w\.-]+@[\w\.-]+'
])


ZIP_CODE = frozenset([
    r'(\d{5})([-])?(\d{4})?', '(\d{3})([-])?(\d{4})?'
])


COUNTRY = frozenset([
    'Argentina', 'Armenia', 'Australia', 'Belgium',
    'Brazil', 'Croatia', 'Cyprus', 'Denmark',
    'Edinburge', 'Edinburgh', 'Egypt', 'England',
    'Finland', 'France', 'Germany', 'Greece',
    'Israel', 'Italy', 'Japan', 'Korea',
    'Kuwait', 'Lithuania', 'Netherlands', 'Nigeria',
    'Norway', 'Peru', 'Philippines', 'Russia',
    'Spain', 'Switzerland', 'Tanzania',
    'Turkey', 'U.K.', 'U.S.A', 'UK.', 'USA', 'Vietnam'
])


UNIVERSITY_ABBR = frozenset([
    'ucla', 'uc los angeles',
    'ucsd', 'us san diego',
    'caltech',
    'ccny',
    'carnegie mellon university', 'cmu',
    'georgia tech',
    'pennsylvania state university', 'penn state',
    'university of massachusetts amherst', 'umass',
    'city university of new york', ' cuny',
    'havard university school of', 'harvard school of'
])


STREET = frozenset([
    'Street', 'Road', 'Blvd', 'University Ave'
])
