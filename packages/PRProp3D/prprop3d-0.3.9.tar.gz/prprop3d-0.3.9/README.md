# PRProp3D
PRProp3D is a scalar nonlinear optical forward beam propagation package that will run with or without GPU support. It uses the torch package only to determine the availability of a suitable GPU. It was developed to enable modelling of photorefractive nonlinear optical effects such as two beam coupling, image amplification and beam fanning. Full details of the package performance including application to image amplification and solitons can be found at [Three-Dimensional Scalar Time-Dependent Photorefractive Beam Propagation Model](https://www.mdpi.com/3156550)

## Features

- Static and time dependent implementations.
- Runs on GPU or CPU.
- Images may be applied to the beams
- The effects of externally applied bias fields can be investigated

## Installation

You can install the package via **PyPI** or from **source**.

### Install from PyPI
requires torch for detecting presence of GPU 
```bash
pip install PRProp3D
```

### Install from Source (GitHub)

```bash
git clone https://github.com/mcroning/PRProp3D_package.git
cd PRProp3D_package
pip install .
```

## Usage

After installation the following methods will be available: 

propagate(prdict,outputs)
*Static steady state propagation*
* inputs:  
  * prdict:  dictionary of input parameters such as wavelength 
  * outputs: list of requested output arrays   
    * 'ampxz', 'dnxz'  
* returns: amp,derived,outputs  
  * amp: complex amplitude of output field  
  * derived: class containing derived objects used in calculation such as the input amplitude amp0  
  * outputs: class containing requested output arrays, calculated gain,  and objects useful for postprocessing
  

propagate_t(prdict,outputs)
*Time dependent propagation*
* inputs 
  * prdict:  dictionary of input parameters such as wavelength 
  * outputs: list of requested output arrays
    * 'ampxzt', 'dnxzt', 'ampxyt', 'dnxyt'
* returns: amp,derived,outputs  
  * amp: complex amplitude of output field at end time 
  * derived: class containing derived objects used in calculation such as the input amplitude amp0  
  * outputs: class containing requested output arrays, calculated gain vs time, and objects useful for postprocessing
  
gain(amp,prdict,derived) 
*Function for calculating two beam coupling gain*
* inputs 
  * amp: transverse xy complex amplitude on which to calculate gain
  * prdict: (defined above)
  * derived: (defined above)
* returns gain,amps
  * gain: two beam coupling gain
  * amps: list containing separated complex amplitudes for imput and output beams
    * [ampp,ampm,amp0p,amp0m] (beams 1 and 2 outputs, beams 1 and 2 outputs)

The simple example below [proptest.py](https://github.com/mcroning/PRProp3D/blob/ef17a553d5ead1b3d1ca2a634381f3ec4d13d9d0/Package%20README%20usage%20examples/proptest_full.py) and another which allows images to be loaded on the beams [proptest_full.py](https://github.com/mcroning/PRProp3D/blob/ef17a553d5ead1b3d1ca2a634381f3ec4d13d9d0/Package%20README%20usage%20examples/proptest_full.py) are avalable at the Github repository


### Example: Two beam coupling of Gaussian Beams
The following example show the use of the package for two interacting gaussian beams at steady state. The beam ratio is 6.67, the coupling constant length product is -3, the angle of incidence of beam 1 is 0.16 radians, that of beam 2 is -0.16 radians. The beam waists are 100 $\mu m$ and they cross halfway through the interaction length.

    !pip install PRProp3D
    from PRProp3D import *
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import torch
    
    
    # Check if CUDA (GPU support) is available
    GPU = torch.cuda.is_available()
    
    prdict={
    'gl':-3,
    'rat':6.67,
    'image_on_beam':'No Image',
    'image_type':'real image',
    'image_size_factor':1,
    'external_image':'',
    'std_image':'MNIST 0',
    'image_invert':False,
    'noisetype':'none',
    'sigma':0.4,
    'eps':0.02,
    'kt':0,
    'xaper':1000,
    'yaper':1000,
    'xsamp':4096,
    'ysamp':512,
    'rlen':4000,
    'dz':20,
    'lm':0.633,
    'w01':100,
    'w02':100,
    'thout1':0.16,
    'thout2':-0.16,
    'phi1':0,
    'phi2':0,
    'backpropagate':False,
    'time_behavior':'Static',
    'tend':1,
    'tsteps':12,
    'use_cons_tsteps':False,
    'batchnum_spec':1,
    'fanning_study':False,
    'use_old_seeds':False,
    'folder':'',
    'savedata':False,
    'epsr':2500,
    'NT':6.4e22,
    'T':293,
    'refin':2.4,
    'Id':0.01,
    'windowedge':0.1,
    'E_app':0,
    'skip':4,
    'arrin':[],
    'planewave':False
    }
    
    if  prdict['w01'] < 0 or prdict['w02'] < 0: #we are using plane waves, so force periodic conditions
    
      fc=prdict['xsamp']*prdict['lm']/2/prdict['xaper']
      prdict['thout1']=np.arcsin(fc/(2**round(np.log(
        fc/np.sin(abs(prdict['thout1'])))/np.log(2))))*np.sign(prdict['thout1'])
      prdict['thout2']=-prdict['thout1']
      prdict['windowedge']=0
    
    
    # call propagator to propagate input
    amp,derived,output=propagate(prdict,outputs=['ampxz','dnxz'])
    
    print('calculated gain',output.gain)
    amps=output.amps
    if GPU:
      amps[0] = (amps[0]).get()
      amps[1] = (amps[1]).get() 
      amps[2] = (amps[2]).get()
      amps[3] = (amps[3]).get()
    
    
    imoutp=np.rot90(abs(amps[0])**2,k=3)
    imoutm=np.rot90(abs(amps[1])**2,k=3)
    
    iminp=np.rot90(abs(amps[2])**2,k=3)
    iminm=np.rot90(abs(amps[3])**2,k=3)
    
    xaper=prdict['xaper']
    yaper=prdict['yaper']
    xsamp=prdict['xsamp']
    ysamp=prdict['ysamp']
    
    fig1,ax1 = plt.subplots(1,2)
    ax1[0].set_title('Beam 1 in')
    ax1[0].set_xlabel(r'x ($\mu$m)')
    ax1[0].set_ylabel(r'y ($\mu$m)')
    
    im=ax1[0].imshow(iminp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
    fig1.colorbar(im,ax=ax1[0],shrink=0.5)
    ax1[1].set_title('Beam 2 in')
    ax1[1].set_xlabel(r'x ($\mu$m)')
    ax1[1].set_ylabel(r'y ($\mu$m)')
    im=ax1[1].imshow(iminm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
    fig1.colorbar(im,ax=ax1[1],shrink=0.5)
    fig1.tight_layout()
    
    fig2,ax2 = plt.subplots(1,2)
    ax2[0].set_title('Beam 1 out')
    ax2[0].set_xlabel(r'x ($\mu$m)')
    ax2[0].set_ylabel(r'y ($\mu$m)')
    im=ax2[0].imshow(imoutp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
    fig2.colorbar(im,ax=ax2[0],shrink=0.5)
    ax2[1].set_title('Beam 2 out')
    ax2[1].set_xlabel(r'x ($\mu$m)')
    ax2[1].set_ylabel(r'y ($\mu$m)')
    im=ax2[1].imshow(imoutm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
    fig2.colorbar(im,ax=ax2[1],shrink=0.5)
    fig2.tight_layout()
    
    fig3,ax3 = plt.subplots()
    ax3.plot(derived.x,iminp[ysamp//2,:])
    ax3.plot(derived.x,iminm[ysamp//2,:])
    ax3.set_xlabel('transverse x microns')
    ax3.set_ylabel('normalized intensity')
    ax3.legend(['beam1', 'beam2'])
    ax3.set_ylim(0,1)
    ax3.set_title('input')
    
    fig4,ax4 = plt.subplots()
    ax4.plot(derived.x,imoutp[ysamp//2,:])
    ax4.plot(derived.x,imoutm[ysamp//2,:])
    ax4.set_xlabel('transverse x microns')
    ax4.set_ylabel('normalized intensity')
    ax4.legend(['beam 1', 'beam2'])
    ax4.set_title('output')
    
    plt.show()

If you run this code, you should see the following output:\
elapsed time  44.696675062179565 
calculated gain 1.3683214544947206
The elapsed time depends, of course, on which platform you are using.

The calculated gain is less than the nominal gain because the beams have waists of only 100 $\mu$m and have 0.16 radian half angle between them so they interact for only about half of the 4mm long propagation. The elapsed time on an Apple silicon M1 Pro is 47 seconds.  It is more than 100 times faster on an INVIDIA Tesla A100 GPU (0.42 seconds)

The ouput images data chosen for this case are reproduced below: 

**Input intensity xy cross section** 
![Input intensity xy cross section](https://github.com/mcroning/PRProp3D/blob/main/Package%20README%20usage%20examples/Figure_1.png?raw=true)
**Output intensity xy cross section**
![Output intensity xy cross section](https://github.com/mcroning/PRProp3D/blob/main/Package%20README%20usage%20examples/Figure_2.png?raw=true)
**Input beam profile**
![Input beam profile](https://github.com/mcroning/PRProp3D/blob/main/Package%20README%20usage%20examples/Figure_3.png?raw=true)
**Output beam profile**
![Output beam profile](https://github.com/mcroning/PRProp3D/blob/main/Package%20README%20usage%20examples/Figure_4.png?raw=true)


