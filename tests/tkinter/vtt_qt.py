#coding=utf-8
import sys, re, time, threading, os, pathlib, signal
from dataclasses import dataclass, field
from typing import List, Optional

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QTextEdit, QSplitter, QSizePolicy, 
                             QScrollBar, QAbstractSlider)
from PyQt5.QtCore import (Qt, QTimer, QUrl, QEvent, QRectF, QPoint)
from PyQt5.QtGui import (QTextCharFormat, QColor, QTextCursor, QFont, QTextOption)

# --- VLC Setup ---
VLC_PATH = rf"{os.path.expanduser('~')}\Desktop\vlc-3.0.20" 
vlc, VLC_ERROR = None, None
try:
    if not os.path.exists(VLC_PATH):
        env_vlc_path = os.environ.get('VLC_PATH')
        if env_vlc_path and os.path.exists(env_vlc_path): VLC_PATH = env_vlc_path
        else: VLC_PATH = None
    if VLC_PATH and VLC_PATH not in os.environ.get('PATH', ''):
        os.environ['PATH'] = VLC_PATH + os.pathsep + os.environ.get('PATH', '')
    import vlc
except (ImportError, OSError) as e: VLC_ERROR = e

# --- VTT Parsing Logic (Strictly from user attachment: pasted_text_0.txt) ---
@dataclass
class Word: # 【新】定义单个词语及其所有属性
    text: str
    start_ms: int = 0
    end_ms: int = 0
    start_index: Optional[str] = None # For Tkinter, will be unused or overwritten by qt_start_index
    end_index: Optional[str] = None   # For Tkinter, will be unused or overwritten by qt_end_index

@dataclass
class Cue: # Cue现在包含一个Word列表
    start_ms: int
    end_ms: int
    words: List[Word] = field(default_factory=list)
    start_index: Optional[str] = None # 整个句子的开始位置，用于滚动 (For Tkinter)
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
        # content here might start with "WEBVTT\n..."
        # The split `\n\s*\n` will handle the header block correctly (it won't have '-->')
        for block in re.split(r'\n\s*\n', content):
            if '-->' not in block: continue
            lines = block.strip().split('\n')
            try:
                start_str, end_str_with_meta = lines[0].split('-->')
                start_ms = self.time_to_ms(start_str.strip())
                end_ms = self.time_to_ms(end_str_with_meta.strip().split(' ')[0]) # Handle align:start etc.
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
                
                if not words_with_time and raw_text: # If regex didn't match (pure text line)
                    clean_text = re.sub(r'</?[^>]+>', '', raw_text).strip() # Remove any other HTML-like tags
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
                    current_time = float(start_anchor_time) # Use float for precision
                    for word in words_in_segment:
                        word.start_ms = int(current_time)
                        word_duration = len(word.text) * time_per_char
                        current_time += word_duration
                        word.end_ms = int(current_time)
            if words: words[-1].end_ms = cue.end_ms # Ensure last word's end_ms is cue's end_ms

    def _merge_overlapping_cues(self, cues: List[Cue]) -> List[Cue]: # 合并有词语重叠的渐进式字幕
        if not cues: return []
        merged_cues: List[Cue] = []
        # Initialize current_cue with a deep copy of the first cue's words
        current_cue = Cue(cues[0].start_ms, cues[0].end_ms, cues[0].words[:])

        for i in range(1, len(cues)):
            next_cue = cues[i]
            prev_words_text = [w.text for w in current_cue.words]
            next_words_text = [w.text for w in next_cue.words]
            
            overlap_len = 0
            # Iterate backwards from min length to find the longest suffix of prev that is a prefix of next
            for k in range(min(len(prev_words_text), len(next_words_text)), 0, -1):
                if prev_words_text[-k:] == next_words_text[:k]:
                    overlap_len = k
                    break
            
            if overlap_len > 0:
                # If there's an overlap, extend current_cue with non-overlapping words from next_cue
                current_cue.words.extend(next_cue.words[overlap_len:])
                current_cue.end_ms = next_cue.end_ms # Update end time to next_cue's end time
            else:
                # No overlap, finalize current_cue and start a new one with next_cue
                merged_cues.append(current_cue)
                current_cue = Cue(next_cue.start_ms, next_cue.end_ms, next_cue.words[:]) # Deep copy words
        
        merged_cues.append(current_cue) # Add the last processed cue
        return merged_cues

    def parse(self, vtt_path: str) -> List[Cue]: # 最终的公开解析方法
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f: content = f.read()
        except FileNotFoundError:
            print(f"错误: VTT文件未找到 at '{vtt_path}'"); return []
        
        raw_cues = self._parse_raw_cues(content)
        merged_cues = self._merge_overlapping_cues(raw_cues)
        self._interpolate_word_times(merged_cues)
        return merged_cues
