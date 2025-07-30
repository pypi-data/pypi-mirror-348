# =============================================================================
#  Project       : GenomeNinja
#  File          : src/genome_ninja/core/interactive.py
#
#  Author        : Qinzhong Tian <tianqinzhong@qq.com>
#  Created       : 2025-04-30 17:59
#  Last Updated  : 2025-05-10 16:55
#
#  Description   : Interactive command line interface tools for GenomeNinja.
#                  Contains decorators and helper functions for creating interactive CLI prompts
#                  and handling user input. Supports advanced features like required/optional parameters,
#                  auto-completion, parameter validation, and multi-selection.
#
#  Python        : Python 3.13.3
#  Version       : 0.1.12
#
#  Usage         : from genome_ninja.core.interactive import interactive_cmd, ps
#                  @interactive_cmd(
#                      ps("name", "Enter name", rule="2-10 characters"),
#                      ps("age", "Select age", choices=["18-25", "26-35", "36+"]),
#                      ps("files", "Select files", input_type="multiselect")
#                  )
#                  def register(name: str, age: str, files: list[str]):
#                      print(f"Registration successful: {name}, {age}, selected {len(files)} files")
#
#  Copyright © 2025 Qinzhong Tian. All rights reserved.
#  License       : MIT – see LICENSE in project root for full text.
# =============================================================================
from __future__ import annotations

import functools
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Literal

import questionary as qs
import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, FuzzyCompleter, PathCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.validation import ValidationError, Validator
from questionary import Style as QStyle
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from questionary import Choice

console = Console()

# ---------------------------------------------------------------------------
# Questionary colour theme
# ---------------------------------------------------------------------------
QUESTIONARY_STYLE = QStyle(
    [
        ("qmark", "fg:#7aa5ff bold"),  # ❯
        ("question", ""),
        ("answer", "fg:#98e024 bold"),
        ("pointer", "fg:#7aa5ff bold"),
        ("highlighted", "fg:#ffd700 bold"),
        ("selected", "fg:#c18aff bold"),
        ("separator", "fg:#6c6c6c"),
        ("instruction", "fg:#888888 italic"),
    ]
)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
ValidationReturn = bool | str


@dataclass(slots=True)
class PromptSpec:
    """Declarative description of a single interactive parameter."""

    name: str
    question: str
    validate: Callable[[str | list[str]], ValidationReturn] = lambda _: True
    rule: str = ""
    required: bool | Callable[[dict], bool] = True  # 可以是布尔值或接受上下文字典的函数
    choices: list[str] | None = None
    input_type: Literal["text", "confirm", "select", "multiselect"] = "text"
    completer: Completer | None = None
    condition: Callable[[dict], bool] | None = None  # 新增：条件函数，决定是否显示此问题

    def __post_init__(self):
        if self.completer is None and self.name.lower().endswith(
            ("path", "file", "dir", "directory", "paths", "files")
        ):
            self.completer = FuzzyCompleter(PathCompleter())


ps = PromptSpec

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _should_interactive(kwargs: dict[str, Any]) -> bool:
    if kwargs.pop("interactive", False):
        return True
    ctx: typer.Context | None = kwargs.get("ctx")  # type: ignore
    return bool(ctx and getattr(ctx, "obj", None) and ctx.obj.get("interactive", False))


def _format_prompt(spec: PromptSpec, ctx: dict = None) -> Text:
    # 处理动态required属性（lambda函数形式）
    is_required = spec.required
    if callable(spec.required) and ctx is not None:
        is_required = spec.required(ctx)
        
    mark = "[red]*[/]" if is_required else "[dim](optional)[/]"
    body = f"❯ {spec.question} {mark}"
    if spec.rule:
        body += f"\n[dim cyan]({spec.rule})[/]"
    return Text.from_markup(body)


def _wrap_validator(spec: PromptSpec, ctx: dict = None) -> Callable[[Any], ValidationReturn]:
    original = spec.validate
    
    # 处理动态required属性（lambda函数形式）
    is_required = spec.required
    if callable(spec.required) and ctx is not None:
        is_required = spec.required(ctx)

    def _v(val: Any) -> ValidationReturn:
        if is_required and \
           (val is None or \
            (isinstance(val, str) and not val.strip()) or \
            (isinstance(val, list) and not val)):
            return "Input cannot be empty, please try again"
        try:
            res = original(val)
            if isinstance(res, str):
                return res
            return bool(res)
        except Exception as e:
            return f"Input validation failed: {e}"

    return _v


