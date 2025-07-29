class JointCtlParams:
    """
    手臂控制器参数管理类
    提供获取默认 PD 和 ADRC 参数的方法
    """

    # PD 默认参数
    #  kp = [200, 80, 200, 200, 80, 80, 200, 80, 200, 200, 80, 80]
    # # kp = [200, 1, 1, 1, 1, 1, 200, 1, 1, 1, 1, 1]
    # kd = [6, 2, 6, 6, 2, 2, 6, 2, 6, 6, 2, 2]
    
    PD_CW = 3
    LEFT_ARM_KP = [600, 600, 600, 600, 600, 400,400,200]
    LEFT_ARM_KD = [6, 6, 6, 6, 6, 6,6,6]

    RIGHT_ARM_KP = [600, 600, 600, 600, 600, 400,400,200]
    RIGHT_ARM_KD = [6, 6, 6, 6, 6, 6,6,6]

    # ADRC 默认参数
    ADRC_CW = 5
    LEFT_ARM_B0S = [3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200]
    LEFT_ARM_W0S = [250, 250, 250, 250, 250, 250, 250, 250]
    LEFT_ARM_TAR_VELS = [20, 20, 20, 20, 20, 20, 20, 20]
    LEFT_ARM_TAR_CURS = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]

    RIGHT_ARM_B0S = [3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200]
    RIGHT_ARM_W0S = [250, 250, 250, 250, 250, 250, 250, 250]
    RIGHT_ARM_TAR_VELS = [20, 20, 20, 20, 20, 20, 20, 20]
    RIGHT_ARM_TAR_CURS = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]

    @classmethod
    def get_default_adrc_par(cls, joint_ctype, joint_id):
        """
        获得默认的 ADRC 参数
        

        Args:
            joint_ctype (list): 关节类型列表（如 ['ARM_L', 'ARM_R']）
            joint_id (list): 关节 ID 列表（如 [0, 1]）

        Returns:
            tuple: 返回 b0s, w0s, tar_vels, tar_curs
        """
        b0s, w0s, tar_vels, tar_curs = [], [], [], []
        for ctype, jid in zip(joint_ctype, joint_id):
            if ctype == 'ARM_L':
                b0s.append(cls.LEFT_ARM_B0S[jid])
                w0s.append(cls.LEFT_ARM_W0S[jid])
                tar_vels.append(cls.LEFT_ARM_TAR_VELS[jid])
                tar_curs.append(cls.LEFT_ARM_TAR_CURS[jid])
            elif ctype == 'ARM_R':
                b0s.append(cls.RIGHT_ARM_B0S[jid])
                w0s.append(cls.RIGHT_ARM_W0S[jid])
                tar_vels.append(cls.RIGHT_ARM_TAR_VELS[jid])
                tar_curs.append(cls.RIGHT_ARM_TAR_CURS[jid])
            else:
                # 对于其他类型的关节，设置默认值
                b0s.append(0)
                w0s.append(0)
                tar_vels.append(0)
                tar_curs.append(0)
        return b0s, w0s, tar_vels, tar_curs

    @classmethod
    def get_default_pd_par(cls, joint_ctype, joint_id):
        """
        获得默认的 PD 参数

        Args:
            joint_ctype (list): 关节类型列表（如 ['ARM_L', 'ARM_R']）
            joint_id (list): 关节 ID 列表（如 [0, 1]）

        Returns:
            tuple: 返回 kp, kd
        """
        kp, kd = [], []
        for ctype, jid in zip(joint_ctype, joint_id):
            if ctype == 'ARM_L':
                kp.append(cls.LEFT_ARM_KP[jid])
                kd.append(cls.LEFT_ARM_KD[jid])
            elif ctype == 'ARM_R':
                kp.append(cls.RIGHT_ARM_KP[jid])
                kd.append(cls.RIGHT_ARM_KD[jid])
            else:
                # 对于其他类型的关节，设置默认值
                kp.append(100)  # 默认值
                kd.append(1)    # 默认值
        return kp, kd