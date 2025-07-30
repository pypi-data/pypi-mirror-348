import os
import shutil
from pathlib import Path

def clean_build_files(directory='.'):
    """清理构建文件"""
    patterns = ['build', 'dist', '*.egg-info']
    base_path = Path(directory)
    
    for pattern in patterns:
        for path in base_path.glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

def ensure_directory(path):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
