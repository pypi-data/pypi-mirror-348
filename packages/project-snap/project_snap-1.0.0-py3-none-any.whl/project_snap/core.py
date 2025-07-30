import os
import json
import re
from pathlib import Path
from typing import Dict, Set, Any, List, Optional, Union


# Default configuration
DEFAULT_CONFIG = {
    "folders": {
        "include": [],
        "exclude": ["node_modules", "venv", ".git", "__pycache__", ".idea", ".vscode", "dist", "build", 
                   "target", "bin", "obj", ".next", ".nuxt", ".output", ".cache", ".parcel-cache",
                   ".svelte-kit", ".yarn", "coverage", "artifacts", "out", "tmp", "logs"]
    },
    "files": {
        "include": [],
        "exclude": [".DS_Store", "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.class", "*.exe", "*.bin", 
                   "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.ico", "*.svg", "*.tif", "*.tiff", 
                   "yarn.lock", "package-lock.json", "pnpm-lock.yaml", "*.zip", "*.tar", "*.tar.gz", 
                   "*.rar", "*.7z", "*.pdf", "*.mp3", "*.mp4", "*.avi", "*.mov", "*.wmv", "*.flv"]
    },
    "ext": {
        "include": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss", ".sass", ".less", 
                   ".json", ".yml", ".yaml", ".md", ".txt", ".sql", ".sh", ".bash", ".zsh", ".fish",
                   ".c", ".cpp", ".h", ".hpp", ".java", ".go", ".rs", ".rb", ".php", ".svelte",
                   ".vue", ".dart", ".lua", ".ex", ".exs", ".erl", ".hrl", ".clj", ".cljs",
                   ".cs", ".fs", ".fsx", ".swift", ".kt", ".kts", ".jsx", ".tsx", ".toml", ".ini"],
        "exclude": []
    },
    "target_folder": ".",
    "output_folder": ".",
    "snapshot_name": "project_snapshot.md",
    "max_file_size_kb": 500  # Skip files larger than this size (in KB)
}

# File language mappings for syntax highlighting in markdown
FILE_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".json": "json",
    ".md": "markdown",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".xml": "xml",
    ".sql": "sql",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".fish": "fish",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".svelte": "svelte",
    ".vue": "vue",
    ".dart": "dart",
    ".lua": "lua",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".hrl": "erlang",
    ".clj": "clojure",
    ".cljs": "clojure",
    ".cs": "csharp",
    ".fs": "fsharp",
    ".fsx": "fsharp",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".toml": "toml",
    ".ini": "ini",
    ".txt": "",
    ".": "",
}

