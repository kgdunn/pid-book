import numpy as np
import matplotlib.pyplot as plt


def read_dx(filename):
    """Reads a JCAMP DX file and returns the wavelengths and spectra.
    
    The output contains 2-element tuples (wavelengths and spectra) for each
    spectral scan in the file.
    """
    MULTIPLE = 2
    
    f = file(filename)
    found_data = False
    done_one_chunk = False
    raw = np.ones((1000, 8)) * np.NaN
    idx = 0
    maxcol = 0
    out = []
    for line in f.readlines():
        if line[0:2] != '##':
            value = np.fromstring(line.strip(), sep=' ')
            sz = value.size
            
            if sz > 1:
                found_data = True
                if sz > maxcol:
                    maxcol = sz
                raw[idx, 0:sz] = value
                idx += 1
        else:
            if found_data:
                done_one_chunk = True
            found_data = False
                
        if done_one_chunk:
            spectra = raw[0:idx, 0:maxcol]
            wave = spectra[:, [0]]
            spectra = spectra[:, 1::]
            #print spectra
            _, ncols = spectra.shape
            one_spectrum = spectra.ravel().copy()
            N = one_spectrum.shape
            waves = np.linspace(wave[0], wave[-1]+MULTIPLE*(ncols-1), N[0])
            out.append((waves, one_spectrum))
            
            idx = 0
            maxcol = 0
            raw = np.ones((1000, 8)) * np.NaN
            done_one_chunk = False
            
    return out
                
            
all_spectra = read_dx('/Users/kevindunn/ConnectMV/Datasets/Spectral data set - NIR/TEST1.DX')

N = len(all_spectra)
wavelengths = all_spectra[0][0]
K = wavelengths.shape[0]
all_spectral_data = np.zeros((N, K))
for idx, spectrum in enumerate(all_spectra):
     all_spectral_data[idx] = spectrum[1].ravel().reshape(1, K)
all_spectral_data = all_spectral_data[:, 0:K-2]
np.savetxt('spectral-data.csv', all_spectral_data, delimiter=',')

# meandata = np.mean(all_spectral_data, axis=0)
# all_spectral_data -= np.mean(all_spectral_data, axis=0)
# stddev = np.std(all_spectral_data, axis=0, ddof=1)
# print stddev
# all_spectral_data /= np.std(all_spectral_data, axis=0, ddof=1)
# X = np.dot(all_spectral_data.T, all_spectral_data)
# N, K = all_spectral_data.shape
# _, s, v = np.linalg.svd(X)
# v = v.T
# print v.shape
# 
# # Plot the variance explained
# fig = plt.figure()
# ax =fig.add_subplot(1,1,1)
# ax.bar(range(10), s[0:10]/s.sum())
# print s[0:10]/s.sum()
# plt.show()
# 
# #Plot p_1
# fig = plt.figure()
# ax =fig.add_subplot(1,1,1)
# ax.plot(v[])
# plt.show()
# 
# #raw_input()

fig = plt.figure(figsize=(9, 3))  # Use (8, 5.5) for slide aspect ratio
rect = [0.1, 0.22, 0.85, 0.73]  # Left, bottom, width, height
ax = fig.add_axes(rect, frame_on=True)
for loc, spine in ax.spines.iteritems():
    if loc in ['left','bottom']:
        spine.set_position(('outward',10)) # outward by 10 points
    elif loc in ['right','top']:
        spine.set_color('none') # don't draw spine
    
# turn off ticks where there is no spine
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Add labels
ax.set_xlabel('Wavelength (nm)', fontsize=16)
ax.set_ylabel('Absorbance', fontsize=16)
#ax.set_title(r'Spectra of 460 pharmaceutical tablets', fontsize=16, fontweight='bold')
ax.patch.set_facecolor('None')

for spectrum in all_spectra:
     ax.plot(spectrum[0], spectrum[1])
     ax.hold(True)
     
for label in ax.get_xticklabels():
    label.set_fontsize(16)
    label.set_weight(800)
for label in ax.get_yticklabels():
        label.set_fontsize(16)
        label.set_weight(800)


ax.axis([680, 1900, 2, 7])
ax.grid(False)

fig.savefig('pharma-spectra.png', dpi=150, facecolor='w', edgecolor='w', orientation='portrait', papertype=None, format=None, transparent=True)
