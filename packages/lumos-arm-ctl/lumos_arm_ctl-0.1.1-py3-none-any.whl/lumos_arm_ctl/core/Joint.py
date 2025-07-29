import json
import lcm
import sys
import time
import threading
import logging
import numpy as np
from collections import deque
import os
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
logger = logging.getLogger("Joint")
from lumos_arm_ctl.utils.logging_config import setup_logging
setup_logging()
from lumos_arm_ctl.lcm.python.testing_tools_package import testing_tools_package
from lumos_arm_ctl.lcm.python.ecat_debug_data_lcmt import ecat_debug_data_lcmt
from lumos_arm_ctl.lcm.python.ecat_debug_cmd_lcmt import ecat_debug_cmd_lcmt
from lumos_arm_ctl.lcm.python.arm_control_data_lcmt import arm_control_data_lcmt
import copy
from lumos_arm_ctl.core.CTL_CONST import JointCtlParams
from loop_rate_limiters import RateLimiter
class RealTimeController:
    """实时控制基类"""
    def __init__(self):
        self._rt_priority_set = False
        self._cpu_affinity_set = False
        
    def _set_realtime_priority(self):
        """设置实时进程优先级 (Linux)"""
        try:
            #os.system(f"sudo chrt -f 99 {os.getpid()}")
            self._rt_priority_set = True
        except:
            logger.warning("需要root权限设置实时优先级")

    def _set_cpu_affinity(self):
        """绑定CPU核心"""
        try:
            p = psutil.Process()
            p.cpu_affinity([psutil.cpu_count() - 1])
            self._cpu_affinity_set = True
        except:
            logger.warning("无法设置CPU亲和性")

