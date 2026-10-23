from pathlib import Path
import json, math

def rgb(s): return [int(s[i:i+2],16)/255 for i in (1,3,5)]
def lum(s):
 c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb(s)]
 return sum(v*w for v,w in zip(c,[.2126,.7152,.0722]))
def contrast(a,b):
 x,y=sorted([lum(a),lum(b)])
 return (y+.05)/(x+.05)
def blend(a,b,alpha):
 return '#'+''.join(f'{round(x*255*alpha+y*255*(1-alpha)):02x}' for x,y in zip(rgb(a),rgb(b)))
rows=[]
for case,pairs in {
 'case-1-rea': [('Tinta claro', '#0e0e0d','#f4f4f0',4.5),('Atenuado claro','#65655f','#f4f4f0',4.5),('Tinta oscuro','#edede7','#0b0b0c',4.5),('Atenuado oscuro','#8b8b85','#0b0b0c',4.5),('Iniciales claro','#0e0e0d','#ecece6',4.5),('Iniciales oscuro','#edede7','#151517',4.5),('Botón claro','#f4f4f0','#0e0e0d',4.5),('Botón oscuro','#0b0b0c','#edede7',4.5),('Contorno select claro',blend('#0e0e0d','#f4f4f0',.5),'#f4f4f0',3),('Contorno select oscuro',blend('#edede7','#0b0b0c',.45),'#0b0b0c',3),('Foco tinta claro','#0e0e0d','#f4f4f0',3),('Foco tinta oscuro','#edede7','#0b0b0c',3)],
 'case-2-generic': [('Texto','#142923','#ffffff',4.5),('Texto sobre papel','#142923','#f4f6f2',4.5),('Texto atenuado','#53655e','#ffffff',4.5),('Atenuado sobre papel','#53655e','#f4f6f2',4.5),('Rol / acción','#164a36','#ffffff',4.5),('Rótulo sintético','#164a36','#deeadf',4.5),('Especialidades','#142923','#f4f6f2',4.5),('Borde botón','#53655e','#ffffff',3),('Foco','#164a36','#ffffff',3)]
}.items():
 result=[]
 for label,fg,bg,t in pairs:
  ratio=contrast(fg,bg); result.append({'label':label,'foreground':fg,'background':bg,'ratio':round(ratio,4),'threshold':t,'status':'PASS' if ratio>=t else 'FAIL'})
 out={'method':'WCAG sRGB luminance formula, opaque pairs; alpha border composited then rounded to 8-bit sRGB','coverage':'Declared color pairs only. All three REA accents share these text/background pairs; decorative accent rule excluded. Native select popup and selection highlight excluded. Does not establish global accessibility or browser rendering.','results':result}
 (Path(__file__).resolve().parent/Path(case)/'checks'/'contrast.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 rows.append({'case':case,'pairs':len(result),'failures':[r for r in result if r['status']=='FAIL']})
print(json.dumps(rows,ensure_ascii=False,indent=2))
raise SystemExit(1 if any(row['failures'] for row in rows) else 0)