class ProjectSnapshotTool:


    def __init__(self, config_path: Optional[str] = None):
        self.config = DEFAULT_CONFIG.copy()        
        if config_path:
            self.load_config(config_path)
            
        self.excluded_dirs = set(self.config["folders"]["exclude"])
        self.included_dirs = set(self.config["folders"]["include"])
        self.excluded_files = set(self.config["files"]["exclude"])
        self.included_files = set(self.config["files"]["include"])
        self.included_exts = set(self.config["ext"]["include"])
        self.excluded_exts = set(self.config["ext"]["exclude"])
        
        self.excluded_file_patterns = self._convert_glob_patterns(self.excluded_files)
        self.included_file_patterns = self._convert_glob_patterns(self.included_files)        
        self.target_folder = Path(self.config["target_folder"]).absolute()
        self.output_folder = Path(self.config["output_folder"]).absolute()
        self.snapshot_path = self.output_folder / self.config["snapshot_name"]
        
        self.max_file_size = self.config["max_file_size_kb"] * 1024
        self.stats = {
            "processed_dirs": 0,
            "processed_files": 0,
            "skipped_files": 0,
            "skipped_dirs": 0,
            "total_size_kb": 0
        }

    def _convert_glob_patterns(self, patterns: Set[str]) -> List[str]:
        result = []
        for pattern in patterns:
            if '*' in pattern:
                regex = pattern.replace('.', '\\.').replace('*', '.*')
                result.append(regex)
            else:
                result.append(pattern)
        return result

    def load_config(self, config_path: str) -> None:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
            self._deep_merge(self.config, user_config)
            print(f"Loaded configuration from {config_path}")
        except FileNotFoundError:
            print(f"Configuration file not found at {config_path}, using defaults")
        except json.JSONDecodeError:
            print(f"Error parsing configuration file {config_path}, using defaults")
            
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def should_include_dir(self, dir_path: str) -> bool:
        dir_name = os.path.basename(dir_path)
        if dir_name in self.excluded_dirs:
            self.stats["skipped_dirs"] += 1
            return False
            
        if self.included_dirs and dir_name not in self.included_dirs:
            self.stats["skipped_dirs"] += 1
            return False
            
        return True

    def should_include_file(self, file_path: str) -> bool:
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        try:
            if os.path.getsize(file_path) > self.max_file_size:
                print(f"Skipping large file: {file_path}")
                self.stats["skipped_files"] += 1
                return False
        except OSError:
            self.stats["skipped_files"] += 1
            return False
        
        if file_ext in self.excluded_exts:
            self.stats["skipped_files"] += 1
            return False
            
        for pattern in self.excluded_file_patterns:
            if re.match(f"^{pattern}$", file_name):
                self.stats["skipped_files"] += 1
                return False
        
        if self.included_exts and file_ext not in self.included_exts:
            self.stats["skipped_files"] += 1
            return False
            
        if self.included_file_patterns:
            included = False
            for pattern in self.included_file_patterns:
                if re.match(f"^{pattern}$", file_name):
                    included = True
                    break
            if not included:
                self.stats["skipped_files"] += 1
                return False
        
        return True

    def get_file_language(self, file_name: str) -> str:
        ext = os.path.splitext(file_name)[1].lower()
        return FILE_LANGUAGE_MAP.get(ext, "")

    def create_snapshot(self) -> None:
        """Create a snapshot of the project structure and save it to a markdown file."""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        with open(self.snapshot_path, 'w', encoding='utf-8') as out:
            out.write(f"# Project Snapshot: {self.target_folder.name}\n\n")
            out.write(f"Generated on: {os.popen('date').read().strip()}\n\n")
            out.write("## Table of Contents\n\n")
            
            dirs_and_files = []
            for dirpath, dirnames, filenames in os.walk(self.target_folder):
                dirnames[:] = [d for d in dirnames if self.should_include_dir(os.path.join(dirpath, d))]
                
                if not self.should_include_dir(dirpath):
                    continue
                    
                rel_dir = os.path.relpath(dirpath, self.target_folder)
                if rel_dir == '.':
                    rel_dir = 'Root'
                
                dir_slug = rel_dir.replace(' ', '-').replace('/', '-').lower()
                if dir_slug != 'root':  # Skip root in TOC
                    out.write(f"- [Directory: {rel_dir}](#directory-{dir_slug})\n")
                
                dir_files = []
                for filename in sorted(filenames):
                    filepath = os.path.join(dirpath, filename)
                    if self.should_include_file(filepath):
                        dir_files.append(filename)
                
                dirs_and_files.append((rel_dir, dir_files, dirpath))
            
            out.write("\n## Files\n\n")
            
            for rel_dir, dir_files, dirpath in dirs_and_files:
                if not dir_files:  # Skip empty directories
                    continue
                    
                self.stats["processed_dirs"] += 1
                
                dir_slug = rel_dir.replace(' ', '-').replace('/', '-').lower()
                out.write(f"\n<a name=\"directory-{dir_slug}\"></a>\n")
                out.write(f"### Directory: `{rel_dir}`\n\n")
                
                for filename in sorted(dir_files):
                    filepath = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(filepath, self.target_folder)
                    
                    self.stats["processed_files"] += 1
                    
                    out.write(f"\n#### File: `{rel_path}`\n\n")
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            file_size_kb = os.path.getsize(filepath) / 1024
                            self.stats["total_size_kb"] += file_size_kb
                            
                            lang = self.get_file_language(filename)
                            out.write(f"```{lang}\n")
                            out.write(content)
                            if not content.endswith('\n'):
                                out.write('\n')
                            out.write("```\n")
                    except Exception as e:
                        out.write(f"```\n[Could not read file: {e}]\n```\n")

    def print_stats(self) -> None:
        """Print statistics about the snapshot process."""
        print(f"\n✅ Project snapshot saved to `{self.snapshot_path}`")
        print(f"📊 Statistics:")
        print(f"  - Processed {self.stats['processed_dirs']} directories")
        print(f"  - Processed {self.stats['processed_files']} files")
        print(f"  - Skipped {self.stats['skipped_dirs']} directories")
        print(f"  - Skipped {self.stats['skipped_files']} files")
        print(f"  - Total size: {self.stats['total_size_kb']:.2f} KB")


def find_config_file() -> Optional[str]:
    config_files = [
        "project-snapshot-config.json",
        ".project-snapshot.json",
        "project_snapshot_config.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            return config_file
    
    return None


def create_sample_config() -> None:
    config_file = "project-snapshot-config.json"
    
    if os.path.exists(config_file):
        print(f"Configuration file {config_file} already exists.")
        return
        
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
        
    print(f"✅ Sample configuration created at `{config_file}`")
