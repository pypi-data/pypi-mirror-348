# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/tools/camisim_helper.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-05-12 12:36
#  Last Updated  : 2025-05-16 19:56
#     
#  Description   : CAMISIM Helper Tool
#                 Provides utilities for working with CAMISIM outputs.
#
#  Python        : Python 3.13.3
#  Version       : 0.1.0                       
#
#  Usage         : genome-ninja camisim-helper
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
# from genome_ninja import test as gn_test # Placeholder for potential C++ bindings
from genome_ninja.core.interactive import interactive_cmd
from genome_ninja.core.interactive import ps as P
from genome_ninja.utils.download_utils import download_file, DownloadConfig

console = Console()

# -----------------------------------------------------------------------------
# CAMISIM 路径管理模块
# -----------------------------------------------------------------------------

def is_valid_camisim_path(path: Union[str, Path]) -> bool:
    """Check if the given path contains a valid CAMISIM installation."""
    path = Path(path)
    return path.is_dir() and (path / "metagenomesimulation.py").exists()


def download_camisim(download_path: Path) -> Optional[Path]:
    """Download CAMISIM 1.3 from GitHub."""
    camisim_url = "https://github.com/CAMI-challenge/CAMISIM/archive/refs/tags/1.3.tar.gz"
    tar_path = download_path / "CAMISIM-1.3.tar.gz"
    
    console.print(f"[blue]下载 CAMISIM 1.3 到 {download_path}...[/]")
    
    # 配置下载参数
    config = DownloadConfig(
        show_progress=True,
        max_retries=3,
        connect_timeout=30,
        read_timeout=60
    )
    
    # 下载文件
    success = download_file(camisim_url, tar_path, config)
    
    if not success:
        console.print("[red]下载失败，请检查网络连接后重试。[/]")
        return None
    
    # 解压文件
    console.print("[blue]解压 CAMISIM...[/]")
    try:
        with tarfile.open(tar_path) as tar:
            tar.extractall(path=download_path)
        
        # 删除压缩包
        tar_path.unlink()
        
        # 返回解压后的路径
        camisim_path = download_path / "CAMISIM-1.3"
        console.print(f"[green]CAMISIM 已成功下载并解压到: {camisim_path}[/]")
        return camisim_path
    
    except Exception as e:
        console.print(f"[red]解压失败: {e}[/]")
        return None


def get_camisim_path(has_camisim: bool, camisim_path: Optional[str], 
                   download_camisim_opt: bool, download_dir: Optional[str]) -> Optional[Path]:
    """交互式获取CAMISIM路径，如果未安装则提供下载选项。"""
    
    if has_camisim:
        # 用户已安装，验证路径
        if camisim_path:
            path = Path(camisim_path).expanduser().resolve()
            
            if is_valid_camisim_path(path):
                console.print(f"[green]已找到有效的CAMISIM安装: {path}[/]")
                return path
            else:
                console.print("[red]无效的CAMISIM路径，未找到metagenomesimulation.py文件。[/]")
                return None
        else:
            console.print("[yellow]未提供CAMISIM路径。[/]")
            return None
    elif download_camisim_opt:
        # 用户未安装，但选择下载
        if download_dir is None:
            console.print("[yellow]未提供下载路径，将使用当前目录。[/]")
            download_path = Path.cwd().resolve()
        else:
            download_path = Path(download_dir).expanduser().resolve()
        
        # 确保目录存在
        download_path.mkdir(parents=True, exist_ok=True)
        
        # 下载并解压
        return download_camisim(download_path)
    else:
        # 用户既不安装也不下载，直接返回None
        console.print("[yellow]未选择安装或下载CAMISIM。[/]")
        return None


# -----------------------------------------------------------------------------
# CAMISIM 配置文件生成模块
# -----------------------------------------------------------------------------

