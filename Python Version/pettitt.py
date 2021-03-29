import numpy as np

def pettitt_test(data):

    """
    Pettitt test calculated following Pettitt (1979): https://www.jstor.org/stable/2346729?seq=4#metadata_info_tab_contents
    """

    T = len(data)
    U = []
    for t in range(T): 												# t is used to split X into two subseries
        data_stack = np.zeros((t, len(data[t:]) + 1), dtype=int)
        data_stack[:,0] = data[:t] 									# first column is each element of the first subseries
        data_stack[:,1:] = data[t:] 								# all rows after the first element are the second subseries
        U.append(np.sign(data_stack[:,0] - data_stack[:,1:].transpose()).sum()) # sign test between each element of the first subseries and all elements of the second subseries, summed.

    loc = np.argmax(np.abs(U)) 										# location of change (first data point of second sub-series)
    K = np.max(np.abs(U))
    pvalue = 2 * np.exp(-6 * K**2 / (T**3 + T**2))
        
    return (loc, K, pvalue)