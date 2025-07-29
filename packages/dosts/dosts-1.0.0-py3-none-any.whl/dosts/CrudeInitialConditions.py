import numpy as np

class InitialConditions:
    index = 1 # index for keeping track when running different
    dragCoeff = 2
    crossSec = 10
    satMass = 60

    earthMass = 6E+24
    earthRadius = 6.37E+6
    gravConstant = 6.67E-11

    # initial values of satellite
    deltaV = 80.0
    initSatAlt = 400000
    initSatTheta = 0.0
    initSatPhi = np.pi / 3  # equatorial
    initSatLam = 0.0
    initSatRdot = 0.0
    initSatPhidot = np.radians(0.05) / 1.0
    
    v_circ = np.sqrt(gravConstant * earthMass / (earthRadius + initSatAlt))
    v_target = v_circ - deltaV
    term_sq = v_target ** 2 - ((earthRadius + initSatAlt) * initSatPhidot) ** 2
    if term_sq < 0:
        raise ValueError("phi_dot0 too large for given Δv or orbit height")
    
    initSatLamdot = - np.sqrt(term_sq) / ((earthRadius + initSatAlt) * np.sin(initSatPhi))

    # initial settings for bonus
    populatedRadius = 50000  # radius of populated area (m)
    populatedCenters = [
        (np.radians(51.5074), np.radians(-0.1278)),  # London
        (np.radians(40.7128), np.radians(-74.0060)),  # New York
        (np.radians(48.8566), np.radians(2.3522)),  # Paris
        (np.radians(34.0522), np.radians(-118.2437)),  # Los Angeles
    ]
    hThrust = 100000  # height of thrust (m)
    deltaV_from_thrust = 200  # velocity increasing value (m/s)