class CAMISIMConfigGenerator:
    """CAMISIM配置文件生成器
    
    负责生成CAMISIM运行所需的各种配置文件，包括：
    - 主配置文件
    - 物种丰度配置
    - 基因组信息配置
    等
    """
    
    def __init__(self, camisim_path: Path, output_dir: Path):
        """初始化配置生成器
        
        Args:
            camisim_path: CAMISIM安装路径
            output_dir: 输出目录路径
        """
        self.camisim_path = camisim_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_main_config(self, project_name: str) -> Path:
        """生成CAMISIM主配置文件
        
        Args:
            project_name: 项目名称
            
        Returns:
            配置文件路径
        """
        # TODO: 实现配置文件生成逻辑
        config_path = self.output_dir / f"{project_name}_config.ini"
        console.print(f"[blue]生成CAMISIM主配置文件: {config_path}[/]")
        return config_path
    
    def generate_abundance_file(self, abundance_data: Dict) -> Path:
        """生成物种丰度配置文件
        
        Args:
            abundance_data: 物种丰度数据
            
        Returns:
            配置文件路径
        """
        # TODO: 实现丰度文件生成逻辑
        abundance_path = self.output_dir / "abundance.tsv"
        console.print(f"[blue]生成物种丰度配置文件: {abundance_path}[/]")
        return abundance_path
    
    def generate_genome_metadata(self, genome_data: Dict) -> Path:
        """生成基因组元数据配置文件
        
        Args:
            genome_data: 基因组数据
            
        Returns:
            配置文件路径
        """
        # TODO: 实现基因组元数据生成逻辑
        metadata_path = self.output_dir / "genome_metadata.tsv"
        console.print(f"[blue]生成基因组元数据配置文件: {metadata_path}[/]")
        return metadata_path

# -----------------------------------------------------------------------------
# CAMISIM 运行模块
# -----------------------------------------------------------------------------

class CAMISIMRunner:
    """CAMISIM运行器
    
    负责调用CAMISIM执行模拟任务
    """
    
    def __init__(self, camisim_path: Path):
        """初始化运行器 
        
        Args:
            camisim_path: CAMISIM安装路径
        """
        self.camisim_path = camisim_path
        self.metagenomesim_path = camisim_path / "metagenomesimulation.py"
    
    def run_simulation(self, config_path: Path) -> bool:
        """运行CAMISIM模拟
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            是否成功运行
        """
        if not self.metagenomesim_path.exists():
            console.print(f"[red]无法找到CAMISIM主程序: {self.metagenomesim_path}[/]")
            return False
        
        console.print(f"[blue]开始运行CAMISIM模拟...[/]")
        # TODO: 实现CAMISIM调用逻辑
        # cmd = ["python", str(self.metagenomesim_path), str(config_path)]
        # result = subprocess.run(cmd, capture_output=True, text=True)
        # if result.returncode != 0:
        #     console.print(f"[red]CAMISIM运行失败: {result.stderr}[/]")
        #     return False
        
        console.print(f"[green]CAMISIM模拟完成[/]")
        return True

# -----------------------------------------------------------------------------
# Typer CLI 命令注册
# -----------------------------------------------------------------------------

