# PyPI 发布指南

## 准备工作

1. 安装必要工具：
```bash
pip install build twine
```

2. 确保 git 子模块已正确配置：
```bash
git submodule init
git submodule update
git submodule update --remote
```

## 发布步骤

1. 更新版本号：
   - 修改 `pyproject.toml` 中的 `version` 字段
   - 当前版本号格式为：`x.y.z`（例如：1.1.3）

2. 清理旧的构建文件：
```bash
rm -rf build dist *.egg-info
```

3. 构建包：
```bash
python -m build
```

4. 发布到 PyPI：
```bash
python -m twine upload dist/*
```

## 使用 Makefile（推荐）

如果你的系统支持 make，可以使用以下命令：

1. 清理构建文件：
```bash
make clean
```

2. 构建包：
```bash
make build
```

3. 发布到 PyPI：
```bash
make publish
```

## Makefile 内容

```makefile
.PHONY: clean build publish test

clean:
	rm -rf build dist *.egg-info

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

test:
	python -m pytest tests/
```

## 验证

1. 检查包是否成功上传：
   - 访问 https://pypi.org/project/googlesearch-tool/

2. 测试安装：
```bash
pip install --upgrade googlesearch-tool
# 或安装特定版本
pip install googlesearch-tool==1.1.3
```

## 注意事项

1. 发布前检查清单：
   - [ ] 版本号已更新（pyproject.toml）
   - [ ] 所有测试已通过
   - [ ] README.md 已更新
   - [ ] 子模块已更新到最新版本

2. 常见问题：
   - 版本号冲突：确保发布的版本号未被使用
   - 上传失败：检查网络连接和 PyPI 认证状态
   - 构建失败：检查项目结构和依赖配置

3. 文件位置：
   - `pyproject.toml`：项目根目录
   - `MANIFEST.in`：项目根目录
   - `setup.cfg`：项目根目录
