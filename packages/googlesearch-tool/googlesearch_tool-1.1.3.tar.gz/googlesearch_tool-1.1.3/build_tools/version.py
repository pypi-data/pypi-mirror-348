import re
from pathlib import Path

class VersionManager:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        # 尝试多个可能的位置
        possible_paths = [
            self.project_root / 'pyproject.toml',
            self.project_root / 'config' / 'pyproject.toml',
        ]
        
        for path in possible_paths:
            if path.exists():
                self.pyproject_path = path
                break
        else:
            raise FileNotFoundError(f"Could not find pyproject.toml in any of these locations: {possible_paths}")
    
    def get_current_version(self):
        """获取当前版本号"""
        content = self.pyproject_path.read_text(encoding='utf-8')
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        return match.group(1) if match else None
    
    def bump_version(self, bump_type='patch'):
        """
        更新版本号
        :param bump_type: major, minor 或 patch
        """
        current = self.get_current_version()
        if not current:
            return None
            
        major, minor, patch = map(int, current.split('.'))
        
        if bump_type == 'major':
            major += 1
            minor = patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
            
        new_version = f"{major}.{minor}.{patch}"
        self._update_version_in_file(new_version)
        return new_version
    
    def _update_version_in_file(self, new_version):
        """更新配置文件中的版本号"""
        content = self.pyproject_path.read_text(encoding='utf-8')
        updated = re.sub(
            r'(version\s*=\s*)"[^"]+"',
            f'\\1"{new_version}"',
            content
        )
        self.pyproject_path.write_text(updated, encoding='utf-8')
