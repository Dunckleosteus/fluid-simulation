import numpy as np
from matplotlib import pyplot

def distance(x1, y1, x2, y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

plot_every = 50

def main():
    # define variables
    Nx = 400 # width of the simulation
    Ny = 100 # height of the simulation
    tau = .53 # kinematic viscosity
    Nt = 3000 # iterations through time

    # lattice speeds ands weights
    # defining discrete velocity
    NL = 9
    # the length of all these lists should be 9
    cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1]) # checked
    cys = np.array([0, 1, 1, 0, -1, -1,-1, 0, 1]) # checked
    # define wiegths = values assigned to each of the note, linked to Navier-Stokes
    weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36]) # checked

    # Initial conditions
    ## Adding slight inconsistencies (mesoscopic velocity)
    F = np.ones((Ny, Nx, NL)) + .01 * np.random.randn(Ny, Nx, NL) # checked
    # assigning right velocity
    F[:, :, 3] = 2.3 # checked

    # defining geometry
    cylinder = np.full((Ny, Nx), False) # if the value is false = empty space, else it's an obstacle

    for y in range(0, Ny): # checked
        for x in range(0, Nx):
            if(distance(Nx//4, Ny//2, x, y)<20):
                cylinder[y][x] = True

    # main loop
    for it in range(Nt):
        print(it)
        F[:, -1, [6, 7, 8]] = F[:, -2, [6, 7, 8]]
        F[:,  0, [2, 3, 4]] = F[:, 1, [2, 3, 4]]
        # streaming step
        for i, cx, cy in zip(range(NL), cxs, cys): #checked
            F[:, :, i] = np.roll(F[:, :, i], cx, axis=1)
            F[:, :, i] = np.roll(F[:, :, i], cy, axis=0)

        # calculating collisions
        bndryF = F[cylinder, :]
        # if the point is in the cylinder then invert the velocity to make it travel in the other direction
        bndryF = bndryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]] # checked

        # defining variables for calculations
        rho = np.sum(F, 2) # density
        # now doing same thing for momentum
        ux = np.sum(F * cxs, 2)/rho # momentum
        uy = np.sum(F * cys, 2)/rho

        # apply boundaries
        F[cylinder, :] = bndryF
        ux[cylinder] = 0
        uy[cylinder] = 0

        # collision
        Feq = np.zeros(F.shape) # f equilibrium
        for i, cx, cy, w in zip(range(NL), cxs, cys, weights):
            Feq[:, :, i] = rho * w * (
                1 + 3 * (cx*ux + cy*uy) + 9 * (cx*ux + cy*uy)**2 / 2 -3 * (ux**2 + uy**2)/2
            )
        F = F + -(1/tau) * (F-Feq)
    
        if (it%plot_every == 0):
            pyplot.imshow(np.sqrt(ux**2 + uy**2))
            pyplot.pause(0.01)
            pyplot.cla


if __name__ == "__main__":
    main()
