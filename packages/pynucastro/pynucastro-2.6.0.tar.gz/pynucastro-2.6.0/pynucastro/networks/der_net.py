import numba
import numpy as np
from numba.experimental import jitclass

from pynucastro.rates import Tfactors
from pynucastro.screening import PlasmaState, ScreenFactors

jp = 0
jhe4 = 1
jfe52 = 2
jco55 = 3
jni56 = 4
nnuc = 5

A = np.zeros((nnuc), dtype=np.int32)

A[jp] = 1
A[jhe4] = 4
A[jfe52] = 52
A[jco55] = 55
A[jni56] = 56

Z = np.zeros((nnuc), dtype=np.int32)

Z[jp] = 1
Z[jhe4] = 2
Z[jfe52] = 26
Z[jco55] = 27
Z[jni56] = 28

names = []
names.append("h1")
names.append("he4")
names.append("fe52")
names.append("co55")
names.append("ni56")

fe52_temp_array = np.array([0.01, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 275.0])
fe52_pf_array = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.000004, 1.000022, 1.000087, 1.000261, 1.006988, 1.036149, 1.097022, 1.187924, 1.302823, 1.435985, 1.583461, 1.743116, 2.097506, 2.50807, 3.004926, 3.650892, 4.565183, 8.23, 18.6, 49.1, 139.0, 399.0, 1140.0, 3190.0, 8840.0, 24200.0, 65800.0, 774000.0, 8800000.0, 97700000.0, 1070000000.0, 11500000000.0, 122000000000.0, 1290000000000.0, 13400000000000.0, 138000000000000.0, 1410000000000000.0, 1.42e+16, 1.42e+17, 1.41e+18, 1.39e+19, 1.36e+20, 1.32e+21, 1.27e+22, 1.22e+23, 1.16e+24, 1.1e+25, 1.04e+26, 9.76e+26, 9.14e+27, 8.53e+28, 7.93e+29, 7.36e+30, 6.82e+31, 6.3e+32, 5.81e+33, 5.35e+34, 4.52e+36, 3.81e+38, 3.2e+40, 2.69e+42, 2.26e+44, 1.91e+46, 1.61e+48, 1.07e+53])

co55_temp_array = np.array([0.01, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 275.0])
co55_pf_array = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.000002, 1.000033, 1.000215, 1.000878, 1.002654, 1.006532, 1.013879, 1.046472, 1.120054, 1.263795, 1.521559, 1.960822, 3.86, 8.81, 21.5, 54.5, 141.0, 369.0, 980.0, 2630.0, 7110.0, 19400.0, 241000.0, 3040000.0, 38200000.0, 476000000.0, 5850000000.0, 70800000000.0, 846000000000.0, 9970000000000.0, 116000000000000.0, 1340000000000000.0, 1.52e+16, 1.71e+17, 1.91e+18, 2.11e+19, 2.32e+20, 2.52e+21, 2.73e+22, 2.94e+23, 3.15e+24, 3.35e+25, 3.55e+26, 3.75e+27, 3.95e+28, 4.14e+29, 4.33e+30, 4.53e+31, 4.72e+32, 4.91e+33, 5.1e+34, 5.3e+35, 5.7e+37, 6.12e+39, 6.58e+41, 7.08e+43, 7.64e+45, 8.27e+47, 9e+49, 1.14e+55])

ni56_temp_array = np.array([0.01, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0, 170.0, 175.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 275.0])
ni56_pf_array = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.000001, 1.000018, 1.000148, 1.000669, 1.002103, 1.005194, 1.010868, 1.034512, 1.084652, 1.180068, 1.354034, 1.666865, 3.23, 8.19, 23.7, 71.7, 219.0, 664.0, 2010.0, 6080.0, 18300.0, 55200.0, 860000.0, 13100000.0, 196000000.0, 2860000000.0, 40600000000.0, 563000000000.0, 7640000000000.0, 102000000000000.0, 1330000000000000.0, 1.71e+16, 2.17e+17, 2.71e+18, 3.35e+19, 4.1e+20, 4.96e+21, 5.94e+22, 7.05e+23, 8.3e+24, 9.71e+25, 1.13e+27, 1.3e+28, 1.5e+29, 1.71e+30, 1.94e+31, 2.2e+32, 2.49e+33, 2.8e+34, 3.14e+35, 3.51e+36, 3.93e+37, 4.87e+39, 6.02e+41, 7.41e+43, 9.11e+45, 1.12e+48, 1.38e+50, 1.7e+52, 2.9e+57])

