import re
import glob
import os
import numpy as np
import copy
from pytopdrawer.topplot import Join, TopPlot
import re
from smpl import plot
import pandas as pd
import matplotlib.pyplot as plt
from uncertainties import unumpy

def read(topfile,powheg=True,mcfm=False):
	if powheg:
		return read_powheg(topfile,powheg)
	elif mcfm:
		return read_mcfm(topfile,mcfm)

def read_mcfm(topdir,mcfm=True,draw=False):
	# TODO output param
	if os.path.exists('mcfm.yoda'):
		os.remove('mcfm.yoda')
	for topfile in glob.glob(topdir + '/*.txt'):
		if not "TeV_" in topfile:
			continue
		df = pd.read_csv(topfile,sep=r'\s+',skiprows=5,header=None)
		df.columns = ['xlow','xhigh','sumw','sumw2sq']
		# 1000 to pb and divide by bin width
		df["sumw"] = df["sumw"]/1000
		df["sumw2sq"] = df["sumw2sq"]/1000
		df["sumw2"] = df["sumw2sq"]**2
		print(df)
		print(df["sumw"].sum())
		if draw:
			plot.data((df["xhigh"]+df['xlow'])/2,unumpy.uarray(df["sumw"],df["sumw2sq"])/(df["xhigh"]-df["xlow"]),logy=True)
			plot.show()

		type = topfile.replace('.txt','').split('TeV_')[-1].replace('_','')

		f = open("mcfm.yoda", "a")
		f.write("BEGIN YODA_HISTO1D_V2 /ALICE_2022_FSP/" + type + "\nPath: /ALICE_2022_FSP/" + type + "\nTitle: \nType: \"Histo1D\"\n---\n")
		f.close()
		df.astype(float).round(7).to_csv("mcfm.yoda",sep=' ',mode='a',header=False,index=False,columns=['xlow','xhigh','sumw','sumw2'])
		f = open("mcfm.yoda", "a")
		f.write("END YODA_HISTO1D_V2\n\n")
		f.close()
	return []



def read_powheg(topfile,powheg=True):
	topplots = []
	cur = TopPlot()
	cur_data = []
	lim = re.compile(r'set\s+limits\s+x\s+([0-9\.E\+-]+)\s+([0-9\.E\+-]+)\s+y\s+([0-9\.E\+-]+)\s+([0-9\.E\+-]+)')
	title = re.compile(r'title\s+(\w+)\s+"(.*)"')
	data = re.compile(r'([0-9\.Ee\+-]+)\s+([0-9\.Ee\+-]+)')
	join = re.compile(r'join')
	newplot = re.compile('newplot')
	with open(topfile) as topo_file:
		for line in topo_file:
			g = lim.search(line)
			if g is not None:
				cur.limits.xmin = float(g.group(1))
				cur.limits.xmax = float(g.group(2))
				cur.limits.ymin = float(g.group(3))
				cur.limits.ymax = float(g.group(4))
			g = title.search(line)
			if g is not None:
				cur.title.position = g.group(1)
				cur.title.text = g.group(2)
			g = data.search(line)
			if g is not None:
				cur_data.append([float( g.group(1)) ,float( g.group(2)) ])
			g = join.search(line)
			if g is not None:
				if len(cur_data) == 2:
					j = Join(cur_data[0][0],cur_data[0][1],cur_data[1][0],cur_data[1][1])
					cur.joins.append(j)
				else:
					cur.data = cur_data
				cur_data = []
			g = newplot.search(line)
			if g is not None:
				if powheg:
					cur.joins.append(Join(0,0,1,0))
					cur.joins.append(Join(0,0,0,1))
					cur._doskip(1)
				topplots.append(copy.deepcopy(cur))
				cur_data = []
				cur = TopPlot()
	return topplots