class JointController(RealTimeController):
    """
    关节控制器类，支持单关节和多关节控制。
    
    参数:
        joint_ctype (list或str): 关节类型，可以是以下值之一或列表：
            'LEG_L' - 左腿
            'LEG_R' - 右腿
            'ARM_L' - 左臂
            'ARM_R' - 右臂
            'HEAD' - 头部
            'WAIST' - 腰部
            
        joint_id (list或int): 关节ID或ID列表
        
        ctl_word (list或int): 控制字或控制字列表，可选值：
            -1: 清除错误
             0: 调试模式
           200: 复位
             3: 混合环控制
             4: 串联PID控制
             5: ARDC位置环控制
             6: ARDC速度环控制
           255: 电机断使能
            14: 保存错误数据
             8: 标零
           156: 读取错误数据
           157: 参数设置
           158: 齿槽力开关
           249: 无编码器的自转/编码器校准
           251: ARDC控制模式下的齿槽力、摩擦力标定
           252: PID速度环控制模式下的齿槽力、摩擦力标定
           254: Eoffset标定
        
        ctl_par (list或dict, 可选): 每个关节的控制参数，list中元素为dict
    """
    
    def __init__(self, joint_ctype=None, joint_id=None,ctl_word=None, ctl_par=None,udp_url="udpm://239.255.76.67:7667?ttl=255"):
        """
        初始化关节控制器
        
        参数:
            joint_ctype: 关节类型
            joint_id: 关节ID
            ctl_word: 默认控制字
            ctl_par: 默认控制参数
        """
        self._validate_init_params(joint_ctype, joint_id, ctl_word, ctl_par)
    
        # 初始化成员变量
        self.joint_num = len(self.joint_id)  # 关节数量
        self.udp_url=udp_url
        self.WATER_MARK = 100  # 初始数据丢弃阈值
        self._initial_mask_flag = False  # 初始数据跳过标志
        self.lcm = None  # LCM对象
        self.isconnect = False  # 连接状态
        self.receive = 0  # 接收计数器
        self.joint_data = [None] * self.joint_num  # 关节数据存储
        self.joint_cmd_data = [None] * self.joint_num  # 关节命令数据存储
        self.lcm_flag = False  # LCM线程运行标志
        self.lcm_thread = None  # LCM线程对象
        self.lock=threading.Lock()
        self.joint_limit=[-np.pi*5/6,np.pi*5/6]
        #数据存储
        self.data_buffer = [deque(maxlen=100) for _ in range(self.joint_num)]
        self.last_update_time = [0] * self.joint_num
        self.record_fre=200
        self.rate_ctl= RateLimiter(self.record_fre)
        
        # #关节绘图
        # self.joint_positions_history = [[] for _ in range(self.joint_num)]  # 每个关节的历史数据
        # self.time_history = []  # 时间戳历史
        # self.start_time = time.time()  # 记录开始时间
        # self.save_plot = False
        # self.rows = int(self.joint_num**0.5)  # 行数（尽量接近正方形）
        # self.cols = (self.joint_num + self.rows - 1) // self.rows  # 列数
        # self.fig, axs = plt.subplots(self.rows, self.cols, figsize=(4 * self.cols, 3 * self.rows))
        # if self.joint_num == 1:
        #     self.axs = [[axs]]  # 单关节时手动包装成二维数组
        # else:
        #     self.axs = [list(axs.flatten())[:self.joint_num]]  # 调整为二维列表并截取多余子图
        # # 初始化线条
        # self.lines = []
        # for i in range(self.joint_num):
        #     row, col = divmod(i, self.cols)  # 计算当前关节对应的子图位置
        #     line, = self.axs[row][col].plot([], [], lw=2)
        #     self.lines.append(line)
        
        # self.save_plot = False  # 是否保存图像的标志
        

    def safety_shutdown_on_joint_limit_reached(self):
        """软限位，出现超角度退出"""
        logger.info("安全检测线程已启动")
        # # 启动动态画图
        # # 启动动态画图
        # ani = FuncAnimation(
        #     self.fig,
        #     self.update_plot,          # 更新函数
        #     init_func=self.init_plot,  # 初始化函数
        #     interval=10,               # 每 10 毫秒更新一次
        #     blit=True                  # 使用 blit 提高性能
        # )
        # self.time_history.append(current_time)
        # for i, pos in enumerate(pos_list):
        #     self.joint_positions_history[i].append(pos)
            
        while True:
            pos_list=self.get_joint_pos()
            #current_time = time.time() - self.start_time
            for pos in pos_list:
                if pos<self.joint_limit[0] or pos>self.joint_limit[1]:
                    logger.error(f"关节位置{pos}超过限位({self.joint_limit[0]},{self.joint_limit[1]})，紧急退出")
                    self.disconnect()
                    raise ValueError(f"关节位置{pos}超过限位({self.joint_limit[0]},{self.joint_limit[1]})，紧急退出")
            time.sleep(0.001)
    
    # def init_plot(self):
    #     """初始化绘图"""
    #     for line in self.lines:
    #         line.set_data([], [])  # 清空线条数据
    #     return self.lines

    # def update_plot(self, frame):
    #     """更新动态绘图"""
    #     for i, line in enumerate(self.lines):
    #         row, col = divmod(i, self.cols)  # 计算当前关节对应的子图位置
    #         line.set_data(self.time_history, self.joint_positions_history[i])
    #         self.axs[row][col].set_xlim(0, max(10, self.time_history[-1]))  # 动态调整 x 轴范围
    #         self.axs[row][col].set_ylim(self.joint_limit[0], self.joint_limit[1])  # 动态调整 y 轴范围
    #         self.axs[row][col].set_title(f"Joint {i}")
    #         self.axs[row][col].set_xlabel("Time (s)")
    #         self.axs[row][col].set_ylabel(f"Angle (rad)")
    #     return self.lines

    # def save_dynamic_plot(self):
    #     """保存动态图像为 PNG 和 PDF 文件"""
    #     timestamp = time.strftime("%Y%m%d_%H%M%S")
    #     png_filename = f"joint_angles_{timestamp}.png"
    #     pdf_filename = f"joint_angles_{timestamp}.pdf"
        
    #     # 保存 PNG 图像
    #     plt.savefig(png_filename, dpi=300)
    #     logger.info(f"动态图像已保存为 PNG 文件: {png_filename}")
        
    #     # 保存 PDF 文件
    #     plt.savefig(pdf_filename)
    #     logger.info(f"动态图像已保存为 PDF 文件: {pdf_filename}")
    
        
    
    def _validate_init_params(self, joint_ctype, joint_id, ctl_word, ctl_par):
        """参数验证优化"""
        if not any([joint_ctype, joint_id, ctl_word, ctl_par]):
            raise ValueError("所有参数都不能为空!")
            
        # 类型转换
        self.joint_ctype = [joint_ctype] if isinstance(joint_ctype, str) else list(joint_ctype)
        self.joint_id = [joint_id] if isinstance(joint_id, int) else list(joint_id)
        self.joint_ctl_word = [ctl_word] if isinstance(ctl_word, int) else list(ctl_word)
        self.ctl_par = [ctl_par] if isinstance(ctl_par, (int, dict)) else list(ctl_par)
        self.jType = "J_MOTOR_1TO5"

        # 长度检查
        param_lengths = {
            "joint_ctype": len(self.joint_ctype),
            "joint_id": len(self.joint_id),
            "joint_ctl_word": len(self.joint_ctl_word),
            "ctl_par": len(self.ctl_par)
        }
        if len(set(param_lengths.values())) != 1:
            raise ValueError(f"参数长度不匹配: {param_lengths}")
    

    def connect(self):
        """
        连接LCM并启动监听线程
        
        参数:
            udp_url: LCM网络地址
        """
        if self.isconnect:
            logger.warning("已连接，无需重复连接")
            return
        
        self._set_realtime_priority()
        self._set_cpu_affinity()
        
        # 启动LCM监听线程    
        self.lcm_flag = True
        self.lcm_thread = threading.Thread(
            target=self._rt_lcm_listener,
            args=(self.udp_url,),
            name="LCM_RT_Thread",
            daemon=True
        )
        self.lcm_thread.start() 
        self.isconnect = True
        logger.info(f"实时控制器已启动 @ {self.udp_url}")
        
        # 软限位
        self.safety_shutdow_thread = threading.Thread(
            target=self.safety_shutdown_on_joint_limit_reached,
            name="safety_shutdown",
            daemon=True
        )
        self.safety_shutdow_thread.start()


    def _rt_lcm_listener(self, udp_url):
        """实时LCM监听线程"""
        try:
            # 低延迟LCM配置
            self.lcm = lcm.LCM(udp_url)
            #self.lcm.set_queue_capacity(0)  # 禁用缓冲
            
            # 高效订阅
            subscriptions = []
            channel_map = {}  # 通道到索引的映射
            
            for i, ctype in enumerate(self.joint_ctype):
                channel = (f"ecat_debug_data_{ctype}" if ctype in ['ARM_L', 'ARM_R'] 
                          else f"ecat_debug_data{ctype}")
                channel_map[channel] = i
                subscriptions.append(self.lcm.subscribe(channel, self._handle_rt_data))
            
            # 实时处理循环
            while self.lcm_flag:
                self.lcm.handle_timeout(100)  # 1ms超时
                # proc_time = (time.perf_counter() - start) * 1000
                # if proc_time > 100:  # 超过2ms警告
                #     logger.warning(f"LCM处理延迟: {proc_time:.2f}ms")
                    
        except Exception as e:
            logger.error(f"监听线程异常: {str(e)}")
            raise
        finally:
            for sub in subscriptions:
                self.lcm.unsubscribe(sub)
            logger.info("LCM监听线程已退出")

    def _handle_rt_data(self, channel, data):
        """优化后的实时数据处理"""
        try:
            # 批量解码消息并更新关节数据
            for i, ctype in enumerate(self.joint_ctype):
                if channel == f"ecat_debug_data_{ctype}" and ctype in ['ARM_L', 'ARM_R']:
                    msg = arm_control_data_lcmt.decode(data)
                    cur_pos = msg.joint_curPos[self.joint_id[i]]
                    cur_vel = msg.joint_curVel[self.joint_id[i]]
                elif channel == f"ecat_debug_data{ctype}" and ctype in ['LEG_L', 'LEG_R']:
                    msg = ecat_debug_data_lcmt.decode(data)
                    cur_pos = msg.original_curPos[self.joint_id[i]]
                    cur_vel = msg.original_curVel[self.joint_id[i]]
                else:
                    continue
                
                # 更新接收计数器
                if self.receive < self.WATER_MARK:
                    self.receive += 1
                
                # 更新关节数据
                with self.lock:
                    self.joint_data[i] = [cur_pos, cur_vel]
        except Exception as e:
            logger.error(f"接收数据消息时出错: {str(e)}")


    def handle_cmd_data(self, channel, data):
        """
        处理接收到的关节命令消息
        
        参数:
            channel: 消息通道
            data: 原始消息数据
        """
        try:
            for i, ctype in enumerate(self.joint_ctype):
                if channel == f"ecat_debug_cmd{ctype}":
                    msg = ecat_debug_cmd_lcmt.decode(data)
                    if self.receive < self.WATER_MARK:
                        self.receive += 1
                    self.joint_cmd_data[i] = [
                        msg.tarPosL[self.joint_id[i]],
                        msg.tarVel[self.joint_id[i]]]
        except Exception as e:
            logger.error(f"处理关节命令消息时出错: {str(e)}")
            

    def disconnect(self):
        """断开LCM连接并停止监听线程"""
        if not self.isconnect:
            logger.warning("没有连接上，无需断开")
            return
        if self.lcm_thread and self.lcm_thread.is_alive():
            self.lcm_thread.join(timeout=2)
        if self.safety_shutdow_thread and self.safety_shutdow_thread.is_alive():
            self.safety_shutdow_thread.join(timeout=2)
        self.joint_disable()
        logger.info("关节已释放")
        self._initial_mask_flag = False
        self.lcm_flag = False
        self.isconnect = False
        self.receive=0
        # if self.save_plot:
        #     self.save_dynamic_plot()  # 保存图像
        #     if hasattr(self, 'fig') and self.fig:
        #         plt.close(self.fig)

    def get_ctrl_data(self, tar_joint_pos_list, ctl_word_list=None, ctl_mode_pars_list=None):
        """
        生成控制指令数据。
            参数:
                tar_joint_pos_list (list): 每个关节的目标位置列表。
                    - 列表中的每个元素是一个浮点数，表示对应关节的目标位置：
                    [
                        target_pos_1,
                        target_pos_2,
                        ...
                    ]
                ctl_word_list (list): 控制字列表  
                    -当 self.joint_ctl_word=3 对应电流环控制时，ctl_mode_par 的参数为：
                        [
                            {
                                "res1": kp, # 比例增益
                                "res2": kd, # 微分增益
                            },
                            ...
                        ]        self.subscription_completed = False

                ctl_mode_pars_list (list): 每个关节对应的控制参数字典列表。
                    - 列表中的每个元素是一个字典，与 self.joint_ctl_word 对应：
                        - 当 self.joint_ctl_word=5 对应 ARDC 位置环控制时，ctl_mode_par 的参数为：
                            [
                                {
                                    "res3": b0s,       # 初始速度
                                    "res4": w0s,       # 初始加速度
                                    "tarVel": tarvels, # 目标速度
                                    "tarCur": tarcurs, # 目标电流
                                },
                                ...
                            ]
                        -

            返回:
                list: 包含控制指令数据的列表，按 "cType" 分组。
                    格式示例：
                    [
                        {
                            "cType": "LEG_L",  # 关节类型
                            "joints": [       # 同一类型的关节数据列表
                                {
                                    "id": 1,                 # 关节编号
                                    "jType": "J_MOTOR_1TO5", # 关节类型
                                    "ctrlWord": 5,          # 控制字
                                    "targetPos": 0.5,       # 目标位置
                                    "res3": 1.0,            # 参数 res3
                                    "res4": 2.0,            # 参数 res4
                                    "tarVel": 0.1,          # 目标速度
                                    "tarCur": 0.2           # 目标电流
                                },
                                ...
                            ]
                        },
                        ...
                ]
        """
        # 参数检查和处理
        if ctl_word_list is None:
            ctl_word_list = self.joint_ctl_word
        if ctl_mode_pars_list is None:
            ctl_mode_pars_list = self.ctl_par
        
        # 将输入标准化为列表
        if not isinstance(ctl_mode_pars_list, list):
            ctl_mode_pars_list = [ctl_mode_pars_list]
        if not isinstance(tar_joint_pos_list, list):
            tar_joint_pos_list = [tar_joint_pos_list]
        if not isinstance(ctl_word_list, list):
            ctl_word_list = [ctl_word_list]
        
 
        # 检查参数长度是否匹配
        if not (
            len(self.joint_id) == len(ctl_mode_pars_list) and
            len(ctl_mode_pars_list) == len(tar_joint_pos_list) and
            len(tar_joint_pos_list) == len(ctl_word_list)
            ):
            raise ValueError("输入的关节数量与控制参数或目标位置的数量不匹配！")
        #TODO 同种关节检查序号是否相冲突
        #TODO 检查控制字和对应的控制参数是否匹配
        # 构造控制数据
        cType_dict = {}  # 按关节类型分组
        
        for i in range(len(self.joint_id)):
            # 构造单个关节的控制数据
            joint_data = {
                "id": self.joint_id[i],
                "jType": self.jType,
                "ctrlWord": ctl_word_list[i],
                "targetPos": tar_joint_pos_list[i],
                **(ctl_mode_pars_list[i] if ctl_mode_pars_list[i] else {})
            }

            # 按关节类型分组
            cType = self.joint_ctype[i]
            if cType not in cType_dict:
                cType_dict[cType] = {"cType": cType, "joints": []}
            cType_dict[cType]["joints"].append(joint_data)

        return list(cType_dict.values())
    
    def _get_ctrl_data(self,ctl_word_list=None, ctl_mode_pars_list=None):
        """
        生成控制指令数据。
        """
        # 参数检查和处理
        if ctl_word_list is None:
            ctl_word_list = self.joint_ctl_word
        if ctl_mode_pars_list is None:
            ctl_mode_pars_list = self.ctl_par
        
        # 将输入标准化为列表
        if not isinstance(ctl_mode_pars_list, list):
            ctl_mode_pars_list = [ctl_mode_pars_list]
        if not isinstance(ctl_word_list, list):
            ctl_word_list = [ctl_word_list]
            
        # 检查参数长度是否匹配
        if not (len(self.joint_id) == len(ctl_mode_pars_list) == len(ctl_word_list)):
            raise ValueError("输入的关节数量与控制参数或目标位置的数量不匹配！")
        #TODO 同种关节检查序号是否相冲突
        #TODO 检查控制字和对应的控制参数是否匹配
        # 构造控制数据
        cType_dict = {}  # 按关节类型分组
        
        for i in range(len(self.joint_id)):
            # 构造单个关节的控制数据
            joint_data = {
                "id": self.joint_id[i],
                "jType": self.jType,
                "ctrlWord": ctl_word_list[i],
                **(ctl_mode_pars_list[i] if ctl_mode_pars_list[i] else {})
            }

            # 按关节类型分组
            cType = self.joint_ctype[i]
            if cType not in cType_dict:
                cType_dict[cType] = {"cType": cType, "joints": []}
            cType_dict[cType]["joints"].append(joint_data)

        return list(cType_dict.values())

    def joint_ctrl(self, tar_joint_pos_list, ctl_word_list=None, ctl_mode_pars_list=None):
        """
        发送多关节控制指令
        
        参数:
            tar_joint_pos_list: 目标位置列表
            ctl_word_list: 控制字列表(可选)
            ctl_mode_pars_list: 控制参数列表(可选)
        """
        if not self.isconnect:
            logger.error("未连接LCM无法控制")
            raise ConnectionError("未连接到LCM，请先调用connect方法")
            
        # 生成控制指令数据
        ctrl_data_list = self.get_ctrl_data(
            tar_joint_pos_list,
            ctl_word_list,
            ctl_mode_pars_list
        )
        logger.info(f"控制指令：{ctrl_data_list}")

        # 发送控制指令
        try:
            json_data = json.dumps(ctrl_data_list, separators=(',', ':'))  # 紧凑格式
            pkg = testing_tools_package()
            pkg.command = json_data
            
            with self.lock:
                self.lcm.publish("EXAMPLE_COMMAND", pkg.encode())
                
        except Exception as e:
            logger.error(f"指令发送失败: {str(e)}")
            raise
        
    def _joint_ctrl(self,ctl_word_list=None, ctl_mode_pars_list=None):
        """直接根据控制字和控制参数控制"""
        if not self.isconnect:
            raise ConnectionError("未连接到LCM，请先调用connect方法")
            
        # 生成控制指令数据
        ctrl_data_list = self._get_ctrl_data(
            ctl_word_list,
            ctl_mode_pars_list
        )
        logger.info(f"控制指令：{ctrl_data_list}")

        # 发送控制指令
        try:
            json_data = json.dumps(ctrl_data_list)
            logger.debug(f"发送关节指令数据: {json_data}")
            pkg = testing_tools_package()
            pkg.command = json_data
            self.lcm.publish("EXAMPLE_COMMAND", pkg.encode())
            logger.info("关节指令已发送")
        except Exception as e:
            logger.error(f"发送关节指令时出错: {str(e)}")
            raise
        

    def wait_skip_initial_mask(self, time_out=20):
        """
        等待并跳过初始的100个数据
        
        参数:
            time_out: 超时时间(秒)
            
        异常:
            TimeoutError: 如果超时未收到足够数据
        """
        if self._initial_mask_flag:
            return
            
        start_time = time.perf_counter()
        while self.receive < self.WATER_MARK:
            logger.info("正在丢弃初始数据(%d/%d)...", self.receive, self.WATER_MARK)
            if time.perf_counter() - start_time > time_out:
                raise TimeoutError(f"无法获取足够数据：超过{time_out}秒超时")
            time.sleep(1)
            
        logger.info(f"已成功跳过初始{self.WATER_MARK}个数据")
        self._initial_mask_flag = True
        

    def get_joint_pos(self):
        """获取当前关节位置列表"""
        #self.wait_skip_initial_mask()
        if self.lock:
            return [joint_data[0] for joint_data in self.joint_data if joint_data]
            #return self.joint_data[0]

    def get_joint_vel(self):
        """获取当前关节速度列表"""
        #self.wait_skip_initial_mask()
        if self.lock:
            return [joint_data[1] for joint_data in self.joint_data if joint_data]
            #return self.joint_data[1]

    # def get_joint_tor(self):
    #     """获取当前关节力矩列表"""
    #     self.wait_skip_initial_mask()
    #     return [joint_data[2] for joint_data in self.joint_data if joint_data]

    # def get_joint_LssPos(self):
    #     """获取当前关节Lss位置列表"""
    #     self.wait_skip_initial_mask()
    #     return [joint_data[3] for joint_data in self.joint_data if joint_data]

    def initialize_joint(self, pos_mode="CURRENT"):
        """
        关节初始化
        
        参数:
            pos_mode: 初始化位置模式
                "HOME" : 回到零点
                "CURRENT" : 保持当前位置
        """
        self.reset_joint_pos(pos_mode)

    def get_cmd_pos(self):
        """获取指令位置列表"""
        return [joint_cmd_data[0] for joint_cmd_data in self.joint_cmd_data if joint_cmd_data]

    def get_cmd_vel(self):
        """获取指令速度列表"""
        return [joint_cmd_data[1] for joint_cmd_data in self.joint_cmd_data if joint_cmd_data]

    def joint_disable(self):
        """关节失能"""
        self.reset_200()

    def reset_200(self):
        """发送reset 200指令"""
        logger.info("开始发送reset 200指令...")

        # 构造reset指令参数
        tar_joint_pos_list = list(np.zeros(self.joint_num))
        ctrl_word_list =list(200 * np.ones(self.joint_num))
        ctl_mode_pars_list = [{'res1': 0, 'res2': 0} for _ in range(self.joint_num)]
        
        # 发送指令
        self.joint_ctrl(tar_joint_pos_list, ctrl_word_list, ctl_mode_pars_list)
        logger.info("reset 200指令发送完成")
        #time.sleep(0.01)
    def reset_joint_pos(self, reset_mode="HOME"):
        """
        重置关节位置

                "CURRENT" : 保持当前位置
        """
        # 获取目标位置
        joint_pos = np.zeros(self.joint_num)
        if reset_mode == "CURRENT":
            joint_pos = self.get_joint_pos()
            
        # 执行重置流程
        self.reset_200()
        self.linear_trajectory_plan_pd(self.get_joint_pos,joint_pos)
        #self.joint_ctrl(joint_pos, self.joint_ctl_word, self.ctl_par)
        self.reset_200()
        logger.info(f"关节位置已重置({reset_mode}模式)")

    
     
    def linear_trajectory_plan_pd(self,pos_start=None ,pos_end=None,interp_num=500,kp=None,kd=None):
        """线性插入值规划轨迹"""
        if pos_start is None:
            pos_start=self.get_joint_pos()
        if pos_end is None:
            pos_end=self.get_joint_pos()
            
        if not (len(pos_start)==len(pos_end)==self.joint_num):
            logger.error("轨迹规划起始关节位置长度与关节长度不匹配")
            raise ValueError("轨迹规划起始关节位置长度与关节长度不匹配,请检查起始位置长度")
        
        if kp is None or kd is None:
            kp,kd=JointCtlParams.get_default_pd_par(self.joint_ctype,self.joint_id)
            
        kp = [kp] if not isinstance(kp, list) else kp
        kd = [kd] if not isinstance(kd,list) else kd
        ctl_word = [JointCtlParams.PD_CW for _ in range(self.joint_num)]
        ctl_par=[{"res1":kp[i],"res2":kd[i]} for i in range(self.joint_num)]
        # 将输入参数转换为列表形式
        pos_start = [pos_start] if not isinstance(pos_start, list) else pos_start
        pos_end = [pos_end] if not isinstance(pos_end, list) else pos_end
        #重置之前设置
        self.reset_200()
        # 开始轨迹规划
        interpolated_points = [np.linspace(start, end, interp_num) for start, end in zip(pos_start, pos_end)]
        for i in range(interp_num):
            target_pos = [joint_points[i] for joint_points in interpolated_points]
            self.joint_ctrl(target_pos,ctl_word,ctl_par)
            time.sleep(0.005)
            
    def joint_pd_ctl(self,pos_end,kp=None,kd=None):
        """线性插入值规划轨迹"""
            
        if not (len(pos_end)==self.joint_num):
            logger.error("轨迹规划起始关节位置长度与关节长度不匹配")
            raise ValueError("轨迹规划起始关节位置长度与关节长度不匹配,请检查起始位置长度")
        
        if kp is None or kd is None:
            kp,kd=JointCtlParams.get_default_pd_par(self.joint_ctype,self.joint_id)
            
        kp = [kp] if not isinstance(kp, list) else kp
        kd = [kd] if not isinstance(kd,list) else kd
        ctl_word = [JointCtlParams.PD_CW for _ in range(self.joint_num)]
        ctl_par=[{"res1":kp[i],"res2":kd[i]} for i in range(self.joint_num)]
        # 将输入参数转换为列表形式
        pos_end = [pos_end] if not isinstance(pos_end, list) else pos_end
        #重置之前设置
        #self.reset_200()
        self.joint_ctrl(pos_end,ctl_word,ctl_par)
        
        
        
    def joint_adrc_ctl(self,pos_start=None,pos_end=None,b0s=None,w0s=None,tar_vels=None,tar_curs=None):
        """ADRC直接控制"""
        if pos_end is not None:
            if not (len(pos_end)==self.joint_num):
                logger.error("ADRC起始关节位置长度与关节长度不匹配")
                raise ValueError("ADRC起始关节位置长度与关节长度不匹配,请检查起始位置长度")
        if pos_start is not None:
            if not (len(pos_start)==self.joint_num):
                logger.error("ADRC起始关节位置长度与关节长度不匹配")
                raise ValueError("ADRC起始关节位置长度与关节长度不匹配,请检查起始位置长度")
        # 将输入参数转换为列表形式
        if pos_start is not None:
            pos_start = [pos_start] if not isinstance(pos_start, list) else pos_start
        if pos_end is not None:
            pos_end = [pos_end] if not isinstance(pos_end, list) else pos_end
        
        if b0s is None or w0s is None or tar_vels is None or tar_curs is None:
            b0s,w0s,tar_vels,tar_curs=JointCtlParams.get_default_adrc_par(self.joint_ctype,self.joint_id)
        joints_cw=[JointCtlParams.ADRC_CW for _ in range(self.joint_num)]
        #ctl_word_par=[{"res4":w0s[i],"tarVel":tar_vels[i],"tarCur":tar_curs[i]} for i in range(self.joint_num)]
        # ctl_word_par=[{"res4":200,"tarVel":10,"tarCur":2.5}]
        ctl_word_par=[{"res3":b0s[i],"res4":w0s[i],"tarVel":tar_vels[i],"tarCur":tar_curs[i]} for i in range(self.joint_num)]
        #ctl_word_par=[{"res4":w0s[i],"tarVel":tar_vels[i]} for i in range(self.joint_num)]
        print(ctl_word_par)
        # #重置之前设置
        # self.reset_200()
        if pos_start is not None:
            self.joint_ctrl(pos_start,joints_cw,ctl_word_par)
            time.sleep(1)
        if pos_end is not None:
            self.joint_ctrl(pos_end,joints_cw,ctl_word_par)
    
    def joint_adrc_linear_plan(self,pos_start,pos_end,b0s=None,w0s=None,tar_vels=None,tar_curs=None,interp_num=400):
        """ADRC直接控制"""
        if not (len(pos_start)==len(pos_end)==self.joint_num):
            logger.error("ADRC起始关节位置长度与关节长度不匹配")
            raise ValueError("ADRC起始关节位置长度与关节长度不匹配,请检查起始位置长度")
        # 将输入参数转换为列表形式
        pos_start = [pos_start] if not isinstance(pos_start, list) else pos_start
        pos_end = [pos_end] if not isinstance(pos_end, list) else pos_end
        
        if b0s is None or w0s is None or tar_vels is None or tar_curs is None:
            b0s,w0s,tar_vels,tar_curs=JointCtlParams.get_default_adrc_par(self.joint_ctype,self.joint_id)
        joints_cw=[JointCtlParams.ADRC_CW for _ in range(self.joint_num)]
        #ctl_word_par=[{"res4":w0s[i],"tarVel":tar_vels[i],"tarCur":tar_curs[i]} for i in range(self.joint_num)]
        # ctl_word_par=[{"res4":200,"tarVel":10,"tarCur":2.5}]
        ctl_word_par=[{"res3":b0s[i],"res4":w0s[i],"tarVel":tar_vels[i],"tarCur":tar_curs[i]} for i in range(self.joint_num)]
        #ctl_word_par=[{"res4":w0s[i],"tarVel":tar_vels[i]} for i in range(self.joint_num)]
        #重置之前设置
        self.reset_200()
        interpolated_points = [np.linspace(start, end, interp_num) for start, end in zip(pos_start, pos_end)]
        for i in range(interp_num):
            target_pos = [joint_points[i] for joint_points in interpolated_points]
            self.joint_ctrl(target_pos,joints_cw,ctl_word_par)
            time.sleep(0.005)
    
    def reset_word3(self):
        cw=[3 for _ in range(self.joint_num)]
        cw_par=[{"res4":0} for _ in range(self.joint_num)] 
        pos=[0 for _ in range(self.joint_num)]
        self.joint_ctrl(pos,cw,cw_par)
        print("控制字3已重置")  
        
    def set_zero(self):
        self.reset_200()
        pos=[0 for _ in range(self.joint_num)]
        ctl_word=[8 for _ in range(self.joint_num)]
        ctl_par=[{"res1":0,"res2":0} for _ in range(self.joint_num)]
        self.joint_ctrl(pos,ctl_word,ctl_par)
        
    def ctl_joint_pd(self):
        pass
    
    def ctl_joint_bw(self):
        pass
    def record_data_mode(self):
        """拖动数据采集"""
        # pos=self.get_joint_pos()
        # cw=[3]*self.joint_num
        # cw_par=[{"res1":0,"res2":0}]*self.joint_num
        # self.joint_ctrl(pos,cw,cw_par)
        pass
    
    def record_and_save_data(self, duration, filename="joint_data.json"):
        """
        记录关节角度数据并保存到文件。
        :param joint_controller: 关节控制器实例
        :param duration: 记录数据的总时长（秒）
        :param filename: 保存数据的文件名
        """
        logger.info("开始记录关节角度数据...")
        start_time = time.time()
        data = []

        while time.time() - start_time < duration:
            cur_pos = self.get_joint_pos()
            data.append(cur_pos)
            self.rate_ctl.sleep()
        # 保存数据到文件
        with self.lock:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
        logger.info(f"数据已保存到文件: {filename}")
        
    def load_record_data(self, filename="joint_data.json"):
        """
        从文件加载关节角度数据。
        :param joint_controller: 关节控制器实例
        :param filename: 数据文件名
        """
        logger.info("开始加载并运行关节角度数据...")
        try:
            # 从文件加载数据
            with open(filename, "r") as f:
                data = json.load(f)
            self.print_data_info(data)
            return data
        except FileNotFoundError:
            logger.error(f"文件 {filename} 未找到，请先记录数据！")
            
    def print_data_info(self,data):
        if data is not None:
            logger.info(f"数据类型: {type(data)}")
            # 打印数据大小（字节）
            data_size_bytes = len(json.dumps(data).encode('utf-8'))
            logger.info(f"数据大小: {data_size_bytes} 字节")
            # 打印数据尺寸（时间步数 x 关节数）
            num_time_steps = len(data)  # 时间步数
            num_joints = len(data[0]) if data else 0  # 每个时间步的关节数
            logger.info(f"数据尺寸: {num_time_steps} 时间步 x {num_joints} 关节")
        else:
            logger.warning("空数据")
                
        
        
