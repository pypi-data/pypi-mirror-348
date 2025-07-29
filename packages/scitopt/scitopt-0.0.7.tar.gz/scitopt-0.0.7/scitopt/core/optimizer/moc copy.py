from typing import Literal
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
class MOC_Config(common.Sensitivity_Config):
    interpolation: Literal["SIMP"] = "SIMP"
    mu_p: float = 2.0
    lambda_v: float = 0.1
    lambda_decay: float = 0.95


# log(x) = -0.4   →   x ≈ 0.670
# log(x) = -0.3   →   x ≈ 0.741
# log(x) = -0.2   →   x ≈ 0.819
# log(x) = -0.1   →   x ≈ 0.905
# log(x) =  0.0   →   x =  1.000
# log(x) = +0.1   →   x ≈ 1.105
# log(x) = +0.2   →   x ≈ 1.221
# log(x) = +0.3   →   x ≈ 1.350
# log(x) = +0.4   →   x ≈ 1.492


def moc_log_update_logspace(
    rho,
    dC, lambda_v, scaling_rate,
    eta, move_limit,
    tmp_lower, tmp_upper,
    rho_min, rho_max
):
    eps = 1e-8
    
    print("dC:", dC.min(), dC.max())
    np.negative(dC, out=scaling_rate)
    scaling_rate /= (lambda_v + eps)
    np.maximum(scaling_rate, eps, out=scaling_rate)
    np.log(scaling_rate, out=scaling_rate)
    scaling_rate -= np.mean(scaling_rate) # 
    # np.clip(scaling_rate, -0.05, 0.05, out=scaling_rate)
    # np.clip(scaling_rate, -0.10, 0.10, out=scaling_rate)
    # np.clip(scaling_rate, -0.20, 0.20, out=scaling_rate)
    np.clip(scaling_rate, -0.30, 0.30, out=scaling_rate)
    np.clip(rho, rho_min, 1.0, out=rho)
    np.log(rho, out=tmp_lower)
    
    

    # 

    # 
    # 
    # tmp_upper = exp(tmp_lower) = rho (real space)
    np.exp(tmp_lower, out=tmp_upper)
    # tmp_upper = log(1 + move_limit / rho)
    np.divide(move_limit, tmp_upper, out=tmp_upper)
    np.add(tmp_upper, 1.0, out=tmp_upper)
    np.log(tmp_upper, out=tmp_upper)

    # tmp_lower = lower bound = log(rho) - log_move_limit
    np.subtract(tmp_lower, tmp_upper, out=tmp_lower)

    # tmp_upper = upper bound = log(rho) + log_move_limit
    np.add(tmp_lower, 2 * tmp_upper, out=tmp_upper)

    # rho = log(rho)
    np.log(rho, out=rho)

    # log(rho) += η * scaling_rate
    rho += eta * scaling_rate

    # clip in log-space
    np.clip(rho, tmp_lower, tmp_upper, out=rho)

    # back to real space
    np.exp(rho, out=rho)
    np.clip(rho, rho_min, rho_max, out=rho)


