import tkinter as tk
from tkinter import ttk
import re, time, threading, pathlib, signal, os
from dataclasses import dataclass, field
from typing import List, Optional

# 【核心修复】在导入vlc之前，必须先将VLC的路径添加到系统PATH中
# 请根据你的VLC解压/安装位置修改此路径
VLC_PATH = r"C:\Users\qgb\Desktop\vlc-3.0.12" 
if os.path.exists(VLC_PATH) and VLC_PATH not in os.environ['PATH']:
    os.environ['PATH'] = VLC_PATH + os.pathsep + os.environ['PATH']

try:
    import vlc
except (ImportError, OSError) as e:
    vlc = None # 将vlc设为None，以便后续检查
    VLC_ERROR = e

@dataclass
class Word: # 定义单个词语及其所有属性
    text: str; start_ms: int = 0; end_ms: int = 0
    start_index: Optional[str] = None; end_index: Optional[str] = None

@dataclass
class Cue: # Cue现在包含一个Word列表
    start_ms: int; end_ms: int
    words: List[Word] = field(default_factory=list)
    start_index: Optional[str] = None # 整个句子的开始位置，用于滚动
    @property
    def text(self) -> str: return ' '.join(w.text for w in self.words)

class VTTParser: # 解析器全面升级，支持词级时间戳和插值
    def time_to_ms(self, time_str: str) -> int: # 将 HH:MM:SS.ms 格式的时间字符串转换为毫秒
        try:
            parts = time_str.split(':'); s_ms = parts[2].split('.')
            return int(parts[0])*3600000 + int(parts[1])*60000 + int(s_ms[0])*1000 + int(s_ms[1])
        except (ValueError, IndexError): return 0

    def _parse_raw_cues(self, content: str) -> List[Cue]: # 初步解析，但这次保留原始文本以提取词级时间
        raw_cues = []
        for block in re.split(r'\n\s*\n', content):
            if '-->' not in block: continue
            lines = block.strip().split('\n')
            try:
                start_str, end_str = lines[0].split('-->')
                start_ms = self.time_to_ms(start_str.strip())
                end_ms = self.time_to_ms(end_str.strip().split(' ')[0])
                raw_text = ' '.join(lines[1:])
                words_with_time = []
                pattern = r'([^<]*)<(\d{2}:\d{2}:\d{2}\.\d{3})><c>\s*([^<]+?)\s*</c>'
                last_pos = 0
                for match in re.finditer(pattern, raw_text):
                    pre_text = match.group(1).strip()
                    if pre_text: words_with_time.extend([(word, None) for word in pre_text.split()])
                    timestamp = self.time_to_ms(match.group(2))
                    word_text = match.group(3).strip()
                    if word_text: words_with_time.append((word_text, timestamp))
                    last_pos = match.end()
                remaining_text = raw_text[last_pos:].strip()
                if remaining_text: words_with_time.extend([(word, None) for word in re.sub(r'</?c>', '', remaining_text).split()])
                if not words_with_time and raw_text:
                    clean_text = re.sub(r'</?[^>]+>', '', raw_text).strip()
                    words_with_time.extend([(word, None) for word in clean_text.split()])
                if words_with_time:
                    cue_words = [Word(text=wt[0], start_ms=wt[1] or 0) for wt in words_with_time]
                    raw_cues.append(Cue(start_ms=start_ms, end_ms=end_ms, words=cue_words))
            except (ValueError, IndexError): continue
        return sorted(raw_cues, key=lambda c: c.start_ms)

    def _interpolate_word_times(self, cues: List[Cue]): # 【核心】为所有词语计算精确或插值的起止时间
        for cue in cues:
            words = cue.words
            if not words: continue
            time_anchors = [(0, cue.start_ms)]
            for i, word in enumerate(words):
                if word.start_ms > 0: time_anchors.append((i, word.start_ms))
            time_anchors.append((len(words), cue.end_ms))
            for i in range(len(time_anchors) - 1):
                start_anchor_idx, start_anchor_time = time_anchors[i]
                end_anchor_idx, end_anchor_time = time_anchors[i+1]
                words_in_segment = words[start_anchor_idx:end_anchor_idx]
                if not words_in_segment: continue
                total_chars = sum(len(w.text) for w in words_in_segment)
                duration = end_anchor_time - start_anchor_time
                if total_chars == 0 or duration <= 0:
                    time_per_word = duration / len(words_in_segment) if len(words_in_segment) > 0 else 0
                    for j, word in enumerate(words_in_segment):
                        word.start_ms = int(start_anchor_time + j * time_per_word)
                        word.end_ms = int(start_anchor_time + (j + 1) * time_per_word)
                else:
                    time_per_char = duration / total_chars
                    current_time = start_anchor_time
                    for word in words_in_segment:
                        word.start_ms = int(current_time)
                        word_duration = len(word.text) * time_per_char
                        current_time += word_duration
                        word.end_ms = int(current_time)
            if words: words[-1].end_ms = cue.end_ms

    def _merge_overlapping_cues(self, cues: List[Cue]) -> List[Cue]: # 合并有词语重叠的渐进式字幕
        if not cues: return []
        merged_cues: List[Cue] = []
        current_cue = Cue(cues[0].start_ms, cues[0].end_ms, cues[0].words[:])
        for i in range(1, len(cues)):
            next_cue = cues[i]
            prev_words_text = [w.text for w in current_cue.words]
            next_words_text = [w.text for w in next_cue.words]
            overlap_len = 0
            for k in range(min(len(prev_words_text), len(next_words_text)), 0, -1):
                if prev_words_text[-k:] == next_words_text[:k]: overlap_len = k; break
            if overlap_len > 0:
                current_cue.words.extend(next_cue.words[overlap_len:])
                current_cue.end_ms = next_cue.end_ms
            else:
                merged_cues.append(current_cue)
                current_cue = Cue(next_cue.start_ms, next_cue.end_ms, next_cue.words[:])
        merged_cues.append(current_cue)
        return merged_cues

    def parse(self, vtt_path: str) -> List[Cue]: # 最终的公开解析方法
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f: content = f.read()
        except FileNotFoundError: print(f"错误: VTT文件未找到 at '{vtt_path}'"); return []
        raw_cues = self._parse_raw_cues(content)
        merged_cues = self._merge_overlapping_cues(raw_cues)
        self._interpolate_word_times(merged_cues)
        return merged_cues

