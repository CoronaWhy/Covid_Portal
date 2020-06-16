import numpy as np;
data = np.arange(0,100);
print(list(enumerate(data[::10])));
for i,n in enumerate(data[::10]):
	print(str(i)+" "+str(n));
