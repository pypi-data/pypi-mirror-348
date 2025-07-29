import os
import ctypes
import numpy as np

# Find the shared library in the same directory as this file
lib_path = os.path.join(os.path.dirname(__file__), "libCO2CO2.so")
lib = ctypes.CDLL(lib_path)

# ---- Dimension and version getters ----

def get_p1b_dim():
    lib.get_p1b_dim.restype = ctypes.c_int
    return lib.get_p1b_dim()

def get_p2b_dim():
    lib.get_p2b_dim.restype = ctypes.c_int
    return lib.get_p2b_dim()

def get_p2b_4_dim():
    lib.get_p2b_4_dim.restype = ctypes.c_int
    return lib.get_p2b_4_dim()

def get_p2b_5_dim():
    lib.get_p2b_5_dim.restype = ctypes.c_int
    return lib.get_p2b_5_dim()

def get_sapt_dim():
    lib.get_sapt_dim.restype = ctypes.c_int
    return lib.get_sapt_dim()

def get_version():
    lib.get_version.restype = ctypes.c_char_p
    return lib.get_version().decode("utf-8")

# ---- 1B: Monomer energy, gradient, hessian ----

def p1b(xyz):
    """Monomer energy (expects xyz as length-9 np.array)"""
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    return lib.p1b(arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

def p1b_gradient(xyz):
    """Monomer gradient (returns np.array shape (9,))"""
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    grad = np.zeros(9, dtype=np.double)
    lib.p1b_gradient(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        grad.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return grad

def p1b_hessian_rev(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(9*9, dtype=np.double)
    lib.p1b_hessian_rev(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(9, 9)

def p1b_hessian_fwd(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(9*9, dtype=np.double)
    lib.p1b_hessian_fwd(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(9, 9)

# ---- 2B: Dimer energy, gradient, hessian (4th order) ----

def p2b_4(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    return lib.p2b_4(arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

def p2b_gradient_4(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    grad = np.zeros(18, dtype=np.double)
    lib.p2b_gradient_4(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        grad.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return grad

def p2b_hessian_4_rev(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.p2b_hessian_4_rev(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)

def p2b_hessian_4_fwd(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.p2b_hessian_4_fwd(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)

# ---- 2B: Dimer energy, gradient, hessian (5th order) ----

def p2b_5(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    return lib.p2b_5(arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

def p2b_gradient_5(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    grad = np.zeros(18, dtype=np.double)
    lib.p2b_gradient_5(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        grad.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return grad

def p2b_hessian_5_rev(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.p2b_hessian_5_rev(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)

def p2b_hessian_5_fwd(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.p2b_hessian_5_fwd(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)


# ---- SAPT-S: energy, gradient, hessian ----

def sapt(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    return lib.sapt(arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

def sapt_gradient(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    grad = np.zeros(18, dtype=np.double)
    lib.sapt_gradient(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        grad.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return grad

def sapt_hessian_rev(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.sapt_hessian_rev(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)

def sapt_hessian_fwd(xyz):
    arr = np.ascontiguousarray(xyz, dtype=np.double)
    hess = np.zeros(18*18, dtype=np.double)
    lib.sapt_hessian_fwd(
        arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        hess.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    )
    return hess.reshape(18, 18)


# Example usage
if __name__ == "__main__":
    # Example: dimer geometry
    xyz = np.array([
        0.0,  0.0,  0.000,
        0.0,  0.0, -1.162,
        0.0,  0.0,  1.162,
        3.75, 0.0,  0.000,
        3.75, 0.0, -1.162,
        3.75, 0.0,  1.162
    ], dtype=np.double)
    print("p2b_5 energy:", p2b_5(xyz))
    print("SAPT-S energy:", sapt(xyz))
    print("p2b_5 gradient:", p2b_gradient_5(xyz))
    print("p2b_5 Hessian:", p2b_hessian_5(xyz))