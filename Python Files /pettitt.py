import numpy as np
def pettitt(data):
	T = len(data)
	U = []
	for t in range(T):
		res = 0
		for i in range(t):
			for j in range(t+1, T):
				res += np.sign(data[i] - data[j])
				U.append(res)
		loc = np.argmax(np.abs(U))
	K = np.max(np.abs(U))
	pvalue = 2 * np.exp(-6*K**2/(T**3+T**2))
	return (loc, K, pvalue)