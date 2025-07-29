from typing import Literal
from dataclasses import dataclass
import numpy as np
import scitopt
from scitopt.core import misc
from scitopt.core.optimizer import common


@dataclass
class MOC_Config(common.SensitivityConfig):
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
    # if percentile > 0:
    np.negative(dC, out=scaling_rate)
    scaling_rate /= (lambda_v + eps)
    np.maximum(scaling_rate, eps, out=scaling_rate)
    np.log(scaling_rate, out=scaling_rate)
    scaling_rate -= np.mean(scaling_rate) # 
    # np.clip(scaling_rate, -0.05, 0.05, out=scaling_rate)
    # np.clip(scaling_rate, -0.10, 0.10, out=scaling_rate)
    # np.clip(scaling_rate, -0.20, 0.20, out=scaling_rate)
    # np.clip(scaling_rate, -0.30, 0.30, out=scaling_rate)
    np.clip(scaling_rate, -0.50, 0.50, out=scaling_rate)
    np.clip(rho, rho_min, 1.0, out=rho)
    np.log(rho, out=tmp_lower)
    

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


class MOC_Optimizer(common.SensitivityAnalysis):
    def __init__(
        self,
        cfg: MOC_Config,
        tsk: scitopt.mesh.TaskConfig,
    ):
        super().__init__(cfg, tsk)
        self.recorder.add("-dC", plot_type="min-max-mean-std", ylog=True)
        self.recorder.add("lambda_v", ylog=True) # True

    
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
        elements_volume_design: np.ndarray,
        elements_volume_design_sum: float,
        vol_frac: float
    ):
        cfg = self.cfg
        tsk = self.tsk
        eps = 1e-8
        
        if percentile > 0:
            scale = np.percentile(np.abs(dC_drho_ave), percentile)
            self.recorder.feed_data("-dC", -dC_drho_ave)
            # scale = np.percentile(np.abs(dC_drho_full[tsk.design_elements]), percentile)
            # scale = np.median(np.abs(dC_drho_full[tsk.design_elements]))
            self.running_scale = 0.2 * self.running_scale + (1 - 0.2) * scale if iter_loop > 1 else scale
            print(f"running_scale: {self.running_scale}")
            dC_drho_ave = dC_drho_ave / (self.running_scale + eps)
        else:
            pass    
        # np.minimum(
        #     dC_drho_full,
        #     -lambda_lower*0.1,
        #     out=dC_drho_full
        # )
        # np.clip(dC_drho_full, -lambda_upper * 10, -lambda_lower * 0.1, out=dC_drho_full)
        
        
        
        # vol_error = np.mean(rho_projected[tsk.design_elements]) - vol_frac
        vol_error = np.sum(
            rho_projected[tsk.design_elements] * elements_volume_design
        ) / elements_volume_design_sum - vol_frac
        
        penalty = cfg.mu_p * vol_error
        self.lambda_v = cfg.lambda_decay * self.lambda_v + penalty if iter_loop > 1 else penalty
        self.lambda_v = np.clip(self.lambda_v, cfg.lambda_lower, cfg.lambda_upper)
        self.recorder.feed_data("lambda_v", self.lambda_v)
        self.recorder.feed_data("vol_error", vol_error)
        self.recorder.feed_data("-dC", -dC_drho_ave)
        
        # 
        moc_log_update_logspace(
            rho_candidate,
            dC_drho_ave,
            self.lambda_v, scaling_rate,
            move_limit,
            eta,
            tmp_lower, tmp_upper,
            cfg.rho_min, 1.0
        )
        
    
    
if __name__ == '__main__':
    import argparse
    from scitopt.mesh import toy_problem

    parser = argparse.ArgumentParser(
        description=''
    )
    parser = misc.add_common_arguments(parser)
    parser.add_argument(
        '--mu_p', '-MUP', type=float, default=100.0, help=''
    )
    parser.add_argument(
        '--lambda_v', '-LV', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--lambda_decay', '-LD', type=float, default=0.95, help=''
    )
    args = parser.parse_args()
    

    if args.task_name == "toy1":
        tsk = toy_problem.toy1()
    elif args.task_name == "toy1_fine":
        tsk = toy_problem.toy1_fine()
    elif args.task_name == "toy2":
        tsk = toy_problem.toy2()
    else:
        tsk = toy_problem.toy_msh(args.task_name, args.mesh_path)
    
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