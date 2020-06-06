# import taxa
python manage.py import_taxa explorer/data/imports/taxonomy_parsed.csv
# import proteins
python manage.py import_protein explorer/data/imports/initial_protein.csv
# import alignments
python manage.py import_alignment explorer/data/imports/initial_alignment.csv
# import sequence records
python manage.py import_sequencerecord explorer/data/imports/spike_sequence_records.csv
# import sequence alignments
python manage.py import_sequence explorer/data/imports/spike_sequence_alignment_20200505.csv
# import epitope alignments
python manage.py import_epitope explorer/data/imports/aligned_epitopes.csv
# import epitope experiments
python manage.py import_epitopeexperiment explorer/data/imports/epitopes_experiments.csv
# import position nomenclature
python manage.py import_nomenclature explorer/data/imports/HKU-N2_nomenclature.csv
# import structures
python manage.py import_structure explorer/data/structure/imports/structureChains.csv
# import structure sequences
python manage.py import_structuresequence explorer/data/structure/imports/structureSequences.csv
# import structure residues and atoms
python manage.py import_structureatom explorer/data/structure/imports/structureAtoms.csv
