NUMERATION_GLOBULAIRE = 1
HEMOPARASITES = 2
HEMOGLOBINOPATHIES = 3

EXAMEN_TYPE_CHOICES = (
        ('Examen Numeration Globulaire', (
        ('NFS+PL', 'NFS+PL'),
        ('RETICULOCYTES', 'RETICULOCYTES'),
        ('VS', 'VS'),
        ('CD4', 'CD4'),
        ('CELL DE HAR','CELL DE HAR')
        )
        ),
        ('Examen Hemoparsites', (
        ('GOUTTE EPAISSE', 'GOUTTE EPAISSE'),
        ('TDR', 'TDR'),
        ('MICRO FIL SANG', 'MICRO FIL SANG'),
        ('SNIP TEST', 'SNIP TEST'),
        )
        ),
        ('Examen Hemoglobinopathies', (
        ('ELECTROPHORESE', 'ELECTROPHORESE'),
        )
        ),
        )
EXAMENS_DICT_CHOICES = {
            "Examen Numeration Globulaire": {
            "NFS+PL":"NFS+PL",
            "RETICULOCYTES":"RETICULOCYTES",
            "VS":"VS",
            "CD4":"CD4",
            "CELL DE HAR":"CELL DE HAR",
            }
            ,
            "Examen Hemoparsites": {
            "GOUTTE EPAISSE":"GOUTTE EPAISSE",
            "TDR":"TDR",
            "MICRO FIL SANG":"MICRO FIL SANG",
            "SNIP TEST":"SNIP TEST",
            }
            ,
            "Examen Hemoglobinopathies":
            {"ELECTROPHORESE":"ELECTROPHORESE",}
            }