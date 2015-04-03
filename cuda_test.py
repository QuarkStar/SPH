from particle import Particle
from gpu_interface import ParticleGPUInterface


# Generate test particles
particles = [
	Particle(2,2,2,2,2,2,2,2),
	Particle(3,3,3,3,3,3,3,3),
	Particle(4,4,4,4,4,4,4,4),
	Particle(5,5,5,5,5,5,5,5),
	Particle(6,6,6,6,6,6,6,6)
]

# Print initial particle states
print "Initial states"
for particle in particles:
	print particle.formatProperties()

# Initialize the gpu interface, pass in particles
gpu_particles = ParticleGPUInterface(particles)

# Calls the demo function on GPU, no data transfered back
# Formula for demo function: id[i] = mass[i] + pos_x[i]
gpu_particles.demo_particle_function()

# Transfer the results back to CPU
updated_particles = gpu_particles.getResultsFromDevice()

print "ID = MASS + POS_X"
# Print final particle states
for particle in updated_particles:
	print particle.formatProperties()


# Calls the demo function on GPU, no data transfered back
# Formula for demo function: id[i] = mass[i] + pos_x[i]
gpu_particles.demo_particle_function_with_argument(500)

# Transfer the results back to CPU
updated_particles = gpu_particles.getResultsFromDevice()
print "ID = ID + 500"
# Print final particle states
for particle in updated_particles:
	print particle.formatProperties()