#coding=utf-8
import sys,pathlib			   # .py/tkinter/test  /qgb   / 
gsqp=pathlib.Path(__file__).absolute().parent.parent.parent.parent.absolute().__str__()
if gsqp not in sys.path:sys.path.append(gsqp)#py3 works
from qgb import py
U,T,N,F=py.importUTNF()

import tkinter as tk
import re

class SubtitlePlayer:
	def __init__(self, f):
		self.root = tk.Tk()
		self.root.overrideredirect(True)
		self.root.wm_attributes("-topmost", True)
		self.root.attributes("-alpha", 0.8)
		self.root.config(bg='gray')
		
		self.labels = [tk.Label(self.root, font=("Arial", 16), fg="white", bg="gray") 
					  for _ in range(5)]
		for lbl in self.labels:
			lbl.pack(pady=2, anchor='w')
		
		self.drag_pos = (0, 0)
		self.root.bind("<Button-1>", self.start_drag)
		self.root.bind("<B1-Motion>", self.do_drag)
		
		self.cues = []
		self.active_subs = []
		self.load_vtt(f)
		
		for start, end, text in self.cues:
			self.root.after(start, lambda t=text: self.add_sub(t))
			self.root.after(end, lambda t=text: self.remove_sub(t))

	def start_drag(self, event): 
		self.drag_pos = (event.x, event.y)

	def do_drag(self, event):
		dx = event.x - self.drag_pos[0]
		dy = event.y - self.drag_pos[1]
		self.root.geometry(f"+{self.root.winfo_x()+dx}+{self.root.winfo_y()+dy}")

	def time_to_ms(self, t):
		h, m, s = map(float, t.split(':'))
		return int((h*3600 + m*60 + s) * 1000)

	def load_vtt(self, path):
		with open(path, 'r', encoding='utf-8') as f:
			raw = f.read()
			
		pattern = r"(\d+:\d+:\d+\.\d+)\s*-->\s*(\d+:\d+:\d+\.\d+).*?\n((?:.*\n)*?)(?=\n\d|$)"
		for start, end, text in re.findall(pattern, raw):
			text = re.sub(r'<.*?>', '', text).replace('\n', ' ').strip()
			if text:
				self.cues.append((
					self.time_to_ms(start),
					self.time_to_ms(end),
					text
				))

	def add_sub(self, text):
		if len(self.active_subs) >= 5:
			self.active_subs.pop(0)
		self.active_subs.append(text)
		self.update_display()

	def remove_sub(self, text):
		if text in self.active_subs:
			self.active_subs.remove(text)
		self.update_display()

	def update_display(self):
		for i, lbl in enumerate(self.labels):
			lbl.config(text=self.active_subs[i] if i < len(self.active_subs) else "")

	def run(self):
		self.root.mainloop()

def merge_subtitles(cues):
	merged = []
	current_text = ''
	last_end = 0

	for start, end, text in cues:
		# 寻找最大重叠（逆向检测提高效率）
		max_overlap = 0
		max_possible = min(len(current_text), len(text))
		for overlap in range(max_possible, 0, -1):
			if current_text.endswith(text[:overlap].rstrip()):  # 忽略末尾空格
				max_overlap = overlap
				break
		
		# 智能处理标点衔接
		new_part = text[max_overlap:].lstrip()  # 去除前导空格
		if current_text and new_part and not current_text[-1].isspace():
			new_part = ' ' + new_part

		if new_part:
			# 记录有效时间段（取最晚开始时间）
			actual_start = max(start, last_end)
			merged.append((actual_start, end, new_part))
			current_text += (' ' if current_text else '') + new_part
			last_end = end

	# 生成最终完整文本
	full_text = ' '.join([t for _, _, t in merged])
	return full_text


if __name__ == "__main__":
	N.rpcServer(globals=globals(),locals=locals(),port=U.pid)
	# 使用示例
	# merged = merge_subtitles(player.cues)
	# for segment in merged:
		# print(segment[2])  # 打印合并后的文本段落

	# final_text = ' '.join([t for _, _, t in merged])

	
	player = SubtitlePlayer(r'C:\test\youtube\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt')
	player.run()
