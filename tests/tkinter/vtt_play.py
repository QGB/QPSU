#coding=utf-8
import sys,pathlib				 # .py/tkinte/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import tkinter as tk
from tkinter import ttk
import re, time, threading, pathlib, signal, os
from dataclasses import dataclass, field
from typing import List, Optional

VLC_PATH = rf"{os.path.expanduser('~')}\Desktop\vlc-3.0.20" # 必须和python 相同 64位
vlc, VLC_ERROR = None, None
try:
    if os.path.exists(VLC_PATH) and VLC_PATH not in os.environ.get('PATH', ''):
        os.environ['PATH'] = VLC_PATH + os.pathsep + os.environ.get('PATH', '')
    import vlc
except (ImportError, OSError) as e:
    VLC_ERROR = e

@dataclass
class Word:
    text: str; start_ms: int = 0; end_ms: int = 0
    start_index: Optional[str] = None; end_index: Optional[str] = None
@dataclass
class Cue: # 现在仅作为所有单词的容器
    start_ms: int; end_ms: int
    words: List[Word] = field(default_factory=list)

class VTTParser: # 最终版解析器，修复所有丢词和重复问题
    def time_to_ms(self, time_str: str) -> int:
        try:
            parts = time_str.split(':'); s_ms = parts[2].split('.')
            return int(parts[0])*3600000 + int(parts[1])*60000 + int(s_ms[0])*1000 + int(s_ms[1])
        except (ValueError, IndexError): return 0
    def parse(self, vtt_path: str) -> List[Cue]:
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f: content = f.read()
        except FileNotFoundError:
            print(f"错误: VTT文件未找到 at '{vtt_path}'"); return []
        word_map = {} # 使用字典以时间戳为键，彻底去重
        blocks = re.split(r'\n\s*\n', content.replace('WEBVTT', '').strip())
        for block in blocks:
            if '-->' not in block: continue
            lines = block.strip().split('\n')
            content_lines = lines[1:] if len(lines) > 1 else []
            for line in content_lines:
                tagged_words = list(re.finditer(r'<(\d{2}:\d{2}:\d{2}\.\d{3})><c>\s*([^<]+?)\s*</c>', line))
                for match in tagged_words:
                    time_ms = self.time_to_ms(match.group(1))
                    word_text = match.group(2).strip()
                    word_map[time_ms] = word_text
                if tagged_words: # 【关键】处理行首的无标签单词 (如 'share')
                    prefix_text = line[:tagged_words[0].start()].strip()
                    if prefix_text:
                        first_tagged_word_time = self.time_to_ms(tagged_words[0].group(1))
                        for i, p_word in enumerate(reversed(prefix_text.split())):
                            pseudo_time = first_tagged_word_time - (i + 1) # 赋予一个微小的时间偏移
                            if pseudo_time not in word_map: word_map[pseudo_time] = p_word
        if not word_map: return []
        sorted_words = [Word(text=text, start_ms=ms) for ms, text in sorted(word_map.items())]
        for i in range(len(sorted_words) - 1): # 计算每个单词的结束时间
            sorted_words[i].end_ms = sorted_words[i+1].start_ms
        if sorted_words: sorted_words[-1].end_ms = sorted_words[-1].start_ms + 1000
        return [Cue(start_ms=sorted_words[0].start_ms, end_ms=sorted_words[-1].end_ms, words=sorted_words)]