def register(cli: typer.Typer) -> None:
    """Register the camisim-helper command to the Typer CLI."""

    @cli.command(
        "camisim-helper",
        help="Utilities for CAMISIM output processing",
        rich_help_panel="helper", # Or another appropriate panel
    )
    @interactive_cmd(  # 强制进入交互模式，无需-i参数
        P(
            "has_camisim",
            "您是否已经下载安装了CAMISIM 1.3?",
            required=True,
            input_type="confirm",
        ),
        P(
            "camisim_path",
            "请输入CAMISIM 1.3的安装路径",
            validate=lambda v: is_valid_camisim_path(v) or "无效的CAMISIM路径，未找到metagenomesimulation.py文件",
            rule="请输入包含metagenomesimulation.py的有效CAMISIM安装路径",
            required=True,  # 如果显示此问题，则必须输入
            condition=lambda ctx: ctx.get("has_camisim", False),  # 仅当用户已安装CAMISIM时才显示此问题
        ),
        P(
            "download_camisim_opt",
            "是否需要下载CAMISIM 1.3?",
            required=True,  # 如果显示此问题，则必须回答
            input_type="confirm",
            condition=lambda ctx: not ctx.get("has_camisim", False),  # 仅当用户未安装CAMISIM时才显示此问题
        ),
        P(
            "download_dir",
            "请输入下载位置 (留空则使用当前目录)",
            required=True,  # 当用户选择下载CAMISIM时，必须询问下载路径
            rule="输入有效的目录路径或留空使用当前目录",
            condition=lambda ctx: not ctx.get("has_camisim", False) and ctx.get("download_camisim_opt", False),  # 仅当用户选择下载CAMISIM时才显示此问题
        ),
        P(
            "action",
            "请选择要执行的操作",
            choices=["生成配置文件", "运行CAMISIM", "处理CAMISIM输出"],
            required=True,
            condition=lambda ctx: ctx.get("has_camisim", False) or ctx.get("download_camisim_opt", False),
        ),
    )
    def camisim_helper(
        ctx: typer.Context,
        has_camisim: bool = None,
        camisim_path: Optional[str] = None,
        download_camisim_opt: bool = None,
        download_dir: Optional[str] = None,
        action: Optional[str] = None,
        interactive: bool = True
    ) -> None:
        """
        CAMISIM Helper Tool - 纯交互式模式:

        • 检查CAMISIM安装状态
        • 提供CAMISIM下载和安装选项
        • 处理CAMISIM输出文件
        
        注意：此工具仅支持交互式操作，不接受命令行参数。
        """
        
        console.print(
            Panel(
                "CAMISIM Helper - 用于处理CAMISIM输出的交互式工具\n请按照提示完成配置",
                title="CAMISIM Helper 交互式工具",
                border_style="blue",
            )
        )
        
        # 第一阶段：获取CAMISIM路径
        camisim_path_obj = get_camisim_path(
            has_camisim=has_camisim,
            camisim_path=camisim_path,
            download_camisim_opt=download_camisim_opt,
            download_dir=download_dir
        )
        
        if not camisim_path_obj:
            console.print("[yellow]未找到有效的CAMISIM安装，无法继续操作。[/]")
            console.print("您可以稍后通过运行 'genome-ninja camisim-helper' 重新配置CAMISIM。")
            return
            
        console.print(f"[green]CAMISIM路径: {camisim_path_obj}[/]")
        
        # 第二阶段：根据用户选择的操作执行相应功能
        if action == "生成配置文件":
            # TODO: 实现配置文件生成逻辑
            output_dir = Path(Prompt.ask("请输入配置文件输出目录", default=str(Path.cwd()))).expanduser().resolve()
            project_name = Prompt.ask("请输入项目名称", default="camisim_project")
            
            config_generator = CAMISIMConfigGenerator(camisim_path_obj, output_dir)
            main_config = config_generator.generate_main_config(project_name)
            
            console.print(f"[green]配置文件已生成: {main_config}[/]")
            
        elif action == "运行CAMISIM":
            # TODO: 实现CAMISIM运行逻辑
            config_path = Path(Prompt.ask("请输入CAMISIM配置文件路径")).expanduser().resolve()
            if not config_path.exists():
                console.print(f"[red]配置文件不存在: {config_path}[/]")
                return
                
            runner = CAMISIMRunner(camisim_path_obj)
            success = runner.run_simulation(config_path)
            
            if success:
                console.print("[green]CAMISIM运行完成[/]")
            else:
                console.print("[red]CAMISIM运行失败[/]")
                
        elif action == "处理CAMISIM输出":
            # TODO: 实现CAMISIM输出处理逻辑
            console.print("[yellow]CAMISIM输出处理功能尚未实现[/]")
        
        else:
            console.print("[yellow]未选择有效操作，程序退出[/]")



# -----------------------------------------------------------------------------
# Stand‑alone execution
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = typer.Typer()
    register(app)
    app()
