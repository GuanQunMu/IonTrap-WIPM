# 示例：循环生成波形
GAmp = 200;

ul = 1000
f = 140;
w0 = WAVE([0]);
tmp = []
for i in range(3):
    _w = Sin(f, L=ul*(i+1))
    tmp.append(_w(1,T))
    tmp.append(w0(ul,C))
    
s1 = SEQ(tmp);

OUT1 = s1;
OUT2 = s1;