class VTTPlayerApp: # 主应用界面
    def __init__(self, root: tk.Tk, vtt_path: str, vlc_instance: 'vlc.Instance'):
        self.root = root; self.is_playing: bool = False
        self.current_cue_index: int = -1; self.current_word_index: int = -1
        self.cues: List[Cue] = []; self.total_duration_ms: int = 0
        self.vlc_instance = vlc_instance
        self.player = self.vlc_instance.media_player_new() if self.vlc_instance else None
        self._setup_window()
        self._create_widgets()
        self._load_media(vtt_path)
        self._bind_events()

    def _setup_window(self): # 配置标准窗口
        self.root.title("VTT Sync Player"); self.root.geometry("1000x750+50+50")
        self.root.configure(bg='#2B2B2B')
        self.root.grid_rowconfigure(0, weight=1); self.root.grid_columnconfigure(0, weight=1)

    def _create_widgets(self): # 创建并布局所有UI控件
        self.main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg='#2B2B2B')
        self.main_pane.grid(row=0, column=0, sticky="nsew")
        self.video_frame = tk.Frame(self.main_pane, bg="black"); self.main_pane.add(self.video_frame, height=400)
        text_frame = ttk.Frame(self.main_pane); self.main_pane.add(text_frame)
        text_frame.grid_rowconfigure(0, weight=1); text_frame.grid_columnconfigure(0, weight=1)
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Segoe UI", 14), bg='#2B2B2B', fg='white', padx=15, pady=15, spacing3=8, insertbackground='cyan', selectbackground='#0078D7', borderwidth=0, highlightthickness=0)
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.tag_config('highlight', background='#FFC700', foreground='black')
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview); scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_widget.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        control_frame = ttk.Frame(self.root, padding="5"); control_frame.grid(row=1, column=0, sticky="ew")
        self.play_pause_btn = ttk.Button(control_frame, text="▶", command=self.toggle_play_pause); self.play_pause_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.time_label = ttk.Label(control_frame, text="00:00.000 / 00:00.000", font=("Segoe UI", 11), anchor="w"); self.time_label.pack(side=tk.LEFT, fill="x", expand=True)
        self.speed_var = tk.StringVar(value='1.0x'); speed_options = ['0.5x', '0.75x', '1.0x', '1.5x', '2.0x']
        self.speed_menu = ttk.Combobox(control_frame, textvariable=self.speed_var, values=speed_options, width=5, state="readonly"); self.speed_menu.pack(side=tk.RIGHT)
        ttk.Label(control_frame, text="Speed:").pack(side=tk.RIGHT, padx=(5, 2))

    def _load_media(self, vtt_path: str): # 加载并处理VTT和视频数据
        self.cues = VTTParser().parse(vtt_path)
        if not self.cues: self.play_pause_btn.config(state=tk.DISABLED); return
        self.text_widget.config(state=tk.NORMAL); self.text_widget.delete('1.0', tk.END)
        for cue in self.cues:
            cue.start_index = self.text_widget.index(tk.INSERT)
            for word in cue.words:
                word.start_index = self.text_widget.index(tk.INSERT)
                self.text_widget.insert(tk.INSERT, word.text + ' ')
                word.end_index = self.text_widget.index(f"{word.start_index} + {len(word.text)} chars")
            self.text_widget.insert(tk.INSERT, "\n\n")
        self.text_widget.config(state=tk.DISABLED)
        if not self.player: self.play_pause_btn.config(state=tk.DISABLED); return
        video_path = pathlib.Path(vtt_path).with_suffix('.mp4')
        if video_path.exists():
            media = self.vlc_instance.media_new(str(video_path))
            self.player.set_media(media); self.player.set_hwnd(self.video_frame.winfo_id())
            self.player.play(); self.player.pause()
            self.root.after(500, self._fetch_duration)
        else:
            print(f"警告: 未找到对应的视频文件 '{video_path}'"); self.play_pause_btn.config(state=tk.DISABLED)

    def _fetch_duration(self): # 获取视频总时长
        if not self.player: return
        duration = self.player.get_length()
        if duration > 0: self.total_duration_ms = duration; self._update_time_label()
        else: self.root.after(200, self._fetch_duration)

    def _bind_events(self): # 绑定事件
        self.text_widget.bind('<Button-1>', self._on_text_click)
        self.speed_menu.bind("<<ComboboxSelected>>", self._on_speed_change)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _on_text_click(self, event): # 处理文本点击，实现精准到词的跳转播放
        if not self.player: return
        click_index = self.text_widget.index(f"@{event.x},{event.y}")
        for cue_idx, cue in enumerate(self.cues):
            for word_idx, word in enumerate(cue.words):
                if self.text_widget.compare(click_index, '>=', word.start_index) and self.text_widget.compare(click_index, '<=', word.end_index):
                    self.seek_to(word.start_ms)
                    if not self.is_playing: self.toggle_play_pause()
                    return

    def _on_speed_change(self, event=None): # 处理速度变化
        if not self.player: return
        rate = float(self.speed_var.get().replace('x', ''))
        self.player.set_rate(rate)

    def seek_to(self, time_ms: float): # 跳转到指定时间点（同步视频和字幕）
        if not self.player: return
        self.player.set_time(int(time_ms))
        self._update_ui_from_time(time_ms)

    def get_current_time_ms(self) -> int: return self.player.get_time() if self.player else 0

    def toggle_play_pause(self): # 切换播放/暂停状态
        if not self.player: return
        if self.player.is_playing():
            self.player.pause(); self.is_playing = False
        else:
            if self.player.get_state() == vlc.State.Ended: self.seek_to(0)
            self.player.play(); self.is_playing = True
            threading.Thread(target=self._playback_loop, daemon=True).start()
        self.play_pause_btn.config(text="❚❚" if self.is_playing else "▶")

    def _playback_loop(self): # 后台计时与调度线程
        while self.is_playing:
            current_time = self.get_current_time_ms()
            self.root.after(0, self._update_ui_from_time, current_time)
            if self.player and self.player.get_state() == vlc.State.Ended:
                self.root.after(0, self.toggle_play_pause); break
            time.sleep(0.02)

    def _find_indices_for_time(self, current_time: float) -> (Optional[int], Optional[int]): # 查找当前时间和词的索引
        for i, cue in enumerate(self.cues):
            if cue.start_ms <= current_time <= cue.end_ms:
                for j, word in enumerate(cue.words):
                    if word.start_ms <= current_time <= word.end_ms: return i, j
        return None, None

    def _update_time_label(self): # 更新时间标签
        current_time_ms = self.get_current_time_ms()
        def format_ms(ms): return f"{int(ms/1000)//60:02d}:{int(ms/1000)%60:02d}.{int(ms%1000):03d}"
        self.time_label.config(text=f"{format_ms(current_time_ms)} / {format_ms(self.total_duration_ms)}")

    def _update_ui_from_time(self, current_time: float): # 在主线程根据时间更新UI
        self._update_time_label()
        cue_idx, word_idx = self._find_indices_for_time(current_time)
        if cue_idx is not None and (cue_idx != self.current_cue_index or word_idx != self.current_word_index):
            self.current_cue_index, self.current_word_index = cue_idx, word_idx
            self.text_widget.tag_remove('highlight', '1.0', 'end')
            cue, word = self.cues[cue_idx], self.cues[cue_idx].words[word_idx]
            if word.start_index and word.end_index:
                self.text_widget.tag_add('highlight', word.start_index, word.end_index)
                if self.current_word_index == 0: self.text_widget.see(cue.start_index)

    def on_close(self): self.is_playing = False; self.player.stop() if self.player else None; self.root.destroy()

if __name__ == "__main__":
    vlc_instance = None
    if vlc is None:
        print("="*80)
        print(f"错误: 导入VLC库失败。原始错误: {VLC_ERROR}")
        print("视频播放功能将不可用。请确认:")
        print("1. 你已经下载或安装了VLC。")
        print("2. 安装的VLC版本 (64位/32位) 与你的Python版本匹配。")
        print(f"3. 脚本顶部的 'VLC_PATH' 变量已正确指向你的VLC目录。当前设置为: '{VLC_PATH}'")
        print("="*80)
    else:
        vlc_instance = vlc.Instance()

    vtt_file_path = r'C:\test\qgbcs\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt' # 请将此路径替换为你的VTT文件路径
    if not pathlib.Path(vtt_file_path).is_file():
        print(f"错误: VTT文件 '{vtt_file_path}' 不存在。请检查路径。"); exit()
    
    main_window = tk.Tk(); app = VTTPlayerApp(main_window, vtt_file_path, vlc_instance)
    def signal_handler(sig, frame): app.on_close()
    signal.signal(signal.SIGINT, signal_handler)
    print("应用已启动。在终端按 Ctrl+C 可退出。"); main_window.mainloop()
