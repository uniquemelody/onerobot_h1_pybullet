# PyBullet 发布与上游贡献

## 当前发布状态

本项目是由 OneRobotics 独立维护的 PyBullet 资产适配，包含右臂、左臂和
双臂支架三个模型。代码与资产发布于：

<https://github.com/uniquemelody/onerobot_h1_pybullet>

PyBullet 没有 Gazebo Fuel 那样的网页资产上传表单。本仓库可直接克隆和验证，
但目前不代表这些模型已被 PyBullet 官方收录。

## 上游贡献流程

官方仓库：<https://github.com/bulletphysics/bullet3>

PyBullet 官方快速入门说明用户可以提供自己的数据文件，也可以使用随 PyBullet
发布的 `pybullet_data`。官方资产目录位于：

```text
examples/pybullet/gym/pybullet_data/
```

如果需要将模型提交至上游，建议先阅读官方最新贡献规范，并通过 Issue 确认
新增资产的接收要求。通常流程为：

1. 用个人 GitHub 账号 fork `bulletphysics/bullet3`；
2. 新建贡献分支；
3. 将 `assets/` 下三个完整模型目录复制到上述 `pybullet_data/`；
4. 保留每个目录里的 `README.md`、`LICENSE.txt` 和 `metadata.json`；
5. 增加一个最小加载示例并在 PyBullet DIRECT/GUI 中复验；
6. 推送个人 fork，向官方仓库发 Pull Request。

在上游 PR 合并前，对外应始终将本项目表述为独立适配，不宣称已被 PyBullet 官方收录。

## 上传行为记录模板

| 项目 | 记录 |
|---|---|
| 源仓库 | `katazen/onerobot_h1` |
| 源 commit | `ecf530911284ba0e559f7a24dc222fd8e60d31ed` |
| 适配平台 | PyBullet 3.2.7 |
| 模型 | right / left / bimanual |
| 本地测试 | `bash scripts/validate_all.sh` |
| 项目仓库 | `uniquemelody/onerobot_h1_pybullet` |
| 上游候选目录 | `bulletphysics/bullet3/examples/pybullet/gym/pybullet_data` |
| 许可证 | 资产 CC BY 4.0；新增代码 BSD-3-Clause |
