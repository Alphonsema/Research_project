import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

df_pmma = (pd.read_csv("data.csv"))

pmma = df_pmma.dropna()

fsr = (299792458 / (2 * .006))

frequencyAxisValues = np.linspace(-fsr, fsr, 1024)/10**9

pmma["frequencyAxis"] = frequencyAxisValues

plt.plot(frequencyAxisValues, pmma["Y"])
plt.yscale("log")
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('PMMA')

peaks, _ = find_peaks(pmma["Y"], height=100, distance=200)

B1Values = (frequencyAxisValues[(peaks[0] - 50):(peaks[0] + 50)])

B2Values = (frequencyAxisValues[(peaks[2] - 50):(peaks[2] + 50)])


def laurentian(x, amp, wid, centre):
    return (amp * wid ** 2) / ((x - centre) ** 2 + wid ** 2)


plt.plot(frequencyAxisValues, pmma["Y"], 'bo', label='experiment data')


popt1, pcov = curve_fit(laurentian, B1Values, pmma["Y"][(peaks[0] - 50):(peaks[0] + 50)], maxfev=1000000,
                        bounds=((0, 0, min(B1Values)), (1000, 1000, max(B1Values))))


X1fit = B1Values
plt.plot(X1fit, laurentian(X1fit, *popt1), 'r', label='fit parameters')

popt2, pcovo = curve_fit(laurentian, B2Values, pmma["Y"][(peaks[2] - 50):(peaks[2] + 50)], maxfev=1000000,
                         bounds=((0, 0, min(B2Values)), (1000, 1000, max(B2Values))))

X2fit = B2Values
plt.plot(X2fit, laurentian(X2fit, *popt2), 'g', label='fit parameters')
print(plt.show())
