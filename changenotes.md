# CoronaWhy Explorer Change Notes

## June 23, 2020. Nic.
Added pre-calculation of residue/atom positions in aligned structure-chain sequences at the data entry point. New property is called `resaln`, and specifies the position of the residue an atom belongs to relative to a specified alignment. This links atoms to sequence alignment positions so that atom-derived information can be displayed in the alignment framework of the explorer panels.

To activate this change you need to:
1. Migrate:
    * `python manage.py makemigrations explorer`.
    * `python manage.py migrate explorer`.
2. Run the alignment table generator:
    * Go to the structure alignment folder [webCovidPortal/explorer/data/structure/alignment](webCovidPortal/explorer/data/structure/alignment/), note that the [readme](webCovidPortal/explorer/data/structure/alignment/README.md) there has more detailed documentation of this process.
    * Make sure that you have an existing `conformed_alignments.csv` in [webCovidPortal/explorer/data/structure/alignment](webCovidPortal/explorer/data/structure/alignment) and that these conformed sequences have successfully been imported using the [manager commands](webCovidPortal/explorer/management/commands/README.md#importing_structures).
    * Build the alignment table by running `build_alignment_table.py`.
    * This will output a file called `conformed_alignment_table.csv`.
3. Import the results:
    * Note that depending on how many atoms are defined, importing may take a minute or two.
    * Go to [webCovidPortal/](webCovidPortal/) and import using `python manage.py import_structureresiduealignment explorer/data/structure/alignment/conformed_alignment_table.csv`.
4. Test:
    * You can test by using the API directly with the following link: http://localhost:8000/explorer/structureresidueatoms?mesh_id=D064370&atom=CA&alignment=20200505&pdbchains=5X5B.A%2C5X5B.C