@jitclass([
    ("he4_fe52__ni56", numba.float64),
    ("p_co55__ni56", numba.float64),
    ("he4_fe52__p_co55", numba.float64),
    ("ni56__he4_fe52__derived", numba.float64),
    ("ni56__p_co55__derived", numba.float64),
    ("p_co55__he4_fe52__derived", numba.float64),
])
class RateEval:
    def __init__(self):
        self.he4_fe52__ni56 = np.nan
        self.p_co55__ni56 = np.nan
        self.he4_fe52__p_co55 = np.nan
        self.ni56__he4_fe52__derived = np.nan
        self.ni56__p_co55__derived = np.nan
        self.p_co55__he4_fe52__derived = np.nan

@numba.njit()
def ye(Y):
    return np.sum(Z * Y)/np.sum(A * Y)

@numba.njit()
def he4_fe52__ni56(rate_eval, tf):
    # fe52 + he4 --> ni56
    rate = 0.0

    # ths8r
    rate += np.exp(  66.6417 + -91.6819*tf.T913i + -9.51885*tf.T913
                  + -0.533014*tf.T9 + 0.0892607*tf.T953 + -0.666667*tf.lnT9)

    rate_eval.he4_fe52__ni56 = rate

@numba.njit()
def p_co55__ni56(rate_eval, tf):
    # co55 + p --> ni56
    rate = 0.0

    # ths8r
    rate += np.exp(  37.3736 + -38.1053*tf.T913i + -0.210947*tf.T913
                  + -2.68377*tf.T9 + 0.355814*tf.T953 + -0.666667*tf.lnT9)

    rate_eval.p_co55__ni56 = rate

@numba.njit()
def he4_fe52__p_co55(rate_eval, tf):
    # fe52 + he4 --> p + co55
    rate = 0.0

    # ths8r
    rate += np.exp(  62.2207 + -91.6819*tf.T913i + -0.329235*tf.T913
                  + -0.780924*tf.T9 + 0.0425179*tf.T953 + -0.666667*tf.lnT9)

    rate_eval.he4_fe52__p_co55 = rate

@numba.njit()
def ni56__he4_fe52__derived(rate_eval, tf):
    # ni56 --> he4 + fe52
    rate = 0.0

    # ths8r
    rate += np.exp(  91.62258922810439 + -92.801099329237*tf.T9i + -91.6819*tf.T913i + -9.51885*tf.T913
                  + -0.533014*tf.T9 + 0.0892607*tf.T953 + 0.833333*tf.lnT9)

    # setting he4 partition function to 1.0 by default, independent of T
    he4_pf = 1.0

    # interpolating fe52 partition function
    fe52_pf_exponent = np.interp(tf.T9, xp=fe52_temp_array, fp=np.log10(fe52_pf_array))
    fe52_pf = 10.0**fe52_pf_exponent

    # interpolating ni56 partition function
    ni56_pf_exponent = np.interp(tf.T9, xp=ni56_temp_array, fp=np.log10(ni56_pf_array))
    ni56_pf = 10.0**ni56_pf_exponent

    z_r = he4_pf*fe52_pf
    z_p = ni56_pf
    rate *= z_r/z_p

    rate_eval.ni56__he4_fe52__derived = rate

@numba.njit()
def ni56__p_co55__derived(rate_eval, tf):
    # ni56 --> p + co55
    rate = 0.0

    # ths8r
    rate += np.exp(  63.131770608640906 + -83.14741674893808*tf.T9i + -38.1053*tf.T913i + -0.210947*tf.T913
                  + -2.68377*tf.T9 + 0.355814*tf.T953 + 0.833333*tf.lnT9)

    # setting p partition function to 1.0 by default, independent of T
    p_pf = 1.0

    # interpolating co55 partition function
    co55_pf_exponent = np.interp(tf.T9, xp=co55_temp_array, fp=np.log10(co55_pf_array))
    co55_pf = 10.0**co55_pf_exponent

    # interpolating ni56 partition function
    ni56_pf_exponent = np.interp(tf.T9, xp=ni56_temp_array, fp=np.log10(ni56_pf_array))
    ni56_pf = 10.0**ni56_pf_exponent

    z_r = p_pf*co55_pf
    z_p = ni56_pf
    rate *= z_r/z_p

    rate_eval.ni56__p_co55__derived = rate

