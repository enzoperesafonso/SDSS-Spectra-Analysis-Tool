import matplotlib.pyplot as plt
import warnings
from matplotlib.widgets import RangeSlider, Button
from astroquery.sdss import SDSS
from astropy import units as u
from specutils.spectra import Spectrum1D, SpectralRegion
from specutils.fitting import fit_generic_continuum

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 7),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
         'text.usetex': True} 

plt.rcParams.update(params)

######################################## Downloading and storing the spectrum .fits file from SDSS ######################################## 

plateIn = 712
plateInDate = 52179
fiberIn = 12

spectrum = SDSS.get_spectra(plate=plateIn, fiberID=fiberIn, mjd=plateInDate)[0]
fluxSDSS = spectrum[1].data['flux']
lamSDSS = 10**(spectrum[1].data['loglam'])

fittedSpectrum  = Spectrum1D(flux = fluxSDSS*u.ST, spectral_axis = lamSDSS * u.Angstrom)

with warnings.catch_warnings():  # Ignores warnings
    warnings.simplefilter('ignore')
    continuum_fit = fit_generic_continuum(fittedSpectrum)

y_continuum_fitted = continuum_fit(lamSDSS*u.Angstrom)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.25)

spectraPlot = ax.plot(lamSDSS, fluxSDSS, color='k', linewidth=0.5)
contFit, = ax.plot(lamSDSS, y_continuum_fitted, color = 'r', linewidth=1)

ax.set_title('Plate:{}/{}  Fibre:{} '.format(plateIn,plateInDate,fiberIn))
ax.set_xlabel(r'Wavelength (\AA)')
ax.set_xlim(lamSDSS.min(), lamSDSS.max())
ax.set_ylabel(r'Flux ($10^{-17}$ erg cm$^{-2}$ s$^{-1}$ \AA$^{-1}$)')

########################################  GUI HANDLING ######################################## 

def updateRange(val):
    ax.set_xlim(val[0],val[1])
    fig.canvas.draw_idle()

def toggleContinuum(val):
        isVis = plt.getp(contFit, 'visible')
        plt.setp(contFit, visible = not isVis)
        fig.canvas.draw()
    

# Create the RangeSlider and Buttons

slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
slider = RangeSlider(slider_ax, "Wavlength Range", lamSDSS.min(), lamSDSS.max(),valinit=(lamSDSS.min(), lamSDSS.max()))
slider.on_changed(updateRange)

bToggleContinuum_ax = fig.add_axes([0.20, 0.025, 0.1, 0.05])
bToggleContinuum = Button(bToggleContinuum_ax, 'Toggle Continuum Fit')
bToggleContinuum.on_clicked(toggleContinuum)




plt.show()