# --- End of VTT Parsing Logic ---

class VTTPlayerApp(QMainWindow):
    MANUAL_SCROLL_OVERRIDE_MS = 2000 

    def __init__(self, vtt_path: str):
        super().__init__(); self.vtt_path = vtt_path
        self.player: Optional['vlc.MediaPlayer'] = None; self.vlc_instance: Optional['vlc.Instance'] = None
        self.is_playing: bool = False; self.playback_rate: float = 0.6
        self.current_word_idx_overall: int = -1 
        self.all_words: List[Word] = [] 
        self.total_duration_ms: int = 0
        
        self.user_scrolling: bool = False
        self.scroll_override_timer = QTimer(self); self.scroll_override_timer.setSingleShot(True)
        self.scroll_override_timer.timeout.connect(self._reset_user_scrolling)

        self.playback_timer = QTimer(self); self.playback_timer.timeout.connect(self._update_ui_on_timer)
        self.playback_timer.start(30) 
        
        self.highlight_format = QTextCharFormat(); self.highlight_format.setBackground(QColor("#FFC700")); self.highlight_format.setForeground(QColor("black"))
        
        self._setup_window(); self._create_widgets(); self._load_media(); self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("VTT Sync Player (PyQt)"); self.setGeometry(14, 20, 1355, 772)

    def _create_widgets(self):
        central_widget = QWidget(self); self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget); main_layout.setContentsMargins(0,0,0,0)
        main_splitter = QSplitter(Qt.Vertical); main_layout.addWidget(main_splitter)
        
        self.video_frame = QWidget(self); self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_splitter.addWidget(self.video_frame)
        
        text_container = QWidget(self); text_layout = QVBoxLayout(text_container); text_layout.setContentsMargins(0,0,0,0)
        self.text_widget = QTextEdit(self); self.text_widget.setReadOnly(True)
        self.text_widget.setFont(QFont("Segoe UI", 16)); self.text_widget.setStyleSheet("QTextEdit { background-color: #2B2B2B; color: white; border: none; padding: 15px; }")
        self.text_widget.setWordWrapMode(QTextOption.WordWrap)
        text_layout.addWidget(self.text_widget); main_splitter.addWidget(text_container)
        main_splitter.setSizes([400, 372])
        
        control_frame = QWidget(self); control_layout = QHBoxLayout(control_frame); control_layout.setContentsMargins(5,5,5,5)
        control_frame.setStyleSheet("background-color: #404040; color: white;"); main_layout.addWidget(control_frame)
        
        self.play_pause_btn = QPushButton("▶", self); self.play_pause_btn.setFixedSize(30,30); self.play_pause_btn.setStyleSheet("font-size: 18px;")
        control_layout.addWidget(self.play_pause_btn)
        self.time_label = QLabel("00:00.000 / 00:00.000", self); self.time_label.setFont(QFont("Segoe UI", 11)); self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        control_layout.addWidget(self.time_label, 1)
        self.rate_label = QLabel(f"{self.playback_rate:.1f}x", self); self.rate_label.setFont(QFont("Segoe UI", 10))
        control_layout.addWidget(self.rate_label)
        self.rate_slider = QSlider(Qt.Horizontal, self); self.rate_slider.setRange(20, 200); self.rate_slider.setValue(int(self.playback_rate * 100))
        self.rate_slider.setSingleStep(10); self.rate_slider.setPageStep(20); self.rate_slider.setFixedWidth(150)
        control_layout.addWidget(self.rate_slider)

    def _load_media(self):
        parsed_cues = VTTParser().parse(self.vtt_path) # Use the fully integrated user's parser
        self.all_words = []
        for cue in parsed_cues: self.all_words.extend(cue.words) # Flatten cues into a list of Word objects

        if not self.all_words:
            print("Error: Failed to parse VTT or VTT is empty."); self.play_pause_btn.setEnabled(False); return
        
        self.total_duration_ms = self.all_words[-1].end_ms if self.all_words else 0
        
        self.text_widget.setPlainText("") 
        cursor = self.text_widget.textCursor()
        cursor.beginEditBlock()
        for i, word_obj in enumerate(self.all_words):
            word_obj.qt_start_index = cursor.position() # Store QTextEdit start index
            cursor.insertText(word_obj.text)
            word_obj.qt_end_index = cursor.position()   # Store QTextEdit end index (exclusive for selection)
            if i < len(self.all_words) - 1:
                cursor.insertText(" ") # Add space between words for display
        cursor.endEditBlock()
        QTimer.singleShot(0, lambda: self.text_widget.verticalScrollBar().setValue(0)) 
        self._update_time_label()

        if vlc and self.player is None:
            self.vlc_instance = vlc.Instance("--no-xlib --avcodec-hw=d3d11va")
            self.player = self.vlc_instance.media_player_new()
            video_path = pathlib.Path(self.vtt_path).with_suffix('.mp4')
            if video_path.exists():
                media = self.vlc_instance.media_new(str(video_path))
                self.player.set_media(media)
                if sys.platform.startswith('linux'): self.player.set_xwindow(int(self.video_frame.winId()))
                elif sys.platform == 'win32': self.player.set_hwnd(int(self.video_frame.winId()))
                QTimer.singleShot(500, self._fetch_vlc_duration) 
            else:
                self.player = None; print(f"Warning: Video file not found '{video_path}'."); self.play_pause_btn.setEnabled(False)
        elif not vlc:
            print(f"Warning: VLC library load failed ({VLC_ERROR}). Video playback disabled."); self.play_pause_btn.setEnabled(False)

    def _fetch_vlc_duration(self):
        if not self.player: return
        duration = self.player.get_length()
        if duration > 0:
            self.total_duration_ms = duration
            if self.all_words and self.all_words[-1].end_ms < duration : self.all_words[-1].end_ms = duration 
            self._update_time_label()
        else: QTimer.singleShot(200, self._fetch_vlc_duration) 

    def _connect_signals(self):
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.rate_slider.valueChanged.connect(self._on_rate_change)
        self.text_widget.viewport().installEventFilter(self) 
        self.text_widget.verticalScrollBar().sliderPressed.connect(self._manual_scroll_detected)
        self.text_widget.installEventFilter(self) # For wheel events on text_widget itself

    def eventFilter(self, obj, event):
        if obj is self.text_widget.viewport() and event.type() == QEvent.MouseButtonPress:
            cursor = self.text_widget.cursorForPosition(event.pos())
            clicked_pos = cursor.position()
            for idx, word in enumerate(self.all_words):
                if hasattr(word, 'qt_start_index') and hasattr(word, 'qt_end_index') and \
                   word.qt_start_index <= clicked_pos < word.qt_end_index : # Click is within word boundaries
                    self.seek_to(word.start_ms)
                    if not self.is_playing: self.toggle_play_pause() 
                    return True
        elif obj is self.text_widget and event.type() == QEvent.Wheel: 
            self._manual_scroll_detected()
            return super().eventFilter(obj, event) 
        return super().eventFilter(obj, event)

    def _manual_scroll_detected(self):
        if not self.user_scrolling: print("[ScrollControl] Manual scroll detected. Auto-scroll paused.")
        self.user_scrolling = True
        self.scroll_override_timer.start(self.MANUAL_SCROLL_OVERRIDE_MS)

    def _reset_user_scrolling(self):
        self.user_scrolling = False; print("[ScrollControl] Auto-scroll re-enabled.")

    def _on_rate_change(self, value: int):
        new_rate = value / 100.0; self.rate_label.setText(f"{new_rate:.1f}x"); self.playback_rate = new_rate
        if self.player and self.is_playing: self.player.set_rate(self.playback_rate)

    def get_current_time_ms(self) -> int:
        return self.player.get_time() if self.player else 0

    def seek_to(self, time_ms: int):
        if not self.player: return
        original_is_playing = self.is_playing
        if self.player.get_state() == vlc.State.Playing: self.player.pause() 
        self.player.set_time(int(time_ms))
        
        current_time_for_ui = int(time_ms)
        new_word_idx = self._find_word_index_for_time(current_time_for_ui)
        self.current_word_idx_overall = new_word_idx if new_word_idx is not None else -1
        self._update_highlight(self.current_word_idx_overall)
        if not self.user_scrolling: self._smart_scroll(self.current_word_idx_overall)
        self._update_time_label(current_time_for_ui)

        if original_is_playing:
            if self.player.get_state() != vlc.State.Playing:
                self.player.play()
                QTimer.singleShot(20, lambda: self.player.set_rate(self.playback_rate) if self.player else None)
        self.play_pause_btn.setText("❚❚" if self.is_playing else "▶")

    def toggle_play_pause(self):
        if not self.player: return
        if self.is_playing:
            self.player.pause(); self.is_playing = False
        else:
            if self.player.get_state() == vlc.State.Ended: self.player.set_time(0) 
            self.player.play()
            self.player.set_rate(self.playback_rate) 
            self.is_playing = True
        self.play_pause_btn.setText("❚❚" if self.is_playing else "▶")

    def _update_ui_on_timer(self): 
        if not self.is_playing or not self.player: return
        current_time = self.get_current_time_ms()
        if self.player.get_state() == vlc.State.Ended:
            if self.is_playing: self.stop_playback()
            self._update_time_label(self.total_duration_ms); return

        self._update_time_label(current_time)
        word_idx = self._find_word_index_for_time(current_time)
        
        if word_idx is not None and word_idx != self.current_word_idx_overall:
            self.current_word_idx_overall = word_idx
            self._update_highlight(word_idx)
            if not self.user_scrolling: self._smart_scroll(word_idx)
        elif word_idx is None and current_time > 0 and self.current_word_idx_overall != -1 : 
            self._update_highlight(-1) 

    def stop_playback(self):
        if self.is_playing: self.toggle_play_pause() 
        if self.player: self.player.set_time(0)
        self.current_word_idx_overall = -1
        self._update_highlight(-1); QTimer.singleShot(0, lambda: self.text_widget.verticalScrollBar().setValue(0))
        self._update_time_label(0)

    def _find_word_index_for_time(self, current_time: int) -> Optional[int]:
        if not self.all_words: return None
        start_search = max(0, self.current_word_idx_overall - 5)
        end_search = min(len(self.all_words), self.current_word_idx_overall + 10) # Check a window around current
        for i in range(start_search, end_search):
            word = self.all_words[i]
            if word.start_ms <= current_time < word.end_ms: return i
        for i, word in enumerate(self.all_words): # Fallback to full search
            if word.start_ms <= current_time < word.end_ms: return i
        if self.all_words and current_time >= self.all_words[-1].end_ms: return len(self.all_words) - 1 
        if self.all_words and current_time < self.all_words[0].start_ms: return 0 
        return None

    def _update_time_label(self, current_time_ms: Optional[int] = None):
        if current_time_ms is None: current_time_ms = self.get_current_time_ms()
        def fmt_ms(ms): ms=int(ms); s=ms//1000; m=s//60; s%=60; ms%=1000; return f"{m:02d}:{s:02d}.{ms:03d}"
        self.time_label.setText(f"{fmt_ms(current_time_ms)} / {fmt_ms(self.total_duration_ms)}")

    def _update_highlight(self, word_idx_overall: int):
        cursor = self.text_widget.textCursor()
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document); cursor.setCharFormat(QTextCharFormat()); cursor.clearSelection() 
        if 0 <= word_idx_overall < len(self.all_words):
            word = self.all_words[word_idx_overall]
            if hasattr(word, 'qt_start_index') and hasattr(word, 'qt_end_index'):
                cursor.setPosition(word.qt_start_index)
                cursor.setPosition(word.qt_end_index, QTextCursor.KeepAnchor) # qt_end_index is exclusive end
                cursor.mergeCharFormat(self.highlight_format)
        cursor.endEditBlock()

    def _smart_scroll(self, word_idx_overall: int):
        ''' 我们希望在播放到目标行时，如果目标行在屏幕底部，则滚动到屏幕顶部（向下滚动一页），其他情况不动。这样可以最小化滚动次数。保证高亮部分始终可见。。。
不要省略任何代码 给我整个程序完整紧凑代码 ，不要多余空行和非必要注释，必要注释可以写代码后面，不要另外一行 '''
        if self.user_scrolling: return 
        if word_idx_overall < 0 or word_idx_overall >= len(self.all_words): return
        word = self.all_words[word_idx_overall]
        if not hasattr(word, 'qt_start_index'): return

        text_widget = self.text_widget; cursor = text_widget.textCursor()
        cursor.setPosition(word.qt_start_index)
        
        word_char_rect_vp = text_widget.cursorRect(cursor)
        line_top_vp = word_char_rect_vp.top(); line_height_approx = text_widget.fontMetrics().height()
        line_bottom_vp = line_top_vp + line_height_approx
        
        viewport_h = text_widget.viewport().height(); scrollbar = text_widget.verticalScrollBar()
        current_scroll_val = scrollbar.value()
        target_scroll_to_make_line_top = current_scroll_val + line_top_vp

        is_line_fully_visible = (line_top_vp >= 0 and line_bottom_vp <= viewport_h)
        if not is_line_fully_visible:
            scrollbar.setValue(int(target_scroll_to_make_line_top))
            return

        is_at_screen_bottom = (line_bottom_vp >= viewport_h )
        is_not_at_screen_top = (line_top_vp > 5) 
        if is_at_screen_bottom and is_not_at_screen_top:
            scrollbar.setValue(int(target_scroll_to_make_line_top))

    def closeEvent(self, event): print("Closing application..."); os._exit(0) 

