#!/usr/bin/env python
# coding: utf-8

# <style>
# @import url(https://www.numfys.net/static/css/nbstyle.css);
# </style>
# <a href="https://www.numfys.net"><img class="logo" /></a>
# 
# # Planetary Motion - Three Body Problem
# 
# ### Examples - Astrophysics
# <section class="post-meta">
# By Jonas Tjemsland, Andreas Krogen, Håkon Ånes and Jon Andreas Støvneng
# </section>
# Last edited: March 22nd 2018 
# ___

# This example is a continuation of [Planetary Motion](https://nbviewer.jupyter.org/urls/www.numfys.net/media/notebooks/planetary_motion.ipynb), which discussed different constant step size ordinary differential equation (ODE) solvers (such as Forward Euler, Explicit Trapezoid, Midpoint Rule and fourth order Runge-Kutta) applied on a two dimensional one body problem. In this example we will use an adaptive step size ODE solver (Embedded Runge-Kutta pair) to solve two and three body problems. A brief motivation for the adaptive step size is explained in [Adaptive Runge-Kutta Methods](https://nbviewer.jupyter.org/urls/www.numfys.net/media/notebooks/adaptive_runge_kutta_methods.ipynb).
# 
# ![CMoore orbit](images/CMoore1993.gif) <center>Figure-8 orbit discovered by C. Moore in 1993 [1].</center>
# 
# 
# First we import the necessary libraries and set some common figure parameters.

# In[1]:


# Import libraries
import numpy as np

import time




# ### Equations of motion
# 
# The gravitational pull between two objects is under classical conditions given by Newton's law of gravitation,
# 
# $$
# \vec{F}_{21}(t)=\vec{F}_{12}(t) = -\frac{Gm_1m_2}{{\vec{r_{12}}(t)}^3}\vec r_{12},
# $$
# 
# where $m_1$ and $m_2$ are the masses of the two objects, $r$ is the distance between them and $G\approx 6.67\times 10^{-11} \,\text{m}^3/ \text{kg}\,\text{s}^2$ is the gravitational constant. Newton's  law holds if it is assumed that the masses of the objects are isotropically distributed.
# 
# Consider a three body problem with three objects given by masses $m_1$, $m_2$ and $m_3$. By the principle of superposition, the gravitational pull on an object will be the sum of the gravitational pull of all the other objects $F_1 = F_{12} + F_{13}$. Thus, the equations of motion (EoM) of say $m_1$ is given by
# 
# $$
# \ddot{\vec{r}}_1(t) = -\frac{Gm_2}{\left[\vec{r}_{2}(t)-\vec{r}_{1}(t)\right]^3}\left[\vec{r}_{2}(t)-\vec{r}_{1}(t)\right]-\frac{Gm_3}{\left[\vec{r}_{3}(t)-\vec{r}_{1}(t)\right]^3}\left[\vec{r}_{3}(t)-\vec{r}_{1}(t)\right],
# $$
# 
# $$
# \dot{\vec{r}}_1(t)=\vec{v}_1.
# $$
# 
# The EoM in this problem is a set of ODEs. By giving two initial conditions, e.g. the starting velocity and position, we can reduce the problem to two ODEs, where the next step of the first ODE depends on the previous step of the second ODE. The right hand side (RHS) of the EoM can be described by the following function:

# In[2]:


def RHS(t, y):
    """Calculate the RHS of the EoM, as described above.
    Parameters:
        y: array. Vector of length 12 holding the current position and velocity of the three objects 
           in the following manner: y = [x1, y2, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3].
    Returns:
        z: array. Vector of length 12 holding the derivative of the current position and velocity 
           (the velocity and acceleration) of the three object in the following manner:
           z = [vx1, vy1, vx2, vy2, vx3, vy3, ax1, ay1, ax2, ay2, ax3, ay3].
    """
    
    # Allocate a vector to hold the output values
    z = np.zeros(12)
    # Define initial velocities and distances between objects
    z[:6] = [y[6], y[7], y[8], y[9], y[10], y[11]]
    r21 = ((y[2] - y[0])**2.0 + (y[3] - y[1])**2.0)**0.5
    r31 = ((y[4] - y[0])**2.0 + (y[5] - y[1])**2.0)**0.5
    r32 = ((y[4] - y[2])**2.0 + (y[5] - y[3])**2.0)**0.5
    # Pairwise forces
    Fx21 = G*m2*m1*(y[2] - y[0])/r21**3.0
    Fy21 = G*m2*m1*(y[3] - y[1])/r21**3.0
    Fx31 = G*m3*m1*(y[4] - y[0])/r31**3.0
    Fy31 = G*m3*m1*(y[5] - y[1])/r31**3.0
    Fx32 = G*m3*m2*(y[4] - y[2])/r32**3.0
    Fy32 = G*m3*m2*(y[5] - y[3])/r32**3.0
    # Accelerations
    z[6] = (Fx21 + Fx31)/m1
    z[7] = (Fy21 + Fy31)/m1
    z[8] = (-Fx21 + Fx32)/m2
    z[9] = (-Fy21 + Fy32)/m2
    z[10] = (-Fx31 - Fx32)/m3
    z[11] = (-Fy31 - Fy32)/m3
    
    return z



# Furthermore, in this setup the absolute angular momentum $\vec L = \vec R\times m\vec v$ stays constant, and can be calculated by:


def angularMomentum(y):
    """Calculate absolute angular momentum of the three body system.
    Parameters:
        y:          array. Vector of length 12 holding the current position and velocity of the three objects
                    in the following manner: y = [x1, y2, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3].
    Returns:
        L1, L2, L3: array. Total absolute angular momentum of the system.
    """
    
    L1 = m1*(y[0]*y[7] - y[1]*y[6])
    L2 = m2*(y[2]*y[9] - y[3]*y[8])
    L3 = m3*(y[4]*y[11] - y[5]*y[10])
    
    return [L1, L2, L3]


