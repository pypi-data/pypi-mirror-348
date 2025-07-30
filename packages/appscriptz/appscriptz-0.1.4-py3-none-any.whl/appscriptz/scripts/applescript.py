""" 脚本交互 """

import subprocess
from llama_index.core import PromptTemplate
import shlex

def run_applescript(script:str)->str:
    """运行apple script 脚本

    Args:
        script (str): applescript 脚本

    Returns:
        str: 脚本的输出
    """
    result = subprocess.run(['osascript', '-e', script],capture_output=True,check=False)
    return result.stdout.decode().replace('\n','')


class Notes():

    @staticmethod
    def write(content):
        content = content.replace("\n",",").replace('- [ ]','')
        # 构造 AppleScript 脚本  TODO 解决无法换行问题
        script = f'''
        tell application "Notes"
            activate
            -- 获取默认账户
            set defaultAccount to default account
            -- 创建一个新的备忘录
            set newNote to make new note in defaultAccount
            -- 写入文本信息到备忘录
            set body of newNote to "{content}"
            -- 显示新创建的备忘录
            show newNote
        end tell
        '''
        return run_applescript(script)

class Reminder():

    @staticmethod
    def write_reminder(content, 
                        list_name="Reminders",  # 指定列表名称
                        due_date=None,         # 设置到期日
                        priority=None,         # 设置优先级(1-4)
                        notes=""               # 添加备注
                    ):
        # 预处理内容
        processed_content = content.replace('\n', ' ').replace('- [ ]', '').strip()
        processed_content = processed_content.replace('"', '\\"')
        notes = notes.replace('"', '\\"')
        
        # 构建属性字典
        properties = [f'name:"{processed_content}"']
        if due_date:
            properties.append(f'due date:(date "{due_date}")')
        if priority and 1 <= priority <= 4:
            properties.append(f'priority:{priority}')
        if notes:
            properties.append(f'body:"{notes}"')
        
        # 构造AppleScript
        script = f'''
        tell application "Reminders"
            activate
            set targetList to list "{list_name}"
            make new reminder in targetList with properties {{{', '.join(properties)}}}
        end tell
        '''
        script = f'''
        tell application "Reminders"
            activate
            set targetList to default list
            set newReminder to make new reminder in targetList with properties {{{', '.join(properties)}}}
            show newReminder
        end tell
        '''
        return run_applescript(script)

class Calulate():
    @staticmethod
    def update(start_date:str = "2025年4月25日8:00",
                end_date:str = "2025年4月25日9:00",
                event_name:str = "会议"):
        script = PromptTemplate(template='''
        tell application "Calendar"
            activate
            tell calendar "Obsidian" -- 或者 tell first calendar
                -- nih
                -- 假设您已经将开始时间、结束时间和标题存储在变量中
                set theStartDate to date "{start_date}" -- 示例日期时间
                set theEndDate to date "{end_date}" -- 示例日期时间
                set theSummary to "{event_name}" -- 示例标题
                make new event with properties {summary:theSummary, start date:theStartDate, end date:theEndDate}
            end tell
        end tell
        ''')

        # 构造 AppleScript 脚本
        script = script.format(start_date=start_date,end_date=end_date,event_name=event_name)

        return run_applescript(script)

    @staticmethod
    def delete(event_name:str):
        script = PromptTemplate(template='''
        tell application "Calendar"
            -- 设置你要删除的日程名称
            set eventNameToRemove to "{event_name}" -- **这里已经设置为“会议”**
            
            -- 遍历所有的日历
            repeat with i from 1 to (count of calendars)
                set cal to item i of calendars
                
                -- 获取当前日历的所有日程到一个变量中
                set allEvents to every event in cal
                
                -- 从后往前遍历日程列表
                repeat with j from (count of allEvents) to 1 by -1
                    set ev to item j of allEvents
                    -- 检查日程的摘要（名称）是否匹配
                    if summary of ev is equal to eventNameToRemove then
                        -- 如果匹配，删除该日程
                        delete ev
                        display notification "已删除日程: " & eventNameToRemove & " (来自 " & name of cal & ")" with title "Calendar Script"
                    end if
                end repeat
            end repeat
            
        end tell
        ''')

        # 构造 AppleScript 脚本
        script = script.format(event_name=event_name)

        # 执行 AppleScript 脚本
        return run_applescript(script)


