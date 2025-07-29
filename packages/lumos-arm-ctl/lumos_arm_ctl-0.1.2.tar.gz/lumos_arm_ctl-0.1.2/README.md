# 环境配置
## 克隆项目到本地
```
git clone http://git.lumosbot.tech/lumosbot/manipulation/lumos-arm-ctl.git

cd lumos_arm_ctl
```

## conda环境配置
### 安装conda环境
```
conda create -n lumos-arm-ctl python=3.10 -y
```
### 安装依赖

```
pip install -e .
```

# 项目运行
## 上位机设置

### 设置lcm

```
cd lumos_arm_ctl/lcm/
./make_types.sh

# 回到主目录
cd ~/lumos_arm_ctl
```

### 配置 ip 与rk3588网段相同
```
cd setup_scripts
./setup_usb.sh # 可进入修改其中的网络设备名

# 回到主目录
cd ~/lumos_arm_ctl
```

## rk3588设置
连上网线 `ssh boybrick@192.168.54.110` 到rk3588,`cd lumos_controller/build` `./run_arms.sh`,运行lcm命令解析程序

在上位机可通过以下查看，机器人关节角判断lcm连接是否建立成功
```
cd setup_scripts
./launch_lcm_spy.sh # 可修改对应udp地址

```

## 示例程序运行
### 实例化关节控制器

```
from lumos_arm_ctl.core.Joint import LeftRightArmController,LeftArmController

# 设置监听udp多播地址
udp_url="udpm://239.255.76.67:7667?ttl=255"

# 左右双臂
joint_controller=LeftRightArmController(left_joint_id=[i for i in range(7)],right_joint_id=[i for i in range(7)],udp_url=udp_url)

# 只有左臂
joint_controller = LeftArmController(joint_id=[i for i in range(8)],udp_url=udp_url)

# 只有右臂
joint_controller = RightArmController(joint_id=[i for i in range(8)],udp_url=udp_url)


# 任意关节控制
#需要给定，待控制joint_id的list,对应关节id的joint_ctype的list，以及默认的位置控制模式的ctl_word的list和ctl_par的list

joint_controller = JointController(joint_ctype=joint_ctype, joint_id=joint_id,ctl_word=ctl_word, ctl_par=ctl_par,udp_url=udp_url)

# 详细说明
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
    
```


连接并监听lcm

```
# 连接到 LCM
joint_controller.connect()
```
### 获取关节信息
控制接口
```
pos = joint_controller.get_joint_pos()
vel = joint_controller.get_joint_vel()

```
示例程序
```
from lumos_arm_ctl.core.Joint import LeftRightArmController,LeftArmController
# 设置监听udp多播地址
udp_url="udpm://239.255.76.67:7667?ttl=255"
## 设置需要被控制的关节id
joint_controller=LeftRightArmController(left_joint_id=[i for i in range(7)],right_joint_id=[i for i in range(7)],udp_url=udp_url)
# 连接到 LCM
joint_controller.connect()
# 跳过前面的消息
joint_controller.wait_skip_initial_mask()
# 获取关节速度和位置
pos = joint_controller.get_joint_pos()
vel = joint_controller.get_joint_vel()
os.system('clear')
print("接收到关节信息")
print(f"位置: {pos}")
print(f"速度: {vel}")
```

### 关节位置pd控制
控制接口

线性插值
```
# 默认参数
joint_controller.linear_trajectory_plan_pd(cur_pos,pos_end)
或
# 设定参数
joint_controller.linear_trajectory_plan_pd(cur_pos,pos_end,interp_num=1000,kp=kp,kd=kd)
```

直接控制
```
# 默认参数
joint_controller.joint_pd_ctl(pos_end=pos_end) 
或
# 设定参数
joint_controller.joint_pd_ctl(pos_end=cur_pos,kp=kp,kd=kd)
```
示例程序：

pd线性插值规划
```
import time
from lumos_arm_ctl.core.Joint import LeftRightArmController,LeftArmController

udp_url="udpm://239.255.76.67:7667?ttl=255"
joint_controller = LeftArmController(joint_id=[i for i in range(8)],udp_url=udp_url)
# 连接到 LCM
joint_controller.connect()
joint_controller.wait_skip_initial_mask()

cur_pos = joint_controller.get_joint_pos()
# 设置每个关节的pd参数
kp = [400, 200, 100, 600, 400, 400,400,400]
kd = [6, 2, 6, 6, 6, 6,6,6]
pos_end=cur_pos.copy()
pos_end[0]+=0.6
joint_controller.reset_200()
joint_controller.reset_word3()
joint_controller.reset_200()
# 进行插值控制
joint_controller.linear_trajectory_plan_pd(cur_pos,pos_end,interp_num=1000,kp=kp,kd=kd)

    
```

直接使用pd控制
```
joint_controller.joint_pd_ctl(pos_end=cur_pos,kp=kp,kd=kd)

```
也可使用默认kp,kd参数

```
joint_controller.linear_trajectory_plan_pd(cur_pos,pos_end)
# 或者
joint_controller.joint_pd_ctl(pos_end=cur_pos,kp=kp,kd=kd)
```


### 关节位置adrc控制
控制接口
```
# 默认参数
joint_controller.joint_adrc_ctl(pos_end=pos_end) 
或
# 设定参数
joint_controller.joint_adrc_ctl(pos_end=pos_end,b0s=b0s,w0s=w0s,tar_vels=tar_vels,tar_curs=tar_curs) 
```
示例程序
```
import time
import lcm
import sys
import os
from lumos_arm_ctl.core.Joint import LeftRightArmController,LeftArmController

#joint_controller = LeftRightArmController([i for i in range(6)],[i for i in range(6)])
#joint_controller = LeftArmController([i for i in range(7)])
udp_url="udpm://239.255.76.67:7667?ttl=255"
joint_controller = LeftArmController(joint_id=[i for i in range(8)],udp_url=udp_url)
#joint_controller = LeftArmController([0],[3],[{"res1":200,"res2":6}])
# 连接到 LCM
joint_controller.connect()
#joint_controller.connect("udpm://239.255.76.66:7668?ttl=1")
joint_controller.wait_skip_initial_mask()

# 读取并输出当前关节数据
try:
    b0s=[200,0,0,0,0,0,0,0]
    w0s=[200,100,100,200,100,100,0,0]
    # b0s=[0]
    # w0s=[200]
    joint_controller.reset_200()
    tar_vels=[0.4 for _ in range(joint_controller.joint_num)]
    tar_curs=[2.5 for _ in range(joint_controller.joint_num)]
    cur_pos = joint_controller.get_joint_pos()
    pos_end=cur_pos.copy()
    pos_end[0]=1.4
    #pos_end[5]+=0.4s
    # pos_end[6]=0.8
    # pos_end[7]=0.8
    pos_end[6]=0
    pos_end[7]=0
    # adrc控制
    joint_controller.joint_adrc_ctl(pos_end=pos_end,b0s=b0s,w0s=w0s,tar_vels=tar_vels,tar_curs=tar_curs)

    
except KeyboardInterrupt:
    joint_controller.reset_200()
    print("读取已停止。")
finally:
     # 断开 LCM 连接
     joint_controller.disconnect()
```
或者使用默认参数：
```
joint_controller.joint_adrc_ctl(pos_end=pos_end)
```

### 通用控制接口
根据对应关节id的目标位置，控制字，以及控制字对应控制参数 可见ethercat协议
```
joint_controller.joint_ctrl(tar_joint_pos_list=tar_pos,ctl_word_list=ctl_word_list, ctl_mode_pars_list=control_word_par)
```







