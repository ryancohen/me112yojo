"""
ME 112, Project 2
R Cohen, Feb 2019

Full electro-dynamic analysis of simple jumping robot.
"""

"""
implicit assumptions:
    - symmetric leg lengths (top and bottom)
    - tensile spring (elastic)
    - number of legs
    - number of sets of legs
"""

import params
import numpy as np
import pdb

k_s = np.nan
theta_0 = np.nan
N = np.nan

def calc_motor_speed(T_m):
    T_em = T_m + params.T_fric
    i = T_em/params.k_m
    V_em = params.V_b - i*params.R_m
    if V_em <= 0:
        raise Exception("Motor stalled.")
    w_m = V_em/params.k_m
    return w_m

def calc_motor_power_in(T_m):
    T_em = T_m + params.T_fric
    i = T_em/params.k_m
    return i*params.V_b

def calc_loading_speed(w_m):
    w_shaft = w_m/N
    v_loading = w_shaft*params.r_shaft
    return v_loading


def calc_motor_torque(F_T):
    T_shaft = F_T * params.r_shaft
    return T_shaft/N/params.eta_g


def calc_dx(theta):
    return 2*params.l*(np.cos(np.radians(theta)) - np.cos(np.radians(theta_0)))

def calc_vertical_force(theta):  # same for either F_t (string tension) or F_N
    dx = calc_dx(theta)
    F_spring = k_s * dx
    F_y = F_spring * np.tan(np.radians(theta))
    return F_y


def calc_spring_length(theta):
    return 2*params.l*np.cos(np.radians(theta)) + 0.0291  # add in distance between legs at base


def calc_angle_from_spring_length(length):
    return np.degrees(np.arccos((length - 0.0291)/2/params.l))

def run_dynamics_anal():
    n_sim = 5000  # number of steps in loading and unloading simulations

    # Loading
    t = np.linspace(0, params.t, n_sim)
    dt = params.t / n_sim
    theta = np.nan*np.zeros(n_sim)
    y = np.nan*np.zeros(n_sim)
    F_N = np.nan*np.zeros(n_sim)
    P_in = np.nan*np.zeros(n_sim)

    theta[0] = theta_0
    y[0] = 2*params.l*np.sin(np.radians(theta_0))
    F_N[0] = 0
    P_in[0] = 0

    for index in range(n_sim - 1):
        if theta[index] <= 0:
            raise Exception("Robot finished loading " + str(params.t - t[index]) + " seconds too early.")
        F_t = calc_vertical_force(theta[index])
        T_m = calc_motor_torque(F_t)
        w_m = calc_motor_speed(T_m)
        P_in[index + 1] = calc_motor_power_in(T_m)
        dy_dt = calc_loading_speed(w_m)
        dy = dy_dt * dt
        y[index + 1] = y[index] - dy
        theta[index + 1] = np.degrees(np.arcsin(y[index + 1]/(2*params.l)))
        F_N[index+1] = F_t  # F_T on loading is same as F_N on release

    pdb.set_trace()
    print "The angle when fully loaded is " + str(theta[-1]) + " degrees."
    print "The average motor power is " + str(np.average(P_in)) + " watts."
    print "The maximum tensile force is " + str(np.nanmax(F_N))

    #Unloading
    # theta_unload = np.linspace(theta[-1], theta[0], n_sim)
    # F_N = np.nan*np.zeros(n_sim)
    # y_unload = np.nan*np.zeros(n_sim)
    #
    # for index in range(n_sim - 1):
    #     pass
        # this is just calculating loading down and then the same thing back up
    return -np.trapz(F_N, y)
    # TODO account for losses in upwards collision as it jumps
    # TODO choose gearbox ratio



if __name__ == '__main__':
    mode = 'SINGLE'
    # mode = 'OPTIMIZE'

    if mode == 'SINGLE':
        k_s = 760.05  # [N/m] spring constant
        theta_0 = calc_angle_from_spring_length(0.127)  # [degrees]
        N = 196.7
        print run_dynamics_anal()

    if mode == 'OPTIMIZE':
        max_energy = 0
        max_k = np.nan
        max_theta_0 = np.nan
        max_N = np.nan
        for N_1 in (11.6, 29.8, 76.5, 196.7, 505.9, 1300.9):
            for th_0 in range(45, 65, 5):
                for k in range(200, 800, 5):
                    try:
                        theta_0 = th_0
                        N = N_1
                        k_s = k
                        energy = run_dynamics_anal()
                        if energy > max_energy:
                            max_energy = energy
                            max_k = k_s
                            max_theta_0 = theta_0
                            max_N = N
                            print max_energy, k_s, N
                    except:
                        pass
        print max_energy
        print max_k
        print max_theta_0
        print max_N