class MOC_Optimizer(common.Sensitivity_Analysis):
    def __init__(
        self,
        cfg: MOC_Config,
        tsk: scitopt.mesh.TaskConfig,
    ):
        super().__init__(cfg, tsk)
        self.recorder.add("- dC", plot_type="min-max-mean-std", ylog=True)
        self.recorder.add("lambda_v", ylog=True) # True
        

    def optimize(self):
        tsk = self.tsk
        cfg = self.cfg
        
        elements_volume = tsk.elements_volume[tsk.design_elements]
        elements_volume_sum = np.sum(elements_volume)
        # print("elements_volume-ave-std", np.mean(elements_volume), np.std(elements_volume))
        
        rho = np.zeros_like(tsk.all_elements, dtype=np.float64)
        iter_begin = 1
        if cfg.restart:
            if cfg.restart_from > 0:
                data = np.load(
                    f"{cfg.dst_path}/data/{str(cfg.restart_from).zfill(6)}-rho.npz"
                )
            else:
                iter, data_path = misc.find_latest_iter_file(f"{cfg.dst_path}/data")
                data = np.load(data_path)
                iter_begin = iter

            rho[tsk.design_elements] = data["rho_design_elements"]
            del data
        else:
            _vol_frac = cfg.vol_frac if cfg.vol_frac_step < 0 else cfg.vol_frac_init
            # rho += _vol_frac + 0.1 * (np.random.rand(len(tsk.all_elements)) - 0.5)
            rho += _vol_frac
            np.clip(rho, cfg.rho_min, cfg.rho_max, out=rho)

        if cfg.design_dirichlet is True:
            rho[tsk.force_elements] = 1.0
        else:
            rho[tsk.dirichlet_force_elements] = 1.0
        
        rho[tsk.fixed_elements_in_rho] = 1.0
        self.init_schedulers()
        
        if cfg.interpolation == "SIMP":
        # if False:
            density_interpolation = composer.simp_interpolation_numba
            dC_drho_func = derivatives.dC_drho_simp
        else:
            raise ValueError("should be SIMP")
        
        rho_prev = np.zeros_like(rho)
        rho_filtered = np.zeros_like(rho)
        rho_projected = np.zeros_like(rho)
        dH = np.empty_like(rho)
        grad_filtered = np.empty_like(rho)
        dC_drho_projected = np.empty_like(rho)
        strain_energy_ave = np.zeros_like(rho)
        compliance_avg = np.zeros_like(rho)
        dH = np.zeros_like(rho)

        # dC_drho_ave = np.zeros_like(rho)
        dC_drho_full = np.zeros_like(rho)
        dC_drho_ave = np.zeros_like(rho[tsk.design_elements])
        scaling_rate = np.empty_like(rho[tsk.design_elements])
        rho_candidate = np.empty_like(rho[tsk.design_elements])
        tmp_lower = np.empty_like(rho[tsk.design_elements])
        tmp_upper = np.empty_like(rho[tsk.design_elements])
        force_list = tsk.force if isinstance(tsk.force, list) else [tsk.force]
        lambda_v = cfg.lambda_v
        lambda_lower = cfg.lambda_lower
        lambda_upper = cfg.lambda_upper
        eta = cfg.eta
        
        filter_radius_prev = cfg.filter_radius_init if cfg.filter_radius_step > 0 else cfg.filter_radius
        self.helmholz_solver.update_radius(tsk.mesh, filter_radius_prev)
        self.recorder.feed_data("rho", rho)
        for iter_loop, iter in enumerate(range(iter_begin, cfg.max_iters+iter_begin)):
            print(f"iterations: {iter} / {cfg.max_iters}")
            p, vol_frac, beta, move_limit, percentile, filter_radius = (
                self.schedulers.values(iter)[k] for k in ['p', 'vol_frac', 'beta', 'move_limit', 'percentile', 'filter_radius']
            )
            if filter_radius_prev != filter_radius:
                self.helmholz_solver.update_radius(tsk.mesh, filter_radius)
            print(f"p {p:.4f}, vol_frac {vol_frac:.4f}, beta {beta:.4f}, move_limit {move_limit:.4f}")
            print(f"eta {eta:.4f}, percentile {percentile:.4f} filter_radius {filter_radius:.4f}")
            rho_prev[:] = rho[:]
            rho_filtered[:] = self.helmholz_solver.filter(rho)
            projection.heaviside_projection_inplace(
                rho_filtered, beta=beta, eta=cfg.beta_eta, out=rho_projected
            )
            dC_drho_ave[:] = 0.0
            dC_drho_full[:] = 0.0
            strain_energy_ave[:] = 0.0
            compliance_avg[:] = 0.0
            for force in force_list:
                dH[:]= 0.0
                compliance, u = solver.compute_compliance_basis(
                    tsk.basis, tsk.free_nodes, tsk.dirichlet_nodes, force,
                    tsk.E0, tsk.Emin, p, tsk.nu0,
                    rho_projected,
                    elem_func=density_interpolation
                )
                compliance_avg += compliance
                strain_energy = composer.strain_energy_skfem(
                    tsk.basis, rho_projected, u,
                    tsk.E0, tsk.Emin, p, tsk.nu0,
                    elem_func=density_interpolation
                )
                strain_energy_ave += strain_energy
                
                np.copyto(
                    dC_drho_projected,
                    dC_drho_func(
                        rho_projected,
                        strain_energy, tsk.E0, tsk.Emin, p
                    )
                )
                projection.heaviside_projection_derivative_inplace(
                    rho_filtered,
                    beta=beta, eta=cfg.beta_eta, out=dH
                )
                np.multiply(dC_drho_projected, dH, out=grad_filtered)
                dC_drho_full[:] += self.helmholz_solver.gradient(grad_filtered)
                # dC_drho_ave[:] += dC_drho_full[tsk.design_elements]
                # dC_drho_dirichlet[:] += dC_drho_full[tsk.dirichlet_elements]
                
            dC_drho_full /= len(force_list)
            strain_energy_ave /= len(force_list)
            compliance_avg /= len(force_list)
            print(f"dC_drho_full- min:{dC_drho_full.min()} max:{dC_drho_full.max()}")
            
            filtered = self.helmholz_solver.filter(dC_drho_full)
            np.copyto(dC_drho_full, filtered)
            
            eps = 1e-8
            scale = np.percentile(np.abs(dC_drho_full[tsk.design_elements]), percentile)
            # scale = np.median(np.abs(dC_drho_full[tsk.design_elements]))
            running_scale = 0.9 * running_scale + (1 - 0.9) * scale if iter_loop > 0 else scale
            dC_drho_full = dC_drho_full / (running_scale + eps)
            
            # np.minimum(
            #     dC_drho_full,
            #     -lambda_lower*0.1,
            #     out=dC_drho_full
            # )
            # np.clip(dC_drho_full, -lambda_upper * 10, -lambda_lower * 0.1, out=dC_drho_full)
            print(f"running_scale: {running_scale}")
            
            dC_drho_ave[:] = dC_drho_full[tsk.design_elements]
            # dC_drho_dirichlet[:] = dC_drho_full[tsk.dirichlet_elements]
            
            
            # vol_error = np.mean(rho_projected[tsk.design_elements]) - vol_frac
            vol_error = np.sum(
                rho_projected[tsk.design_elements] * elements_volume
            ) / elements_volume_sum - vol_frac
            
            lambda_v = cfg.lambda_decay * lambda_v + cfg.mu_p * vol_error
            lambda_v = np.clip(lambda_v, lambda_lower, lambda_upper)
            rho_candidate[:] = rho[tsk.design_elements] # Dont forget. inplace
            
            # 
            moc_log_update_logspace(
                rho=rho_candidate,
                dC=dC_drho_ave,
                lambda_v=lambda_v, scaling_rate=scaling_rate,
                move_limit=move_limit,
                eta=eta,
                tmp_lower=tmp_lower, tmp_upper=tmp_upper,
                rho_min=cfg.rho_min, rho_max=1.0
            )
            # 
            rho[tsk.design_elements] = rho_candidate
            if cfg.design_dirichlet is True:
                rho[tsk.force_elements] = 1.0
            else:
                rho[tsk.dirichlet_force_elements] = 1.0

            # rho_diff = np.mean(np.abs(rho[tsk.design_elements] - rho_prev[tsk.design_elements]))

            self.recorder.feed_data("rho", rho[tsk.design_elements])
            self.recorder.feed_data("rho_projected", rho_projected[tsk.design_elements])
            self.recorder.feed_data("strain_energy", strain_energy_ave)
            self.recorder.feed_data("lambda_v", lambda_v)
            self.recorder.feed_data("compliance", compliance_avg)
            self.recorder.feed_data("- dC", - dC_drho_ave)
            self.recorder.feed_data("scaling_rate", scaling_rate)
            self.recorder.feed_data("vol_error", vol_error)
            
            if iter % (cfg.max_iters // self.cfg.record_times) == 0 or iter == 1:
            # if True:
                print(f"Saving at iteration {iter}")
                self.recorder.print()
                # self.recorder_params.print()
                self.recorder.export_progress()
                
                visualization.save_info_on_mesh(
                    tsk,
                    rho_projected, rho_prev, strain_energy_ave,
                    cfg.vtu_path(iter),
                    cfg.image_path(iter, "rho"),
                    f"Iteration : {iter}",
                    cfg.image_path(iter, "strain_energy"),
                    f"Iteration : {iter}"
                )
                visualization.export_submesh(
                    tsk, rho, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
                )
                np.savez_compressed(
                    f"{cfg.dst_path}/data/{str(iter).zfill(6)}-rho.npz",
                    rho_design_elements=rho[tsk.design_elements],
                    # compliance=compliance
                )

        visualization.rho_histo_plot(
            rho[tsk.design_elements],
            f"{self.cfg.dst_path}/mesh_rho/last.jpg"
        )
        visualization.export_submesh(
            tsk, rho, 0.5, f"{cfg.dst_path}/cubic_top.vtk"
        )
    
    def rho_update(
        self,
        iter_loop,
        rho_candidate,
        rho_projected,
        dC_drho_ave,
        lambda_v,
        scaling_rate,
        move_limit,
        eta,
        tmp_lower,
        tmp_upper,
        lambda_lower,
        lambda_upper,
        percentile,
        interploation,
        elements_volume_design,
        elements_volume_design_sum,
        vol_frac
    ):
        eps = 1e-8
        scale = np.percentile(np.abs(dC_drho_ave), percentile)
        # scale = np.percentile(np.abs(dC_drho_full[tsk.design_elements]), percentile)
        # scale = np.median(np.abs(dC_drho_full[tsk.design_elements]))
        self.running_scale = 0.9 * self.running_scale + (1 - 0.9) * scale if iter_loop > 0 else scale
        dC_drho_ave = dC_drho_ave / (self.running_scale + eps)
        
        # np.minimum(
        #     dC_drho_full,
        #     -lambda_lower*0.1,
        #     out=dC_drho_full
        # )
        # np.clip(dC_drho_full, -lambda_upper * 10, -lambda_lower * 0.1, out=dC_drho_full)
        print(f"running_scale: {self.running_scale}")
        
        
        # vol_error = np.mean(rho_projected[tsk.design_elements]) - vol_frac
        vol_error = np.sum(
            rho_projected[tsk.design_elements] * elements_volume_design
        ) / elements_volume_design_sum - vol_frac
        
        penalty = cfg.mu_p * vol_error
        lambda_v = cfg.lambda_decay * lambda_v + penalty if iter_loop > 0 else penalty
        lambda_v = np.clip(lambda_v, lambda_lower, lambda_upper)
        
        # 
        moc_log_update_logspace(
            rho=rho_candidate,
            dC=dC_drho_ave,
            lambda_v=lambda_v, scaling_rate=scaling_rate,
            move_limit=move_limit,
            eta=eta,
            tmp_lower=tmp_lower, tmp_upper=tmp_upper,
            rho_min=cfg.rho_min, rho_max=1.0
        )
        
    
    
if __name__ == '__main__':
    import argparse
    from scitopt.mesh import toy_problem

    parser = argparse.ArgumentParser(
        description=''
    )

    parser.add_argument(
        '--interpolation', '-I', type=str, default="RAMP", help=''
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
        '--move_limit_step', '-MLR', type=float, default=5, help=''
    )
    parser.add_argument(
        '--percentile_init', '-PTI', type=float, default=60, help=''
    )
    parser.add_argument(
        '--percentile_step', '-PTR', type=int, default=3, help=''
    )
    parser.add_argument(
        '--percentile', '-PT', type=float, default=90, help=''
    )
    parser.add_argument(
        '--eta', '-ET', type=float, default=0.3, help=''
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
        '--vol_frac_step', '-VFT', type=int, default=3, help=''
    )
    parser.add_argument(
        '--p_init', '-PI', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--p', '-P', type=float, default=3.0, help=''
    )
    parser.add_argument(
        '--p_step', '-PRT', type=int, default=3, help=''
    )
    parser.add_argument(
        '--beta_init', '-BI', type=float, default=0.1, help=''
    )
    parser.add_argument(
        '--beta', '-B', type=float, default=5.0, help=''
    )
    parser.add_argument(
        '--beta_step', '-BR', type=int, default=3, help=''
    )
    parser.add_argument(
        '--beta_eta', '-BE', type=float, default=0.5, help=''
    )
    parser.add_argument(
        '--mu_p', '-MUP', type=float, default=100.0, help=''
    )
    # parser.add_argument(
    #     '--mu_d', '-MUD', type=float, default=200.0, help=''
    # )
    # parser.add_argument(
    #     '--mu_i', '-MUI', type=float, default=10.0, help=''
    # )
    parser.add_argument(
        '--lambda_v', '-LV', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--lambda_decay', '-LD', type=float, default=0.95, help=''
    )
    parser.add_argument(
        '--lambda_lower', '-BSL', type=float, default=1e-2, help=''
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
    
    tsk.Emin = 1e-2
    print("load toy problem")
    
    print("generate MOC_Config")
    cfg = MOC_Config.from_defaults(
        **vars(args)
    )

    print("optimizer")
    optimizer = MOC_Optimizer(cfg, tsk)
    print("parameterize")
    optimizer.parameterize()
    # optimizer.parameterize(preprocess=False)
    # optimizer.load_parameters()
    print("optimize")
    optimizer.optimize()
    # optimizer.optimize_org()