def _error(msg: str) -> None:
    console.print(Panel(msg, border_style="red", title="[bold red]✗ Input Error[/]"))


def _ask_question(spec: PromptSpec, ctx: dict = None, default_value: Any = None) -> Any:
    # 检查条件是否满足
    if spec.condition is not None and ctx is not None:
        if not spec.condition(ctx):
            # 条件不满足，跳过此问题
            return None
    
    # 处理动态required属性（lambda函数形式）
    is_required = spec.required
    if callable(spec.required) and ctx is not None:
        is_required = spec.required(ctx)
        
    prompt = str(_format_prompt(spec, ctx))
    validator = _wrap_validator(spec, ctx)
    
    # 准备基本提示
    base_prompt = prompt
    
    # 如果有默认值，添加历史记录信息（作为单独一行，更美观）
    if default_value is not None:
        if isinstance(default_value, list):
            default_str = ", ".join(default_value) if default_value else "None"
        else:
            default_str = str(default_value) if default_value is not None else "None"
        
        # 创建历史记录提示（作为单独的样式行）- 使用更明亮的颜色以便在暗色界面更容易看见
        history_line = Text.from_markup(f"[bold cyan]上次使用的值: {default_str}[/]")
        
        # 不直接修改原始提示文本，而是在显示时处理

    # SELECT / MULTISELECT
    if spec.choices is not None:
        choices = list(spec.choices)
        if spec.input_type == "select" and not is_required:  # 使用计算后的is_required
            choices.append("<skip>")
        if spec.input_type == "multiselect":
            # Prepare default values from history, ensuring they are strings
            default_values_from_history_as_strings = []
            if default_value is not None: # default_value is from history, e.g., ['accurate', 'auto'] or "accurate,auto"
                if isinstance(default_value, list):
                    default_values_from_history_as_strings = [str(v).strip() for v in default_value if str(v).strip()]
                elif isinstance(default_value, str):
                    default_values_from_history_as_strings = [s.strip() for s in default_value.split(',') if s.strip()]
            
            # 'choices' is the list of available string options, e.g., ['quick', 'accurate', 'auto']
            # Filter the historical defaults to include only those that are valid current choices
            valid_defaults_for_parameter = [
                val for val in default_values_from_history_as_strings if val in choices # 'choices' here is the list of string options
            ]
            # Ensure uniqueness if there were duplicates in history that are valid
            if valid_defaults_for_parameter:
                 valid_defaults_for_parameter = list(dict.fromkeys(valid_defaults_for_parameter))

            # Create questionary.Choice objects.
            # The 'checked' attribute is set based on these valid historical defaults.
            configured_questionary_choices = []
            for choice_item_str in choices: # Iterate over the original string choices
                is_checked = choice_item_str in valid_defaults_for_parameter # Check against the filtered, valid defaults
                configured_questionary_choices.append(
                    Choice(title=str(choice_item_str), value=choice_item_str, checked=is_checked)
                )
            
            # The 'default' parameter for qs.checkbox should be a list of *values* (strings in this case)
            # or None if no valid defaults.
            default_param_for_qs = valid_defaults_for_parameter if valid_defaults_for_parameter else None

            while True:
                if default_value is not None: # Show history line if there was any default_value initially
                    console.print(history_line)
                
                ans = qs.checkbox(
                    base_prompt,
                    choices=configured_questionary_choices,  # Pass List[questionary.Choice]
                    style=QUESTIONARY_STYLE,
                    default=None  # Explicitly set default to None as per the strategy
                ).ask()
                
                res = validator(ans)
                if res is True:
                    return ans
                _error(res if isinstance(res, str) else "Validation failed")
        else:
            # 设置默认选中项
            default_index = None
            if default_value is not None and default_value in choices:
                default_index = choices.index(default_value)
            
            while True:
                # 如果有历史记录，先显示历史记录行
                if default_value is not None:
                    console.print(history_line)
                
                ans = qs.select(
                    base_prompt, 
                    choices=choices, 
                    style=QUESTIONARY_STYLE,
                    default=choices[default_index] if default_index is not None else None
                ).ask()
                if ans == "<skip>":
                    ans = None
                res = validator(ans)
                if res is True:
                    return ans
                _error(res if isinstance(res, str) else "Validation failed")

    # CONFIRM
    if spec.input_type == "confirm":
        # 如果有历史记录，先显示历史记录行
        if default_value is not None:
            console.print(history_line)
        
        # 使用历史记录中的值作为默认值
        default = bool(default_value) if default_value is not None else False
        return qs.confirm(base_prompt, style=QUESTIONARY_STYLE, default=default).ask()

    # TEXT with completer
    if spec.completer is not None:
        session = PromptSession()

        class V(Validator):
            def validate(self, document):  # type: ignore[override]
                res = validator(document.text)
                if res is True:
                    return
                raise ValidationError(
                    message=res if isinstance(res, str) else "Validation failed"
                )

        # 如果有历史记录，先显示历史记录行
        if default_value is not None:
            console.print(history_line)

        while True:
            ans = session.prompt(
                FormattedText([("class:question", f"{base_prompt}: ")]),
                completer=spec.completer,
                validator=V(),
                validate_while_typing=False,
                default=str(default_value) if default_value is not None else ""
            )
            return ans

    # FALLBACK TEXT
    # 如果有历史记录，先显示历史记录行
    if default_value is not None:
        console.print(history_line)
        
    while True:
        ans = qs.text(
            base_prompt, 
            style=QUESTIONARY_STYLE,
            default=str(default_value) if default_value is not None else ""
        ).ask()
        res = validator(ans)
        if res is True:
            return ans
        _error(res if isinstance(res, str) else "Validation failed")


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------