@numba.njit()
def p_co55__he4_fe52__derived(rate_eval, tf):
    # co55 + p --> he4 + fe52
    rate = 0.0

    # ths8r
    rate += np.exp(  61.443418619463486 + -9.65364776674457*tf.T9i + -91.6819*tf.T913i + -0.329235*tf.T913
                  + -0.780924*tf.T9 + 0.0425179*tf.T953 + -0.666667*tf.lnT9)

    # setting he4 partition function to 1.0 by default, independent of T
    he4_pf = 1.0

    # interpolating fe52 partition function
    fe52_pf_exponent = np.interp(tf.T9, xp=fe52_temp_array, fp=np.log10(fe52_pf_array))
    fe52_pf = 10.0**fe52_pf_exponent

    # setting p partition function to 1.0 by default, independent of T
    p_pf = 1.0

    # interpolating co55 partition function
    co55_pf_exponent = np.interp(tf.T9, xp=co55_temp_array, fp=np.log10(co55_pf_array))
    co55_pf = 10.0**co55_pf_exponent

    z_r = he4_pf*fe52_pf
    z_p = p_pf*co55_pf
    rate *= z_r/z_p

    rate_eval.p_co55__he4_fe52__derived = rate

def rhs(t, Y, rho, T, screen_func=None):
    return rhs_eq(t, Y, rho, T, screen_func)

