import yaml
from pathlib import Path

class YamlConfigLoader:
    def __init__(self, file_path='application.yml', profile=None):
        self.file_path = Path(file_path)
        self.profile = profile
        self._data = self._load()

    def _load(self):
        with self.file_path.open() as f:
            base_data = yaml.safe_load(f)

        if self.profile and 'profiles' in base_data:
            profile_data = base_data['profiles'].get(self.profile, {})
            base_data.update(profile_data)

        return base_data

    def get(self, key_path, default=None):
        keys = key_path.split('.')
        data = self._data
        for key in keys:
            data = data.get(key)
            if data is None:
                return default
        return data