class VTTPlayerApp:
    def __init__(self, root: tk.Tk, vtt_path: str):
        self.root = root; self.vtt_path = vtt_path
        self.player: Optional['vlc.MediaPlayer'] = None; self.vlc_instance: Optional['vlc.Instance'] = None
        self.is_playing: bool = False; self.playback_start_time: float = 0.0; self.paused_elapsed_time: float = 0.0
        self.playback_rate: float = 0.6 # 默认播放速率
        self.current_word_index: int = -1
        self.all_words: List[Word] = []
        self.total_duration_ms: int = 0
        self.playback_thread: Optional[threading.Thread] = None; self.shutdown_requested: bool = False
        self._setup_window(); self._create_widgets()
        self._load_media(); self._bind_events()
    def _setup_window(self):
        self.root.title("VTT Sync Player (Final Version)"); self.root.geometry("1355x772+14+-15"); self.root.configure(bg='#2B2B2B')
        self.root.grid_rowconfigure(0, weight=1); self.root.grid_columnconfigure(0, weight=1)
    def _create_widgets(self):
        self.main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg='#2B2B2B')
        self.main_pane.grid(row=0, column=0, sticky="nsew")
        self.video_frame = tk.Frame(self.main_pane, bg="black"); self.main_pane.add(self.video_frame, height=400)
        text_frame = ttk.Frame(self.main_pane); self.main_pane.add(text_frame)
        text_frame.grid_rowconfigure(0, weight=1); text_frame.grid_columnconfigure(0, weight=1)
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Segoe UI", 16), bg='#2B2B2B', fg='white', padx=15, pady=15, spacing1=8, spacing3=8, insertbackground='cyan', selectbackground='#0078D7', borderwidth=0, highlightthickness=0)
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.tag_config('highlight', background='#FFC700', foreground='black')
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview); scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        control_frame = ttk.Frame(self.root, padding="5"); control_frame.grid(row=1, column=0, sticky="ew")
        self.play_pause_btn = ttk.Button(control_frame, text="▶", command=self.toggle_play_pause); self.play_pause_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.time_label = ttk.Label(control_frame, text="00:00.000 / 00:00.000", font=("Segoe UI", 11), anchor="w"); self.time_label.pack(side=tk.LEFT, fill="x", expand=True)
        self.rate_label = ttk.Label(control_frame, text=f"{self.playback_rate:.1f}x", font=("Segoe UI", 10)); self.rate_label.pack(side=tk.RIGHT, padx=(5, 0))
        self.rate_scale = ttk.Scale(control_frame, from_=0.2, to=2.0, value=self.playback_rate, orient=tk.HORIZONTAL, command=self._on_rate_change); self.rate_scale.pack(side=tk.RIGHT, fill="x")
    def _load_media(self):
        cues = VTTParser().parse(self.vtt_path)
        if not cues or not cues[0].words: self.play_pause_btn.config(state=tk.DISABLED); return
        self.all_words = cues[0].words
        self.total_duration_ms = self.all_words[-1].end_ms
        self.text_widget.config(state=tk.NORMAL); self.text_widget.delete('1.0', tk.END)
        for word in self.all_words: # 将所有单词加载为单体文本，并记录每个词的精确索引
            word.start_index = self.text_widget.index(tk.INSERT)
            self.text_widget.insert(tk.INSERT, word.text + ' ')
            word.end_index = self.text_widget.index(f"{word.start_index} + {len(word.text)} chars")
        self.text_widget.config(state=tk.DISABLED); self._update_time_label()
        if vlc:
            self.vlc_instance = vlc.Instance("--no-xlib --avcodec-hw=none"); self.player = self.vlc_instance.media_player_new()
            video_path = pathlib.Path(self.vtt_path).with_suffix('.mp4')
            if video_path.exists():
                self.player.set_media(self.vlc_instance.media_new(str(video_path))); self.player.set_hwnd(self.video_frame.winfo_id())
                self.root.after(500, self._fetch_vlc_duration)
            else: self.player = None; print(f"警告: 未找到视频文件 '{video_path}'。")
        else: print(f"警告: VLC库加载失败({VLC_ERROR})。")
    def _fetch_vlc_duration(self):
        if not self.player or self.shutdown_requested: return
        duration = self.player.get_length()
        if duration > 0:
            self.total_duration_ms = duration
            if self.all_words: self.all_words[-1].end_ms = duration
            self._update_time_label()
        else: self.root.after(200, self._fetch_vlc_duration)
    def _bind_events(self):
        self.text_widget.bind('<Button-1>', self._on_text_click)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def _on_text_click(self, event):
        click_index = self.text_widget.index(f"@{event.x},{event.y}")
        for word in self.all_words:
            if self.text_widget.compare(click_index, '>=', word.start_index) and self.text_widget.compare(click_index, '<=', word.end_index):
                self.seek_to(word.start_ms); return
    def _on_rate_change(self, rate_str: str):
        new_rate = float(rate_str)
        self.rate_label.config(text=f"{new_rate:.1f}x")
        if abs(self.playback_rate - new_rate) < 0.01: return
        self.playback_rate = new_rate
        if self.player: self.player.set_rate(self.playback_rate)
        if self.is_playing: self.resync_time()
    def get_current_time_ms(self) -> float:
        if not self.is_playing: return self.paused_elapsed_time
        elapsed = (time.monotonic() - self.playback_start_time) * self.playback_rate
        return self.paused_elapsed_time + elapsed * 1000
    def resync_time(self):
        if not self.player or self.shutdown_requested: return
        self.paused_elapsed_time = self.player.get_time()
        self.playback_start_time = time.monotonic()
        self._update_time_label()
    def seek_to(self, time_ms: float):
        if not self.player: return
        self.player.set_time(int(time_ms))
        if not self.is_playing: self.toggle_play_pause()
        else: self.root.after(100, self.resync_time)
    def toggle_play_pause(self):
        if not self.player: return
        if self.is_playing:
            self.player.pause(); self.is_playing = False; self.resync_time()
        else:
            if self.player.get_state() == vlc.State.Ended: self.player.set_time(0)
            self.player.play(); self.player.set_rate(self.playback_rate); self.is_playing = True; self.resync_time()
            if not self.playback_thread or not self.playback_thread.is_alive():
                self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True); self.playback_thread.start()
        self.play_pause_btn.config(text="❚❚" if self.is_playing else "▶")
    def _playback_loop(self):
        while self.is_playing and not self.shutdown_requested:
            current_time = self.get_current_time_ms()
            if self.total_duration_ms > 0 and current_time >= self.total_duration_ms:
                self.root.after(0, self.stop_playback); break
            word_idx = self._find_word_index_for_time(current_time)
            if word_idx is not None and word_idx != self.current_word_index:
                self.current_word_index = word_idx
                if not self.shutdown_requested: self.root.after(0, self._update_ui, word_idx)
            else:
                if not self.shutdown_requested: self.root.after(0, self._update_time_label)
            time.sleep(0.02)
    def stop_playback(self):
        if self.is_playing: self.toggle_play_pause()
        self.seek_to(0)
    def _find_word_index_for_time(self, current_time: float) -> Optional[int]:
        for i, word in enumerate(self.all_words):
            if word.start_ms <= current_time < word.end_ms: return i
        return None
    def _update_time_label(self):
        def format_ms(ms): return f"{int(ms/1000)//60:02d}:{int(ms/1000)%60:02d}.{int(ms%1000):03d}"
        if not self.shutdown_requested: self.time_label.config(text=f"{format_ms(self.get_current_time_ms())} / {format_ms(self.total_duration_ms)}")
    def _update_ui(self, word_idx: int):
        self._update_time_label()
        if self.shutdown_requested: return
        self.text_widget.tag_remove('highlight', '1.0', 'end')
        if word_idx != -1:
            word = self.all_words[word_idx]
            if word.start_index and word.end_index:
                self.text_widget.tag_add('highlight', word.start_index, word.end_index)
                self._smart_scroll(word.start_index) # 【关键】滚动到当前单词的精确位置
    def _smart_scroll(self, index: str):
        self.root.after(50, self._perform_scroll, index)
    def _perform_scroll(self, index: str):
        if self.shutdown_requested or not index: return
        try:
            if not self.text_widget.winfo_exists(): return
            self.text_widget.see(index) # 首先，确保目标可见（最小化滚动）
            self.root.update_idletasks() # 等待UI更新以获取正确的位置信息
            bbox = self.text_widget.dlineinfo(index) # 获取目标在可视区域内的位置
            if not bbox: return # 如果目标不可见（例如窗口已关闭），则中止
            line_y, view_height = bbox[1], self.text_widget.winfo_height()
            if line_y > view_height * 0.85: # 如果目标行在屏幕底部 (在可视区域的后85%位置)
                # 将其滚动到屏幕顶部，以提供更好的阅读上下文
                if self.is_playing:self.toggle_play_pause()# 这中间好卡，界面都无响应几秒钟，不得不临时暂停，有更好修复方法吗
                display_line_start_index = f"{index} display linestart" # 使用'display'前缀处理自动换行
                display_line_num = self.text_widget.count("1.0", display_line_start_index, "displaylines")[0]
                total_display_lines = self.text_widget.count("1.0", tk.END, "displaylines")[0]
                if total_display_lines > 0:
                    self.text_widget.yview_moveto(display_line_num / total_display_lines)
                self.toggle_play_pause()    
        except (tk.TclError, AttributeError, ZeroDivisionError) as e:
            print(f"滚动时发生错误 (index: {index}): {e}")
    def on_close(self): # 【关键】严格按照您的指令，使用强制退出
        os._exit(0)

if __name__ == "__main__":
    N.rpcServer(globals=globals(),locals=locals(),port=1133)
    vtt_file_path = r'C:\test\qgbcs\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt' # 【您的配置】
    if not pathlib.Path(vtt_file_path).is_file():
        print(f"错误: VTT文件 '{vtt_file_path}' 不存在。程序退出。"); exit()
    main_window = tk.Tk()
    app = VTTPlayerApp(main_window, vtt_file_path)
    def signal_handler(sig, frame): app.on_close() # 信号处理也调用您的关闭方法
    signal.signal(signal.SIGINT, signal_handler)
    print("应用已启动。在终端按 Ctrl+C 或关闭窗口可退出。")
    main_window.mainloop()