@numba.njit()
def rhs_eq(t, Y, rho, T, screen_func):

    tf = Tfactors(T)
    rate_eval = RateEval()

    # reaclib rates
    he4_fe52__ni56(rate_eval, tf)
    p_co55__ni56(rate_eval, tf)
    he4_fe52__p_co55(rate_eval, tf)

    # derived rates
    ni56__he4_fe52__derived(rate_eval, tf)
    ni56__p_co55__derived(rate_eval, tf)
    p_co55__he4_fe52__derived(rate_eval, tf)

    if screen_func is not None:
        plasma_state = PlasmaState(T, rho, Y, Z)

        scn_fac = ScreenFactors(2, 4, 26, 52)
        scor = screen_func(plasma_state, scn_fac)
        rate_eval.he4_fe52__ni56 *= scor
        rate_eval.he4_fe52__p_co55 *= scor

        scn_fac = ScreenFactors(1, 1, 27, 55)
        scor = screen_func(plasma_state, scn_fac)
        rate_eval.p_co55__ni56 *= scor
        rate_eval.p_co55__he4_fe52__derived *= scor

    dYdt = np.zeros((nnuc), dtype=np.float64)

    dYdt[jp] = (
       -rho*Y[jp]*Y[jco55]*rate_eval.p_co55__ni56
       -rho*Y[jp]*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       +rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__p_co55
       +Y[jni56]*rate_eval.ni56__p_co55__derived
       )

    dYdt[jhe4] = (
       -rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__ni56
       -rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__p_co55
       +Y[jni56]*rate_eval.ni56__he4_fe52__derived
       +rho*Y[jp]*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    dYdt[jfe52] = (
       -rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__ni56
       -rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__p_co55
       +Y[jni56]*rate_eval.ni56__he4_fe52__derived
       +rho*Y[jp]*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    dYdt[jco55] = (
       -rho*Y[jp]*Y[jco55]*rate_eval.p_co55__ni56
       -rho*Y[jp]*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       +rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__p_co55
       +Y[jni56]*rate_eval.ni56__p_co55__derived
       )

    dYdt[jni56] = (
       -Y[jni56]*rate_eval.ni56__he4_fe52__derived
       -Y[jni56]*rate_eval.ni56__p_co55__derived
       +rho*Y[jhe4]*Y[jfe52]*rate_eval.he4_fe52__ni56
       +rho*Y[jp]*Y[jco55]*rate_eval.p_co55__ni56
       )

    return dYdt

def jacobian(t, Y, rho, T, screen_func=None):
    return jacobian_eq(t, Y, rho, T, screen_func)

@numba.njit()
def jacobian_eq(t, Y, rho, T, screen_func):

    tf = Tfactors(T)
    rate_eval = RateEval()

    # reaclib rates
    he4_fe52__ni56(rate_eval, tf)
    p_co55__ni56(rate_eval, tf)
    he4_fe52__p_co55(rate_eval, tf)

    # derived rates
    ni56__he4_fe52__derived(rate_eval, tf)
    ni56__p_co55__derived(rate_eval, tf)
    p_co55__he4_fe52__derived(rate_eval, tf)

    if screen_func is not None:
        plasma_state = PlasmaState(T, rho, Y, Z)

        scn_fac = ScreenFactors(2, 4, 26, 52)
        scor = screen_func(plasma_state, scn_fac)
        rate_eval.he4_fe52__ni56 *= scor
        rate_eval.he4_fe52__p_co55 *= scor

        scn_fac = ScreenFactors(1, 1, 27, 55)
        scor = screen_func(plasma_state, scn_fac)
        rate_eval.p_co55__ni56 *= scor
        rate_eval.p_co55__he4_fe52__derived *= scor

    jac = np.zeros((nnuc, nnuc), dtype=np.float64)

    jac[jp, jp] = (
       -rho*Y[jco55]*rate_eval.p_co55__ni56
       -rho*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jp, jhe4] = (
       +rho*Y[jfe52]*rate_eval.he4_fe52__p_co55
       )

    jac[jp, jfe52] = (
       +rho*Y[jhe4]*rate_eval.he4_fe52__p_co55
       )

    jac[jp, jco55] = (
       -rho*Y[jp]*rate_eval.p_co55__ni56
       -rho*Y[jp]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jp, jni56] = (
       +rate_eval.ni56__p_co55__derived
       )

    jac[jhe4, jp] = (
       +rho*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jhe4, jhe4] = (
       -rho*Y[jfe52]*rate_eval.he4_fe52__ni56
       -rho*Y[jfe52]*rate_eval.he4_fe52__p_co55
       )

    jac[jhe4, jfe52] = (
       -rho*Y[jhe4]*rate_eval.he4_fe52__ni56
       -rho*Y[jhe4]*rate_eval.he4_fe52__p_co55
       )

    jac[jhe4, jco55] = (
       +rho*Y[jp]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jhe4, jni56] = (
       +rate_eval.ni56__he4_fe52__derived
       )

    jac[jfe52, jp] = (
       +rho*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jfe52, jhe4] = (
       -rho*Y[jfe52]*rate_eval.he4_fe52__ni56
       -rho*Y[jfe52]*rate_eval.he4_fe52__p_co55
       )

    jac[jfe52, jfe52] = (
       -rho*Y[jhe4]*rate_eval.he4_fe52__ni56
       -rho*Y[jhe4]*rate_eval.he4_fe52__p_co55
       )

    jac[jfe52, jco55] = (
       +rho*Y[jp]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jfe52, jni56] = (
       +rate_eval.ni56__he4_fe52__derived
       )

    jac[jco55, jp] = (
       -rho*Y[jco55]*rate_eval.p_co55__ni56
       -rho*Y[jco55]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jco55, jhe4] = (
       +rho*Y[jfe52]*rate_eval.he4_fe52__p_co55
       )

    jac[jco55, jfe52] = (
       +rho*Y[jhe4]*rate_eval.he4_fe52__p_co55
       )

    jac[jco55, jco55] = (
       -rho*Y[jp]*rate_eval.p_co55__ni56
       -rho*Y[jp]*rate_eval.p_co55__he4_fe52__derived
       )

    jac[jco55, jni56] = (
       +rate_eval.ni56__p_co55__derived
       )

    jac[jni56, jp] = (
       +rho*Y[jco55]*rate_eval.p_co55__ni56
       )

    jac[jni56, jhe4] = (
       +rho*Y[jfe52]*rate_eval.he4_fe52__ni56
       )

    jac[jni56, jfe52] = (
       +rho*Y[jhe4]*rate_eval.he4_fe52__ni56
       )

    jac[jni56, jco55] = (
       +rho*Y[jp]*rate_eval.p_co55__ni56
       )

    jac[jni56, jni56] = (
       -rate_eval.ni56__he4_fe52__derived
       -rate_eval.ni56__p_co55__derived
       )

    return jac
