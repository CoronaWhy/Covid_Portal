import numpy as np, pandas as pd;
################################################################################
infile = "../alignment/aligned.fasta";
reference = "QIS60846.1";
outfile = reference+"-nomenclature.csv";
################################################################################
def loadFASTA(fh):
	"""Load sequences from a FASTA file.

	Parameters
	----------
	fh : file_object

	Returns
	-------
	pandas.Series
		A series of sequence strings indexed by ID/name

	Examples
	--------
	Minimal working example.
	>>> import numpy as np, pandas as pd;
	>>> import simpleSeq.IO as ssio;
	>>> with open('SEQUENCES.fasta','r') as fh:
	>>> 	seqs = ssio.loadFASTA(fh);
	>>> print(seqs);

	"""
	seqs = {};
	current = "";
	for l in fh.read().split('\n'):
		if l[0]=='>': current = l[1:];
		else:
			if current in seqs.keys():
				seqs[current] += str(l);
			else:
				seqs[current] = str(l);
	return pd.Series(seqs, dtype=str);
################################################################################
max_subdigits = 3;
with open(infile,'r') as fh:
    seqs = loadFASTA(fh);
pnom = [];
pos = 0;
subpos = 0;
for c in seqs[reference]:
    if c=='-':
        subpos += 1;
    else:
        subpos=0;
        pos+=1;
    pnom.append(str(pos)+"."+str(subpos).rjust(max_subdigits,'0'));
pnom = pd.DataFrame({ 'nomenclature': pnom });
pnom.to_csv(outfile);



#print(seqs);
