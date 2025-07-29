from typing import Callable
from collections import defaultdict

import scipy
from numba import njit, prange
import numpy as npu

import skfem
from skfem import Basis, asm
from skfem.helpers import ddot, sym_grad, trace, eye
from skfem.models.elasticity import lame_parameters
from skfem.assembly import BilinearForm
from skfem import asm, Basis
from skfem import BilinearForm
from skfem.helpers import transpose
from skfem.models.elasticity import lame_parameters
from skfem.models.elasticity import linear_elasticity
from skfem.helpers import identity
from skfem import Functional
from skfem.helpers import transpose
# from skfem import asm, LinearForm

import numpy as np


@njit
def simp_interpolation(rho, E0, Emin, p):
    E_elem = Emin + (E0 - Emin) * (rho ** p)
    return E_elem


@njit
def ramp_interpolation(rho, E0, Emin, p):
    """
    ram: E(rho) = Emin + (E0 - Emin) * [rho / (1 + p(1 - rho))]
    Parameters:
      rho  : array of densities in [0,1]
      E0   : maximum Young's modulus
      Emin : minimum Young's modulus
      p    : ram parameter
    Returns:
      array of element-wise Young's moduli
    """
    # avoid division by zero
    E_elem = Emin + (E0 - Emin) * (rho / (1.0 + p*(1.0 - rho)))
    return E_elem


simp_interpolation_numba = simp_interpolation
ramp_interpolation_numba = ramp_interpolation


@njit
def lam_mu(E, nu):
    lam = (nu * E) / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = E / (2.0 * (1.0 + nu))
    return lam, mu


def assemble_stiffness_matrix(
    basis: Basis,
    rho: np.ndarray,
    E0: float, Emin: float, p: float, nu: float,
    elem_func: Callable=simp_interpolation
):
    """
    Assemble the global stiffness matrix for 3D linear elasticity with SIMP material interpolation.
    
    Parameters:
        basis : skfem Basis for the mesh (built with ElementVector(ElementTetP1) on MeshTet).
        rho   : 1D array of length n_elements with density values for each element.
        E0    : Young's modulus of solid material (for rho = 1).
        Emin  : Minimum Young's modulus for void material (for rho = 0, ensures numerical stability).
        p     : Penalization power for SIMP (typically >= 1, e.g., 3 for standard topology optimization).
        nu    : Poisson's ratio (assumed constant for all elements).
    
    Returns:
        Sparse stiffness matrix (scipy.sparse.csr_matrix) assembled for the given density distribution.
    """
    # 1. Compute Young's modulus for each element using SIMP / RAMP
    E_elem = elem_func(rho, E0, Emin, p)  # array of size [n_elements]
    
    # 2. Compute Lamé parameters for each element
    lam = (nu * E_elem) / ((1.0 + nu) * (1.0 - 2.0 * nu))   # first Lamé parameter λ_e per element
    mu  = E_elem / (2.0 * (1.0 + nu))                      # second Lamé parameter (shear modulus) μ_e per element
    # lam, mu = lam_mu(E_elem, nu)
    
    # Reshape to allow broadcasting over integration points (each as [n_elem, 1] column vectors)
    lam = lam.reshape(-1, 1)
    mu  = mu.reshape(-1, 1)
    
    # 3. Define the bilinear form for elasticity (integrand of stiffness entries)
    @BilinearForm
    def stiffness_form(u, v, w):
        # sym_grad(u) is the strain tensor ε(u) at integration points
        # trace(sym_grad(u)) is the volumetric strain (divergence of u)
        # ddot(A, B) computes the double-dot (Frobenius) product of two matrices A and B
        strain_u = sym_grad(u)
        strain_v = sym_grad(v)
        # Apply Lamé parameters for each element (w corresponds to integration context)
        # lam and mu are arrays of shape [n_elem, 1], broadcasting to [n_elem, n_quad] with strain arrays
        term_volumetric = lam * trace(strain_u) * trace(strain_v)      # λ * tr(ε(u)) * tr(ε(v))
        term_dev = 2.0 * mu * ddot(strain_u, strain_v)                 # 2μ * (ε(u) : ε(v))
        return term_volumetric + term_dev  # integrand for stiffness
    
    # 4. Assemble the stiffness matrix using the basis
    K = asm(stiffness_form, basis)
    return K



