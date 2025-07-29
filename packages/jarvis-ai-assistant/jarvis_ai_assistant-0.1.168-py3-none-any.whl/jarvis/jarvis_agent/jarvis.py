# -*- coding: utf-8 -*-
import argparse
import os
import sys

from typing import Dict  # 仅保留实际使用的类型导入

from jarvis.jarvis_utils.config import get_data_dir
from prompt_toolkit import prompt
import yaml
from yaspin import yaspin
from jarvis.jarvis_agent import (
     PrettyOutput, OutputType,
     get_multiline_input,
     user_confirm,
     Agent,
     origin_agent_system_prompt
)
from jarvis.jarvis_tools.registry import ToolRegistry
from jarvis.jarvis_utils.utils import init_env
from jarvis.jarvis_agent.file_input_handler import file_input_handler
from jarvis.jarvis_agent.shell_input_handler import shell_input_handler
from jarvis.jarvis_agent.builtin_input_handler import builtin_input_handler


def _load_tasks() -> Dict[str, str]:
    """Load tasks from .jarvis files in user home and current directory."""
    tasks: Dict[str, str] = {}

    # Check pre-command in data directory
    data_dir = get_data_dir()
    pre_command_path = os.path.join(data_dir, "pre-command")
    if os.path.exists(pre_command_path):
        spinner_text = f"从{pre_command_path}加载预定义任务..."
        with yaspin(text=spinner_text, color="cyan") as spinner:
            try:
                with open(pre_command_path, "r", encoding="utf-8", errors="ignore") as f:
                    user_tasks = yaml.safe_load(f)
                if isinstance(user_tasks, dict):
                    for name, desc in user_tasks.items():
                        if desc:
                            tasks[str(name)] = str(desc)
                spinner.text = "预定义任务加载完成"
                spinner.ok("✅")
            except (yaml.YAMLError, OSError):
                spinner.text = "预定义任务加载失败"
                spinner.fail("❌")

    # Check .jarvis/pre-command in current directory
    pre_command_path = ".jarvis/pre-command"
    if os.path.exists(pre_command_path):
        abs_path = os.path.abspath(pre_command_path)
        spinner_text = f"从{abs_path}加载预定义任务..."
        with yaspin(text=spinner_text, color="cyan") as spinner:
            try:
                with open(pre_command_path, "r", encoding="utf-8", errors="ignore") as f:
                    local_tasks = yaml.safe_load(f)
                if isinstance(local_tasks, dict):
                    for name, desc in local_tasks.items():
                        if desc:
                            tasks[str(name)] = str(desc)
                spinner.text = "预定义任务加载完成"
                spinner.ok("✅")
            except (yaml.YAMLError, OSError):
                spinner.text = "预定义任务加载失败"
                spinner.fail("❌")

    return tasks

def _select_task(tasks: Dict[str, str]) -> str:
    """Let user select a task from the list or skip. Returns task description if selected."""
    if not tasks:
        return ""
    
    task_names = list(tasks.keys())
    task_list = ["可用任务:"]
    for i, name in enumerate(task_names, 1):
        task_list.append(f"[{i}] {name}")
    task_list.append("[0] 跳过预定义任务")
    PrettyOutput.print("\n".join(task_list), OutputType.INFO)


    while True:
        try:
            choice_str = prompt("\n请选择一个任务编号（0 跳过预定义任务）：").strip()
            if not choice_str:
                return ""

            choice = int(choice_str)
            if choice == 0:
                return ""
            if 1 <= choice <= len(task_names):
                selected_task = tasks[task_names[choice - 1]]
                # 询问是否需要补充信息
                need_additional = user_confirm("需要为此任务添加补充信息吗？", default=False)
                if need_additional:
                    additional_input = get_multiline_input("请输入补充信息：")
                    if additional_input:
                        selected_task = f"{selected_task}\n\n补充信息:\n{additional_input}"
                return selected_task
            PrettyOutput.print("无效的选择。请选择列表中的一个号码。", OutputType.WARNING)

        except (KeyboardInterrupt, EOFError):
            return ""
        except ValueError as val_err:
            PrettyOutput.print(f"选择任务失败: {str(val_err)}", OutputType.ERROR)




def main() -> None:
    """Jarvis main entry point"""
    init_env()
    parser = argparse.ArgumentParser(description='Jarvis AI assistant')
    parser.add_argument('-p', '--platform', type=str, help='Platform to use')
    parser.add_argument('-m', '--model', type=str, help='Model to use')
    parser.add_argument('-t', '--task', type=str, help='Directly input task content from command line')
    args = parser.parse_args()

    try:
        agent = Agent(
            system_prompt=origin_agent_system_prompt,
            platform=args.platform,
            model_name=args.model,
            input_handler=[file_input_handler, shell_input_handler, builtin_input_handler],
            output_handler=[ToolRegistry()],
            need_summary=False
        )

        # 优先处理命令行直接传入的任务
        if args.task:
            agent.run(args.task)
            sys.exit(0)

        tasks = _load_tasks()
        if tasks and (selected_task := _select_task(tasks)):
            PrettyOutput.print(f"执行任务: {selected_task}", OutputType.INFO)
            agent.run(selected_task)
            sys.exit(0)

        user_input = get_multiline_input("请输入你的任务（输入空行退出）:")
        if user_input:
            agent.run(user_input)
        sys.exit(0)

    except Exception as err:  # pylint: disable=broad-except
        PrettyOutput.print(f"初始化错误: {str(err)}", OutputType.ERROR)
        sys.exit(1)

if __name__ == "__main__":
    main()