class LeftArmController(JointController):
    """左臂控制类"""
    def __init__(self,joint_id=None, ctl_word=None, ctl_par=None,udp_url="udpm://239.255.76.67:7667?ttl=255"):
        
        # 参数检查
        if joint_id is None:
            logger.error("请输入左臂关节id")
            raise ValueError("左臂关节id不能为空")
        joint_id= [joint_id] if not isinstance(joint_id,list) else joint_id
        joint_ctype=["ARM_L"]*len(joint_id)
        
        # 如果ctl_par，ctl_par有其中一个为空则使用内置控制
        if not ctl_par or not ctl_par:
            logger.warning("左臂控制未同时给定默认控制字与控制字参数，使用内置控制字与控制字参数，内置为控制字 3 ")
            ctl_word=[JointCtlParams.PD_CW for _ in range(len(joint_id))]
            kp,kd=JointCtlParams.get_default_pd_par(joint_ctype=joint_ctype,joint_id=joint_id)
            ctl_par=[{"res1":kp[i],"res2":kd[i]} for i in range(len(joint_id))]
        super().__init__(joint_ctype, joint_id, ctl_word, ctl_par,udp_url)
        
class RightArmController(JointController):
    """右臂控制类"""
    def __init__(self,joint_id=None, ctl_word=None, ctl_par=None,udp_url="udpm://239.255.76.67:7667?ttl=255"):
        
        # 参数检查
        if joint_id is None:
            logger.error("请输入右臂关节id")
            raise ValueError("左臂关节id不能为空")
        joint_id= [joint_id] if not isinstance(joint_id,list) else joint_id
        joint_ctype=["ARM_R"]*len(joint_id)
        
        # 如果ctl_par，ctl_par有其中一个为空则使用内置控制
        if not ctl_par or not ctl_par:
            logger.warning("右臂控制未同时给定默认控制字与控制字参数，使用内置控制字与控制字参数，内置为控制字 3 ")
            ctl_word=[JointCtlParams.PD_CW for _ in range(len(joint_id))]
            kp,kd=JointCtlParams.get_default_pd_par(joint_ctype=joint_ctype,joint_id=joint_id)
            ctl_par=[{"res1":kp[i],"res2":kd[i]} for i in range(len(joint_id))]
        super().__init__(joint_ctype, joint_id, ctl_word, ctl_par,udp_url)
        


