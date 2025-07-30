import os
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from build_tools.version import VersionManager
from build_tools.utils import clean_build_files


def init_submodule():
    """初始化和更新子模块"""
    commands = [
        ['git', 'submodule', 'init'],
        ['git', 'submodule', 'update'],
        ['git', 'submodule', 'update', '--remote']
    ]

    for cmd in commands:
        subprocess.run(cmd, check=True)


def build_package():
    """构建包"""
    subprocess.run([sys.executable, '-m', 'build'], check=True)


def bump_version(project_root, bump_type='patch'):
    """更新版本号"""
    version_manager = VersionManager(project_root)
    new_version = version_manager.bump_version(bump_type)
    print(f"更新版本号至: {new_version}")
    return new_version


def main(do_bump_version=True):
    # 获取脚本所在目录的父目录
    project_root = Path(__file__).parent.parent

    # 切换到项目根目录
    os.chdir(project_root)

    # 初始化子模块
    init_submodule()

    # 清理旧的构建文件
    clean_build_files()

    # 自动更新版本号（可选）
    if do_bump_version:
        bump_version(project_root)

    # 构建包
    build_package()

    print("构建完成！")


if __name__ == '__main__':
    main()