@njit(parallel=True)
def _get_elements_volume_tet_numba(t_conn, p_coords) -> np.ndarray:
    n_elements = t_conn.shape[1]
    elements_volume = np.zeros(n_elements)
    for e in prange(n_elements):
        n0, n1, n2, n3 = t_conn[:, e]
        
        v1 = p_coords[:, n1] - p_coords[:, n0]
        v2 = p_coords[:, n2] - p_coords[:, n0]
        v3 = p_coords[:, n3] - p_coords[:, n0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0
        elements_volume[e] = vol

    return elements_volume


def _get_elements_volume_tet(t_conn, p_coords) -> np.ndarray:
    n_elements = t_conn.shape[1]
    elements_volume = np.zeros(n_elements)
    
    # for e in prange(n_elements):
    for e in range(n_elements):
        n0, n1, n2, n3 = t_conn[:, e]
        
        v1 = p_coords[:, n1] - p_coords[:, n0]
        v2 = p_coords[:, n2] - p_coords[:, n0]
        v3 = p_coords[:, n3] - p_coords[:, n0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0

        if vol < -1e-12:
            print("Element", e, "has negative volume:", vol)
            raise ValueError("!!!")
        
        elements_volume[e] = vol

    return elements_volume


@njit
def _tet_volume_numba(p0, p1, p2, p3):
    v1 = p1 - p0
    v2 = p2 - p0
    v3 = p3 - p0
    return abs(np.dot(np.cross(v1, v2), v3)) / 6.0


def _get_elements_volume_hex(t_conn, p_coords) -> np.ndarray:
    """
    Compute volume of Hex elements by decomposing into 6 tetrahedra.

    Parameters
    ----------
    t_conn : (8, n_elem) int
        Hexahedral element connectivity
    p_coords : (3, n_nodes) float
        Node coordinates

    Returns
    -------
    elements_volume : (n_elem,) float
        Approximate volumes
    """
    n_elements = t_conn.shape[1]
    elements_volume = np.zeros(n_elements)

    for e in prange(n_elements):
        n = t_conn[:, e]

        #   7--------6
        #  /|       /|
        # 4--------5 |
        # | |      | |
        # | 3------|-2
        # |/       |/
        # 0--------1
        vol = 0.0
        vol += _tet_volume_numba(p_coords[:, n[0]], p_coords[:, n[1]], p_coords[:, n[3]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[2]], p_coords[:, n[3]], p_coords[:, n[6]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[5]], p_coords[:, n[6]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[3]], p_coords[:, n[6]], p_coords[:, n[7]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[3]], p_coords[:, n[6]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[6]], p_coords[:, n[5]], p_coords[:, n[4]])

        elements_volume[e] = vol

    return elements_volume


@njit(parallel=True)
def _get_elements_volume_hex_numba(t_conn, p_coords) -> np.ndarray:
    """
    Compute volume of Hex elements by decomposing into 6 tetrahedra.

    Parameters
    ----------
    t_conn : (8, n_elem) int
        Hexahedral element connectivity
    p_coords : (3, n_nodes) float
        Node coordinates

    Returns
    -------
    elements_volume : (n_elem,) float
        Approximate volumes
    """
    n_elements = t_conn.shape[1]
    elements_volume = np.zeros(n_elements)

    for e in prange(n_elements):
        n = t_conn[:, e]

        # Tetra 6分割 (番号は Gmsh の Hex8 想定：0-7)
        #   7--------6
        #  /|       /|
        # 4--------5 |
        # | |      | |
        # | 3------|-2
        # |/       |/
        # 0--------1

        vol = 0.0
        vol += _tet_volume_numba(p_coords[:, n[0]], p_coords[:, n[1]], p_coords[:, n[3]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[2]], p_coords[:, n[3]], p_coords[:, n[6]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[5]], p_coords[:, n[6]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[3]], p_coords[:, n[6]], p_coords[:, n[7]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[3]], p_coords[:, n[6]], p_coords[:, n[4]])
        vol += _tet_volume_numba(p_coords[:, n[1]], p_coords[:, n[6]], p_coords[:, n[5]], p_coords[:, n[4]])

        elements_volume[e] = vol

    return elements_volume




def get_elements_volume(
    mesh: skfem.Mesh
) -> np.ndarray:
    if isinstance(mesh, skfem.MeshTet):
        return _get_elements_volume_tet(mesh.t, mesh.p)
    elif isinstance(mesh, skfem.MeshHex):
        return _get_elements_volume_hex(mesh.t, mesh.p)
    else:
        raise NotImplementedError("skfem.MeshTet or skfem.MeshHex")
    


@njit(parallel=True)
def _assemble_stiffness_matrix_numba_tet(
    p_coords, t_conn,
    element_dofs, E0, Emin, nu, E_elem
):
    n_elements = t_conn.shape[1]
    data = np.zeros(n_elements * 144)  # 12x12 per element
    row = np.zeros_like(data, dtype=np.int32)
    col = np.zeros_like(data, dtype=np.int32)

    # Base elasticity matrix (for E=1.0, scaled later by E_eff)
    lam_base, mu_base = lam_mu(E0, nu)
    C0 = np.array([
        [1 - nu,    nu,       nu,       0,                   0,                   0                  ],
        [nu,        1 - nu,   nu,       0,                   0,                   0                  ],
        [nu,        nu,       1 - nu,   0,                   0,                   0                  ],
        [0,         0,        0,        (1 - 2*nu) / 2.0,    0,                   0                  ],
        [0,         0,        0,        0,                   (1 - 2*nu) / 2.0,    0                  ],
        [0,         0,        0,        0,                   0,                   (1 - 2*nu) / 2.0 ]
    ])
    C0 *= lam_base

    for e in prange(n_elements):
        nodes = t_conn[:, e]
        coords = p_coords[:, nodes]  # shape (3, 4)

        n0, n1, n2, n3 = t_conn[:, e]
        v1 = p_coords[:, n1] - p_coords[:, n0]
        v2 = p_coords[:, n2] - p_coords[:, n0]
        v3 = p_coords[:, n3] - p_coords[:, n0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0

        M = np.ones((4, 4))
        for i in range(4):
            M[i, :3] = coords[:, i]
        
        # vol = abs(np.linalg.det(M)) / 6.0
        Minv = np.linalg.inv(M)
        grads = Minv[:3, :]  # shape (3, 4)

        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            B[0, 3*j    ] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j    ] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j    ] = dNdz

        E_eff = E_elem[e]
        C_e = C0 * (E_eff / E0)
        ke = B.T @ C_e @ B * vol

        dofs = element_dofs[:, e]
        for i in range(12):
            for j in range(12):
                idx = e * 144 + i * 12 + j
                data[idx] = ke[i, j]
                row[idx] = dofs[i]
                col[idx] = dofs[j]

    return data, (row, col)



@njit(parallel=True)
def _assemble_stiffness_matrix_hex8_gauss(
    p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem):
    n_elements = t_conn.shape[1]
    ndofs = 24  # 8 nodes * 3 dofs

    data = np.zeros(n_elements * ndofs * ndofs)
    row = np.zeros_like(data, dtype=np.int32)
    col = np.zeros_like(data, dtype=np.int32)

    lam = (nu * E0) / ((1.0 + nu) * (1.0 - 2.0 * nu))
    mu = E0 / (2.0 * (1.0 + nu))

    C0 = np.array([
        [lam + 2 * mu, lam,         lam,         0,       0,       0],
        [lam,          lam + 2 * mu, lam,         0,       0,       0],
        [lam,          lam,         lam + 2 * mu, 0,       0,       0],
        [0,            0,           0,            mu,      0,       0],
        [0,            0,           0,            0,       mu,      0],
        [0,            0,           0,            0,       0,       mu],
    ])

    # Gauss points and weights for 2x2x2 integration
    gp = np.array([ -np.sqrt(1/3), np.sqrt(1/3) ])
    weights = np.array([1.0, 1.0])

    for e in prange(n_elements):
        nodes = t_conn[:, e]
        coords = p_coords[:, nodes]  # (3, 8)
        E_eff = E_elem[e]
        C = C0 * (E_eff / E0)
        ke = np.zeros((24, 24))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    xi, eta, zeta = gp[i], gp[j], gp[k]
                    w = weights[i] * weights[j] * weights[k]

                    # Shape function derivatives wrt natural coordinates
                    dN_nat = np.array([
                        [-(1 - eta) * (1 - zeta), -(1 - xi) * (1 - zeta), -(1 - xi) * (1 - eta)],
                        [ (1 - eta) * (1 - zeta), -(1 + xi) * (1 - zeta), -(1 + xi) * (1 - eta)],
                        [ (1 + eta) * (1 - zeta),  (1 + xi) * (1 - zeta), -(1 + xi) * (1 + eta)],
                        [-(1 + eta) * (1 - zeta),  (1 - xi) * (1 - zeta), -(1 - xi) * (1 + eta)],
                        [-(1 - eta) * (1 + zeta), -(1 - xi) * (1 + zeta),  (1 - xi) * (1 - eta)],
                        [ (1 - eta) * (1 + zeta), -(1 + xi) * (1 + zeta),  (1 + xi) * (1 - eta)],
                        [ (1 + eta) * (1 + zeta),  (1 + xi) * (1 + zeta),  (1 + xi) * (1 + eta)],
                        [-(1 + eta) * (1 + zeta),  (1 - xi) * (1 + zeta),  (1 - xi) * (1 + eta)],
                    ]) / 8.0  # shape (8, 3)

                    J = np.zeros((3, 3))
                    for a in range(8):
                        for i_dim in range(3):
                            for j_dim in range(3):
                                J[i_dim, j_dim] += dN_nat[a, j_dim] * coords[i_dim, a]

                    detJ = np.linalg.det(J)
                    invJ = np.linalg.inv(J)
                    dN_global = dN_nat @ invJ.T  # (8, 3)

                    B = np.zeros((6, 24))
                    for a in range(8):
                        dNdx, dNdy, dNdz = dN_global[a]
                        B[0, 3*a]     = dNdx
                        B[1, 3*a + 1] = dNdy
                        B[2, 3*a + 2] = dNdz
                        B[3, 3*a]     = dNdy
                        B[3, 3*a + 1] = dNdx
                        B[4, 3*a + 1] = dNdz
                        B[4, 3*a + 2] = dNdy
                        B[5, 3*a + 2] = dNdx
                        B[5, 3*a]     = dNdz

                    ke += B.T @ C @ B * detJ * w

        dofs = element_dofs[:, e]
        for i in range(24):
            for j in range(24):
                idx = e * 24 * 24 + i * 24 + j
                data[idx] = ke[i, j]
                row[idx] = dofs[i]
                col[idx] = dofs[j]

    return data, (row, col)


def assemble_stiffness_matrix_numba(
    basis, rho, E0, Emin, pval, nu,
    elem_func: Callable=simp_interpolation_numba
):
    p_coords = basis.mesh.p
    t_conn = basis.mesh.t
    element_dofs = basis.element_dofs
    E_elem = elem_func(rho, E0, Emin, pval)
    
    if isinstance(basis.mesh, skfem.MeshTet):
        data, rowcol = _assemble_stiffness_matrix_numba_tet(
            p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem
        )
    elif isinstance(basis.mesh, skfem.MeshHex):
        raise NotImplementedError("use tet instead")
        # data, rowcol = _assemble_stiffness_matrix_hex8_gauss(
        #     p_coords, t_conn, element_dofs, E0, Emin, nu, E_elem
        # )
    else:
        raise ValueError("mesh is not tet nor hex")
    
    ndof = basis.N
    return scipy.sparse.coo_matrix(
        (data, rowcol), shape=(ndof, ndof)
    ).tocsr()


def assemble_stiffness_matrix_simp(
    basis: Basis,
    rho: np.ndarray,
    E0: float, Emin: float, p: float, nu: float
):
    return assemble_stiffness_matrix(
        basis,
        rho,
        E0, Emin, p, nu,
        elem_func=simp_interpolation
    )


def assemble_stiffness_matrix_ramp(
    basis: Basis,
    rho: np.ndarray,
    E0: float, Emin: float, p: float, nu: float
):
    return assemble_stiffness_matrix(
        basis,
        rho,
        E0, Emin, p, nu,
        elem_func=ramp_interpolation
    )


def adjacency_matrix(mesh: skfem.MeshTet):
    n_elements = mesh.t.shape[1]
    face_to_elements = defaultdict(list)
    for i in range(n_elements):
        tet = mesh.t[:, i]
        faces = [
            tuple(sorted([tet[0], tet[1], tet[2]])),
            tuple(sorted([tet[0], tet[1], tet[3]])),
            tuple(sorted([tet[0], tet[2], tet[3]])),
            tuple(sorted([tet[1], tet[2], tet[3]])),
        ]
        for face in faces:
            face_to_elements[face].append(i)

    adjacency = [[] for _ in range(n_elements)]
    for elems in face_to_elements.values():
        if len(elems) == 2:
            i, j = elems
            adjacency[i].append(j)
            adjacency[j].append(i)
    return adjacency


# def strain_energy_hdcode_numba(
#     u,
#     element_dofs,
#     node_coords,  # mesh.p
#     rho,
#     E0,
#     Emin,
#     penal,
#     nu0
# )
def strain_energy_hdcode(
    u,
    element_dofs,
    node_coords,
    rho,
    E0,
    Emin, penal, nu0
):
    """Compute element-wise strain energy for a 3D tetrahedral mesh using SIMP material interpolation."""
    # mesh = basis.mesh
    # Material constants for elasticity matrix
    lam_factor = lambda E: E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))  # common factor for isotropic C
    mu_factor  = lambda E: E / (2.0 * (1.0 + nu0))               # shear modulus μ

    n_elems = element_dofs.shape[1]  # number of elements (columns of element_dofs)
    energies = np.zeros(n_elems)
    # Precompute base elasticity matrix for E0 (could also compute fresh each time scaled by E_e)
    C0 = lam_factor(E0) * np.array([
        [1 - nu0,    nu0,       nu0,       0,                   0,                   0                  ],
        [nu0,        1 - nu0,   nu0,       0,                   0,                   0                  ],
        [nu0,        nu0,       1 - nu0,   0,                   0,                   0                  ],
        [0,          0,         0,         (1 - 2*nu0) / 2.0,   0,                   0                  ],
        [0,          0,         0,         0,                   (1 - 2*nu0) / 2.0,   0                  ],
        [0,          0,         0,         0,                   0,                   (1 - 2*nu0) / 2.0 ]
    ])
    # Loop over each element in the design domain
    for idx in range(n_elems):
        # Global DOF indices for this element and extract their coordinates
        edofs = element_dofs[:, idx]                  # 12 DOF indices (3 per node for 4 nodes)
        # Infer the 4 node indices (each node has 3 DOFs). We assume DOFs are grouped by node.
        node_ids = [int(edofs[3*j] // 3) for j in range(4)]
        # Coordinates of the 4 nodes (3x4 matrix)
        coords = node_coords[:, node_ids]
        # Build matrix M for shape function coefficient solve
        # Each row: [x_i, y_i, z_i, 1] for node i
        M = np.column_stack((coords.T, np.ones(4)))
        # Minv = np.linalg.inv(M)
        # Minv = np.linalg.solve(M, np.eye(3))
        Minv = np.linalg.pinv(M)
        # Gradients of shape functions (each column i gives grad(N_i) = [dN_i/dx, dN_i/dy, dN_i/dz])
        grads = Minv[:3, :]  # 3x4 matrix of gradients
        # Construct B matrix (6x12) for this element
        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            # Fill B for this node j
            B[0, 3*j    ] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j    ] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j    ] = dNdz
        # Compute volume of the tetrahedron (abs(det(M))/6)
        vol = abs(np.linalg.det(M)) / 6.0
        # Young's modulus for this element via SIMP
        E_eff = Emin + (rho[idx] ** penal) * (E0 - Emin)
        # Form elasticity matrix C_e (scale base matrix by E_eff/E0 since ν constant)
        C_e = C0 * (E_eff / E0)
        # Element nodal displacements
        u_e = u[edofs]
        # Compute strain = B * u_e
        strain = B.dot(u_e)
        # Strain energy density = 0.5 * strain^T * C_e * strain
        Ue = 0.5 * strain.dot(C_e.dot(strain)) * vol
        energies[idx] = Ue
    return energies


