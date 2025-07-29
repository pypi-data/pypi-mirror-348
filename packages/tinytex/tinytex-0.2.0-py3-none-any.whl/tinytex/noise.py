from __future__ import annotations
import typing
from typing import Union

import torch
import numpy as np
from scipy.spatial import cKDTree

from tinycio import MonoImage

from .util import *
from .smoothstep import Smoothstep



# SPATIAL-DOMAIN

class SpatialNoise:

    """Spatial-domain procedural noise generators."""

    err_hw_pot = "height and width must be power-of-two"
    err_density_zero = "density cannot be zero"

    #TODO: value noise
    #https://iquilezles.org/articles/gradientnoise/
    # simplex noise
    #https://www.shadertoy.com/view/Msf3WH



    # From: https://github.com/pvigier/perlin-numpy/blob/master/perlin_numpy/perlin2d.py
    # Copyright (c) 2019 Pierre Vigier

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:

    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.
    @classmethod
    def __perlin_np(cls, 
        shape:tuple, 
        res:tuple, 
        tileable:tuple=(True, True), 
        interpolant:str='quintic_polynomial'):
        """Generate a 2D numpy array of perlin noise.

        Args:
            shape: The shape of the generated array (tuple of two ints).
                This must be a multple of res.
            res: The number of periods of noise to generate along each
                axis (tuple of two ints). Note shape must be a multiple of
                res.
            tileable: If the noise should be tileable along each axis
                (tuple of two bools). Defaults to (False, False).
            interpolant: The interpolation function, defaults to
                t*t*t*(t*(t*6 - 15) + 10).

        Returns:
            A numpy array of shape shape with the generated noise.

        Raises:
            ValueError: If shape is not a multiple of res.
        """

        delta = (res[0] / shape[0], res[1] / shape[1])
        d = (shape[0] // res[0], shape[1] // res[1])
        grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1
        # Gradients
        angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        if tileable[0]: gradients[-1,:] = gradients[0,:]
        if tileable[1]: gradients[:,-1] = gradients[:,0]
        gradients = gradients.repeat(d[0], 0).repeat(d[1], 1)
        g00 = gradients[    :-d[0],    :-d[1]]
        g10 = gradients[d[0]:     ,    :-d[1]]
        g01 = gradients[    :-d[0],d[1]:     ]
        g11 = gradients[d[0]:     ,d[1]:     ]
        # Ramps
        n00 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]  )) * g00, 2)
        n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]  )) * g10, 2)
        n01 = np.sum(np.dstack((grid[:,:,0]  , grid[:,:,1]-1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
        # Interpolation
        t = Smoothstep.interpolate(interpolant, grid)
        n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
        n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
        return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

    @classmethod
    def perlin(cls, 
        shape:tuple, 
        density:float=5., 
        tileable:tuple=(True, True), 
        interpolant:str='quintic_polynomial') -> torch.Tensor:
        """
        Generate 2D Perlin noise.

        :param shape: Output shape as (height, width).
        :param density: Controls frequency of the noise pattern.
        :param tileable: Whether noise should tile along each axis.
        :param interpolant: Interpolation function name (e.g., 'linear', 'quintic_polynomial').
        :return: Tensor of shape [1, H, W] with values in [0, 1].
        """
        assert density > 0., cls.err_density_zero
        assert is_pot(shape[0]) and is_pot(shape[1]), cls.err_hw_pot
        res = (
            closest_divisor(shape[0], np.ceil(shape[0]/256.*density)), 
            closest_divisor(shape[1], np.ceil(shape[1]/256.*density)))
        out = cls.__perlin_np(shape, res, tileable, interpolant)
        return torch.from_numpy(np.expand_dims(out, 0).astype(np.float32)*0.5+0.5).clamp(0., 1.)

    # From: https://github.com/pvigier/perlin-numpy/blob/master/perlin_numpy/perlin2d.py
    # Copyright (c) 2019 Pierre Vigier

    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:

    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.
    @classmethod
    def __fractal_np(cls, 
            shape:tuple, 
            res:tuple, 
            octaves:int=1, 
            persistence:float=0.5,
            lacunarity:int=2, 
            tileable:tuple=(True, True),
            interpolant:str='quintic_polynomial', 
            turbulence:bool=False) -> np.ndarray:
        """Generate a 2D numpy array of fractal noise.

        Args:
            shape: The shape of the generated array (tuple of two ints).
                This must be a multiple of lacunarity**(octaves-1)*res.
            res: The number of periods of noise to generate along each
                axis (tuple of two ints). Note shape must be a multiple of
                (lacunarity**(octaves-1)*res).
            octaves: The number of octaves in the noise. Defaults to 1.
            persistence: The scaling factor between two octaves.
            lacunarity: The frequency factor between two octaves.
            tileable: If the noise should be tileable along each axis
                (tuple of two bools). Defaults to (False, False).
            interpolant: The, interpolation function, defaults to
                t*t*t*(t*(t*6 - 15) + 10).

        Returns:
            A numpy array of fractal noise and of shape shape generated by
            combining several octaves of perlin noise.

        Raises:
            ValueError: If shape is not a multiple of
                (lacunarity**(octaves-1)*res).
        """
        noise = np.zeros(shape)
        frequency = 1
        amplitude = 1
        for _ in range(octaves):
            perlin = cls.__perlin_np(
                shape, 
                (min(frequency*res[0], shape[0]), min(frequency*res[1], shape[1])), 
                tileable, 
                interpolant
            )
            noise += amplitude * (np.abs(perlin) if turbulence else perlin)            
            frequency *= lacunarity
            amplitude *= persistence
        return noise

    @classmethod
    def fractal(cls, 
            shape:tuple, 
            density:float=5., 
            octaves:int=5, 
            persistence:float=0.5,
            lacunarity:int=2, 
            tileable:tuple=(True, True),
            interpolant:str='quintic_polynomial') -> torch.Tensor:
        """
        Generate 2D fractal noise using layered Perlin noise.

        :param shape: Output shape as (height, width).
        :param density: Base frequency scale.
        :param octaves: Number of noise layers.
        :param persistence: Amplitude falloff per octave.
        :param lacunarity: Frequency multiplier per octave.
        :param tileable: Whether noise should tile along each axis.
        :param interpolant: Interpolation function name.
        :return: Tensor of shape [1, H, W] with values in [0, 1].
        """
        assert density > 0., cls.err_density_zero
        assert is_pot(shape[0]) and is_pot(shape[1]), cls.err_hw_pot
        res = (
            closest_divisor(shape[0], np.ceil(shape[0]/256.*density)), 
            closest_divisor(shape[1], np.ceil(shape[1]/256.*density)))
        out = cls.__fractal_np(shape, res, octaves, persistence, lacunarity, tileable, interpolant, turbulence=False)
        return torch.from_numpy(np.expand_dims(out, 0).astype(np.float32)*0.5+0.5).clamp(0., 1.)

    @classmethod
    def turbulence(cls, 
            shape:tuple, 
            density:float=5., 
            octaves:int=5, 
            persistence:float=0.5,
            lacunarity:int=2, 
            tileable:tuple=(True, True),
            interpolant:str='quintic_polynomial', 
            ridge:bool=False) -> torch.Tensor:
        """
        Generate 2D turbulence noise (absolute layered Perlin).

        :param shape: Output shape as (height, width).
        :param density: Base frequency scale.
        :param octaves: Number of noise layers.
        :param persistence: Amplitude falloff per octave.
        :param lacunarity: Frequency multiplier per octave.
        :param tileable: Whether noise should tile along each axis.
        :param interpolant: Interpolation function name.
        :param ridge: If True, applies ridge-remapping for sharper features.
        :return: Tensor of shape [1, H, W] with values in [0, 1].
        """
        assert density > 0., cls.err_density_zero
        assert is_pot(shape[0]) and is_pot(shape[1]), cls.err_hw_pot
        res = (
            closest_divisor(shape[0], np.ceil(shape[0]/256.*density)), 
            closest_divisor(shape[1], np.ceil(shape[1]/256.*density)))
        out = cls.__fractal_np(shape, res, octaves, persistence, lacunarity, tileable, interpolant, turbulence=True)
        if ridge:
            out = 1. - out
            out = out ** 2
        return torch.from_numpy(np.expand_dims(out, 0).astype(np.float32)).clamp(0., 1.)
    
    @classmethod
    def __worley_np(cls, 
        shape:tuple, 
        density:float, 
        tileable:tuple=(True, True)) -> np.ndarray:
        height, width = shape[0], shape[1]
        points = []
        density = int(density)
        base = [[np.random.randint(0, height), np.random.randint(0, width)] for _ in range(density)]
        
        for h in range(3):
            if not tileable[0] and h != 1: continue
            for w in range(3):
                if not tileable[1] and w != 1: continue
                for v in range(density):
                    h_offset = h * height
                    w_offset = w * width
                    points.append([base[v][0] + h_offset, base[v][1] + w_offset])

        coord = np.dstack(np.mgrid[0:height*3, 0:width*3])
        tree = cKDTree(points)
        distances = tree.query(coord, workers=-1)[0].astype(np.float32)
        return distances[height:height*2, width:width*2]

    @classmethod
    def worley(cls, 
        shape:tuple, 
        density:float=5., 
        intensity:float=1., 
        tileable:tuple=(True, True)) -> torch.Tensor:
        """
        Generate 2D Worley (cellular) noise.

        :param shape: Output shape as (height, width).
        :param density: Number of feature points per axis.
        :param intensity: Multiplier for the distance field.
        :param tileable: Whether noise should tile along each axis.
        :return: Tensor of shape [1, H, W] with values in [0, 1].
        """
        assert density > 0., cls.err_density_zero
        assert is_pot(shape[0]) and is_pot(shape[1]), cls.err_hw_pot
        density *= 10
        intensity = 0.01 * intensity
        out = cls.__worley_np(shape, density, tileable)
        return torch.from_numpy(np.expand_dims(out*intensity, 0).astype(np.float32)).clamp(0., 1.)

# SPECTRAL-DOMAIN

class SpectralNoise:
    """
    Spectral-domain procedural noise generators.
    """

    @classmethod
    def noise_psd_2d(cls, height:int, width:int, psd=lambda f: torch.ones_like(f)):
        """
        Generate spectral 2D noise field. Shape (height, width) with a spectral shaping function psd.
        
        :param height: Field height.
        :param width: Field width.
        :param psd: a function that accepts a tensor f of shape (height, width//2+1) of frequency magnitudes
             and returns a tensor of the same shape.
        """
        # Generate 2D white noise in the frequency domain.
        X_white = torch.fft.rfft2(torch.randn(height, width))
        
        # Create frequency grids for the rfft2 output.
        # For the first dimension, use full FFT frequencies.
        fy = torch.fft.fftfreq(height, d=1.0)  # shape: (height,)
        # For the second dimension, use rFFT frequencies.
        fx = torch.fft.rfftfreq(width, d=1.0)   # shape: (width//2 + 1,)
        
        # Build 2D grids by broadcasting.
        fy_grid = fy.view(height, 1)            # shape: (height, 1)
        fx_grid = fx.view(1, -1)                 # shape: (1, width//2+1)
        f_grid = torch.sqrt(fx_grid**2 + fy_grid**2)  # shape: (height, width//2+1)
        
        # Compute the spectral shaping function S and normalize its mean-square.
        S = psd(f_grid)
        S[0, 0] = 0  # Prevent NaN at DC
        S = S / torch.sqrt(torch.mean(S ** 2, dim=(-2, -1), keepdim=True) + 1e-8)  # Avoid div by zero
        
        # Shape the white noise spectrum.
        X_shaped = X_white * S
        
        # Inverse FFT to obtain a spatial-domain noise field.
        return torch.fft.irfft2(X_shaped, s=(height, width))

    @classmethod
    def white(cls, height: int, width: int) -> torch.Tensor:
        """
        Generate 2D white noise (flat power spectrum).

        :param height: Output height.
        :param width: Output width.
        :return: 2D tensor of white noise with shape (height, width).
        """
        return cls.noise_psd_2d(height, width, psd=lambda f: torch.ones_like(f))

    @classmethod
    def pink(cls, height: int, width: int) -> torch.Tensor:
        """
        Generate 2D pink noise (1/f spectrum).

        :param height: Output height.
        :param width: Output width.
        :return: 2D tensor of pink noise with shape (height, width).
        """
        return cls.noise_psd_2d(height, width, psd=lambda f: f.pow(-1))

    @classmethod
    def brownian(cls, height: int, width: int) -> torch.Tensor:
        """
        Generate 2D brownian (red) noise (1/f² spectrum).

        :param height: Output height.
        :param width: Output width.
        :return: 2D tensor of brownian noise with shape (height, width).
        """
        return cls.noise_psd_2d(height, width, psd=lambda f: f.pow(-2))

    @classmethod
    def blue(cls, height: int, width: int) -> torch.Tensor:
        """
        Generate 2D blue noise (f spectrum).

        :param height: Output height.
        :param width: Output width.
        :return: 2D tensor of blue noise with shape (height, width).
        """
        return cls.noise_psd_2d(height, width, psd=lambda f: f)

    @classmethod
    def violet(cls, height: int, width: int) -> torch.Tensor:
        """
        Generate 2D violet noise (f² spectrum).

        :param height: Output height.
        :param width: Output width.
        :return: 2D tensor of violet noise with shape (height, width).
        """
        return cls.noise_psd_2d(height, width, psd=lambda f: f.pow(2))
