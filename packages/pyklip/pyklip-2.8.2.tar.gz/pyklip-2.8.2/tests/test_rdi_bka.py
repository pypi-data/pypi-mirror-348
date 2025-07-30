import os
import glob
from time import time
import numpy as np
import astropy.io.fits as fits

import pyklip.instruments.Instrument as Instrument
import pyklip.parallelized as parallelized
import pyklip.rdi as rdi
import pyklip.fakes as fakes
import scipy
import pyklip.fmlib.fmpsf as fmpsf
import pyklip.fmlib.matchedFilter as mf
import pyklip.fitpsf as fitpsf
import matplotlib.pylab as plt

testdir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep



def test_bka_rdi():
    """
    Tests RDI forward modeling of the PSF.
    """
    filtername = "f300m"

    basedir = "../../../../OneDrive/Research/JWST/nircam_sims/"

    # read in roll 1
    with fits.open(basedir + "NIRCam_target_Roll1_{0}.fits".format(filtername)) as hdulist:
        roll1_cube = hdulist[0].data
        print(roll1_cube.shape)
        
    # read in roll 2
    with fits.open(basedir + "NIRCam_target_Roll2_{0}.fits".format(filtername)) as hdulist:
        roll2_cube = hdulist[0].data   
        print(roll2_cube.shape)
        
    # read in ref star
    with fits.open(basedir + "NIRCam_refs_SGD_{0}.fits".format(filtername)) as hdulist:
        ref_cube = hdulist[0].data 
        print(ref_cube.shape)
        
    # read in unocculted PSF
    with fits.open(basedir + "NIRCam_unocculted_{0}.fits".format(filtername)) as hdulist:
        psf_cube = hdulist[0].data 
        print(psf_cube.shape)  

    
    # combine the two rows
    full_seq = np.concatenate([roll1_cube, roll2_cube], axis=0)

    # two rolls are offset 10 degrees, this is the right sign (trust me)
    pas = np.append([0 for _ in range(roll1_cube.shape[0])], [10 for _ in range(roll2_cube.shape[0])])

    # for each image, the (x,y) center where the star is is just the center of the image
    centers = np.array([np.array(frame.shape)/2. for frame in full_seq])

    # give it some names, just in case we want to refer to them
    filenames = np.append(["roll1_{0}".format(i) for i in range(roll1_cube.shape[0])],
                        ["roll2_{0}".format(i) for i in range(roll1_cube.shape[0])])

    # create the GenericData object. This will standardize the data for pyKLIP
    dataset = Instrument.GenericData(full_seq, centers, IWA=4, parangs=pas, filenames=filenames)
    dataset.flipx = False # get the right handedness of the data

    # combine both science target and reference target images into a psf library array
    psflib_imgs = np.append(ref_cube, full_seq, axis=0)
    ref_filenames = ["ref_{0}".format(i) for i in range(ref_cube.shape[0])]
    psflib_filenames = np.append(ref_filenames, filenames, axis=0)
    # all frames aligned to image center (Which are the same size)
    ref_center = np.array(ref_cube[0].shape)/2

    # make the PSF library
    # we need to compute the correlation matrix of all images vs each other since we haven't computed it before
    psflib = rdi.PSFLibrary(psflib_imgs, ref_center, psflib_filenames, compute_correlation=True)

    # prepare the PSF Library to run on our science dataset
    psflib.prepare_library(dataset)

    # collapse reference psf in time
    psf_frame = np.nanmean(psf_cube, axis=0)

    # find the centroid
    bestfit = fakes.gaussfit2d(psf_frame, 71, 30, searchrad=3, guessfwhm=2, guesspeak=1, refinefit=True)

    psf_xcen, psf_ycen = bestfit[2:4]
    print(psf_xcen, psf_ycen)

    # recenter PSF to that location
    x, y = np.meshgrid(np.arange(-20,20.1,1), np.arange(-20,20.1,1))
    x += psf_xcen
    y += psf_ycen

    psf_stamp = scipy.ndimage.map_coordinates(psf_frame, [y,x])

    # setup FM guesses
    numbasis = np.array([1, 3, 10]) # KL basis cutoffs you want to try
    guess_dx = 6.7 # in pxiels (positive is to the left)
    guess_dy = 19.6 # in pixels (positive is up)
    guesssep = np.sqrt(guess_dx**2 + guess_dy**2) # estimate of separation in pixels
    guesspa = np.degrees(np.arctan2(guess_dx, guess_dy)) # estimate of position angle, in degrees
    guessflux = 1e-4 # estimated contrast
    guessspec = np.array([1]) # braodband, so don't need to guess spectrum

    # initialize the FM Planet PSF class
    fm_class = fmpsf.FMPlanetPSF(dataset.input.shape, numbasis, guesssep, guesspa, guessflux, np.array([psf_stamp]),
                                np.unique(dataset.wvs), spectrallib_units="contrast", spectrallib=[guessspec])

    # PSF subtraction parameters
    # You should change these to be suited to your data!
    outputdir = "./" # where to write the output files
    prefix = "fm-RDI-k50m1" # fileprefix for the output files
    annulus_bounds = [[guesssep-20, guesssep+20]] # one annulus centered on the planet
    subsections = 1 # we are not breaking up the annulus
    padding = 0 # we are not padding our zones
    movement = 1 # basically, we want to use the other roll angle for ADI.

    # run KLIP-FM
    import pyklip.fm as fm
    fm.klip_dataset(dataset, fm_class, mode="RDI", outputdir=outputdir, fileprefix=prefix, numbasis=numbasis,
                    annuli=annulus_bounds, subsections=subsections, padding=padding, movement=movement, maxnumbasis=50,
                    psf_library=psflib)

    output_prefix = os.path.join(outputdir, prefix)
    with fits.open(output_prefix + "-fmpsf-KLmodes-all.fits") as fm_hdu:
        # get FM frame, use KL=7
        fm_frame = fm_hdu[0].data[1]
        fm_centx = fm_hdu[0].header['PSFCENTX']
        fm_centy = fm_hdu[0].header['PSFCENTY']

    with fits.open(output_prefix + "-klipped-KLmodes-all.fits") as data_hdu:
        # get data_stamp frame, use KL=7
        data_frame = data_hdu[0].data[1]
        data_centx = data_hdu[0].header["PSFCENTX"]
        data_centy = data_hdu[0].header["PSFCENTY"]

    fitboxsize = 17
    fma = fitpsf.FMAstrometry(guesssep, guesspa, fitboxsize)

    # generate FM stamp
    # padding should be greater than 0 so we don't run into interpolation problems
    fma.generate_fm_stamp(fm_frame, [fm_centx, fm_centy], padding=5)

    # generate data_stamp stamp
    # not that dr=4 means we are using a 4 pixel wide annulus to sample the noise for each pixel
    # exclusion_radius excludes all pixels less than that distance from the estimated location of the planet
    fma.generate_data_stamp(data_frame, [data_centx, data_centy], dr=4, exclusion_radius=10)

    # set kernel
    corr_len_guess = 3. # in pixels, our guess for the correlation length
    corr_len_label = r"$l$" # label for this variable.
    fma.set_kernel("matern32", [corr_len_guess], [corr_len_label])

    # set prior boundson parameters
    x_range = 1.0 # pixels
    y_range = 1.0 # pixels
    flux_range = 1. # flux can vary by an order of magnitude
    corr_len_range = 1. # between 0.3 and 30
    fma.set_bounds(x_range, y_range, flux_range, [corr_len_range])

    # run MCMC fit
    fma.fit_astrometry(nwalkers=100, nburn=200, nsteps=800, numthreads=2)

    fig = plt.figure()
    fig = fma.best_fit_and_residuals(fig=fig)

    fig = fma.make_corner_plot()

    plt.show()

