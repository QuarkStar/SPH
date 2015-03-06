from particle import Particle
import numpy as np
import cli

"""
This is the framework for iterating over a list of particles, computing particle accelerations, and numerically integrating their equations of motion.
"""

__author__ = "Colby"
__version__ = "1.0.1"

""" THIS VERSION HAS NOT BEEN TESTED, BUT RUNS SUCCESSFULLY AT THE VERY LEAST """


def Newtonian_gravity(p,q):
	# Newton's gravitational constant
	CONST_G = 6.67384 # * 10^(-11) m^3 kg^-1 s^-2
	
	'''
	F = (m_p)a = G(m_p)(m_q)(r)/r^3 -> a = (G * m_q)(r)/(g(r,r)^(3/2)), with g(_,_) the Euclidian inner product
	Note that this is all in the r-direction vectorially
	'''

	r = q.pos - p.pos # separation vector
	R = np.sqrt(r.dot(r)) # magnitude of the separation vector
	return ((CONST_G * q.mass) / (R**3)) * r


def sim(particles, bound, kernel, maxiter, pnum, smooth, t_norm, x_norm, interval):
    CONST_H = 1.0   # size of timestep (this should come from config file)
#    CONST_T_MAX = 10    # max iteration time (this should come from config file)
    CONST_T_MAX = maxiter
    t = 0.0     # elapsed time

    '''
	So we can do this one of two ways.
	1) Keep only one copy of the system in memory.
	   This is what is implemented here. This does not require
	   data duplication, but necessitates two iterations through
	   the list.
	2) Keep two lists. One for t = t_N, one for t = t_(N+1).
	   This way we can remove a for-loop, but requires more memory.
	Luckily, it is likely these problems only affect the serial algorithm.
	'''
	
    save = 0
    while(t < CONST_T_MAX):
        # while CONST_T_MAX = 60 and interval = 10
        if (save*interval) == t:
            print "[+] Saved @ iteration %d" % int(t)
            save = save+1

		# main simulation loop
        for p in particles:
			# preemptively start the Velocity Verlet computation (first half of velocity update part)
			p.vel += (CONST_H/2.0) * p.acc
			temp = p.acc
			p.acc = 0
			for q in particles:
			    # Calculate gravitational pull for each particle on every OTHER particle
				if(p.id != q.id):
					p.acc += Newtonian_gravity(p,q)
			# finish velocity update
			p.vel += (CONST_H/2.0) * p.acc

        '''
        Velocity Verlet integration: Works only assuming force is velocity-independent
        http://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
        '''

        for p in particles:
        	# perform position update
        	p.pos += CONST_H * (p.vel + (CONST_H/2.0)*temp)

        t += CONST_H # advance time

    print "[+] Saved @ iteration %d \t(last iteration)\n" % int(t)
    return t    # returns the last t-value, which is useful for displaying total iterations