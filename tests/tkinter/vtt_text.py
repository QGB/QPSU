#coding=utf-8
import sys,pathlib			   # .py/tkinter/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)
from qgb import py
U,T,N,F=py.importUTNF()

#coding=utf-8
import tkinter as tk
from tkinter import ttk
import re
import time
import threading

class VTTPlayer:
    def __init__(self, vtt_path):
        self.root = tk.Tk()
        self.root.title("VTT Player")
        self.root.geometry("800x600")
        self.root.attributes("-alpha", 0.85)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 高性能文本组件
        self.text_box = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 12),
                              bg='#333333', fg='white', insertbackground='white',
                              highlightthickness=0)
        vsb = ttk.Scrollbar(self.root, command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=vsb.set)
        
        # 布局优化
        self.text_box.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        
        # 控制面板
        self.btn_frame = ttk.Frame(self.root)
        self.play_btn = ttk.Button(self.btn_frame, text="▶", command=self.toggle_play)
        self.btn_frame.grid(row=1, column=0, pady=5, sticky="ew")
        self.play_btn.pack(side=tk.LEFT, padx=5)

        # 初始化数据
        self.cues = self.parse_vtt(vtt_path)
        self.playing = False
        self.start_time = 0
        self.last_pos = -1
        self.text_box.tag_config('highlight', background='yellow', foreground='black')
        self.load_text()
        
        # 窗口调整事件绑定
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """窗口调整大小时重置高亮位置"""
        if self.playing and self.last_pos != -1:
            s_idx = self.index_map[self.last_pos][2]
            self.text_box.see(s_idx)

    def parse_vtt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        cues = []
        pattern = re.compile(
            r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})(?:.*?\n)((?:.*\n)+?)(?=\n\d+:|$|\n\s*\n)"
        )
        for start, end, text in pattern.findall(raw):
            # 改进的文本清理逻辑
            text = re.sub(r'<\/?[^>]+>', '', text)  # 保留换行处理
            text = re.sub(r'\n+', ' ', text).strip()
            if text and text not in [c[2] for c in cues]:  # 去重
                cues.append((
                    self.time_to_ms(start),
                    self.time_to_ms(end),
                    text
                ))
        return sorted(cues, key=lambda x: x[0])

    def time_to_ms(self, t):
        h, m, s = t.split(':')
        s, ms = s.split('.')
        return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

    def load_text(self):
        self.text_box.delete('1.0', tk.END)
        full_text = []
        index_map = []
        pos = 0
        
        for idx, (start, end, text) in enumerate(self.cues):
            # 处理连续重复文本
            if idx > 0 and text.startswith(self.cues[idx-1][2]):
                display_text = text[len(self.cues[idx-1][2]):].strip()
            else:
                display_text = text
                
            if display_text:
                start_idx = f"1.0 + {pos} chars"
                pos += len(display_text)
                end_idx = f"1.0 + {pos} chars"
                index_map.append( (start, end, start_idx, end_idx) )
                full_text.append(display_text)
                pos += 1  # 添加空格
        
        self.text_box.insert('1.0', ' '.join(full_text))
        self.index_map = index_map

    def toggle_play(self):
        self.playing = not self.playing
        if self.playing:
            self.start_time = time.time() * 1000
            threading.Thread(target=self.update_highlight, daemon=True).start()

    def update_highlight(self):
        while self.playing:
            current_time = time.time() * 1000 - self.start_time
            
            # 二分查找当前时间段
            low, high = 0, len(self.index_map)-1
            best_match = -1
            while low <= high and self.playing:
                mid = (low + high) // 2
                s, e, _, _ = self.index_map[mid]
                if s <= current_time <= e:
                    best_match = mid
                    break
                elif current_time < s:
                    high = mid - 1
                else:
                    low = mid + 1
            
            if best_match != -1 and best_match != self.last_pos:
                self.root.after(0, self._update_ui, best_match)
                self.last_pos = best_match
            
            time.sleep(0.05)  # 降低CPU占用

    def _update_ui(self, index):
        """UI更新主线程操作"""
        self.text_box.tag_remove('highlight', '1.0', 'end')
        s_idx = self.index_map[index][2]
        e_idx = self.index_map[index][3]
        self.text_box.tag_add('highlight', s_idx, e_idx)
        self.text_box.see(s_idx)

if __name__ == "__main__":
    N.rpcServer(globals=globals(),locals=locals(),port=U.pid)
    player = VTTPlayer(r'C:\test\youtube\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt')
    player.root.mainloop()


'''参考样本
WEBVTT
Kind: captions
Language: en

00:00:00.120 --> 00:00:01.510 align:start position:0%
 
if<00:00:00.240><c> we</c><00:00:00.359><c> talk</c><00:00:00.599><c> about</c><00:00:00.799><c> the</c><00:00:00.960><c> construction</c>

00:00:01.510 --> 00:00:01.520 align:start position:0%
if we talk about the construction
 

00:00:01.520 --> 00:00:03.750 align:start position:0%
if we talk about the construction
industry<00:00:02.159><c> one</c><00:00:02.399><c> name</c><00:00:02.679><c> rises</c><00:00:03.080><c> above</c><00:00:03.320><c> the</c><00:00:03.480><c> dust</c>

00:00:03.750 --> 00:00:03.760 align:start position:0%
industry one name rises above the dust
 

00:00:03.760 --> 00:00:06.630 align:start position:0%
industry one name rises above the dust
and<00:00:03.959><c> noise</c><00:00:04.640><c> caterpillar</c><00:00:05.240><c> Inc</c><00:00:05.960><c> this</c><00:00:06.160><c> industry</c>

00:00:06.630 --> 00:00:06.640 align:start position:0%
and noise caterpillar Inc this industry
 

00:00:06.640 --> 00:00:08.990 align:start position:0%
and noise caterpillar Inc this industry
Titan<00:00:07.200><c> has</c><00:00:07.359><c> not</c><00:00:07.520><c> only</c><00:00:07.720><c> Built</c><00:00:08.080><c> machines</c><00:00:08.800><c> but</c>

00:00:08.990 --> 00:00:09.000 align:start position:0%
Titan has not only Built machines but
 

00:00:09.000 --> 00:00:10.910 align:start position:0%
Titan has not only Built machines but
also<00:00:09.280><c> carved</c><00:00:09.599><c> a</c><00:00:09.760><c> legacy</c><00:00:10.240><c> into</c><00:00:10.480><c> the</c><00:00:10.639><c> very</c>

'''     
