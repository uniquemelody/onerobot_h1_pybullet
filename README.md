# OneRobotics A1 for PyBullet

这是 OneRobotics A1 的 PyBullet 适配仓库，包含右臂、左臂和双臂支架三个模型。
模型可以直接加载、运动和自动验证；不修改 PyBullet 仿真器本身。

## 第一次查看（复制两行）

```bash
cd ~/桌面/onerobot_h1-pybullet
bash scripts/open_demo.sh right
```

第一次运行会自动安装独立环境。看到 PyBullet 窗口和机械臂即表示右臂加载成功；
关闭窗口或在终端按 `Ctrl+C` 退出。

查看另外两个模型：

```bash
bash scripts/open_demo.sh left
bash scripts/open_demo.sh bimanual
```

模型名称只有三个：`right`（右臂）、`left`（左臂）、`bimanual`（双臂）。

## 一键自动验收

```bash
bash scripts/validate_all.sh
```

最后出现 `ALL VALIDATIONS PASSED` 表示：源码哈希、三个 URDF、所有网格路径、
7/7/14 个可动关节、关节限位、小幅运动、命令和代码格式都通过。

## 已完成的适配

- 固定公开来源：<https://github.com/katazen/onerobot_h1> commit
  `ecf530911284ba0e559f7a24dc222fd8e60d31ed`；
- 生成三个自包含目录，`model.urdf` 引用的 STL 均在同一资产目录内；
- 仅移除 PyBullet 不使用的顶层 MuJoCo 标签，物理模型字段保持不变；
- 使用 PyBullet 3.2.7、Python 3.11，并隔离本机 ROS Python 环境；
- 提供 GUI 演示、DIRECT 无界面测试、来源哈希和许可证记录。

主要成果位于：

```text
assets/onerobotics_a1_right_arm/
assets/onerobotics_a1_left_arm/
assets/onerobotics_a1_bimanual_stand/
```

## 来源与许可证

OneRobotics A1 机器人资产 © 2026 OneRobotics，采用 CC BY 4.0 许可。
改动与署名详见 `ASSET_LICENSE_STATUS.md`，完整条款见
`LICENSES/CC-BY-4.0.txt`。本仓库新增代码采用 BSD 3-Clause 许可。

独立手臂的 Link7 质量和惯量仍是上游标注的临时值；模型不含夹爪。
双臂源 URDF 中的零 effort/velocity 是上游占位值，演示加载器按公开的硬件参数
提供控制力，不把这些控制参数伪装成 CAD 原始数据。

当前发布状态和上游贡献流程见 [`docs/PUBLISHING.md`](docs/PUBLISHING.md)。
