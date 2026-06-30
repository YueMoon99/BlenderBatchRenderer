import sys
import time
import os
import json
import subprocess
import tempfile
import copy
import re
import math
import ctypes
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QLineEdit,
    QComboBox, QFileDialog, QTextEdit, QSplitter, QGroupBox,
    QGridLayout, QMessageBox, QAbstractItemView,QCheckBox,
    QProgressBar, QDialog, QStyle, QStyledItemDelegate, QSizePolicy, QMenu, QSystemTrayIcon, 
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QTime
from PyQt6.QtGui import QColor, QBrush, QIcon, QAction
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

THEME_COLORS = {
    "bg_app": "#18181B",          # 主背景
    "bg_panel": "#27272A",        # 面板/卡片背景
    "bg_input": "#3F3F46",        # 输入框/下拉框背景
    "bg_input_hover": "#52525B",  # 输入框悬浮
    "text_main": "#F4F4F5",       # 主标题/亮色文字
    "text_muted": "#A1A1AA",      # 次要文字/提示
    "border_light": "#3F3F46",    # 极浅的分割线
    "border_focus": "#3B82F6",    # 输入框激活时的蓝色边框
    "accent": "#3B82F6", 
    "accent_hover": "#60A5FA",
    "btn_start": "#10B981", 
    "btn_start_hover": "#34D399",
    "btn_stop": "#EF4444", 
    "btn_stop_hover": "#F87171",
    "progress_bg": "#3F3F46",
    "progress_chunk": "#10B981",
    "list_wait": "#fff",
    "list_running": "#3B82F6",
    "list_complete": "#10B981",
    "list_failed": "#EF4444",
    "list_stopped": "#71717A",
}

TRANSLATIONS = {
    "zh": {
        "title": "Blender 批量渲染器 Pro 丨 By 舟午YueMoon",
        "blender_group": "Blender 程序路径",
        "set_path": "选择路径",
        "lang_btn": "English",
        "project_list": "任务列表",
        "params_group": "任务参数设置",
        "control_group": "控制台",
        "start": "▶ 开始渲染",
        "stop": "■ 停止渲染",
        "import": "导入工程", "copy": "复制选中", "delete": "删除选中",
        "refresh": "刷新参数", "reset": "重置状态", "clear": "清空列表",
        "after": "完成后:", "none": "无", "shutdown": "关机", "sleep": "睡眠", "restart": "重启",
        "warning": "提示",
        "error": "错误",
        "select_task_warn": "请先在列表中选中需要操作的任务！",
        "set_blender_first": "请先设置Blender程序路径！",
        "extraction_error": "参数提取错误",
        "file": "文件",
        "reason": "错误原因",
        "add_file": "添加文件",
        "blender_exe": "Blender可执行文件",
        "output": "输出路径",
        "render_complete_prompt": "渲染完成提示",
        "tasks_completed_tip": "所有任务已完成，将在 {countdown}秒 后执行 {action}",
        "cancel": "取消",
        "execute_now": "立即执行 {action}",
        "scene": "场景:",
        "camera": "相机:",
        "res_x": "分辨率X:",
        "res_y": "分辨率Y:",
        "start_frame": "起始帧:",
        "end_frame": "结束帧:",
        "step_frame": "帧步长:",
        "format": "格式:",
        "output_path": "输出路径:",
        "browse": "浏览",
        "system_usage": "系统占用: --%",
        "total_frames_tip": "总帧数: {total} | 已渲染: {rendered} | 任务数: {count} | 已完成: {completed}",
        "cpu_ram_usage": "CPU: {cpu}% | 内存: {ram}% | GPU: {gpu}%",
        "status_waiting": "等待渲染",
        "status_rendering": "正在渲染",
        "status_completed": "渲染完成",
        "status_stopped": "手动停止",
        "status_failed": "渲染出错",
        "status_loading": "加载中",
        "close_warning": "当前存在渲染任务，请停止渲染后再关闭本软件。" ,
        "log_task_start": "开始渲染第 {idx} 个任务，任务名：“{name}”，保存位置：“{path}”",
        "log_frame_done": "完成第 {idx} 任务的第 {frame} 帧，用时 {time_str}",
        "log_missing": "⚠️ 警告：检测到工程中有内容丢失 -> {detail}",
        "log_task_done": "完成渲染：“{name}”，总用时： {time_str}",
        "log_all_done": "全部渲染任务完成，本次共渲染 {task_count} 个任务，共 {frame_count} 帧，总计用时 {time_str}",
        "log_stopped": "渲染被手动停止",
        "clear_log": "清空日志",
        "time_stats": "总耗时: {total} | 当前帧: {current} | 平均帧: {avg} | 预计剩余: {eta}",
        "show_main": "显示主界面",
        "quit_app": "完全退出程序",
        "minimized": "已最小化",
        "running_in_bg": "渲染器已在后台运行",
        "quit_warning_text": "当前存在渲染任务，是否确认停止渲染并退出软件？",
        "confirm_quit": "确认退出",
        "frame_sample": "当前帧采样: %v / %m",
        "total_progress": "总渲染进度: %p%",
        "custom_frames": "自定义帧:",
        "custom_frames_ph": "输入自定义渲染的帧，用英文逗号隔开",
        "custom_frames_err_log": "⚠️ 警告：任务 “{name}” 的自定义帧格式错误，只能包含数字和英文逗号！",
        "custom_frames_err_box": "任务 “{name}” 的自定义帧格式错误！\n请确保只能输入数字，并用英文逗号隔开。\n\n例如：1,5,10",
        "auto_fill": "自动填入缺失帧",
        "clear_cf": "清空",
        "no_output_path": "请先设置输出路径！",
        "no_missing_frames": "当前范围内没有发现缺失的帧！",
        "log_auto_fill": "任务 “{name}” 已自动填入 {count} 个缺失帧。",
        "cpu_limit": "CPU资源分配:",
        "cpu_100": "100% (全速渲染)",
        "cpu_75": "75% (预留给系统)",
        "cpu_50": "50% (边看网页边渲)",
        "cpu_25": "25% (纯后台潜水)",
        "indep_process": "每帧渲染完成后自动清空内存（大项目推荐勾选）",
        "indep_process_tt": "适用于物理/SSS等复杂场景：每渲完一帧自动杀进程清空内存，防止越来越慢",
        "frame_sample_tiled": "当前帧进度: Sample: {c_s}/{t_s} | Tiles: {c_t}/{t_t}",
        "denoising": "正在降噪...",
    },

    "en": {
        "title": "Blender Batch Renderer Pro | By 舟午YueMoon",
        "blender_group": "Where is your Blender?",
        "set_path": "Set Blender Path",
        "lang_btn": "中文",
        "project_list": "Project List",
        "params_group": "Task Parameter Settings",
        "control_group": "Control",
        "start": "▶ Start",
        "stop": "■ Stop",
        "import": "Import", "copy": "Copy Sel", "delete": "Delete Sel",
        "refresh": "Refresh Para", "reset": "Reset Status", "clear": "Clear All",
        "after": "After:", "none": "None", "shutdown": "Shut Down", "sleep": "Sleep", "restart": "Restart",
        "warning": "Warning",
        "error": "Error",
        "select_task_warn": "Please select the task to operate first!",
        "set_blender_first": "Set Blender path first!",
        "extraction_error": "Extraction Error",
        "file": "File",
        "reason": "Reason",
        "add_file": "Add file",
        "blender_exe": "Blender Executable",
        "output": "Output",
        "render_complete_prompt": "Render Completion Prompt",
        "tasks_completed_tip": "Tasks completed. {action} in {countdown}s",
        "cancel": "Cancel",
        "execute_now": "{action} Now",
        "scene": "Scene:",
        "camera": "Camera:",
        "res_x": "Res X:",
        "res_y": "Res Y:",
        "start_frame": "Start:",
        "end_frame": "End:",
        "step_frame": "Step:",
        "format": "Format:",
        "output_path": "Output:",
        "browse": "Browse",
        "system_usage": "System Usage: --%",
        "total_frames_tip": "Total Frames: {total} | Rendered: {rendered} | Tasks: {count} | Completed: {completed}",
        "cpu_ram_usage": "CPU: {cpu}% | RAM: {ram}% | GPU: {gpu}%",
        "status_waiting": "Waiting",
        "status_rendering": "Rendering",
        "status_completed": "Completed",
        "status_stopped": "Stopped",
        "status_failed": "Failed",
        "status_loading": "Loading",
        "close_warning": "There is an active rendering task. Please stop rendering before closing the software.",
        "log_task_start": "Started rendering task: {idx}, Task Name: \"{name}\", Output: \"{path}\"",
        "log_frame_done": "Completed task {idx}, frame {frame}, time taken {time_str}",
        "log_missing": "⚠️ Warning: Missing content detected in project -> {detail}",
        "log_task_done": "Finished rendering: “{name}”，total time:  {time_str}",
        "log_all_done": "All tasks completed. Rendered {task_count} tasks, {frame_count} frames. Total time {time_str}.",
        "log_stopped": "Rendering was manually stopped",
        "clear_log": "Clear Log",
        "time_stats": "Total: {total} | Current: {current} | Average: {avg} | ETA: {eta}",
        "show_main": "Show Main Window",
        "quit_app": "Quit Application",
        "minimized": "Minimized",
        "running_in_bg": "Renderer is running in the background",
        "quit_warning_text": "Active rendering task exists. Stop rendering and quit?",
        "confirm_quit": "Confirm Quit",
        "frame_sample": "Frame Sampling: %v / %m",
        "total_progress": "Total Progress: %p%",
        "custom_frames": "Custom Frames:",
        "custom_frames_ph": "Enter custom frames, separated by commas",
        "custom_frames_err_log": "⚠️ Warning: Task '{name}' custom frames format is invalid! Use only numbers and commas.",
        "custom_frames_err_box": "Task '{name}' has invalid custom frames format!\nPlease use only numbers separated by commas.\n\nExample: 1,5,10",
        "auto_fill": "Auto-Fill Missing",
        "clear_cf": "Clear",
        "no_output_path": "Please set the output path first!",
        "no_missing_frames": "No missing frames found in the current range!",
        "log_auto_fill": "Task '{name}': Auto-filled {count} missing frames.",
        "cpu_limit": "CPU Allocation:",
        "cpu_100": "100% (Full Speed)",
        "cpu_75": "75% (Leave some room)",
        "cpu_50": "50% (Multitasking)",
        "cpu_25": "25% (Background)",
        "indep_process": "Per-Frame Independent Rendering",
        "indep_process_tt": "Kills process after each frame to prevent memory leaks in complex scenes.",
        "frame_sample_tiled": "Frame Sample: {c_s}/{t_s} | Tiles: {c_t}/{t_t}",
        "denoising": "Denoising...",
    }
}

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CONFIG_FILE = "BlenderBatchRenderer_config.json"
SESSION_FILE = "BlenderBatchRenderer_session.json"

class MyDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.StateFlag.State_HasFocus:
            option.state &= ~QStyle.StateFlag.State_HasFocus
        super().paint(painter, option, index)

class RenderTask:
    def __init__(self, blend_path):
        self.blend_path = blend_path
        self.name = os.path.basename(blend_path)
        self.scene_name = ""
        self.camera_name = ""
        self.frame_start = 1
        self.frame_end = 250
        self.frame_step = 1
        self.resolution_x = 1920
        self.resolution_y = 1080
        self.output_path = ""
        self.output_format = "PNG"
        self.custom_frames = ""
        self.independent_process = False
        self.status = "Waiting"
        self.load_status = "Loading" 
        self.error_msg = ""
        self.scenes_list = []  
        self.cameras_list = [] 
        self.after_render_action = "None"
        self.rendered_frames = 0
        self.scene_data = {}

    def to_dict(self):
        return {
            "blend_path": self.blend_path,
            "name": self.name,
            "scene_name": self.scene_name,
            "camera_name": self.camera_name,
            "frame_start": self.frame_start,
            "frame_end": self.frame_end,
            "frame_step": self.frame_step,
            "resolution_x": self.resolution_x,
            "resolution_y": self.resolution_y,
            "output_path": self.output_path,
            "output_format": self.output_format,
            "status": self.status,
            "load_status": self.load_status,
            "error_msg": self.error_msg,
            "scenes_list": self.scenes_list,
            "cameras_list": self.cameras_list,
            "after_render_action": self.after_render_action,
            "rendered_frames": self.rendered_frames,
            "scene_data": getattr(self, 'scene_data', {}),
            "custom_frames": getattr(self, 'custom_frames', ''),
            "independent_process": getattr(self, 'independent_process', False),
        }

    @classmethod
    def from_dict(cls, data):
        t = cls(data.get("blend_path", ""))
        for k, v in data.items():
            if hasattr(t, k) or k == "scene_data":
                setattr(t, k, v)
        return t
    
class ParamExtractorThread(QThread):
    task_finished = pyqtSignal(object)
    def __init__(self, blender_path, task):
        super().__init__()
        self.blender_path = blender_path
        self.task = task
    def run(self):
        json_p = os.path.join(tempfile.gettempdir(), f"render_info_{id(self.task)}.json")
        
        script = f"""
import bpy, json
try:
    d = {{"active": bpy.context.scene.name, "scenes": {{}}}}
    for s in bpy.data.scenes:
        d["scenes"][s.name] = {{
            "cl": [o.name for o in s.objects if o.type=='CAMERA'],
            "cc": s.camera.name if s.camera else "",
            "fs": s.frame_start, "fe": s.frame_end, "st": s.frame_step,
            "rx": s.render.resolution_x, "ry": s.render.resolution_y, 
            "out": s.render.filepath, "fm": s.render.image_settings.file_format
        }}
    with open(r"{json_p}", 'w', encoding='utf-8') as f:
        json.dump(d, f)
except Exception as e:
    print(e)
"""
        
        ts = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script); ts = f.name
            
            subprocess.run(
                [self.blender_path, "-b", self.task.blend_path, "-P", ts], 
                capture_output=True, text=True, timeout=120,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if os.path.exists(json_p):
                with open(json_p, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    
                    self.task.scene_data = d.get('scenes', {})
                    self.task.scenes_list = list(self.task.scene_data.keys())
                    self.task.scene_name = d.get('active', "")
                    
                    if self.task.scene_name in self.task.scene_data:
                        sd = self.task.scene_data[self.task.scene_name]
                        self.task.cameras_list = sd.get('cl', [])
                        self.task.camera_name = sd.get('cc', "")
                        self.task.frame_start = sd.get('fs', 1)
                        self.task.frame_end = sd.get('fe', 250)
                        self.task.frame_step = sd.get('st', 1)
                        self.task.resolution_x = sd.get('rx', 1920)
                        self.task.resolution_y = sd.get('ry', 1080)
                        self.task.output_path = sd.get('out', "")
                        self.task.output_format = sd.get('fm', "PNG")
                        
                self.task.load_status = "Success"
            else:
                self.task.load_status = "Failed"
                self.task.error_msg = "Blender did not output parameter JSON."
        except Exception as e:
            self.task.load_status = "Failed"
            self.task.error_msg = str(e)
        finally:
            if ts and os.path.exists(ts): os.remove(ts)
            if os.path.exists(json_p): os.remove(json_p)
            self.task_finished.emit(self.task)

class BatchRenderThread(QThread):
    status_updated = pyqtSignal(object, str)
    log_updated = pyqtSignal(str)
    all_finished = pyqtSignal()
    frame_done = pyqtSignal(object, str)
    sample_updated = pyqtSignal(int, int, str)
    
    def __init__(self, tasks, blender_path):
        super().__init__()
        self.tasks = tasks
        self.blender_path = blender_path
        self.is_running = True
        self.current_process = None
        self.current_rendering_task = None
        
    def run(self):
        for task in self.tasks:
            if not self.is_running: break
            if task.status in ["Completed", "Stopped", "Failed"] or task.load_status != "Success": continue
            self.current_rendering_task = task
            self.render_single_task(task)
        self.all_finished.emit()
        
    def render_single_task(self, task):
        temp_script = None
        try:
            task.rendered_frames = 0
            self.status_updated.emit(task, "Rendering")
            safe_out = task.output_path.replace("\\", "/")
            
            script_content = f"""
import bpy
try:
    scene = bpy.context.scene
    if "{task.camera_name}" in bpy.data.objects:
        scene.camera = bpy.data.objects["{task.camera_name}"]
    scene.frame_start = {task.frame_start}
    scene.frame_end = {task.frame_end}
    scene.frame_step = {task.frame_step}
    scene.render.resolution_x = {task.resolution_x}
    scene.render.resolution_y = {task.resolution_y}
    scene.render.filepath = r"{safe_out}"
    scene.render.image_settings.file_format = "{task.output_format}"
except Exception as e:
    print(f"RENDER_ERROR: {{e}}")
"""
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script_content); temp_script = f.name
                
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            
            cf = getattr(task, 'custom_frames', '').strip()
            if cf:
                frame_list = [f.strip() for f in cf.split(',') if f.strip().isdigit()]
            else:
                frame_list = [str(f) for f in range(task.frame_start, task.frame_end + 1, task.frame_step)]
                
            is_indep = getattr(task, 'independent_process', False)
            
            process_args_list = []
            if is_indep:
                for f_val in frame_list:
                    args = [self.blender_path, "-b", task.blend_path]
                    if task.scene_name: args.extend(["-S", task.scene_name])
                    args.extend(["-P", temp_script, "-f", f_val])
                    process_args_list.append(args)
            else:
                args = [self.blender_path, "-b", task.blend_path]
                if task.scene_name: args.extend(["-S", task.scene_name])
                args.extend(["-P", temp_script])
                if cf:
                    for f_val in frame_list: args.extend(["-f", f_val])
                else:
                    args.append("-a")
                process_args_list.append(args)
                
            for args in process_args_list:
                if not self.is_running: break
                
                self.current_process = subprocess.Popen(
                    args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW, bufsize=0, env=env
                )
                
                if HAS_PSUTIL and getattr(self, 'cpu_pct', 1.0) <= 1.0:
                    try:
                        p = psutil.Process(self.current_process.pid)
                        total_cores = psutil.cpu_count(logical=True)
                        cores_to_use = max(1, int(total_cores * getattr(self, 'cpu_pct', 1.0)))
                        p.cpu_affinity(list(range(cores_to_use)))
                    except: pass
                    
                line_buf = bytearray() 
                frame_max_current = 0
                
                while self.is_running:
                    byte_char = self.current_process.stdout.read(1)
                    if not byte_char: 
                        if line_buf:
                            clean_line = line_buf.decode('utf-8', errors='replace').strip()
                            if clean_line: self.log_updated.emit(clean_line)
                        break
                        
                    if byte_char == b'\r' or byte_char == b'\n':
                        if not line_buf: continue
                        clean_line = line_buf.decode('utf-8', errors='replace').strip()
                        line_buf.clear() 
                        if not clean_line: continue

                        lower_line = clean_line.lower()
                        if "denoising" in lower_line or "降噪" in lower_line:
                            self.sample_updated.emit(1, 1, "DENOISING")
                        
                        elif "sample" in lower_line or "采样" in lower_line:
                            tile_match = re.search(r'(?:tile|rendered|区块|渲染)\D*?(\d+)\s*/\s*(\d+)\s*(?:tiles|区块)?.*?(?:sample|采样)\D*?(\d+)\s*/\s*(\d+)', lower_line)
                        
                            if tile_match:
                                num_val = int(tile_match.group(1))
                                tot_tile = int(tile_match.group(2))
                                cur_samp = int(tile_match.group(3))
                                tot_samp = int(tile_match.group(4))
                            
                                if "rendered" in lower_line or "渲染" in lower_line:
                                    if cur_samp == tot_samp:
                                        completed_tiles = max(0, num_val - 1)
                                    else:
                                        completed_tiles = num_val
                                else:
                                    completed_tiles = max(0, num_val - 1)
                                
                                if tot_tile > 0 and tot_samp > 0:
                                    abs_current = cur_samp + completed_tiles * tot_samp
                                    abs_total = tot_tile * tot_samp
                                    if abs_current < frame_max_current:
                                        abs_current = frame_max_current
                                    else:
                                        frame_max_current = abs_current

                                    current_tile_index = min(completed_tiles + 1, tot_tile)
                                    format_str = f"TILES:{cur_samp}:{tot_samp}:{current_tile_index}:{tot_tile}"
                                    self.sample_updated.emit(abs_current, abs_total, format_str)
                                
                            else:
                                match = re.search(r'(\d+)\s*/\s*(\d+)', lower_line)
                                if match:
                                    cur_samp = int(match.group(1))
                                    tot_samp = int(match.group(2))
                                    if tot_samp > 0 and cur_samp <= tot_samp:
                                        if cur_samp < frame_max_current:
                                            cur_samp = frame_max_current
                                        else:
                                            frame_max_current = cur_samp
                                        self.sample_updated.emit(cur_samp, tot_samp, "")

                        self.log_updated.emit(clean_line)
                        
                        if "Saved:" in clean_line or "Append frame" in clean_line:
                            frame_num = str(task.rendered_frames + 1)
                            if "Append frame" in clean_line:
                                match = re.search(r'Append frame\s+(\d+)', clean_line)
                                if match: frame_num = match.group(1)
                            elif "Saved:" in clean_line:
                                match = re.findall(r'(\d+)\.[a-zA-Z0-9]+', clean_line)
                                if match: frame_num = match[-1] 
                                
                            self.frame_done.emit(task, frame_num)
                            frame_max_current = 0
                    else:
                        line_buf.extend(byte_char) 
                        
                if self.current_process:
                    self.current_process.wait()
                    if self.current_process.returncode != 0 and self.is_running:
                        if not getattr(task, 'error_msg', ''):
                            task.error_msg = f"Blender进程异常退出 (退出码: {self.current_process.returncode})。\n请查看右侧日志了解详情！"
                        break
                        
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            task.error_msg = f"Python底层启动错误:\n{str(e)}"
            self.log_updated.emit(f"❌ [进程崩溃] 启动渲染引擎失败:\n{error_trace}")
            
        finally:
            if temp_script and os.path.exists(temp_script): 
                try: os.unlink(temp_script)
                except: pass
            
            if not self.is_running and self.current_process:
                self.kill_process_tree(self.current_process.pid)
                
            if self.current_process:
                self.current_process.wait()
            
            if self.is_running:
                is_ok = not bool(getattr(task, 'error_msg', ''))
                self.status_updated.emit(task, "Completed" if is_ok else "Failed")

    def kill_process_tree(self, pid):
        if not HAS_PSUTIL:
            try:
                self.current_process.kill()
            except:
                pass
            return
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except:
                    pass
            try:
                parent.kill()
            except:
                pass
            parent.wait(timeout=3)
        except:
            pass

class QuitConfirmDialog(QDialog):
    def __init__(self, parent=None, tr_func=None):
        super().__init__(parent)
        self.tr = tr_func if tr_func else lambda key: key
        
        self.setWindowTitle(self.tr("warning"))
        self.setFixedSize(380, 120)
        layout = QVBoxLayout(self)
        
        label = QLabel(self.tr("quit_warning_text"))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton(self.tr("cancel"))
        self.btn_cancel.setStyleSheet(f"background-color: {THEME_COLORS['btn_start']}; color: white; font-weight: bold; min-height: 30px;")
        self.btn_ok = QPushButton(self.tr("confirm_quit"))
        self.btn_ok.setStyleSheet(f"background-color: {THEME_COLORS['btn_stop']}; color: white; font-weight: bold; min-height: 30px;")
        
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_ok.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)
        layout.addLayout(btn_layout)