@njit
def strain_energy_hdcode_numba(
    u,
    element_dofs,
    node_coords,  # mesh.p
    rho,
    E0,
    Emin,
    penal,
    nu0
):
    lam_factor = lambda E: E / ((1.0 + nu0) * (1.0 - 2.0 * nu0))

    n_elems = element_dofs.shape[1]
    energies = np.zeros(n_elems)

    # Precompute elasticity matrix C0
    C0 = lam_factor(E0) * np.array([
        [1 - nu0,    nu0,       nu0,       0,                   0,                   0                  ],
        [nu0,        1 - nu0,   nu0,       0,                   0,                   0                  ],
        [nu0,        nu0,       1 - nu0,   0,                   0,                   0                  ],
        [0,          0,         0,         (1 - 2*nu0) / 2.0,   0,                   0                  ],
        [0,          0,         0,         0,                   (1 - 2*nu0) / 2.0,   0                  ],
        [0,          0,         0,         0,                   0,                   (1 - 2*nu0) / 2.0 ]
    ])

    for idx in range(n_elems):
        edofs = element_dofs[:, idx]
        node_ids = np.empty(4, dtype=np.int32)
        coords = np.empty((3, 4))
        
        for j in range(4):
            node_id = int(edofs[3 * j] // 3)
            node_ids[j] = node_id
            for d in range(3):
                coords[d, j] = node_coords[d, node_id]

        # Compute shape function gradients using geometric method
        v1 = coords[:, 1] - coords[:, 0]
        v2 = coords[:, 2] - coords[:, 0]
        v3 = coords[:, 3] - coords[:, 0]
        vol = np.dot(np.cross(v1, v2), v3) / 6.0

        if vol <= 0.0:
            raise ValueError(f"Negative or zero volume at element {idx}: {vol}")

        M = np.ones((4, 4))
        for i in range(4):
            for d in range(3):
                M[i, d] = coords[d, i]
        Minv = np.linalg.inv(M)
        grads = Minv[:3, :]  # ∇ϕ

        B = np.zeros((6, 12))
        for j in range(4):
            dNdx, dNdy, dNdz = grads[0, j], grads[1, j], grads[2, j]
            B[0, 3*j    ] = dNdx
            B[1, 3*j + 1] = dNdy
            B[2, 3*j + 2] = dNdz
            B[3, 3*j    ] = dNdy
            B[3, 3*j + 1] = dNdx
            B[4, 3*j + 1] = dNdz
            B[4, 3*j + 2] = dNdy
            B[5, 3*j + 2] = dNdx
            B[5, 3*j    ] = dNdz

        E_eff = Emin + (rho[idx] ** penal) * (E0 - Emin)
        C_e = C0 * (E_eff / E0)

        u_e = u[edofs]
        strain = B @ u_e
        Ue = 0.5 * strain @ (C_e @ strain) * abs(vol)
        energies[idx] = Ue

    return energies


@Functional
def _strain_energy_density_(w):
    grad = w['uh'].grad  # shape: (3, 3, nelems, nqp)
    symgrad = 0.5 * (grad + transpose(grad))  # same shape
    tr = trace(symgrad)
    I = eye(tr, symgrad.shape[0])  # shape: (3, 3, nelems, nqp)
    # mu, lam の shape: (nqp, nelems) → transpose to (nelems, nqp)
    mu = w['mu_elem'].T  # shape: (nelems, nqp)
    lam = w['lam_elem'].T  # shape: (nelems, nqp)
    # reshape to enable broadcasting
    mu = mu[None, None, :, :]  # → shape (1, 1, nelems, nqp)
    lam = lam[None, None, :, :]  # same

    stress = 2. * mu * symgrad + lam * I  # shape-compatible now
    return 0.5 * ddot(stress, symgrad)


def strain_energy_skfem(
    basis: skfem.Basis,
    rho: np.ndarray, u, 
    E0: float, Emin: float, p: float, nu: float,
    elem_func: Callable=simp_interpolation
) -> np.ndarray:

    uh = basis.interpolate(u)
    E_elem = elem_func(rho, E0, Emin, p) 
    lam_elem, mu_elem = lame_parameters(E_elem, nu)  # shape: (nelements,)
    n_qp = basis.X.shape[1]

    lam_elem = np.tile(lam_elem, (n_qp, 1))  # shape: (n_qp, n_elements)
    mu_elem = np.tile(mu_elem, (n_qp, 1))

    elem_energy = _strain_energy_density_.elemental(
        basis, uh=uh, lam_elem=lam_elem, mu_elem=mu_elem
    )
    return elem_energy


@Functional
def compute_element_stress_tensor(w):
    """
    Return stress tensor per element per quadrature point.
    Output shape: (3, 3, n_elem, n_qp)
    """
    grad = w['uh'].grad                          # shape: (3, 3, nelems, nqp)
    symgrad = 0.5 * (grad + transpose(grad))     # shape: same
    tr = trace(symgrad)                          # shape: (nelems, nqp)
    I = eye(tr, symgrad.shape[0])                # shape: (3, 3, nelems, nqp)

    mu = w['mu_elem'].T[None, None, :, :]        # shape: (1, 1, nelems, nqp)
    lam = w['lam_elem'].T[None, None, :, :]      # shape: same

    stress = 2. * mu * symgrad + lam * I         # shape: (3, 3, nelems, nqp)
    return stress


def stress_tensor_skfem(
    basis: skfem.Basis,
    rho: np.ndarray, u, 
    E0: float, Emin: float, p: float, nu: float,
    elem_func: Callable=simp_interpolation
):
    uh = basis.interpolate(u)
    E_elem = elem_func(rho, E0, Emin, p) 
    lam_elem, mu_elem = lame_parameters(E_elem, nu)  # shape: (nelements,)
    n_qp = basis.X.shape[1]

    lam_elem = np.tile(lam_elem, (n_qp, 1))  # shape: (n_qp, n_elements)
    mu_elem = np.tile(mu_elem, (n_qp, 1))

    stress_tensor = compute_element_stress_tensor.elemental(
        basis,
        uh=uh,
        # uh=u,
        lam_elem=lam_elem, mu_elem=mu_elem
    )
    return stress_tensor  # shape: (n_elem, n_qp, 3, 3)



def von_mises_from_stress_tensor(stress_tensor: np.ndarray) -> np.ndarray:
    """
    Compute Von Mises stress from full stress tensor.
    
    Parameters:
        stress_tensor: ndarray of shape (3, 3, n_elem, n_qp)

    Returns:
        von_mises: ndarray of shape (n_elem, n_qp)
    """
    s = stress_tensor
    s_xx = s[0, 0]
    s_yy = s[1, 1]
    s_zz = s[2, 2]
    s_xy = s[0, 1]
    s_yz = s[1, 2]
    s_zx = s[2, 0]
    
    return np.sqrt(
        0.5 * (
            (s_xx - s_yy)**2 +
            (s_yy - s_zz)**2 +
            (s_zz - s_xx)**2 +
            6 * (s_xy**2 + s_yz**2 + s_zx**2)
        )
    )


if __name__ == '__main__':
    
    import time
    import meshio
    import pyvista as pv
    from memory_profiler import profile

    @profile
    def test_1():
        from scitopt.mesh import toy_problem

        tsk = toy_problem.toy_msh("plate-0.2.msh")
        rho = np.ones(tsk.all_elements.shape)

        K1 = assemble_stiffness_matrix(
            tsk.basis, rho, tsk.E0, 0.0, 1.0, tsk.nu0
        )
        
        lam, mu = lame_parameters(tsk.E0, tsk.nu0)
        def C(T):
            return 2. * mu * T + lam * eye(trace(T), T.shape[0])

        @skfem.BilinearForm
        def stiffness(u, v, w):
            return ddot(C(sym_grad(u)), sym_grad(v))

        _F = tsk.force
        K2 = stiffness.assemble(tsk.basis)
        
        # print("tsk.dirichlet_nodes", tsk.dirichlet_nodes)
        K1_e, F1_e = skfem.enforce(K1, _F, D=tsk.dirichlet_nodes)
        K2_e, F2_e = skfem.enforce(K2, _F, D=tsk.dirichlet_nodes)

        U1_e = scipy.sparse.linalg.spsolve(K1_e, F1_e)
        U2_e = scipy.sparse.linalg.spsolve(K2_e, F2_e)

        print("U1_e:", np.average(U1_e))
        print("U2_e:", np.average(U2_e))
        
        sf = 1.0
        m1 = tsk.mesh.translated(sf * U1_e[tsk.basis.nodal_dofs])
        m1.save('K1.vtk')
        m2 = tsk.mesh.translated(sf * U2_e[tsk.basis.nodal_dofs])
        m2.save('K2.vtk')


        # 
        K1_e, F1_e = skfem.enforce(K1, _F, D=tsk.dirichlet_nodes)
        # K1_e_np = K1_e.toarray()
        U1_e = scipy.sparse.linalg.spsolve(K1_e, F1_e)
        u = U1_e
        K = K1_e.toarray()
        U_global = 0.5 * u @ (K @ u)
        print("Global:", U_global)

        # 
        print(tsk.basis.element_dofs.shape, rho.shape)
        U_elementwise1 = strain_energy_hdcode(
            u, tsk.basis.element_dofs,
            tsk.basis,
            rho,
            tsk.E0,
            tsk.Emin,
            1.0,
            tsk.nu0,
        ).sum()
        
        element_dofs = tsk.basis.element_dofs[:, tsk.design_elements]
        rho_design = rho[tsk.design_elements]
        print(element_dofs.shape, rho_design.shape)
        
        t0 = time.time()
        U_elementwise2 = strain_energy_hdcode(
            u, element_dofs,
            tsk.basis,
            rho_design,
            tsk.E0,
            tsk.Emin,
            1.0,
            tsk.nu0,
        ).sum()
        t1 = time.time()
        
        U_elementwise2_numba1 = strain_energy_hdcode_numba(
            u, element_dofs,
            tsk.mesh.p,
            rho_design,
            tsk.E0,
            tsk.Emin,
            1.0,
            tsk.nu0,
        ).sum()
        t2 = time.time()
        U_elementwise2_numba2 = strain_energy_hdcode_numba(
            u, element_dofs,
            tsk.mesh.p,
            rho_design,
            tsk.E0,
            tsk.Emin,
            1.0,
            tsk.nu0,
        ).sum()
        t3 = time.time()
        
        print("numpy", t1 - t0)
        print("numba-1st", t2 - t1)
        print("numba-2nd", t3 - t2)
        
        element_dofs = tsk.basis.element_dofs[:, tsk.free_nodes]
        rho_design = rho[tsk.free_nodes]
        print(element_dofs.shape, rho_design.shape)
        U_elementwise3 = strain_energy_hdcode(
            u, element_dofs,
            tsk.basis,
            rho_design,
            tsk.E0,
            tsk.Emin,
            1.0,
            tsk.nu0,
        ).sum()
        print("Sum over elements all:", U_elementwise1)
        print("Sum over elements design:", U_elementwise2)
        print("Sum over elements design:", U_elementwise3)

        print("error", np.sum(U_elementwise2 - U_elementwise2_numba1))

    @profile
    def test_2():
        import time
        from scitopt.mesh import toy_problem
        # tsk = toy_problem.toy1()
        tsk = toy_problem.toy_msh("plate-0.2.msh")
        
        rho = np.ones(tsk.all_elements.shape)
        p = 1
        
        t0 = time.time()
        K0 = assemble_stiffness_matrix_numba(
            tsk.basis,
            rho,
            tsk.E0, tsk.Emin, p, tsk.nu0
        )
        t1 = time.time()
        print("numba - 1st", t1 - t0, "sec")
        t0 = time.time()
        K0 = assemble_stiffness_matrix_numba(
            tsk.basis,
            rho,
            tsk.E0, tsk.Emin, p, tsk.nu0
        )
        t1 = time.time()
        print("numba - 2nd (firster than 1st time)", t1 - t0, "sec")

        K1 = assemble_stiffness_matrix(
            tsk.basis,
            rho,
            tsk.E0, tsk.Emin, p, tsk.nu0
        )
        print("numpy", time.time() - t1)
        print("err:", np.sum(K0 - K1))

    @profile
    def test_3():
        import scitopt
        from scitopt.mesh import toy_problem

        tsk = toy_problem.toy_msh("plate-0.2.msh")
        rho = np.ones(tsk.all_elements.shape)

        K0 = assemble_stiffness_matrix(
            tsk.basis, rho, tsk.E0, tsk.Emin, 1.0, tsk.nu0
        )
        # K1 = assemble_stiffness_matrix_numba(
        #     tsk.basis, rho, tsk.E0, tsk.Emin, 1.0, tsk.nu0
        # )
        
        lam, mu = lame_parameters(tsk.E0, tsk.nu0)
        def C(T):
            return 2. * mu * T + lam * eye(trace(T), T.shape[0])

        @skfem.BilinearForm
        def stiffness(u, v, w):
            return ddot(C(sym_grad(u)), sym_grad(v))

        _F = tsk.force
        K2 = stiffness.assemble(tsk.basis)
        
        # print("tsk.dirichlet_nodes", tsk.dirichlet_nodes)
        K0_e, F0_e = skfem.enforce(K0, _F, D=tsk.dirichlet_nodes)
        # K1_e, F1_e = skfem.enforce(K1, _F, D=tsk.dirichlet_nodes)
        K2_e, F2_e = skfem.enforce(K2, _F, D=tsk.dirichlet_nodes)

        # U1_e = scipy.sparse.linalg.spsolve(K1_e, F1_e)
        # U2_e = scipy.sparse.linalg.spsolve(K2_e, F2_e)
        U0_e = scitopt.fea.solver.solve_u(K0_e, F0_e, chosen_solver="pyamg")
        # U1_e = scitopt.fea.solver.solve_u(K1_e, F1_e, chosen_solver="pyamg")
        U2_e = scitopt.fea.solver.solve_u(K2_e, F2_e, chosen_solver="pyamg")

        print("U0_e ave :", np.average(U0_e))
        # print("U1_e ave :", np.average(U1_e))
        print("U2_e ave:", np.average(U2_e))
        print("U0_e max :", np.max(U0_e))
        # print("U1_e max :", np.max(U1_e))
        print("U2_e max:", np.max(U2_e))
        print("U0_e min :", np.min(U0_e))
        # print("U1_e min :", np.min(U1_e))
        print("U2_e min:", np.min(U2_e))
        
        if isinstance(tsk.mesh, skfem.MeshTet):
            mesh_type = "tetra" 
        elif isinstance(tsk.mesh, skfem.MeshHex):
            mesh_type = "hexahedron" 
        else:
            raise ValueError("")
        
        sf = 1.0
        # m1 = tsk.mesh.translated(sf * U1_e[tsk.basis.nodal_dofs])
        # m1.save('K1.vtk')
        m2 = tsk.mesh.translated(sf * U2_e[tsk.basis.nodal_dofs])
        m2.save('K2.vtk')

        # 
        # K1_e, F1_e = skfem.enforce(K1, _F, D=tsk.dirichlet_nodes)
        # U1_e = scipy.sparse.linalg.spsolve(K1_e, F1_e)
        # u = U1_e
        # u = tsk.basis.interpolate(U0_e)
        compliance, u_compliance = scitopt.fea.solver.compute_compliance_basis(
            tsk.basis, tsk.free_nodes, tsk.dirichlet_nodes, _F,
            tsk.E0, tsk.Emin, 1.0, tsk.nu0,
            rho,
            elem_func=simp_interpolation,
            # solver="spsolve"
        )
        strain = strain_energy_skfem(
            tsk.basis, rho, u_compliance,
            tsk.E0, tsk.Emin, 1.0, tsk.nu0,
            elem_func=simp_interpolation
        )
        
        print(np.average(np.abs(U0_e)))
        print(np.average(np.abs(u_compliance)))
        print("u diff :", np.sum((U0_e - u_compliance)**2))
        strain_min_max = (strain.max()/2, strain.max())
        print(f"strain_min_max: {strain_min_max}")
        mesh_path = "strain.vtu"
        cell_outputs = dict()
        # cell_outputs["strain"] = [np.linalg.norm(u, axis=0)]
        cell_outputs["strain"] = [strain]
        meshio_mesh = meshio.Mesh(
            points=tsk.mesh.p.T,
            cells=[(mesh_type, tsk.mesh.t.T)],
            cell_data=cell_outputs
        )
        meshio.write(mesh_path, meshio_mesh)
        
        strain_image_title = "strain"
        strain_image_path = "strain.jpg"
        pv.start_xvfb()
        mesh = pv.read(mesh_path)
        scalar_name = "strain"
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(
            mesh,
            scalars=scalar_name,
            cmap="turbo",
            clim=(cell_outputs["strain"][0].min(), cell_outputs["strain"][0].max()),
            opacity=0.3,
            show_edges=False,
            scalar_bar_args={"title": scalar_name}
        )
        plotter.add_text(strain_image_title, position="upper_left", font_size=12, color="black")
        plotter.screenshot(strain_image_path)
        plotter.close()


    @profile
    def test_4():
        
        from skfem.helpers import ddot
        import scitopt
        from scitopt.mesh import toy_problem
        

        tsk = toy_problem.toy_msh("plate-0.2.msh")
        rho = np.ones(tsk.all_elements.shape)

        K0 = assemble_stiffness_matrix(
            tsk.basis, rho, tsk.E0, 0.0, 1.0, tsk.nu0
        )
        _F = tsk.force
        K_e, F_e = skfem.enforce(K0, _F, D=tsk.dirichlet_nodes)
        u = scitopt.fea.solver.solve_u(K_e, F_e, chosen_solver="pyamg")
        print("np.sum(u[tsk.dirichlet_nodes]):", np.sum(u[tsk.dirichlet_nodes]))
        
        lam, mu = lame_parameters(tsk.E0, tsk.nu0)

        def C(strain):
            return 2.0 * mu * strain + lam * eye(trace(strain), strain.shape[0])

        @Functional
        def strain_energy_density(w):
            grad = w['uh'].grad  # shape: (ndim, nqp, nelements)
            symgrad = 0.5 * (grad + transpose(grad))
            return 0.5 * ddot(C(symgrad), symgrad)

        uh = tsk.basis.interpolate(u)
        total_U = strain_energy_density.assemble(tsk.basis, uh=uh)
        element_U = strain_energy_density.elemental(tsk.basis, uh=uh)
        print(f"Total Strain Energy = {total_U}")
        # print("The Strain Energy Each =", element_U)

        
        elem_energy_simp = strain_energy_skfem(
            tsk.basis, np.ones(tsk.mesh.nelements), u,
            1.0, 0.0, 1.0, 0.3
        )
        
        # print("The Strain Energy Each =", elem_energy_simp)
        print("Difference =", np.sum((elem_energy_simp - element_U)**2))

        stress = stress_tensor_skfem(
            tsk.basis, np.ones(tsk.mesh.nelements), u,
            1.0, 0.0, 1.0, 0.3
        )
        print("stress:", stress.shape)
        von_mises = von_mises_from_stress_tensor(stress)
        print("von_mises:", von_mises.shape)


    # test_1()
    # test_2()
    test_3()
    test_4()