class Display():
    @staticmethod
    def multiple_selection_boxes(prompt_text="请从下面的列表中选择一项：", list_title="请选择", options:list[str]=None, default_option:str=None):
        """
        使用 AppleScript 显示一个列表选择框，并返回用户的选择。

        Args:
            prompt_text (str): 显示在列表上方的提示信息。
            list_title (str): 选择框窗口的标题。
            options (list): 供用户选择的字符串列表。
            default_option (str): 默认选中的项目。

        Returns:
            str: 用户选择的项目。
            None: 如果用户取消或发生错误。
        """
        import sys
        if sys.platform != 'darwin':
            print("错误：此功能仅在 macOS 上可用。")
            return None

        if options is None:
            options = ["选项 A", "选项 B", "选项 C", "另一个选项"] # 默认选项

        # 将 Python 列表转换为 AppleScript 列表字符串: {"item1", "item2", ...}
        applescript_list = '{' + ', '.join([f'"{item}"' for item in options]) + '}'

        # 构建 AppleScript
        script = f'''
        try
            set myList to {applescript_list}
            set thePrompt to "{prompt_text}"
            set theTitle to "{list_title}"
            '''

        # 添加默认项（如果提供且有效）
        if default_option and default_option in options:
            script += f'set defaultChoice to {{"{default_option}"}}\n'
            script += f'set theChoice to choose from list myList with title theTitle with prompt thePrompt default items defaultChoice'
        else:
            script += f'set theChoice to choose from list myList with title theTitle with prompt thePrompt'

        script += f'''
            -- 检查用户是否点击了取消按钮
            if theChoice is false then
                error number -128 -- 引发标准取消错误
            else
                -- 返回选择的第一个项目 (choose from list 返回列表)
                return item 1 of theChoice
            end if
        on error number -128
            -- 捕获取消错误，可以返回特定值或让 Python 处理异常
            return "USER_CANCELLED" -- 返回一个特殊标记
            -- 或者你可以不处理，让 osascript 返回非零退出码
            -- error number -128
        end try
        '''

        try:
            # 不需要 shlex.quote
            result = subprocess.run(
                ['osascript', '-e', script],
                check=True,          # 如果 osascript 返回非零则抛出异常
                capture_output=True, # 捕获 stdout/stderr
                text=True,           # 将输出解码为文本
                encoding='utf-8'     # 指定编码
            )
            output = result.stdout.strip()

            
            if output == "USER_CANCELLED":
                print("用户取消了选择。")
                return None
            else:
                return output # 返回用户的选择
        except subprocess.CalledProcessError as e:
            # osascript 执行失败或返回错误码 (例如，如果我们在 AppleScript 中直接 error -128)
            # 检查 stderr 获取更多信息
            error_message = e.stderr.strip()
            if "-128" in error_message: # 检查是否是用户取消的标准错误代码
                print("用户取消了选择 (通过错误码捕获)。")
            else:
                print(f"执行 AppleScript 时出错: {e}")
                print(f"错误详情: {error_message}")
            return None
        except FileNotFoundError:
            print("错误: 'osascript' 命令未找到。请确保你在 macOS 上运行。")
            return None
        except Exception as e:
            print(f"发生意外错误: {e}")
            return None

    @staticmethod
    def display_dialog(title, text, buttons='"OK"',button_cancel = True):
        # # --- 示例 ---
        # buttons='"OK","vvk"'
        """使用 AppleScript 显示一个简单的对话框"""
        if button_cancel:
            script = f'''
            display dialog "{text}" with title "{title}" buttons {{"cancel",{buttons}}} \
                default button "{buttons.split(',')[0][1:-1]}"
            '''

        else:
            script = f'''
            display dialog "{text}" with title "{title}" buttons {{{buttons}}} \
                default button "{buttons.split(',')[0][1:-1]}"
            '''
        try:
            # 使用 shlex.quote 防止注入
            shlex.quote(script)
            result = subprocess.run(['osascript', '-e', script],
                                    check=True, capture_output=True, text=True)
            # print(result.stdout)
            return result.stdout[16:-1]
        except subprocess.CalledProcessError as e:
            print(f"Error displaying dialog: {e}")
        except FileNotFoundError:
            print("Error: 'osascript' command not found. Ensure you are on macOS.")

class ShortCut():

    @staticmethod
    def run_shortcut(shortcut_name:str,params:str=None):
        """运行快捷指令

        Args:
            shortcut_name (str, optional): 快捷指令名称. Defaults to ''.
            params (str, optional): 参数. Defaults to None.

        Returns:
            str: 快捷指令的输出
        """
        commend = f'run shortcut "{shortcut_name}"' if params is None else f'run shortcut "{shortcut_name}" with input "{params}"'
        script = f'''tell application "Shortcuts"
            {commend}
        end tell'''
        return run_applescript(script)