class ActionConfirmDialog(QDialog):
    def __init__(self, action_name, parent=None, tr_func=None):
        super().__init__(parent)
        self.tr = tr_func if tr_func else lambda key: key
        self.action_name = action_name
        self.countdown = 10
        self.setWindowTitle(self.tr("render_complete_prompt"))
        self.setFixedSize(400, 150)
        layout = QVBoxLayout(self)
        self.tip_label = QLabel(self.tr("tasks_completed_tip").format(action=self.action_name, countdown=self.countdown))
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.tip_label)
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton(self.tr("cancel"))
        self.cancel_btn.clicked.connect(self.reject)
        self.immediate_btn = QPushButton(self.tr("execute_now").format(action=self.action_name))
        self.immediate_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.cancel_btn); btn_layout.addWidget(self.immediate_btn)
        layout.addLayout(btn_layout)
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_countdown); self.timer.start(1000)
    def update_countdown(self):
        self.countdown -= 1
        if self.countdown <= 0: self.timer.stop(); self.accept()
        self.tip_label.setText(self.tr("tasks_completed_tip").format(action=self.action_name, countdown=self.countdown))

class MainWindow(QMainWindow):

    def save_session(self):
        try:
            current_row = self.task_list.currentRow()
            log_content = self.log_out.toHtml()
            
            data_to_save = {
                "current_row": current_row,
                "tasks": [t.to_dict() for t in self.tasks],
                "log_content": log_content
            }
            
            write_thread = threading.Thread(
                target=self._write_to_disk_task, 
                args=(data_to_save,), 
                daemon=True
            )
            write_thread.start()
            
        except Exception:
            pass
        
    def _write_to_disk_task(self, data):
        try:
            with open(SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception:
            pass
        
    def load_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [RenderTask.from_dict(td) for td in data.get("tasks", [])]
                    if "log_content" in data:
                        self.log_out.setHtml(data["log_content"])

                    for t in self.tasks:
                        if t.status == "Rendering":
                            t.status = "Stopped"
                    
                    self.refresh_ui()
                    
                    current_row = data.get("current_row", -1)
                    if 0 <= current_row < len(self.tasks):
                        self.task_list.setCurrentRow(current_row)
                    elif len(self.tasks) > 0:
                        self.task_list.setCurrentRow(0)
                        
            except Exception:
                pass
    
    def on_scene_switched(self, new_scene):
        if not self.current_task or not new_scene or not self.middle_panel.isEnabled(): 
            return
            
        t = self.current_task
        t.scene_name = new_scene
        
        if hasattr(t, 'scene_data') and new_scene in t.scene_data:
            sd = t.scene_data[new_scene]
            
            self.block_signals(True)
            
            self.camera_cb.clear()
            self.camera_cb.addItems(sd.get('cl', []))
            self.camera_cb.setCurrentText(sd.get('cc', ""))
            
            self.f_start.setText(str(sd.get('fs', 1)))
            self.f_end.setText(str(sd.get('fe', 250)))
            self.f_step.setText(str(sd.get('st', 1)))
            self.res_x.setText(str(sd.get('rx', 1920)))
            self.res_y.setText(str(sd.get('ry', 1080)))
            self.out_path_edit.setText(sd.get('out', ""))
            self.fmt_cb.setCurrentText(sd.get('fm', "PNG"))
            
            self.block_signals(False)
            
            self.save_ui_to_task()

    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        self.current_lang = "zh"
        self.extractors = []
        self.tasks = []
        self.blender_path = ""
        self.current_task = None
        self.batch_thread = None
        self.is_rendering = False
        
        try:
            icon = QIcon(resource_path("favicon.ico"))
            self.setWindowIcon(icon)
        except:
            pass

        self.spinner_frames = ["|", "/", "-", "\\"]
        self.spinner_idx = 0
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner)
        self.spinner_timer.start(150)
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_resources)
        self.monitor_timer.start(1000)
        
        self.setAcceptDrops(True)
        self.init_ui()
        self.init_tray()
        self.load_config()
        self.apply_theme()
        self.retranslate_ui()
        self.load_session()

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        try:
            self.tray_icon.setIcon(QIcon(resource_path("favicon.ico")))
        except:
            pass
            
        tray_menu = QMenu()
        self.show_action = QAction(self.tr("show_main"), self)
        self.quit_action = QAction(self.tr("quit_app"), self)
        
        self.show_action.triggered.connect(self.show_normal_app)
        self.quit_action.triggered.connect(self.tray_quit_app)
        
        tray_menu.addAction(self.show_action)
        tray_menu.addAction(self.quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(lambda reason: self.show_normal_app() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
        self.tray_icon.show()

    def show_normal_app(self):
        self.showNormal()
        self.activateWindow()

    def tray_quit_app(self):
        if self.is_rendering:
            dialog = QuitConfirmDialog(self, self.tr)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.stop_render()
                self.tray_icon.hide()
                QApplication.quit()
        else:
            self.tray_icon.hide()
            QApplication.quit()
        
    def tr(self, key):
        return TRANSLATIONS.get(self.current_lang, {}).get(key, key)

    def switch_language(self):
        self.block_signals(True)
        try:
            self.current_lang = "en" if self.current_lang == "zh" else "zh"
            self.retranslate_ui()
            self.save_config()
            self.on_selection_changed()
        finally:
            self.block_signals(False)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("title"))
        if hasattr(self, 'tray_icon'):
            self.tray_icon.setToolTip(self.windowTitle())

        self.top_box.setTitle(self.tr("blender_group"))
        self.btn_set_b.setText(self.tr("set_path"))
        self.lang_btn.setText(self.tr("lang_btn"))
        self.left_box.setTitle(self.tr("project_list"))
        btn_texts = [
            ("import", self.import_btn), ("copy", self.copy_btn), ("delete", self.delete_btn),
            ("refresh", self.refresh_btn), ("reset", self.reset_btn), ("clear", self.clear_btn)
        ]
        for tr_key, btn in btn_texts:
            btn.setText(self.tr(tr_key))
        self.middle_panel.setTitle(self.tr("params_group"))
        self.label_scene.setText(self.tr("scene"))
        self.label_camera.setText(self.tr("camera"))
        self.label_rx.setText(self.tr("res_x"))
        self.label_ry.setText(self.tr("res_y"))
        self.label_format.setText(self.tr("format"))
        self.label_start.setText(self.tr("start_frame"))
        self.label_end.setText(self.tr("end_frame"))
        self.label_step.setText(self.tr("step_frame"))
        self.label_cf.setText(self.tr("custom_frames"))
        if hasattr(self, 'btn_clear_cf'):
            self.btn_clear_cf.setText(self.tr("clear_cf"))
        if hasattr(self, 'btn_auto_fill'):
            self.btn_auto_fill.setText(self.tr("auto_fill"))
        self.label_output.setText(self.tr("output_path"))
        self.label_after.setText(self.tr("after"))
        self.custom_frames_edit.setPlaceholderText(self.tr("custom_frames_ph"))
        self.btn_browse.setText(self.tr("browse"))
        if hasattr(self, 'indep_process_cb'):
            self.indep_process_cb.setText(self.tr("indep_process"))
            self.indep_process_cb.setToolTip(self.tr("indep_process_tt"))
        self.block_signals(True)
        current_action = self.after_render_action.currentData()
        self.after_render_action.clear()
        action_config = [
            ("none", "None"), ("shutdown", "Shut Down"),
            ("sleep", "Sleep"), ("restart", "Restart")
        ]
        for tr_key, data_val in action_config:
            self.after_render_action.addItem(self.tr(tr_key), data_val)
        if current_action:
            index = self.after_render_action.findData(current_action)
            if index >= 0:
                self.after_render_action.setCurrentIndex(index)
        self.block_signals(False)
        self.control_panel.setTitle(self.tr("control_group"))
        self.btn_start.setText(self.tr("start"))
        self.btn_stop.setText(self.tr("stop"))

        if hasattr(self, 'cpu_limit_cb'):
            current_cpu = self.cpu_limit_cb.currentData() or 1.0
            self.cpu_limit_label.setText(self.tr("cpu_limit"))
            self.cpu_limit_cb.blockSignals(True)
            self.cpu_limit_cb.clear()
            self.cpu_limit_cb.addItem(self.tr("cpu_100"), 1.0)
            self.cpu_limit_cb.addItem(self.tr("cpu_75"), 0.75)
            self.cpu_limit_cb.addItem(self.tr("cpu_50"), 0.5)
            self.cpu_limit_cb.addItem(self.tr("cpu_25"), 0.25)
            idx = self.cpu_limit_cb.findData(current_cpu)
            if idx >= 0: self.cpu_limit_cb.setCurrentIndex(idx)
            self.cpu_limit_cb.blockSignals(False)

        self.res_label.setText(self.tr("system_usage"))
        self.update_stat()
        self.btn_clear_log.setText(self.tr("clear_log"))
        if hasattr(self, 'show_action'):
            self.show_action.setText(self.tr("show_main"))
            self.quit_action.setText(self.tr("quit_app"))

        if hasattr(self, 'frame_progress_bar'):
            self.frame_progress_bar.setMaximum(1)
            self.frame_progress_bar.setValue(0)
            self.frame_progress_bar.setFormat(self.tr("frame_sample").replace('%v', '--').replace('%m', '--'))

        if hasattr(self, 'progress_bar'):
            self.progress_bar.setFormat(self.tr("total_progress"))

        self.refresh_ui()

    def update_spinner(self):
        self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_frames)
        self.refresh_ui()

    def apply_theme(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ 
                background-color: {THEME_COLORS['bg_app']}; 
                color: {THEME_COLORS['text_main']}; 
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif; 
                font-size: 13px;
            }}

            QLabel {{ 
                background-color: transparent; 
            }}

            QSplitter::handle {{ background-color: transparent; }}
            QSplitter::handle:hover {{ background-color: {THEME_COLORS['accent']}; }}

            QGroupBox {{ 
                background-color: {THEME_COLORS['bg_panel']}; 
                border: 1px solid {THEME_COLORS['bg_panel']}; 
                border-radius: 8px; 
                margin-top: 14px; 
                padding-top: 18px; 
            }}
            QGroupBox::title {{ 
                subcontrol-origin: margin; 
                left: 12px; 
                top: 4px; 
                color: {THEME_COLORS['text_muted']}; 
                font-weight: bold; 
                font-size: 12px;
                background-color: transparent;
            }}

            QLineEdit, QComboBox, QTextEdit {{ 
                background-color: {THEME_COLORS['bg_input']}; 
                color: {THEME_COLORS['text_main']}; 
                border: 1px solid transparent; 
                border-radius: 6px; 
                padding: 6px 10px; 
                min-height: 24px;
            }}
            QLineEdit:hover, QComboBox:hover {{ background-color: {THEME_COLORS['bg_input_hover']}; }}
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{ border: 1px solid {THEME_COLORS['border_focus']}; }}
            QLineEdit:disabled, QComboBox:disabled {{ color: {THEME_COLORS['text_muted']}; background-color: {THEME_COLORS['bg_app']}; }}
            
            QComboBox::drop-down {{ border: none; padding-right: 8px; }}
            QComboBox QAbstractItemView {{
                background-color: {THEME_COLORS['bg_panel']};
                border: 1px solid {THEME_COLORS['border_light']};
                border-radius: 6px;
                outline: none;
            }}

            QListWidget {{ 
                background-color: {THEME_COLORS['bg_app']}; 
                border: none;
                outline: none;
            }}
            QListWidget::item {{ 
                background-color: {THEME_COLORS['bg_panel']}; 
                border: 1px solid rgba(255, 255, 255, 0.33); 
                border-radius: 2px; 
                margin-top: 4px; 
                margin-left: 4px;
                margin-right: 4px;
                padding: 2px; 
            }}
            QListWidget::item:selected {{ 
                background-color: {THEME_COLORS['border_light']}; 
                border-left: 4px solid {THEME_COLORS['accent']}; 
                color: {THEME_COLORS['text_main']}; 
            }}

            QPushButton {{ 
                background-color: {THEME_COLORS['bg_input']}; 
                color: {THEME_COLORS['text_main']}; 
                border: none; 
                border-radius: 6px; 
                padding: 6px 12px; 
                min-height: 26px;
                font-weight: 500;
            }}
            QPushButton:hover {{ background-color: {THEME_COLORS['bg_input_hover']}; }}
            QPushButton:pressed {{ background-color: {THEME_COLORS['border_light']}; }}
            
            QPushButton#btn_start {{ background-color: {THEME_COLORS['btn_start']}; font-weight: bold; color: white; min-height: 24px; }}
            QPushButton#btn_start:hover {{ background-color: {THEME_COLORS['btn_start_hover']}; }}
            QPushButton#btn_stop {{ background-color: {THEME_COLORS['btn_stop']}; font-weight: bold; color: white; min-height: 24px; }}
            QPushButton#btn_stop:hover {{ background-color: {THEME_COLORS['btn_stop_hover']}; }}

            QProgressBar {{ 
                border: none; 
                border-radius: 6px; 
                text-align: center; 
                background-color: {THEME_COLORS['progress_bg']}; 
                color: {THEME_COLORS['text_main']};
                font-weight: bold;
                min-height: 20px;
            }}
            QProgressBar::chunk {{ 
                background-color: {THEME_COLORS['progress_chunk']}; 
                border-radius: 6px; 
            }}

            QScrollBar:vertical {{ border: none; background: transparent; width: 10px; margin: 0px 0px 0px 0px; }}
            QScrollBar::handle:vertical {{ background: {THEME_COLORS['text_muted']}; min-height: 20px; border-radius: 5px; }}
            QScrollBar::handle:vertical:hover {{ background: {THEME_COLORS['text_main']}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QCheckBox {{
                background-color: transparent; /* 背景改为彻底透明，融入整体 */
                color: {THEME_COLORS['text_muted']}; /* 默认文字颜色稍微暗一点，不喧宾夺主 */
                spacing: 8px; /* 勾选框图标和文字之间的距离 */
            }}
            QCheckBox:hover {{ 
                color: {THEME_COLORS['text_main']}; /* 鼠标放上去时文字变亮 */
            }}
            QCheckBox:disabled {{
                color: {THEME_COLORS['bg_input_hover']}; /* 禁用时的颜色 */
            }}
        """)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        self.top_box = QGroupBox()
        self.top_box.setMinimumHeight(95)
        self.top_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        top_lay = QHBoxLayout(self.top_box)
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.btn_set_b = QPushButton()
        self.btn_set_b.clicked.connect(self.select_blender_path)
        self.lang_btn = QPushButton()
        self.lang_btn.setFixedWidth(100)
        self.lang_btn.clicked.connect(self.switch_language)
        top_lay.addWidget(self.path_edit)
        top_lay.addWidget(self.btn_set_b)
        top_lay.addWidget(self.lang_btn)
        main_layout.addWidget(self.top_box)

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        
        self.left_box = QGroupBox()
        self.left_box.setMinimumWidth(300)
        left_lay = QVBoxLayout(self.left_box)
        self.task_list = QListWidget()
        self.task_list.setItemDelegate(MyDelegate()) 
        self.task_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.task_list.setDragEnabled(True)
        self.task_list.setAcceptDrops(True)
        self.task_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.task_list.installEventFilter(self)
        self.task_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.task_list.itemDoubleClicked.connect(self.check_error_detail) 
        left_lay.addWidget(self.task_list)
        
        list_grid = QGridLayout()
        btns_config = [
            ("import", self.add_task_dialog), ("copy", self.copy_task), ("delete", self.remove_task), 
            ("refresh", self.refresh_task_params), ("reset", self.reset_tasks), ("clear", self.clear_tasks)
        ]
        self.import_btn = self.copy_btn = self.delete_btn = self.refresh_btn = self.reset_btn = self.clear_btn = None
        for i, (tr_key, func) in enumerate(btns_config):
            b = QPushButton()
            b.clicked.connect(func)
            list_grid.addWidget(b, i//3, i%3)
            setattr(self, f"{tr_key}_btn", b)
        left_lay.addLayout(list_grid)
        self.stat_label = QLabel()
        left_lay.addWidget(self.stat_label)
        self.main_splitter.addWidget(self.left_box)
        
        right_v_splitter = QSplitter(Qt.Orientation.Vertical)
        right_v_splitter.setChildrenCollapsible(False)
        
        self.middle_panel = QGroupBox()
        self.middle_panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        param_layout = QVBoxLayout(self.middle_panel)
        
        self.scene_cb = QComboBox()
        self.scene_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.camera_cb = QComboBox()
        self.camera_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.fmt_cb = QComboBox()
        self.fmt_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.fmt_cb.addItems(["PNG", "JPEG", "TIFF", "OPEN_EXR", "AVI_JPEG", "FFMPEG"])
        
        self.out_path_edit = QLineEdit()
        self.btn_browse = QPushButton()
        self.btn_browse.setFixedWidth(80)
        self.btn_browse.clicked.connect(self.select_output_path)
        self.f_start = QLineEdit()
        self.f_end = QLineEdit()
        self.f_step = QLineEdit()
        self.res_x = QLineEdit()
        self.res_y = QLineEdit()
        
        self.after_render_action = QComboBox()
        self.after_render_action.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        form = QGridLayout()
        
        self.label_scene = QLabel()
        self.label_camera = QLabel()
        
        form.addWidget(self.label_scene, 0, 0)
        
        row0_lay = QHBoxLayout()
        row0_lay.setContentsMargins(0, 0, 0, 0)
        row0_lay.addWidget(self.scene_cb, 1)
        row0_lay.addSpacing(15)              
        row0_lay.addWidget(self.label_camera)
        row0_lay.addWidget(self.camera_cb, 1)
        
        form.addLayout(row0_lay, 0, 1, 1, 5) 
        
        self.label_rx = QLabel()
        self.label_ry = QLabel()
        self.label_format = QLabel()
        form.addWidget(self.label_rx, 1, 0)
        form.addWidget(self.res_x, 1, 1)
        form.addWidget(self.label_ry, 1, 2)
        form.addWidget(self.res_y, 1, 3)
        form.addWidget(self.label_format, 1, 4)
        form.addWidget(self.fmt_cb, 1, 5)

        self.label_start = QLabel()
        self.label_end = QLabel()
        self.label_step = QLabel()
        form.addWidget(self.label_start, 2, 0)
        form.addWidget(self.f_start, 2, 1)
        form.addWidget(self.label_end, 2, 2)
        form.addWidget(self.f_end, 2, 3)
        form.addWidget(self.label_step, 2, 4)
        form.addWidget(self.f_step, 2, 5)

        self.label_cf = QLabel()
        self.custom_frames_edit = QLineEdit()
        self.custom_frames_edit.textChanged.connect(self.on_custom_frames_changed)
        self.custom_frames_edit.editingFinished.connect(self.validate_and_save_custom_frames)
        
        self.btn_clear_cf = QPushButton()
        self.btn_clear_cf.clicked.connect(self.clear_custom_frames)
        self.btn_auto_fill = QPushButton()
        self.btn_auto_fill.clicked.connect(self.auto_fill_missing_frames)
        
        form.addWidget(self.label_cf, 3, 0)
        form.addWidget(self.custom_frames_edit, 3, 1, 1, 3)  
        form.addWidget(self.btn_clear_cf, 3, 4)              
        form.addWidget(self.btn_auto_fill, 3, 5)

        self.label_output = QLabel()
        form.addWidget(self.label_output, 4, 0)
        output_lay = QHBoxLayout()
        output_lay.setContentsMargins(0, 0, 0, 0) 
        output_lay.addWidget(self.out_path_edit) 
        output_lay.addWidget(self.btn_browse) 
        form.addLayout(output_lay, 4, 1, 1, 5)
        
        self.label_after = QLabel()
        form.addWidget(self.label_after, 5, 0)
        form.addWidget(self.after_render_action, 5, 1, 1, 2)
        
        self.indep_process_cb = QCheckBox()
        self.indep_process_cb.clicked.connect(self.save_ui_to_task)
        form.addWidget(self.indep_process_cb, 5, 3, 1, 3, Qt.AlignmentFlag.AlignRight)
        param_layout.addLayout(form)

        self.control_panel = QGroupBox()
        self.control_panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        control_lay = QVBoxLayout(self.control_panel)
        self.res_label = QLabel()
        self.btn_start = QPushButton()
        self.btn_start.setObjectName("btn_start")
        self.time_label = QLabel()
        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.hide()

        self.cpu_limit_label = QLabel()
        self.cpu_limit_cb = QComboBox()
        self.cpu_limit_cb.currentIndexChanged.connect(self.apply_cpu_affinity)
        
        cpu_lay = QHBoxLayout()
        cpu_lay.addWidget(self.cpu_limit_label)
        cpu_lay.addWidget(self.cpu_limit_cb)
        control_lay.addLayout(cpu_lay)
        
        self.btn_start.clicked.connect(self.start_render)
        self.btn_stop.clicked.connect(self.stop_render)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat(self.tr("total_progress"))
        self.frame_progress_bar = QProgressBar()
        self.frame_progress_bar.setFormat(self.tr("frame_sample").replace('%v', '--').replace('%m', '--'))
        
        control_lay.addWidget(self.res_label) 
        control_lay.addWidget(self.time_label) 
        control_lay.addWidget(self.btn_start) 
        control_lay.addWidget(self.btn_stop)
        
        progress_lay = QHBoxLayout()
        progress_lay.addWidget(self.progress_bar)        
        progress_lay.addWidget(self.frame_progress_bar)  
        control_lay.addLayout(progress_lay)              

        right_v_splitter.addWidget(self.middle_panel) 
        right_v_splitter.addWidget(self.control_panel)
        
        log_container = QWidget()
        log_lay = QVBoxLayout(log_container)
        log_lay.setContentsMargins(0, 0, 0, 0)
        self.log_out = QTextEdit()
        self.log_out.setReadOnly(True)
        self.btn_clear_log = QPushButton()
        self.btn_clear_log.clicked.connect(self.log_out.clear)
        log_lay.addWidget(self.log_out)
        log_lay.addWidget(self.btn_clear_log)
        
        right_v_splitter.addWidget(log_container)
        right_v_splitter.setStretchFactor(0, 0)
        right_v_splitter.setStretchFactor(1, 0)
        right_v_splitter.setStretchFactor(2, 1)
        
        self.main_splitter.addWidget(right_v_splitter)
        self.main_splitter.setSizes([500, 600])
        main_layout.addWidget(self.main_splitter)
        
        self.scene_cb.currentTextChanged.connect(self.on_scene_switched)
        for w in [self.camera_cb, self.fmt_cb, self.after_render_action]: 
            w.currentTextChanged.connect(self.save_ui_to_task)
        for w in [self.f_start, self.f_end, self.f_step, self.res_x, self.res_y, self.out_path_edit]: 
            w.editingFinished.connect(self.save_ui_to_task)

    def eventFilter(self, source, event):
        if source is self.task_list:
            if event.type() == event.Type.MouseButtonPress:
                if not self.task_list.itemAt(event.pos()):
                    self.task_list.clearSelection()
                    
            elif event.type() == event.Type.KeyPress:
                if event.key() == Qt.Key.Key_Delete:
                    self.remove_task()
                    return True
            
        return super().eventFilter(source, event)
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.save_session()
        self.save_config()
        self.tray_icon.showMessage(self.tr("minimized"), self.tr("running_in_bg"), QSystemTrayIcon.MessageIcon.Information, 2000)

    def refresh_ui(self):
        if self.task_list.count() != len(self.tasks):
            self.task_list.clear()
            for t in self.tasks:
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, t)
                self.task_list.addItem(item)
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            t = item.data(Qt.ItemDataRole.UserRole)
            
            if t.load_status == "Loading":
                status_text = self.tr("status_loading")
                item.setText(f"{self.spinner_frames[self.spinner_idx]} [{status_text}] {t.name}")
                item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
                item.setForeground(QBrush(QColor(THEME_COLORS['list_wait'])))
            else:
                status_map = {
                    "Waiting": "status_waiting",
                    "Rendering": "status_rendering",
                    "Completed": "status_completed",
                    "Stopped": "status_stopped",
                    "Failed": "status_failed"
                }
                status_key = status_map.get(t.status, "status_waiting")
                status_text = self.tr(status_key)

                if t.status == "Rendering":
                    item.setText(f"{self.spinner_frames[self.spinner_idx]} [{status_text}] {t.name}")
                    item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
                    item.setForeground(QBrush(QColor(THEME_COLORS['list_running'])))
                elif t.status == "Waiting":
                    item.setText(f"[{status_text}] {t.name}")
                    item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation))
                    item.setForeground(QBrush(QColor(THEME_COLORS['list_wait'])))
                elif t.status == "Completed":
                    item.setText(f"[{status_text}] {t.name}")
                    item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
                    item.setForeground(QBrush(QColor(THEME_COLORS['list_complete'])))
                elif t.status == "Stopped":
                    item.setText(f"[{status_text}] {t.name}")
                    item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton))
                    item.setForeground(QBrush(QColor(THEME_COLORS['list_stopped'])))
                elif t.load_status == "Failed" or t.status == "Failed":
                    item.setText(f"[{status_text}] {t.name} (双击查看详情)")
                    item.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
                    item.setForeground(QBrush(QColor(THEME_COLORS['list_failed'])))
        
        self.tasks = [self.task_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.task_list.count())]
        self.update_stat()

    def on_selection_changed(self):
        sel = self.task_list.selectedItems()
        self.block_signals(True)
        
        if not sel: 
            self.middle_panel.setEnabled(True)
            self.scene_cb.clear()
            self.camera_cb.clear()
            self.f_start.setText("")
            self.f_end.setText("")
            self.f_step.setText("")
            self.res_x.setText("")
            self.res_y.setText("")
            self.out_path_edit.setText("")
            self.custom_frames_edit.setText("")
            self.fmt_cb.setCurrentIndex(0)
            
            self.scene_cb.setEnabled(False)
            self.camera_cb.setEnabled(False)
            self.f_start.setEnabled(False)
            self.f_end.setEnabled(False)
            self.f_step.setEnabled(False)
            self.res_x.setEnabled(False)
            self.res_y.setEnabled(False)
            self.out_path_edit.setEnabled(False)
            self.custom_frames_edit.setEnabled(False)
            self.fmt_cb.setEnabled(False)
            self.btn_browse.setEnabled(False)
            
            if hasattr(self, 'btn_clear_cf'):
                self.btn_clear_cf.setEnabled(False)
            if hasattr(self, 'btn_auto_fill'):
                self.btn_auto_fill.setEnabled(False)
            if hasattr(self, 'indep_process_cb'):
                self.indep_process_cb.setEnabled(False)
                self.indep_process_cb.setChecked(False)
                
            self.after_render_action.setEnabled(True)
            self.block_signals(False)
            return
        
        t = sel[-1].data(Qt.ItemDataRole.UserRole)
        self.current_task = t
        is_locked = t.status in ["Rendering", "Completed"]
        load_success = t.load_status == "Success"

        self.middle_panel.setEnabled(load_success)
        self.scene_cb.setEnabled(load_success and not is_locked)
        self.camera_cb.setEnabled(load_success and not is_locked)
        self.res_x.setEnabled(load_success and not is_locked)
        self.res_y.setEnabled(load_success and not is_locked)
        self.out_path_edit.setEnabled(load_success and not is_locked)
        self.fmt_cb.setEnabled(load_success and not is_locked)
        self.btn_browse.setEnabled(load_success and not is_locked)
        
        if hasattr(self, 'btn_clear_cf'):
            self.btn_clear_cf.setEnabled(load_success and not is_locked)
        if hasattr(self, 'btn_auto_fill'):
            self.btn_auto_fill.setEnabled(load_success and not is_locked)
            
        self.after_render_action.setEnabled(load_success)

        self.scene_cb.clear(); self.scene_cb.addItems(t.scenes_list); self.scene_cb.setCurrentText(t.scene_name)
        self.camera_cb.clear(); self.camera_cb.addItems(t.cameras_list); self.camera_cb.setCurrentText(t.camera_name)
        self.res_x.setText(str(t.resolution_x)); self.res_y.setText(str(t.resolution_y))
        self.out_path_edit.setText(t.output_path); self.fmt_cb.setCurrentText(t.output_format)
        
        cf = getattr(t, 'custom_frames', '')
        self.custom_frames_edit.setText(cf)
        self.custom_frames_edit.setEnabled(load_success and not is_locked)

        if cf.strip():
            self.f_start.setText(""); self.f_end.setText(""); self.f_step.setText("")
            self.f_start.setEnabled(False); self.f_end.setEnabled(False); self.f_step.setEnabled(False)
        else:
            self.f_start.setText(str(t.frame_start)); self.f_end.setText(str(t.frame_end)); self.f_step.setText(str(t.frame_step))
            self.f_start.setEnabled(load_success and not is_locked)
            self.f_end.setEnabled(load_success and not is_locked)
            self.f_step.setEnabled(load_success and not is_locked)

        if hasattr(self, 'indep_process_cb'):
            self.indep_process_cb.setEnabled(load_success and not is_locked)
            self.indep_process_cb.setChecked(getattr(t, 'independent_process', False))
            
        self.block_signals(False)

    def reset_tasks(self):
        items = self.task_list.selectedItems()
        if not items:
            QMessageBox.warning(self, self.tr("warning"), self.tr("select_task_warn"))
            return
        for i in items:
            t = i.data(Qt.ItemDataRole.UserRole)
            t.status = "Waiting"
            t.rendered_frames = 0
        self.refresh_ui()
        self.on_selection_changed()

    def refresh_task_params(self):
        if not self.check_env(): return
        items = self.task_list.selectedItems()
        if not items:
            QMessageBox.warning(self, self.tr("warning"), self.tr("select_task_warn"))
            return
        for i in items:
            t = i.data(Qt.ItemDataRole.UserRole)
            
            t.status = "Waiting"
            t.rendered_frames = 0
            
            self.start_param_extraction(t) 
        self.refresh_ui()
        self.on_selection_changed()

    def on_custom_frames_changed(self, text):
        if not self.middle_panel.isEnabled(): return
        has_text = bool(text.strip())
        if has_text:
            self.f_start.setText("")
            self.f_end.setText("")
            self.f_step.setText("")
            self.f_start.setEnabled(False)
            self.f_end.setEnabled(False)
            self.f_step.setEnabled(False)
        else:
            if self.current_task:
                self.f_start.setText(str(self.current_task.frame_start))
                self.f_end.setText(str(self.current_task.frame_end))
                self.f_step.setText(str(self.current_task.frame_step))
            is_locked = self.current_task and self.current_task.status in ["Rendering", "Completed"]
            if not is_locked:
                self.f_start.setEnabled(True)
                self.f_end.setEnabled(True)
                self.f_step.setEnabled(True)

    def validate_and_save_custom_frames(self):
        if not self.middle_panel.isEnabled() or not self.current_task: return
        text = self.custom_frames_edit.text().strip()
        if text:
            if not re.match(r'^(\d+\s*,\s*)*\d+\s*,?\s*$', text):
                self.append_log(self.tr("custom_frames_err_log").format(name=self.current_task.name))
        self.save_ui_to_task()

    def clear_custom_frames(self):
        if not self.middle_panel.isEnabled() or not self.current_task: return
        
        self.custom_frames_edit.setText("")
        self.validate_and_save_custom_frames()

    def auto_fill_missing_frames(self):
        if not self.middle_panel.isEnabled() or not self.current_task: return
        
        t = self.current_task
        out_path = self.out_path_edit.text().strip()
        
        if not out_path:
            QMessageBox.warning(self, self.tr("warning"), self.tr("no_output_path"))
            return
            
        start = t.frame_start
        end = t.frame_end
        step = t.frame_step
        
        dir_name = os.path.dirname(out_path)
        base_name = os.path.basename(out_path)
        
        missing_frames = []
        
        if not os.path.exists(dir_name):
            missing_frames = [str(f) for f in range(start, end + 1, step)]
        else:
            existing_frames = set()
            try:
                for file in os.listdir(dir_name):
                    if file.startswith(base_name):
                        suffix = file[len(base_name):]
                        match = re.match(r'^(\d+)', suffix)
                        if match:
                            existing_frames.add(int(match.group(1)))
            except Exception as e:
                self.append_log(f"读取输出目录失败: {str(e)}")
                return
                
            missing_frames = [str(f) for f in range(start, end + 1, step) if f not in existing_frames]
            
        if missing_frames:
            self.custom_frames_edit.setText(", ".join(missing_frames))
            self.validate_and_save_custom_frames()
            self.append_log(self.tr("log_auto_fill").format(name=t.name, count=len(missing_frames)))
        else:
            self.custom_frames_edit.setText("")
            self.validate_and_save_custom_frames()
            QMessageBox.information(self, self.tr("warning"), self.tr("no_missing_frames"))

    def check_error_detail(self, item):
        t = item.data(Qt.ItemDataRole.UserRole)
        if t.load_status == "Failed" or t.status == "Failed":
            error_info = getattr(t, 'error_msg', '')
            if not error_info:
                error_info = "Blender 进程意外终止或发生底层错误。\n👉 请查看软件界面右侧的【日志控制台】获取详细的崩溃报错！"
            QMessageBox.critical(self, self.tr("error"), f"{self.tr('file')}: {t.name}\n\n{self.tr('reason')}:\n{error_info}")

    def add_task_dialog(self):
        if not self.check_env(): return
        fs, _ = QFileDialog.getOpenFileNames(self, self.tr("add_file"), "", "Blender (*.blend)")
        if fs:
            for f in fs:
                t = RenderTask(f)
                self.tasks.append(t)
                self.start_param_extraction(t) 
            self.refresh_ui()

    def start_param_extraction(self, task):
        task.load_status = "Loading"
        worker = ParamExtractorThread(self.blender_path, task)
        self.extractors.append(worker)
        worker.task_finished.connect(lambda: [self.refresh_ui(), self.on_selection_changed()])
        worker.finished.connect(lambda: self.extractors.remove(worker) if worker in self.extractors else None)
        worker.start()

    def save_ui_to_task(self):
        if not self.current_task or not self.middle_panel.isEnabled(): return
        t = self.current_task
        t.scene_name = self.scene_cb.currentText(); t.camera_name = self.camera_cb.currentText()
        try:
            t.resolution_x, t.resolution_y = int(self.res_x.text()), int(self.res_y.text())
        except: pass
        try:
            t.frame_start, t.frame_end, t.frame_step = int(self.f_start.text()), int(self.f_end.text()), int(self.f_step.text())
        except: pass

        t.output_path, t.output_format = self.out_path_edit.text(), self.fmt_cb.currentText()
        t.custom_frames = self.custom_frames_edit.text().strip()
        if hasattr(self, 'indep_process_cb'):
            t.independent_process = self.indep_process_cb.isChecked()
        if hasattr(t, 'scene_data') and t.scene_name in t.scene_data:
            sd = t.scene_data[t.scene_name]
            sd['cc'] = t.camera_name
            sd['fs'] = t.frame_start
            sd['fe'] = t.frame_end
            sd['st'] = t.frame_step
            sd['rx'] = t.resolution_x
            sd['ry'] = t.resolution_y
            sd['out'] = t.output_path
            sd['fm'] = t.output_format
        self.save_session()

    def apply_cpu_affinity(self):
        if not HAS_PSUTIL: return
        pct = self.cpu_limit_cb.currentData()
        if pct is None: pct = 1.0
        
        if hasattr(self, 'batch_thread') and self.batch_thread:
            self.batch_thread.cpu_pct = pct
            
        if self.is_rendering and hasattr(self, 'batch_thread') and self.batch_thread.current_process:
            try:
                pid = self.batch_thread.current_process.pid
                p = psutil.Process(pid)
                total_cores = psutil.cpu_count(logical=True)
                cores_to_use = max(1, int(total_cores * pct))
                p.cpu_affinity(list(range(cores_to_use)))
            except:
                pass

    def start_render(self):
        if not self.check_env(): return
        
        valid_tasks = [t for t in self.tasks if t.load_status == "Success" and t.status in ["Waiting", "Failed", "Stopped"]]
        if not valid_tasks:
            QMessageBox.warning(self, self.tr("warning"), "当前没有可执行的渲染任务！\n(如果需要重新渲染“已完成”的任务，请先在左侧选中它并点击【重置状态】)")
            return
            
        for task in valid_tasks:
            cf = getattr(task, 'custom_frames', '').strip()
            if cf:
                if not re.match(r'^(\d+\s*,\s*)*\d+\s*,?\s*$', cf):
                    QMessageBox.critical(self, self.tr("error"), self.tr("custom_frames_err_box").format(name=task.name))
                    return
                    
        for task in valid_tasks:
            if task.status in ["Failed", "Stopped"]:
                task.status = "Waiting"
                task.rendered_frames = 0
                
        if self.log_out.toPlainText().strip():
            self.log_out.append("\n\n" + "—"*40 + "\n")
        self.is_rendering = True
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        self.btn_start.hide(); self.btn_stop.show()
        if hasattr(self, 'progress_bar'): self.progress_bar.setValue(0)
        self.batch_start_time = time.time()
        self.cached_avg_time_str = "--h--m--s"
        self.cached_eta_str = "--h--m--s"
        
        self.batch_thread = BatchRenderThread(self.tasks, self.blender_path)
        self.batch_thread.cpu_pct = self.cpu_limit_cb.currentData() or 1.0
        self.batch_thread.status_updated.connect(self.on_status_change)
        self.batch_thread.log_updated.connect(self.filter_blender_log)
        self.batch_thread.frame_done.connect(self.on_frame_done)
        self.batch_thread.all_finished.connect(self.on_all_done)
        self.frame_progress_bar.setValue(0)
        self.batch_thread.sample_updated.connect(self.update_frame_progress)
        self.batch_thread.start()
        
        self.on_selection_changed()
        self.refresh_ui()

    def update_frame_progress(self, current, total, format_str=""):
        if format_str == "DENOISING":
            self.frame_progress_bar.setMaximum(1)
            self.frame_progress_bar.setValue(1)
            self.frame_progress_bar.setFormat(self.tr("denoising"))
        else:
            self.frame_progress_bar.setMaximum(total)
            self.frame_progress_bar.setValue(current)
            
            if format_str.startswith("TILES:"):
                _, c_s, t_s, c_t, t_t = format_str.split(":")
                formatted_text = self.tr("frame_sample_tiled").format(c_s=c_s, t_s=t_s, c_t=c_t, t_t=t_t)
                self.frame_progress_bar.setFormat(formatted_text)
            else:
                self.frame_progress_bar.setFormat(self.tr("frame_sample"))


    def on_frame_done(self, task, real_frame_num):
        now = time.time()
        cost_seconds = int(now - getattr(self, 'last_frame_time', now))
        self.last_frame_time = now
        time_str = self.format_time_str(cost_seconds)
        task.rendered_frames += 1
        time_up_to_now = now - getattr(self, 'batch_start_time', now)
        
        total_frames = 0
        rendered_frames = 0
        for t in self.tasks:
            if t.load_status == "Success":
                cf = getattr(t, 'custom_frames', '').strip()
                if cf:
                    t_total = len([f for f in cf.split(',') if f.strip().isdigit()])
                else:
                    t_total = math.ceil((t.frame_end - t.frame_start + 1) / t.frame_step)
                    
                total_frames += t_total
                if t.status == "Completed":
                    rendered_frames += t_total
                else:
                    rendered_frames += getattr(t, 'rendered_frames', 0)
                    
        if rendered_frames > 0:
            avg_time = time_up_to_now / rendered_frames
            eta = avg_time * (total_frames - rendered_frames)
            self.cached_avg_time_str = self.format_time_str(avg_time)
            self.cached_eta_str = self.format_time_str(eta)

        task_idx = self.tasks.index(task) + 1
        msg = self.tr("log_frame_done").format(
            idx=task_idx, 
            frame=real_frame_num, 
            time_str=time_str
        )
        self.append_log(msg)
        self.update_stat()
        
        if hasattr(self, 'frame_progress_bar'):
            self.frame_progress_bar.setMaximum(1)
            self.frame_progress_bar.setValue(0)
            self.frame_progress_bar.setFormat(self.tr("frame_sample").replace('%v', '--').replace('%m', '--'))
            
        self.save_session()

    def on_status_change(self, task_obj, status):
        task_obj.status = status
        if status == "Rendering":
            self.last_frame_time = time.time()
            self.current_task_start_time = time.time() 
            task_idx = self.tasks.index(task_obj) + 1
            msg = self.tr("log_task_start").format(idx=task_idx, name=task_obj.name, path=task_obj.output_path)
            self.append_log(msg)
        elif status == "Completed":
            cost = time.time() - getattr(self, 'current_task_start_time', time.time())
            msg = self.tr("log_task_done").format(name=task_obj.name, time_str=self.format_time_str(cost))
            self.append_log(msg)
        self.refresh_ui()
        self.on_selection_changed()
        self.save_session()

    def on_all_done(self):
        self.is_rendering = False
        self.btn_start.show(); self.btn_stop.hide()
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        rendered_task_count = sum(1 for t in self.tasks if getattr(t, 'rendered_frames', 0) > 0)
        total_frames = sum(getattr(t, 'rendered_frames', 0) for t in self.tasks)
        if total_frames > 0:
            total_cost = time.time() - getattr(self, 'batch_start_time', time.time())
            msg = self.tr("log_all_done").format(
                task_count=rendered_task_count,
                frame_count=total_frames,
                time_str=self.format_time_str(total_cost)
            )
            self.append_log(msg)
            
        action = self.after_render_action.currentData()
        if action != "None":
            action_tr = self.tr(action.lower())
            d = ActionConfirmDialog(action_tr, self, self.tr)
            if d.exec() == QDialog.DialogCode.Accepted: 
                if action == "Shut Down": 
                    subprocess.run(["shutdown", "/s", "/f", "/t", "0"])
                elif action == "Restart": 
                    subprocess.run(["shutdown", "/r", "/f", "/t", "0"])
        self.on_selection_changed()

    def stop_render(self):
        if hasattr(self, 'batch_thread') and self.batch_thread: 
            self.batch_thread.is_running = False
            if self.batch_thread.current_process:
                self.batch_thread.kill_process_tree(self.batch_thread.current_process.pid)
            if self.batch_thread.current_rendering_task:
                self.batch_thread.current_rendering_task.status = "Stopped"
            self.batch_thread.terminate()
            self.batch_thread.wait()
        self.append_log(self.tr("log_stopped"))
        self.is_rendering = False
        self.frame_progress_bar.setMaximum(1)
        self.frame_progress_bar.setValue(0)
        self.frame_progress_bar.setFormat(self.tr("frame_sample").replace('%v', '--').replace('%m', '--'))
        self.on_all_done()
        self.refresh_ui()
        self.on_selection_changed()

    def copy_task(self):
        items = self.task_list.selectedItems()
        for i in items:
            old_t = i.data(Qt.ItemDataRole.UserRole)
            nt = copy.deepcopy(old_t)
            nt.status = "Waiting"
            nt.rendered_frames = 0
            self.tasks.append(nt)
        self.refresh_ui()
        self.save_session()

    def remove_task(self):
        items = self.task_list.selectedItems()
        for i in items:
            t = i.data(Qt.ItemDataRole.UserRole)
            if t in self.tasks: self.tasks.remove(t)
        self.refresh_ui()
        self.save_session()

    def clear_tasks(self): 
        self.tasks.clear()
        self.refresh_ui()
        self.save_session()

    def select_blender_path(self):
        p, _ = QFileDialog.getOpenFileName(self, self.tr("blender_exe"), "", "Exec (*.exe)")
        if p: 
            self.blender_path = p
            self.path_edit.setText(p)
            self.save_config()

    def select_output_path(self):
        p, _ = QFileDialog.getSaveFileName(self, self.tr("output"), self.out_path_edit.text())
        if p: self.out_path_edit.setText(p)

    def save_config(self):
        config_data = {
            "blender_path": self.blender_path,
            "current_lang": self.current_lang,
            "window_width": self.width(),
            "window_height": self.height(),
            "splitter_sizes": self.main_splitter.sizes() if hasattr(self, 'main_splitter') else [500, 600],
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
        except:
            pass

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    self.blender_path = config_data.get('blender_path', "")
                    self.current_lang = config_data.get('current_lang', "zh")
                    self.path_edit.setText(self.blender_path)
                    w = config_data.get('window_width', 1000)
                    h = config_data.get('window_height', 800)
                    self.resize(w, h)
                    if 'splitter_sizes' in config_data and hasattr(self, 'main_splitter'):
                        self.main_splitter.setSizes(config_data['splitter_sizes'])
            except:
                self.current_lang = "zh"
                self.blender_path = ""

    def update_stat(self):
        total_frames = 0
        rendered_frames = 0
        completed_tasks = 0
        for t in self.tasks:
            if t.load_status == "Success":
                cf = getattr(t, 'custom_frames', '').strip()
                if cf:
                    task_total_frames = len([f for f in cf.split(',') if f.strip().isdigit()])
                else:
                    task_total_frames = math.ceil((t.frame_end - t.frame_start + 1) / t.frame_step)
                
                total_frames += task_total_frames
                if t.status == "Completed":
                    rendered_frames += task_total_frames
                    completed_tasks += 1
                else:
                    rendered_frames += getattr(t, 'rendered_frames', 0)
                    
        self.stat_label.setText(self.tr("total_frames_tip").format(
            total=total_frames, 
            rendered=rendered_frames, 
            count=len(self.tasks), 
            completed=completed_tasks
        ))
        
        if total_frames > 0:
            pct = int((rendered_frames / total_frames) * 100)
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(min(100, pct))
        else:
            if hasattr(self, 'progress_bar'):
                self.progress_bar.setValue(0)
        
    
    def append_log(self, text):
        time_str = QTime.currentTime().toString('hh:mm:ss')
        self.log_out.append(f"【({time_str}) {text}】")
    
    def format_time_str(self, seconds):
        h, rem = divmod(int(seconds), 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}h{m:02d}m{s:02d}s"

    def filter_blender_log(self, line):
        clean_line = line.strip()
        if not clean_line:
            return

        if "Warning:" in clean_line or "Missing file" in clean_line or "not found" in clean_line.lower():
            self.append_log(self.tr("log_missing").format(detail=clean_line))
            self.last_log_type = "warning"
            return

        if clean_line.startswith("Error:") or clean_line.startswith("Exception:") or "RuntimeError" in clean_line:
            self.append_log(f"❌ [Blender 底层报错] 渲染可能已中断 -> {clean_line}")
            self.last_log_type = "error"
            return
            
        if "Updating Scene" in clean_line or "Updating copy on write" in clean_line:
            return

        self.last_log_type = "other"

    def get_gpu_usage(self):
     gpu_usage = "--"
     try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count > 0:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_usage = str(util.gpu)
        pynvml.nvmlShutdown()
        return gpu_usage
     except:
        pass
    
     try:
        from pyadl import ADLManager
        devices = ADLManager.getInstance().getDevices()
        if devices:
            gpu_usage = str(devices[0].getUsage())
        return gpu_usage
     except:
        pass
    
     return gpu_usage

    def update_system_resources(self):
        if not self.isVisible():
            return
            
        if HAS_PSUTIL:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            gpu = self.get_gpu_usage()
            self.res_label.setText(self.tr("cpu_ram_usage").format(cpu=cpu, ram=ram, gpu=gpu))
            
        if hasattr(self, 'is_rendering') and self.is_rendering and hasattr(self, 'batch_start_time'):
            now = time.time()
            total_time = now - self.batch_start_time
            current_frame_time = now - getattr(self, 'last_frame_time', now)
            
            avg_str = getattr(self, 'cached_avg_time_str', "--h--m--s")
            eta_str = getattr(self, 'cached_eta_str', "--h--m--s")
            
            self.time_label.setText(self.tr("time_stats").format(
                total=self.format_time_str(total_time),
                current=self.format_time_str(current_frame_time),
                avg=avg_str,
                eta=eta_str
            ))
        else:
            self.time_label.setText(self.tr("time_stats").format(
                total="--h--m--s", current="--h--m--s", avg="--h--m--s", eta="--h--m--s"
            ))

    def check_env(self):
        if not self.blender_path or not os.path.exists(self.blender_path):
            QMessageBox.critical(self, self.tr("error"), self.tr("set_blender_first"))
            return False
        return True

    def block_signals(self, b):
        for w in [self.scene_cb, self.camera_cb, self.fmt_cb, self.after_render_action, self.f_start, self.f_end, self.f_step, self.res_x, self.res_y, self.out_path_edit, self.custom_frames_edit, self.indep_process_cb]: 
            w.blockSignals(b)

    def dragEnterEvent(self, e): 
        if e.mimeData().hasUrls(): e.accept()

    def dropEvent(self, e):
        if not self.check_env(): return
        for url in e.mimeData().urls():
            p = url.toLocalFile()
            if p.endswith(".blend"):
                t = RenderTask(p)
                self.tasks.append(t)
                self.start_param_extraction(t)
        self.refresh_ui()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    SERVER_NAME = "BlenderBatchRenderer_Pro_SingleInstance"
    
    socket = QLocalSocket()
    socket.connectToServer(SERVER_NAME)
    
    if socket.waitForConnected(500):
        socket.write(b"WAKE_UP")
        socket.flush()
        socket.waitForBytesWritten(500)
        sys.exit(0) 
        
    local_server = QLocalServer()
    QLocalServer.removeServer(SERVER_NAME)
    local_server.listen(SERVER_NAME)

    win = MainWindow()

    def on_new_connection():
        client_socket = local_server.nextPendingConnection()
        if client_socket:
            client_socket.waitForReadyRead(500)
            data = client_socket.readAll()
            if data == b"WAKE_UP":
                win.show_normal_app()
            client_socket.deleteLater()

    local_server.newConnection.connect(on_new_connection)

    win.show()
    sys.exit(app.exec())