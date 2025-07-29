import numpy as np

from . pin_module import PinSolver


class JntImpedance:
    def __init__(
            self,
            urdf_path: str,
    b=0.5,k=0.2):
        """
        初始构造函数
        Args:
            urdf_path (str): urdf路径
            b (float): 控制的刚度
            k (float): 控制的阻尼
        """
        self.kd_solver = PinSolver(urdf_path)
        # hyperparameters of impedance controller
        self.B = b* np.ones(self.kd_solver._JOINT_NUM)
        self.k = k* np.ones(self.kd_solver._JOINT_NUM)

    def compute_jnt_torque(self, q_des, v_des, q_cur, v_cur):
        """ 
        robot的关节空间控制的计算公式
            Compute desired torque with robot dynamics modeling:
            > M(q)qdd + C(q, qd)qd + G(q) + tau_F(qd) = tau_ctrl + tau_env

        :param q_des: desired joint position
        :param v_des: desired joint velocity
        :param q_cur: current joint position
        :param v_cur: current joint velocity
        :return: desired joint torque
        """
        M = self.kd_solver.get_inertia_mat(q_cur)
        C = self.kd_solver.get_coriolis_mat(q_cur, v_cur)
        g = self.kd_solver.get_gravity_mat(q_cur)
        # print("惯性矩阵 M(q):")
        # print(np.array2string(M, precision=3, suppress_small=True))
        # print("\n科里奥利矩阵 C(q, qdot):")
        # print(np.array2string(C, precision=3, suppress_small=True))
        # print("\n重力向量 G(q):")
        # print(np.array2string(g, precision=3, suppress_small=False)) 
        print(f"重力；{g}")
        coriolis_force = np.dot(C, v_cur)
        coriolis_gravity = coriolis_force + g  
        acc_desire = self.k * (q_des - q_cur) + self.B * (v_des - v_cur)
        tau = np.dot(M, acc_desire) + coriolis_gravity
        print(f"科里奥力:{coriolis_force }")
        print(f"惯性:{M}")
        return tau
