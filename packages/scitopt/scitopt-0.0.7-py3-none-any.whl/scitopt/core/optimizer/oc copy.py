from typing import Literal, Callable
from dataclasses import dataclass, asdict
import numpy as np
import scitopt
from scitopt.core import derivatives, projection
from scitopt.core import visualization
from scitopt.fea import solver
from scitopt import filter
from scitopt.fea import composer
from scitopt.core import misc
from scitopt.core.optimizer import common


@dataclass
class OC_Config(common.Sensitivity_Config):
    interpolation: Literal["SIMP"] = "SIMP"
    eta_init: float = 0.1
    eta: float = 0.5
    eta_step: int = 3
    

def bisection_with_projection(
    dC, rho_e, rho_min, rho_max, move_limit,
    eta, eps, vol_frac,
    beta, beta_eta,
    scaling_rate, rho_candidate, tmp_lower, tmp_upper,
    elements_volume, elements_volume_sum,
    max_iter=100, tolerance=1e-4,
    l1 = 1e-3,
    l2 = 1e+3
):
    # for _ in range(100):
    # while abs(l2 - l1) <= tolerance * (l1 + l2) / 2.0:
    # while abs(l2 - l1) > tolerance * (l1 + l2) / 2.0:
    while abs(l2 - l1) > tolerance:
        lmid = 0.5 * (l1 + l2)
        np.negative(dC, out=scaling_rate)
        scaling_rate /= (lmid + eps)
        np.power(scaling_rate, eta, out=scaling_rate)

        # Clip
        np.clip(scaling_rate, 0.8, 1.2, out=scaling_rate)
        
        np.multiply(rho_e, scaling_rate, out=rho_candidate)
        np.maximum(rho_e - move_limit, rho_min, out=tmp_lower)
        np.minimum(rho_e + move_limit, rho_max, out=tmp_upper)
        np.clip(rho_candidate, tmp_lower, tmp_upper, out=rho_candidate)

        # 
        # filter might be needed here
        # 
        projection.heaviside_projection_inplace(
            rho_candidate, beta=beta, eta=beta_eta, out=rho_candidate
        )
        
        # vol_error = np.mean(rho_candidate) - vol_frac
        vol_error = np.sum(
            rho_candidate * elements_volume
        ) / elements_volume_sum - vol_frac
        
        if abs(vol_error) < 1e-6:
            break
        if vol_error > 0:
            l1 = lmid
        else:
            l2 = lmid
            
    return lmid, vol_error


