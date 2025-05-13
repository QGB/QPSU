'''

M.download('http://192.168.1.3/C%3A/QGB/babun/cygwin/bin/qgb/tests/micropython/noise_detect.py');d=M.r('noise_detect')

'''

import time, machine
def p(SAMPLE_RATE=0.001,interval=1000):
    NOISE_THRESHOLD = 4095  # 满量程阈值
    index = 0  # ADC引脚号

    # 初始化ADC
    adc = machine.ADC(machine.Pin(index))
    adc.atten(machine.ADC.ATTN_11DB)  # 3.3V量程

    # 统计变量
    peak_count = 0
    last_second = time.ticks_ms()//interval
    max_count=300
    while True:
        # 数据采集
        raw = adc.read()
        voltage = raw / 4095 * 3.3
        
        # 阈值判断
        if raw == NOISE_THRESHOLD:
            peak_count +=1
        
        
        # 时间窗口统计 :t=time.ticks_ms();v=a.read();print(f"{t//1000}.{t%1000:03d}
        t=time.ticks_ms()
        current_second = t//interval
        if current_second != last_second:
            if peak_count>max_count:max_count=peak_count
            noise_ratio = peak_count / max_count #(interval/SAMPLE_RATE) *100  # 计算百分比
            print(f"{t//1000}.{t%1000:03d} noise_detect: {noise_ratio:.2f}% ({peak_count}次)")
            peak_count = 0
            last_second = current_second
        
        time.sleep(SAMPLE_RATE)