# GooglSearch-Tool 打包项目

这是 [googlesearch](https://github.com/huazz233/googlesearch) 项目的打包仓库，用于管理和发布 PyPI 包。

## 项目结构

```
packaging_googlesearch/
├── build_tools/          # 构建工具
│   ├── version.py        # 版本管理
│   └── utils.py          # 工具函数
├── config/               # 配置文件
│   ├── pyproject.toml    # 项目配置
│   ├── setup.cfg        # 额外配置
│   └── MANIFEST.in      # 文件包含配置
├── scripts/              # 脚本
│   ├── build.py         # 构建脚本
│   └── publish.py       # 发布脚本
├── googlesearch/        # 子模块
└── README.md            # 说明文档
```

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/your-username/packaging_googlesearch.git
cd packaging_googlesearch
```

2. 初始化子模块：
```bash
git submodule add https://github.com/huazz233/googlesearch googlesearch
```

3. 安装依赖：
```bash
pip install build twine
```

4. 构建和发布：
```bash
# 仅构建
python scripts/build.py

# 构建并发布
python scripts/publish.py
```

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE.txt) 文件。
