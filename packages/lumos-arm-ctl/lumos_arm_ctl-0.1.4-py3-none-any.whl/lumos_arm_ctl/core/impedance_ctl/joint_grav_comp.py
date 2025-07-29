import threading
import time
import lcm
import sys
from . jnt_imp_controller import JntImpedance
from lumos_arm_ctl.core.Joint import LeftRightArmController
import numpy as np
class JointGravComp:
    def __init__(self,joint_controller=LeftRightArmController([i for i in range(7)],[i for i in range(7)]),urdf_path="models/urdf/lus1_fix_leg_gripper.urdf"):
        self.arm_joint_controller=joint_controller
        self.force_controller=JntImpedance(urdf_path=urdf_path,b=0.5,k=0.2)
        self.lock = threading.Lock()
    
    def grav_comp_step(self,action,grav_comp_enable=True):
        """补偿重力"""
        if grav_comp_enable:
            joint_pos = self.arm_joint_controller.get_joint_pos()
            joint_vel =self.arm_joint_controller.get_joint_vel()
            # 左右两臂自由度相同的处理
            # 如果长度不匹配，调整joint_pos和joint_vel
            if len(joint_pos) != self.force_controller.kd_solver._JOINT_NUM:
                target_num = self.force_controller.kd_solver._JOINT_NUM
                half_target = target_num // 2
                
                # 分割原始数据为前后两半
                orig_half = len(joint_pos) // 2
                front_half = joint_pos[:orig_half]
                back_half = joint_pos[orig_half:]
                
                # 调整前后半部分的长度
                if len(front_half) >= half_target:
                    front_half = front_half[:half_target]
                else:
                    front_half = np.pad(front_half, (0, half_target - len(front_half)), 'constant')
                
                if len(back_half) >= half_target:
                    back_half = back_half[:half_target]
                else:
                    back_half = np.pad(back_half, (0, half_target - len(back_half)), 'constant')
                
                # 合并调整后的数据
                joint_pos = np.concatenate([front_half, back_half])
                
                # 对joint_vel做同样的处理
                front_vel = joint_vel[:orig_half]
                back_vel = joint_vel[orig_half:]
                
                if len(front_vel) >= half_target:
                    front_vel = front_vel[:half_target]
                else:
                    front_vel = np.pad(front_vel, (0, half_target - len(front_vel)), 'constant')
                
                if len(back_vel) >= half_target:
                    back_vel = back_vel[:half_target]
                else:
                    back_vel = np.pad(back_vel, (0, half_target - len(back_vel)), 'constant')
                
                joint_vel = np.concatenate([front_vel, back_vel])
                
                
                # 对action处理
                front_action = action[:orig_half]
                back_action = action[orig_half:]
                
                if len(front_action) >= half_target:
                    front_action = front_action[:half_target]
                else:
                    front_action = np.pad(front_action, (0, half_target - len(front_action)), 'constant')
                
                if len(back_action) >= half_target:
                    back_action = back_action[:half_target]
                else:
                    back_action = np.pad(back_action, (0, half_target - len(back_action)), 'constant')
                
                action = np.concatenate([front_action, back_action])
                   
            print(f"位置：{joint_pos}")
            print(f"速度：{joint_pos}")
            torque = self.force_controller.compute_jnt_torque(
            action,
            v_des=np.zeros(self.force_controller.kd_solver._JOINT_NUM),
            q_cur=np.array(joint_pos),
            v_cur=np.array(joint_vel),
            )
        else:
            torque= np.zeros(self.force_controller.kd_solver._JOINT_NUM)
        
        # 如果不相等变回原来的长度    
        if len(torque) != self.arm_joint_controller.joint_num:
            tor_half_target = self.arm_joint_controller.joint_num // 2
            half_current = len(torque) // 2
            front_tor = torque[:half_current]
            back_tor = torque[half_current:]
            if tor_half_target>=half_current:
                # 前后半部分补零
                front_tor = np.pad(front_tor, (0, tor_half_target - len(torque[:half_current])), 'constant')
                back_tor = np.pad(back_tor, (0, tor_half_target - len(torque[half_current:])), 'constant')
            else:
                front_tor=front_tor[:tor_half_target]
                back_tor=back_tor[:tor_half_target]
            torque = np.concatenate([front_tor, back_tor])
        return list(torque)
        
    def run(self):
        if not self.arm_joint_controller.isconnect:
            self.arm_joint_controller.connect()
            self.arm_joint_controller.wait_skip_initial_mask()
            self.arm_joint_controller.reset_200()
            self.arm_joint_controller.reset_word3()
            self.arm_joint_controller.reset_200()
        try:
            while True:
                tar_pos=self.arm_joint_controller.get_joint_pos()
                torque=self.grav_comp_step(tar_pos,True)
                print(f"当下力矩：{torque}")
                control_word_par=[{"tor":torque[i],"res1":0,"res2":2} for i in range(self.arm_joint_controller.joint_num)]
                with self.lock:
                    self.arm_joint_controller.joint_ctrl(tar_pos,[3]*self.arm_joint_controller.joint_num,control_word_par)
        except:
                self.arm_joint_controller.reset_200()