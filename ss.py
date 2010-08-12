from pygame import init, FULLSCREEN,HWSURFACE,DOUBLEBUF,KEYDOWN,K_ESCAPE,K_SPACE
from pygame.display import set_mode,get_surface,flip
from pygame.image import load as iload
from pygame.transform import smoothscale
from pygame.time import Clock
from pygame.event import get as eget
from pygame.mouse import set_visible

from os import listdir,access,F_OK
from time import sleep
from random import Random

init()

set_mode((0,0),FULLSCREEN|HWSURFACE|DOUBLEBUF)
#set_mode((640,480),HWSURFACE)

set_visible(False)

s=get_surface()

def fit(w,h,ww,hh):
	a=ww/float(w)
	w1=ww; h1=h*a
	if h1<=hh:
		return w1,h1

	return w*(hh/float(h)),hh

def center(w,h,ww,hh):
	return (ww-w)/2,(hh-h)/2

def getseed(d):
	try:
		open(d+'/random').close()
		return Random().random()
	except: return None

def photo(i,p,x,y,px,py):
	c=Clock()
	for t in range(0,101):
		for e in eget():
			if e.type==KEYDOWN:
				if e.key==K_ESCAPE: return
				else: return e.unicode
		s.fill((0,0,0))
		a=int((t/100.0)*255)
		if p and t!=100:
			p.set_alpha(255-a)
			s.blit(p,(px,py))
		i.set_alpha(a)
		s.blit(i,(x,y))
		c.tick(50)
		flip()
	for t in range(0,20):
		for e in eget():
			if e.type==KEYDOWN:
				if e.key==K_ESCAPE: return
				else: return e.unicode
		c.tick(10)
	return ' '

def slide(d):
	p=None; px=0; py=0
	li=[x for x in listdir(d) if x[-4:].lower()=='.jpg']

	seed=getseed(d)
	if seed: Random(seed).shuffle(li)
	else: li.sort()

	while True:
		for x in li:
			i=iload(d+'/'+x)
			w,h=fit(*(i.get_size()+s.get_size()))
			i=smoothscale(i,(int(w),int(h)))
			i=i.convert(s)

			(x,y)=center(*(w,h)+s.get_size())

			c=photo(i,p,x,y,px,py)
			if c!=' ': return c

			p=i; px=x; py=y


d='1'
while d:
	try: d=slide(d)
	except OSError,e:
		d='n'

set_visible(True)

