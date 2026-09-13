# 05-Skills · 本地角色技能接入层

本目录不直接存放私有技能正文，避免把个人技能库混进可分发模板。Harness 装机时通过 `--with-local-skills` 从本机技能库复制到目标项目根目录的 `skills/`。

默认技能源：

```text
日常办公/00-Skills汇总
```

装机示例：

```bash
bash 07-Kit/install.sh /path/to/project --with-local-skills
```

指定技能源：

```bash
bash 07-Kit/install.sh /path/to/project --with-local-skills --skills-source /path/to/00-Skills汇总
```

安装规则：

1. 只复制包含 `SKILL.md` 的技能目录。
2. 自动跳过 `.git`、`__pycache__`、`.DS_Store`。
3. 复制到目标项目 `skills/<skill-name>/`。
4. 自动生成 `.ai/SKILLS.md`，作为项目内技能索引。
5. 目标项目已有同名技能时跳过，避免覆盖项目自定义技能。