if __name__ == "__main__":
    if VLC_PATH and not os.path.exists(VLC_PATH): print(f"Error: Configured VLC path '{VLC_PATH}' not found.")
    elif not VLC_PATH and not VLC_ERROR: print(f"Warning: VLC path not configured or invalid. Video playback disabled.")
    elif VLC_ERROR: print(f"VLC Import Error: {VLC_ERROR}")


    script_dir = pathlib.Path(__file__).parent
    # Try relative path first (assuming VTT is in the same directory as the script)
    vtt_file_name = "The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt" # Or your specific VTT file
    vtt_file_path_str = str(script_dir / vtt_file_name) 
    
    # Fallback to the absolute path if the relative one is not found
    if not pathlib.Path(vtt_file_path_str).is_file():
        print(f"Info: VTT file not found at relative path '{vtt_file_path_str}'. Trying fallback.")
        vtt_file_path_str = rf'C:\test\qgbcs\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt' # User's fallback
    
    if not pathlib.Path(vtt_file_path_str).is_file():
        # As a last resort, try the VTT sample provided if the main one isn't found
        print(f"Error: VTT file '{vtt_file_path_str}' not found. Trying to use embedded sample VTT.")
        sample_vtt_content = """WEBVTT
Kind: captions
Language: en

00:00:00.120 --> 00:00:01.510 align:start position:0%
 if<00:00:00.240><c> we</c><00:00:00.359><c> talk</c><00:00:00.599><c> about</c><00:00:00.799><c> the</c><00:00:00.960><c> construction</c>

00:00:01.510 --> 00:00:01.520 align:start position:0%
if we talk about the construction
 
00:00:01.520 --> 00:00:03.750 align:start position:0%
if we talk about the construction
industry<00:00:02.159><c> one</c><00:00:02.399><c> name</c><00:00:02.679><c> rises</c><00:00:03.080><c> above</c><00:00:03.320><c> the</c><00:00:03.480><c> dust</c>

00:00:03.750 --> 00:00:05.000 align:start position:0%
industry one name rises above the dust
and<00:00:03.959><c> noise</c>
"""
        vtt_file_path_str = "___TEMP_SAMPLE___.vtt"
        with open(vtt_file_path_str, "w", encoding="utf-8") as f:
            f.write(sample_vtt_content)
        print(f"Using temporary sample VTT: {vtt_file_path_str}")


    app = QApplication(sys.argv)
    main_window = VTTPlayerApp(vtt_file_path_str)
    main_window.show()
    print("Application started. Close window to exit.")
    exit_code = app.exec_()
    if pathlib.Path("___TEMP_SAMPLE___.vtt").exists():
        os.remove("___TEMP_SAMPLE___.vtt") # Clean up temp file
    sys.exit(exit_code)
