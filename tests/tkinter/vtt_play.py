import tkinter as tk
import re
from datetime import datetime

class SubtitlePlayer:
	def __init__(self,f):
		self.root = tk.Tk()
		self.root.overrideredirect(True)
		self.root.wm_attributes("-topmost", True)
		self.root.attributes("-alpha", 0.8)
		self.root.config(bg='gray')
		
		self.label = tk.Label(self.root, font=("Arial", 20), fg="white", bg="gray")
		self.label.pack(padx=20, pady=10)
		
		self.drag_pos = (0, 0)
		self.label.bind("<Button-1>", self.start_drag)
		self.label.bind("<B1-Motion>", self.do_drag)
		
		self.root.geometry(f"+300+700")# 屏幕底部显示
		
		self.cues = []
		self.load_vtt(f)
		self.schedule_cue(0)

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
		with open(path, 'r') as f:
			raw = f.read()
			
		for block in re.findall(r"(\d+:\d+:\d+\.\d+).+?(\d+:\d+:\d+\.\d+)[\s\S]*?\n(.+?)(?=\n\n)", raw):
			start, end, text = block
			text = re.sub(r'<.*?>', '', text).replace('\n', ' ')
			self.cues.append((
				self.time_to_ms(start),
				self.time_to_ms(end),
				text.strip()
			))

	def schedule_cue(self, index):
		if index >= len(self.cues): return
		
		start, end, text = self.cues[index]
		delay = start - (self.cues[index-1][1] if index >0 else 0)
		
		self.root.after(delay, lambda: self.show_text(text))
		self.root.after(end - start, lambda: self.label.config(text=""))
		self.root.after(end - start, lambda: self.schedule_cue(index+1))

	def show_text(self, text):
		self.label.config(text=text)

	def run(self):
		self.root.mainloop()

if __name__ == "__main__":
	player = SubtitlePlayer(r'C:\test\youtube\The Entire History of Caterpillar Inc. [46_EC6teOqg].en.vtt')
	player.run()