def interactive_cmd(*specs: PromptSpec):
    """Decorate functions for smart interactive prompting:
    - Implicit interactive on missing required params
    - Explicit interactive via '-i/--interactive'
    - Required params always prompted if missing
    - Optional prompted only if explicit
    - Conditional prompting based on previous answers
    - Branching flows supported through condition functions
    - Automatically remembers previous inputs for each command"""

    def dec(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrap(*args: Any, **kwargs: Any) -> Any:
            explicit = _should_interactive(kwargs)
            
            # 获取命令名称，用于加载历史记录
            command_name = fn.__name__
            
            # 加载历史记录
            history = history_manager.load_history(command_name)
            
            # 创建上下文字典，用于条件性参数和分支逻辑
            ctx_dict = {}
            for sp in specs:
                # 首先检查kwargs中是否有值
                if kwargs.get(sp.name) is not None:
                    ctx_dict[sp.name] = kwargs.get(sp.name)
                # 如果没有，尝试从历史记录中获取
                elif sp.name in history:
                    # 不自动填充到kwargs，只添加到上下文字典中
                    ctx_dict[sp.name] = history[sp.name]
            
            # 检查是否有必填参数缺失（考虑条件函数）
            required_missing = False
            for sp in specs:
                # 处理动态required属性
                is_required = sp.required
                if callable(sp.required):
                    is_required = sp.required(ctx_dict)
                
                # 检查条件是否满足
                condition_met = True
                if sp.condition is not None:
                    condition_met = sp.condition(ctx_dict)
                
                # 只有当条件满足且参数必填且缺失时，才标记为缺失
                if condition_met and is_required and kwargs.get(sp.name) is None:
                    required_missing = True
                    break
            
            interactive = explicit or required_missing

            # —— Enter interactive mode, print introduction and current parameter panel ——
            if interactive:
                # 1) Introduction
                doc = fn.__doc__ or ""
                console.print(
                    Panel(
                        Text(doc.strip(), style="cyan"),
                        title="[green]Tool Introduction[/]",
                        border_style="green",
                        expand=False,
                    )
                )
                # 2) Echo current parameter values and history
                lines: list[str] = []
                for sp in specs:
                    # 检查条件是否满足
                    condition_met = True
                    if sp.condition is not None:
                        condition_met = sp.condition(ctx_dict)
                    
                    if not condition_met:
                        continue  # 跳过不满足条件的参数
                    
                    # 首先检查kwargs中是否有值
                    val = kwargs.get(sp.name)
                    # 如果没有，尝试从历史记录中获取
                    if val is None and sp.name in history:
                        val = history[sp.name]
                        # 显示这是历史记录值
                        has_history = True
                    else:
                        has_history = False
                    
                    # 格式化显示值
                    if isinstance(val, list):
                        val_str = ", ".join(val) if val else "None"
                    else:
                        val_str = str(val) if val is not None else "None"
                    
                    # 处理动态required属性
                    is_required = sp.required
                    if callable(sp.required):
                        is_required = sp.required(ctx_dict)
                    
                    mark = "*" if is_required else "(optional)"
                    history_mark = " [bold cyan]（上次使用的值）[/]" if has_history else ""
                    lines.append(f"{sp.question} {mark} = [cyan]{val_str}[/]{history_mark}")
                
                console.print(
                    Panel(
                        "\n".join(lines),
                        title="[blue]Current Parameters[/]",
                        border_style="blue",
                        expand=False,
                    )
                )

            # Propagate flag for tool-level intros
            ctx = kwargs.get("ctx")  # type: ignore
            if interactive and ctx is not None:
                if getattr(ctx, "obj", None) is None:
                    ctx.obj = {}
                ctx.obj["interactive"] = True
            
            # 用于收集新的历史记录
            new_history = {}
            
            # Prompt required missing always, optional only if explicit
            for sp in specs:
                # 处理动态required属性
                is_required = sp.required
                if callable(sp.required):
                    is_required = sp.required(ctx_dict)
                
                # 检查条件是否满足
                condition_met = True
                if sp.condition is not None:
                    condition_met = sp.condition(ctx_dict)
                
                # 只有当条件满足时才考虑提示
                if condition_met:
                    need_req = is_required and kwargs.get(sp.name) is None
                    need_opt = explicit and not is_required
                    if need_req or need_opt:
                        # 获取历史记录中的默认值
                        default_value = history.get(sp.name)
                        
                        # 调用_ask_question时传入默认值
                        kwargs[sp.name] = _ask_question(sp, ctx_dict, default_value)
                        
                        # 更新上下文字典，以便后续参数可以依赖此参数
                        if kwargs.get(sp.name) is not None:
                            ctx_dict[sp.name] = kwargs.get(sp.name)
                    
                    # 如果参数有值，添加到新的历史记录中
                    if kwargs.get(sp.name) is not None:
                        new_history[sp.name] = kwargs.get(sp.name)
            
            # 保存新的历史记录
            if new_history:
                history_manager.save_history(command_name, new_history)

            return fn(*args, **kwargs)

        return wrap

    return dec


# ---------------------------------------------------------------------------
# 历史记录管理
# ---------------------------------------------------------------------------

class HistoryManager:
    """管理交互式命令的输入历史记录
    
    负责保存和加载用户在不同子命令中的输入历史，以便在下次运行时提供默认值。
    """
    
    def __init__(self):
        """初始化历史记录管理器"""
        # 确定历史记录文件的存储位置
        self.history_dir = self._get_history_dir()
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.history_cache: Dict[str, Dict[str, Any]] = {}
    
    def _get_history_dir(self) -> Path:
        """获取历史记录文件的存储目录
        
        返回:
            历史记录文件的存储目录路径
        """
        # 优先使用XDG_CONFIG_HOME环境变量
        if os.environ.get("XDG_CONFIG_HOME"):
            base_dir = Path(os.environ["XDG_CONFIG_HOME"])
        # 否则使用平台特定的用户配置目录
        elif os.name == "nt":  # Windows
            base_dir = Path(os.environ["APPDATA"])
        else:  # Linux/Mac
            base_dir = Path.home() / ".config"
        
        return base_dir / "genome-ninja" / "history"
    
    def _get_history_file(self, command_name: str) -> Path:
        """获取特定命令的历史记录文件路径
        
        参数:
            command_name: 命令名称
            
        返回:
            历史记录文件路径
        """
        return self.history_dir / f"{command_name}.json"
    
    def load_history(self, command_name: str) -> Dict[str, Any]:
        """加载命令的历史记录
        
        参数:
            command_name: 命令名称
            
        返回:
            历史记录字典，如果不存在则返回空字典
        """
        # 检查缓存
        if command_name in self.history_cache:
            return self.history_cache[command_name]
        
        history_file = self._get_history_file(command_name)
        if not history_file.exists():
            return {}
        
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                self.history_cache[command_name] = history
                return history
        except (json.JSONDecodeError, IOError):
            # 如果文件损坏或无法读取，返回空字典
            return {}
    
    def save_history(self, command_name: str, history: Dict[str, Any]) -> None:
        """保存命令的历史记录
        
        参数:
            command_name: 命令名称
            history: 历史记录字典
        """
        # 更新缓存
        self.history_cache[command_name] = history
        
        # 保存到文件
        history_file = self._get_history_file(command_name)
        try:
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            console.print(f"[yellow]警告: 无法保存历史记录: {e}[/]")  

# 创建全局历史记录管理器实例
history_manager = HistoryManager()

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
__all__ = ["PromptSpec", "ps", "interactive_cmd", "history_manager"]
