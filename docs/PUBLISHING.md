# PyBullet 资产发布记录

## 结论

PyBullet 没有 Gazebo Fuel 那样的网页资产上传表单。正确交付顺序是：先把本仓库
上传到个人 GitHub，mentor 可以直接拉取；如果需要进入 PyBullet 随安装包发布的
官方资产集合，再向 `bulletphysics/bullet3` 提交 Pull Request（PR）。

## 当前个人仓库目标

目标网址：<https://github.com/uniquemelody/onerobot_h1_pybullet>

本地验证通过后，在 GitHub 网页新建一个空的公开仓库
`uniquemelody/onerobot_h1_pybullet`，不要勾选自动添加 README、许可证或
`.gitignore`，然后执行：

```bash
cd ~/桌面/onerobot_h1-pybullet
git remote add personal git@github.com:uniquemelody/onerobot_h1_pybullet.git
git push -u personal main
```

## 如 mentor 要求提交官方 PyBullet

官方仓库：<https://github.com/bulletphysics/bullet3>

PyBullet 官方快速入门说明用户可以提供自己的数据文件，也可以使用随 PyBullet
发布的 `pybullet_data`。官方资产目录位于：

```text
examples/pybullet/gym/pybullet_data/
```

届时执行的流程是：

1. 用个人 GitHub 账号 fork `bulletphysics/bullet3`；
2. 新建贡献分支；
3. 将 `assets/` 下三个完整模型目录复制到上述 `pybullet_data/`；
4. 保留每个目录里的 `README.md`、`LICENSE.txt` 和 `metadata.json`；
5. 增加一个最小加载示例并在 PyBullet DIRECT/GUI 中复验；
6. 推送个人 fork，向官方仓库发 Pull Request。

官方仓库目前没有单独的模型上传表单，也没有找到针对 `pybullet_data` 新模型的
专门贡献说明。因此不要自行宣称“已被官方收录”；在提交 PR 前把个人仓库网址和
本页发给 mentor，确认是否确实要走官方 PR。

## 给 mentor 的简短汇报

> 已完成 OneRobotics A1 右臂、左臂和双臂的 PyBullet 适配与本地验收，三个模型均可加载和运动，代码、资产及来源/许可证记录已整理到：<https://github.com/uniquemelody/onerobot_h1_pybullet>。请确认下一步是否向 `bulletphysics/bullet3` 的 `pybullet_data` 提交 PR。

## 上传行为记录模板

| 项目 | 记录 |
|---|---|
| 源仓库 | `katazen/onerobot_h1` |
| 源 commit | `ecf530911284ba0e559f7a24dc222fd8e60d31ed` |
| 适配平台 | PyBullet 3.2.7 |
| 模型 | right / left / bimanual |
| 本地测试 | `bash scripts/validate_all.sh` |
| 个人仓库 | `uniquemelody/onerobot_h1_pybullet` |
| 官方目标（待确认） | `bulletphysics/bullet3/examples/pybullet/gym/pybullet_data` |
| 许可证 | 资产 CC BY 4.0；新增代码 BSD-3-Clause |