class LeftRightArmController(JointController):
    """左右臂控制类"""
    def __init__(self,left_joint_id=None,right_joint_id=None, ctl_word=None, ctl_par=None,udp_url="udpm://239.255.76.67:7667?ttl=255"):
        
        # 参数检查
        if left_joint_id is None:
            logger.error("请输入左臂关节id")
            raise ValueError("左臂关节id不能为空")
        if right_joint_id is None:
            logger.error("请输入右臂关节id")
            raise ValueError("右臂关节id不能为空")
        left_joint_id= [left_joint_id] if  not isinstance(left_joint_id,list) else left_joint_id
        right_joint_id= [right_joint_id] if not isinstance(right_joint_id,list) else right_joint_id
        joint_id=left_joint_id+right_joint_id
        left_joint_ctype=["ARM_L"]*len(left_joint_id)
        right_joint_ctype=["ARM_R"]*len(right_joint_id)
        joint_ctype=left_joint_ctype+right_joint_ctype
        self.left_arm_num=len(left_joint_id)
        self.right_arm_num=len(right_joint_id)
        # 如果ctl_par，ctl_par有其中一个为空则使用内置控制
        if ctl_par is None or ctl_par is None:
            logger.warning("双臂控制未同时给定默认控制字与控制字参数，使用内置控制字与控制字参数，内置为控制字 3 ")
            ctl_word=[JointCtlParams.PD_CW for _ in range(len(joint_id))]
            kp,kd=JointCtlParams.get_default_pd_par(joint_ctype=joint_ctype,joint_id=joint_id)
            ctl_par=[{"res1":kp[i],"res2":kd[i]} for i in range(len(joint_id))]
        super().__init__(joint_ctype, joint_id, ctl_word, ctl_par,udp_url)
                

        
        