class OC_Optimizer(common.Sensitivity_Analysis):
    def __init__(
        self,
        cfg: OC_Config,
        tsk: scitopt.mesh.TaskConfig,
    ):
        super().__init__(cfg, tsk)
        self.recorder.add("-dC", plot_type="min-max-mean-std", ylog=True)
        self.recorder.add("lmid", ylog=False) # True
            
    
    def init_schedulers(self, export: bool=True):
        super().init_schedulers(False)
        self.schedulers.add(
            "eta",
            self.cfg.eta_init,
            self.cfg.eta,
            self.cfg.eta_step,
            self.cfg.max_iters
        )
        if export:
            self.schedulers.export()

    def parameterize(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_defaults(
            self.tsk.mesh,
            self.cfg.filter_radius,
            solver_type="pyamg",
            dst_path=f"{self.cfg.dst_path}/data",
            
        )

    def load_parameters(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_file(
            f"{self.cfg.dst_path}/data"
        )

    # def optimize(self):

    #     cfg = self.cfg
    #     tsk = self.tsk
    #     elements_volume = tsk.elements_volume[tsk.design_elements]
    #     elements_volume_sum = np.sum(elements_volume)
        
    #     rho = np.zeros_like(tsk.all_elements, dtype=np.float64)
    #     iter_begin = 1
    #     if cfg.restart is True:
    #         if cfg.restart_from > 0:
    #             data = np.load(
    #                 f"{cfg.dst_path}/data/{str(cfg.restart_from).zfill(6)}-rho.npz"
    #             )
    #         else:
    #             iter, data_path = misc.find_latest_iter_file(f"{cfg.dst_path}/data")
    #             data = np.load(data_path)
    #             iter_begin = iter

    #         rho[tsk.design_elements] = data["rho_design_elements"]
    #         del data
    #     else:
    #         _vol_frac = cfg.vol_frac if cfg.vol_frac_step < 0 else cfg.vol_frac_init
    #         # rho += _vol_frac + 0.1 * (np.random.rand(len(tsk.all_elements)) - 0.5)
    #         rho += _vol_frac
    #         np.clip(rho, cfg.rho_min, cfg.rho_max, out=rho)
    #     # rho[tsk.dirichlet_force_elements] = 1.0
    #     # rho[tsk.force_elements] = 1.0
    #     rho[tsk.fixed_elements_in_rho] = 1.0
    #     print("np.average(rho[tsk.design_elements]):", np.average(rho[tsk.design_elements]))
        
    #     self.init_schedulers()
    #     eta = cfg.eta
    #     rho_min = cfg.rho_min
    #     rho_max = 1.0
    #     tolerance = 1e-6
    #     eps = 1e-6

    #     rho_prev = np.zeros_like(rho)

    #     rho_filtered = np.zeros_like(rho)
    #     rho_projected = np.zeros_like(rho)
    #     dH = np.empty_like(rho)
    #     grad_filtered = np.empty_like(rho)
    #     dC_drho_projected = np.empty_like(rho)
    #     strain_energy = np.zeros_like(rho)
    #     strain_energy_ave = np.zeros_like(rho)
    #     compliance_avg = np.zeros_like(rho)
    #     dH = np.zeros_like(rho)

    #     # dC_drho_ave = np.zeros_like(rho)
    #     dC_drho_full = np.zeros_like(rho)
    #     dC_drho_ave = np.zeros_like(rho[tsk.design_elements])
    #     scaling_rate = np.empty_like(rho[tsk.design_elements])
    #     rho_candidate = np.empty_like(rho[tsk.design_elements])
    #     tmp_lower = np.empty_like(rho[tsk.design_elements])
    #     tmp_upper = np.empty_like(rho[tsk.design_elements])
    #     force_list = tsk.force if isinstance(tsk.force, list) else [tsk.force]
    #     if cfg.interpolation == "SIMP":
    #     # if False:
    #         density_interpolation = composer.simp_interpolation
    #         # density_interpolation = composer.simp_interpolation_numba
    #         dC_drho_func = derivatives.dC_drho_simp
    #     else:
    #         raise ValueError("should be SIMP")

    #     filter_radius_prev = cfg.filter_radius_init if cfg.filter_radius_step > 0 else cfg.filter_radius
    #     self.helmholz_solver.update_radius(tsk.mesh, filter_radius_prev)
    #     self.recorder.feed_data("rho", rho)
    #     for iter_loop, iter in enumerate(range(iter_begin, cfg.max_iters + iter_begin)):
    #         print(f"iterations: {iter} / {cfg.max_iters}")
    #         p, vol_frac, beta, move_limit, eta, percentile, filter_radius = (
    #             self.schedulers.values(iter)[k] for k in [
    #                 'p', 'vol_frac', 'beta', 'move_limit', 'eta', 'percentile', 'filter_radius'
    #             ]
    #         )
    #         if filter_radius_prev != filter_radius:
    #             self.helmholz_solver.update_radius(tsk.mesh, filter_radius)
    #         print(f"p {p:.4f}, vol_frac {vol_frac:.4f}, beta {beta:.4f}, move_limit {move_limit:.4f}")
    #         print(f"eta {eta:.4f}, percentile {percentile:.4f} filter_radius {filter_radius:.4f}")

    #         rho_prev[:] = rho[:]
    #         rho_filtered[:] = self.helmholz_solver.filter(rho)
    #         projection.heaviside_projection_inplace(
    #             rho_filtered, beta=beta, eta=cfg.beta_eta, out=rho_projected
    #         )

    #         dC_drho_full[:] = 0.0
    #         dC_drho_ave[:] = 0.0
    #         strain_energy[:] = 0.0
    #         strain_energy_ave[:] = 0.0
    #         compliance_avg[:] = 0.0
    #         for force in force_list:
    #             dH[:] = 0.0
    #             compliance, u = solver.compute_compliance_basis(
    #             # compliance, u = solver.compute_compliance_basis_numba(
    #                 tsk.basis, tsk.free_nodes, tsk.dirichlet_nodes, force,
    #                 tsk.E0, tsk.Emin, p, tsk.nu0,
    #                 rho_projected,
    #                 # rho_filtered,
    #                 elem_func=density_interpolation
    #             )
    #             compliance_avg += compliance
    #             strain_energy = composer.strain_energy_skfem(
    #                 tsk.basis, rho_projected, u,
    #                 tsk.E0, tsk.Emin, p, tsk.nu0,
    #                 elem_func=density_interpolation
    #             )
    #             strain_energy_ave += strain_energy
    #             np.copyto(
    #                 dC_drho_projected,
    #                 dC_drho_func(
    #                     rho_projected,
    #                     strain_energy, tsk.E0, tsk.Emin, p
    #                 )
    #             )
    #             projection.heaviside_projection_derivative_inplace(
    #                 rho_filtered,
    #                 beta=beta, eta=cfg.beta_eta, out=dH
    #             )
    #             np.multiply(dC_drho_projected, dH, out=grad_filtered)
    #             # dC_drho_full += self.helmholz_solver.gradient(grad_filtered)
    #             np.add(dC_drho_full, self.helmholz_solver.gradient(grad_filtered), out=dC_drho_full)
                
    #         dC_drho_full /= len(force_list)
    #         strain_energy_ave /= len(force_list)
    #         compliance_avg /= len(force_list)
            
            
    #         filtered = self.helmholz_solver.filter(dC_drho_full)
    #         np.copyto(dC_drho_full, filtered)
            
    #         # print(f"dC_drho_full- min:{dC_drho_full.min()} max:{dC_drho_full.max()}")
    #         scale = np.percentile(np.abs(dC_drho_full[tsk.design_elements]), percentile)
    #         scale = max(scale, np.mean(np.abs(dC_drho_full[tsk.design_elements])), 1e-4)
    #         # scale = np.median(np.abs(dC_drho_full[tsk.design_elements]))
    #         running_scale = 0.6 * running_scale + (1 - 0.6) * scale if iter_loop > 0 else scale
    #         dC_drho_full /= (running_scale + eps)
    #         # if cfg.interpolation == "SIMP":
    #         #     np.minimum(dC_drho_full - dC_drho_full.max(), -cfg.lambda_lower*10.0, out=dC_drho_full)
            

    #         # np.minimum(dC_drho_full, -cfg.lambda_lower*0.1, out=dC_drho_full)
    #         # np.clip(dC_drho_full, -cfg.lambda_upper * 10, -cfg.lambda_lower * 0.1, out=dC_drho_full)
    #         print(f"running_scale: {running_scale}")
    #         dC_drho_ave[:] = dC_drho_full[tsk.design_elements]
    #         print(f"dC_drho_ave-scaled min:{dC_drho_ave.min()} max:{dC_drho_ave.max()}")
    #         print(f"dC_drho_ave-scaled ave:{np.mean(dC_drho_ave)} sdv:{np.std(dC_drho_ave)}")
            
            
    #         # np.minimum(dC_drho_ave, -cfg.lambda_lower*10.0, out=dC_drho_ave)

    #         rho_e = rho_projected[tsk.design_elements]
    #         rho_candidate, lmid, vol_error = bisection_with_projection(
    #             dC_drho_ave,
    #             # dC_drho_ave[tsk.design_elements],
    #             rho_e, cfg.rho_min, cfg.rho_max, move_limit,
    #             eta, eps, vol_frac,
    #             beta, cfg.beta_eta,
    #             scaling_rate, rho_candidate, tmp_lower, tmp_upper,
    #             elements_volume, elements_volume_sum,
    #             max_iter=1000, tolerance=1e-5,
    #             l1 = cfg.lambda_lower,
    #             l2 = cfg.lambda_upper
    #         )
    #         print(
    #             f"λ: {lmid:.4e}, vol_error: {vol_error:.4f}, mean(rho): {np.mean(rho_candidate):.4f}"
    #         )
    #         rho[tsk.design_elements] = rho_candidate
    #         if cfg.design_dirichlet is True:
    #             rho[tsk.force_elements] = 1.0
    #         else:
    #             rho[tsk.dirichlet_force_elements] = 1.0
    #         rho[tsk.force_elements] = 1.0
    #         # rho_diff = np.mean(np.abs(rho[tsk.design_elements] - rho_prev[tsk.design_elements]))


    #         self.recorder.feed_data("rho", rho)
    #         self.recorder.feed_data("rho_projected", rho_projected[tsk.design_elements])
    #         self.recorder.feed_data("scaling_rate", scaling_rate)
    #         self.recorder.feed_data("compliance", compliance_avg)
    #         self.recorder.feed_data("- dC", -dC_drho_ave)
    #         self.recorder.feed_data("lmid", lmid)
    #         self.recorder.feed_data("vol_error", vol_error)
    #         self.recorder.feed_data("strain_energy", strain_energy)
            
            
    #         if iter % (cfg.max_iters // self.cfg.record_times) == 0 or iter == 1:
    #         # if True:
    #             print(f"Saving at iteration {iter}")
    #             # self.recorder.print()
    #             # self.recorder_params.print()
    #             self.recorder.export_progress()
    #             visualization.save_info_on_mesh(
    #                 tsk,
    #                 rho_projected, rho_prev, strain_energy_ave,
    #                 cfg.vtu_path(iter),
    #                 cfg.image_path(iter, "rho"),
    #                 f"Iteration : {iter}",
    #                 cfg.image_path(iter, "strain_energy"),
    #                 f"Iteration : {iter}"
    #             )
    #             visualization.export_submesh(
    #                 tsk, rho_projected, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
    #             )
    #             np.savez_compressed(
    #                 f"{cfg.dst_path}/data/{str(iter).zfill(6)}-rho.npz",
    #                 rho_design_elements=rho[tsk.design_elements],
    #                 rho_projected_design_elements=rho_projected[tsk.design_elements],
    #             )

    #         # https://qiita.com/fujitagodai4/items/7cad31cc488bbb51f895

    #     visualization.rho_histo_plot(
    #         rho_projected[tsk.design_elements],
    #         f"{self.cfg.dst_path}/mesh_rho/last.jpg"
    #     )
    #     visualization.export_submesh(
    #         tsk, rho_projected, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
    #     )


    def rho_update(
        self,
        iter_loop: int,
        rho_candidate: np.ndarray,
        rho_projected: np.ndarray,
        dC_drho_ave: np.ndarray,
        strain_energy_ave: np.ndarray,
        scaling_rate: np.ndarray,
        move_limit: float,
        eta: float,
        beta: float,
        tmp_lower: np.ndarray,
        tmp_upper: np.ndarray,
        percentile: float,
        interploation: Callable,
        elements_volume_design: np.ndarray,
        elements_volume_design_sum: float,
        vol_frac: float
    ):
        cfg = self.cfg
        tsk = self.tsk
        eps = 1e-6
        
        scale = np.percentile(np.abs(dC_drho_ave), percentile)
        # scale = max(scale, np.mean(np.abs(dC_drho_ave)), 1e-4)
        # scale = np.median(np.abs(dC_drho_full[tsk.design_elements]))
        self.running_scale = 0.6 * self.running_scale + (1 - 0.6) * scale if iter_loop > 1 else scale
        dC_drho_ave /= (self.running_scale + eps)
        print(f"dC_drho_ave-scaled min:{dC_drho_ave.min()} max:{dC_drho_ave.max()}")
        print(f"dC_drho_ave-scaled ave:{np.mean(dC_drho_ave)} sdv:{np.std(dC_drho_ave)}")
        rho_e = rho_projected[tsk.design_elements]

        lmid, vol_error = bisection_with_projection(
            dC_drho_ave,
            rho_e, cfg.rho_min, cfg.rho_max, move_limit,
            eta, eps, vol_frac,
            beta, cfg.beta_eta,
            scaling_rate, rho_candidate, tmp_lower, tmp_upper,
            elements_volume_design, elements_volume_design_sum,
            max_iter=1000, tolerance=1e-5,
            l1 = cfg.lambda_lower,
            l2 = cfg.lambda_upper
        )
        print(
            f"λ: {lmid:.4e}, vol_error: {vol_error:.4f}, mean(rho): {np.mean(rho_candidate):.4f}"
        )
        self.recorder.feed_data("lmid", lmid)
        self.recorder.feed_data("vol_error", vol_error)
        self.recorder.feed_data("-dC", -dC_drho_ave)


if __name__ == '__main__':

    import argparse
    from scitopt.mesh import toy_problem
    
    
    parser = argparse.ArgumentParser(
        description=''
    )

    parser.add_argument(
        '--interpolation', '-I', type=str, default="SIMP", help=''
    )
    parser.add_argument(
        '--max_iters', '-NI', type=int, default=200, help=''
    )
    parser.add_argument(
        '--filter_radius_init', '-FRI', type=float, default=0.2, help=''
    )
    parser.add_argument(
        '--filter_radius', '-FR', type=float, default=0.05, help=''
    )
    parser.add_argument(
        '--filter_radius_step', '-FRS', type=int, default=3, help=''
    )
    parser.add_argument(
        '--move_limit_init', '-MLI', type=float, default=0.8, help=''
    )
    parser.add_argument(
        '--move_limit', '-ML', type=float, default=0.2, help=''
    )
    parser.add_argument(
        '--move_limit_step', '-MLR', type=int, default=5, help=''
    )
    parser.add_argument(
        '--record_times', '-RT', type=int, default=20, help=''
    )
    parser.add_argument(
        '--dst_path', '-DP', type=str, default="./result/test0", help=''
    )
    parser.add_argument(
        '--vol_frac_init', '-VI', type=float, default=0.8, help=''
    )
    parser.add_argument(
        '--vol_frac', '-V', type=float, default=0.4, help=''
    )
    parser.add_argument(
        '--vol_frac_step', '-VFT', type=int, default=2, help=''
    )
    parser.add_argument(
        '--p_init', '-PI', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--p', '-P', type=float, default=3.0, help=''
    )
    parser.add_argument(
        '--p_step', '-PRT', type=int, default=2, help=''
    )
    parser.add_argument(
        '--beta_init', '-BI', type=float, default=0.1, help=''
    )
    parser.add_argument(
        '--beta', '-B', type=float, default=5.0, help=''
    )
    parser.add_argument(
        '--beta_step', '-BR', type=float, default=20.0, help=''
    )
    parser.add_argument(
        '--percentile_init', '-PTI', type=float, default=60, help=''
    )
    parser.add_argument(
        '--percentile_step', '-PTR', type=int, default=2, help=''
    )
    parser.add_argument(
        '--percentile', '-PT', type=float, default=90, help=''
    )
    parser.add_argument(
        '--eta_init', '-ETI', type=float, default=0.01, help=''
    )
    parser.add_argument(
        '--eta_step', '-ETR', type=float, default=-1.0, help=''
    )
    parser.add_argument(
        '--eta', '-ET', type=float, default=0.3, help=''
    )
    parser.add_argument(
        '--beta_eta', '-BE', type=float, default=0.5, help=''
    )
    parser.add_argument(
        '--lambda_lower', '-BSL', type=float, default=1e-4, help=''
    )
    parser.add_argument(
        '--lambda_upper', '-BSH', type=float, default=1e+2, help=''
    )
    parser.add_argument(
        '--restart', '-RS', type=misc.str2bool, default=False, help=''
    )
    parser.add_argument(
        '--restart_from', '-RF', type=int, default=-1, help=''
    )
    parser.add_argument(
        '--rho_min', '-RM', type=float, default=0.01, help=''
    )
    parser.add_argument(
        '--task', '-T', type=str, default="toy1", help=''
    )
    parser.add_argument(
        '--export_img', '-EI', type=misc.str2bool, default=False, help=''
    )
    parser.add_argument(
        '--design_dirichlet', '-DD', type=misc.str2bool, default=True, help=''
    )
    args = parser.parse_args()
    

    if args.task == "toy1":
        tsk = toy_problem.toy1()
    elif args.task == "toy1_fine":
        tsk = toy_problem.toy1_fine()
    elif args.task == "toy2":
        tsk = toy_problem.toy2()
    else:
        tsk = toy_problem.toy_msh(args.task)
    
    print("load toy problem")
    
    print("generate OC_Config")
    cfg = OC_Config.from_defaults(
        **vars(args)
    )
    
    print("optimizer")
    optimizer = OC_Optimizer(cfg, tsk)
    print("parameterize")
    optimizer.parameterize()
    # optimizer.parameterize(preprocess=False)
    # optimizer.load_parameters()
    print("optimize")
    optimizer.optimize()
    # optimizer.optimize_org()