# ### Embedded Runge-Kutta pair
# 
# We now implement the embedded Runge-Kutta pair (often called an adaptive Runge-Kutta method) to solve the EoM. In short, it is a scheme that uses two different Runge-Kutta methods of different order to get an estimate of the local truncation error. Thus, it is possible to more or less decide what accuracy we want the solution to have by adjusting the step size for each iteration. Another advantage of the adaptive step size method is that we achieve better accuracy where it is needed and lower accuracy where it is not (an example will follow). However, these methods may become more computationally demanding, and hence won't improve our implementation in every case.
# 
# The implementation can also be done with a constant step size method, which is done in the animation section below.
# 
# We are going to use the Runge-Kutta-Fehlberg order 4 / order 5 embedded pair (RKF45) as described in [Adaptive Runge-Kutta Methods](https://nbviewer.jupyter.org/urls/www.numfys.net/media/notebooks/adaptive_runge_kutta_methods.ipynb):

# In[5]:


def ode45(f,t,y,h):
    """Calculate next step of an initial value problem (IVP) of an ODE with a RHS described
    by the RHS function with an order 4 approx. and an order 5 approx.
    Parameters:
        t: float. Current time.
        y: float. Current step (position).
        h: float. Step-length.
    Returns:
        q: float. Order 2 approx.
        w: float. Order 3 approx.
    """
    
    s1 = f(t, y)
    s2 = f(t + h/4.0, y + h*s1/4.0)
    s3 = f(t + 3.0*h/8.0, y + 3.0*h*s1/32.0 + 9.0*h*s2/32.0)
    s4 = f(t + 12.0*h/13.0, y + 1932.0*h*s1/2197.0 - 7200.0*h*s2/2197.0 + 7296.0*h*s3/2197.0)
    s5 = f(t + h, y + 439.0*h*s1/216.0 - 8.0*h*s2 + 3680.0*h*s3/513.0 - 845.0*h*s4/4104.0)
    s6 = f(t + h/2.0, y - 8.0*h*s1/27.0 + 2*h*s2 - 3544.0*h*s3/2565 + 1859.0*h*s4/4104.0 - 11.0*h*s5/40.0)
    w = y + h*(25.0*s1/216.0 + 1408.0*s3/2565.0 + 2197.0*s4/4104.0 - s5/5.0)
    q = y + h*(16.0*s1/135.0 + 6656.0*s3/12825.0 + 28561.0*s4/56430.0 - 9.0*s5/50.0 + 2.0*s6/55.0)
    
    return w, q


# To get some basis for comparison we will also use the Ordinary (fourth order) Runge-Kutta method, as described in [Runge Kutta Method](https://nbviewer.jupyter.org/urls/www.numfys.net/media/notebooks/runge_kutta_method.ipynb) (this method will be used to make animations):

# In[6]:


def rk4step(f, t, y, h):
    """Calculate next step of an IVP of an ODE with a RHS described by the RHS function with RK4.
    Parameters:
        f: function. Right hand side of the ODE.
        t: float. Current time.
        y: float. Current step (position).
        h: float. Step-length.
    Returns:
        q: float. Order 2 approx.
        w: float. Order 3 approx.
    """
    
    s1 = f(t, y)
    s2 = f(t + h/2.0, y + h*s1/2.0)
    s3 = f(t + h/2.0, y + h*s2/2.0)
    s4 = f(t + h, y + h*s3)
    
    return y + h/6.0*(s1 + 2.0*s2 + 2.0*s3 + s4)


def threeBody(M1,M2,M3,x1,y1,x2,y2,x3,y3,vx1,vy1,vx2,vy2,vx3,vy3):
# ### Computations
# 
# Time to put it all together and plot the results. Initially, this solution describes a three body problem, but by choosing one of the masses equal to zero, the system will behave as if it is a two body system.
# 
# To start with, we will choose initial conditions and set global constants:


    # Set gravitaional constant and masses.
    # The gravitaional constant is set to 1 for simplicity.
    global G; G = 1.
    global m1; m1 = M1
    global m2; m2 = M2
    global m3; m3 = M3
    
    
    # Period of calculations
    T = 5
    # Tolerance
    TOL = 0.00001
    # Maximum number of steps
    maxi = 1000
    # "Protector-constant" for small w
    theta = 0.001
    # Number of steps (RK4)
    n = 1000

    # Different initial conditions to try out, on the form
    # y = [x1, y2, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]

    z0 = [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]
    # z0 = [2., 2., 0., 0., -2., -2., 0.2, -0.2, 0., 0., -0.2, 0.2]
    # z0 = [-0.970, 0.243, 0.970, -0.243, 0., 0., -0.466, -0.433, -0.466, -0.433, 2*0.466, 2*0.433]
    # z0 = [2., 0., -2., 0., 0., 0., 0., -0.6, -0.6, 0., 0., 0.]
    #z0 = [1., 0.000001, -1., 0., 0., 0., 0., -0.4, 0., 0.4, 0., 0.]


    # In[10]:


    # Set constant step size
    h = T/n

    # Set initial time
    t = 0.

    # Allocate matrices and fill with initial conditions
    Z2 = np.zeros((12, n+1))
    Z2[:, 0] = z0
    

    tic = time.time()
    for i in range(0, n):
        Z2[:, i+1] = rk4step(RHS, t, Z2[:, i], h)
        t += h


    print("%.5f s, run time of RK4 method, with %i steps."% (time.time() - tic, n))


    # Position
    res = Z2[:,-1]
    return res