def test_fmmf_rdi():
    """
    Test FMMF RDI
    """
    filtername = "f300m"

    basedir = "../../../../OneDrive/Research/JWST/nircam_sims/"

    # read in roll 1
    with fits.open(basedir + "NIRCam_target_Roll1_{0}.fits".format(filtername)) as hdulist:
        roll1_cube = hdulist[0].data
        print(roll1_cube.shape)
        
    # read in roll 2
    with fits.open(basedir + "NIRCam_target_Roll2_{0}.fits".format(filtername)) as hdulist:
        roll2_cube = hdulist[0].data   
        print(roll2_cube.shape)
        
    # read in ref star
    with fits.open(basedir + "NIRCam_refs_SGD_{0}.fits".format(filtername)) as hdulist:
        ref_cube = hdulist[0].data 
        print(ref_cube.shape)
        
    # read in unocculted PSF
    with fits.open(basedir + "NIRCam_unocculted_{0}.fits".format(filtername)) as hdulist:
        psf_cube = hdulist[0].data 
        print(psf_cube.shape)  

    
    # combine the two rows
    full_seq = np.concatenate([roll1_cube, roll2_cube], axis=0)

    # two rolls are offset 10 degrees, this is the right sign (trust me)
    pas = np.append([0 for _ in range(roll1_cube.shape[0])], [10 for _ in range(roll2_cube.shape[0])])

    # for each image, the (x,y) center where the star is is just the center of the image
    centers = np.array([np.array(frame.shape)//2. for frame in full_seq])

    # give it some names, just in case we want to refer to them
    filenames = np.append(["roll1_{0}".format(i) for i in range(roll1_cube.shape[0])],
                        ["roll2_{0}".format(i) for i in range(roll1_cube.shape[0])])

    # create the GenericData object. This will standardize the data for pyKLIP
    dataset = Instrument.GenericData(full_seq, centers, IWA=4, parangs=pas, filenames=filenames)
    dataset.flipx = False # get the right handedness of the data

    # combine both science target and reference target images into a psf library array
    psflib_imgs = np.append(ref_cube, full_seq, axis=0)
    ref_filenames = ["ref_{0}".format(i) for i in range(ref_cube.shape[0])]
    psflib_filenames = np.append(ref_filenames, filenames, axis=0)
    # all frames aligned to image center (Which are the same size)
    ref_center = np.array(ref_cube[0].shape)//2

    # make the PSF library
    # we need to compute the correlation matrix of all images vs each other since we haven't computed it before
    psflib = rdi.PSFLibrary(psflib_imgs, ref_center, psflib_filenames, compute_correlation=True)

    # prepare the PSF Library to run on our science dataset
    psflib.prepare_library(dataset)

    # collapse reference psf in time
    psf_frame = np.nanmean(psf_cube, axis=0)

    # find the centroid
    bestfit = fakes.gaussfit2d(psf_frame, 71, 30, searchrad=3, guessfwhm=2, guesspeak=1, refinefit=True)

    psf_xcen, psf_ycen = bestfit[2:4]
    print(psf_xcen, psf_ycen)

    # recenter PSF to that location
    x, y = np.meshgrid(np.arange(-20,20.1,1), np.arange(-20,20.1,1))
    x += psf_xcen
    y += psf_ycen

    psf_stamp = scipy.ndimage.map_coordinates(psf_frame, [y,x])

    # setup FM guesses
    numbasis = np.array([20,]) # KL basis cutoffs you want to try
    guess_dx = 6.7 # in pxiels (positive is to the left)
    guess_dy = 19.6 # in pixels (positive is up)
    guesssep = np.sqrt(guess_dx**2 + guess_dy**2) # estimate of separation in pixels
    guesspa = np.degrees(np.arctan2(guess_dx, guess_dy)) # estimate of position angle, in degrees
    guessflux = 1e-4 # estimated contrast
    guessspec = np.ones(dataset.input.shape[0]) # braodband, so don't need to guess spectrum

    # initialize the FM Planet PSF class
    fm_class = mf.MatchedFilter(dataset.input.shape, numbasis, np.array([psf_stamp]), np.unique(dataset.wvs), [guessspec])

    # PSF subtraction parameters
    # You should change these to be suited to your data!
    outputdir = "./" # where to write the output files
    prefix = "fmmf-RDI-k50" # fileprefix for the output files
    annulus_bounds = [[guesssep-20, guesssep+20]] # one annulus centered on the planet
    subsections = 1 # we are not breaking up the annulus
    padding = 0 # we are not padding our zones
    movement = 1 # basically, we want to use the other roll angle for ADI.

    # run KLIP-FM
    import pyklip.fm as fm
    fm.klip_dataset(dataset, fm_class, mode="RDI", outputdir=outputdir, fileprefix=prefix, numbasis=numbasis,
                    annuli=annulus_bounds, subsections=subsections, padding=padding, movement=movement, maxnumbasis=50,
                    psf_library=psflib)


if __name__ == "__main__":
    # test_bka_rdi()
    test_fmmf_rdi()