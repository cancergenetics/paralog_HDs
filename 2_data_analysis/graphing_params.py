import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D

# svg.fonttype:
# 'none': Assume fonts are installed on the machine where the SVG will be viewed.
# 'path': Embed characters as paths -- supported by most SVG renderers

mpl.rcParams.update({
    'svg.fonttype':'none', 
    'font.family':'Arial',
    'text.usetex': False,
    'axes.spines.top': False,
    'axes.spines.right': False, 
    'axes.axisbelow': True,
    'axes.linewidth':0.8,
    'font.size':9,
    'axes.labelsize':9,
    'legend.fontsize':9,
    'xtick.labelsize':8,
    'ytick.labelsize':8,
    'lines.linewidth':1,
    'figure.dpi': 100,
    'grid.color': '#dddddd',
    'figure.facecolor':'white',
    'legend.edgecolor': '1',
    'legend.facecolor':'#FFFFFF',
    'legend.frameon':True,
    'legend.framealpha': 0.9,
})

# From: okabe-ito from http://jfly.iam.u-tokyo.ac.jp/color/#pallet
def get_palette(name="okabe-ito"):
    if name=="okabe-ito":
        return [get_color(x) for x in ['sky-blue', 'orange', 'green', 'yellow', 'blue', 'dark-orange', 'pink']]
    if name=="okabe-ito-2":
        return [get_color(x) for x in ['sky-blue', 'orange', 'yellow', 'green']]
    if name=="oi-2":
        return [get_color(x) for x in ['sky-blue', 'orange', 'yellow', 'green']]
    if name=="okabe-ito-3":
        return [get_color(x) for x in ['orange', 'sky-blue', 'green']]
    if name=="ess-cats":
        return [get_color(x) for x in ['blue', 'light-grey', 'dark-orange']]
    if name=="ess":
        return [get_color(x) for x in ['light-grey', 'dark-orange']]
    if name=="paralog":
        return [get_color(x) for x in ['yellow','sky-blue']]
    if name=="p":
        return [get_color(x) for x in ['yellow','sky-blue']]
    if name=="p2":
        return [get_color(x) for x in ['sky-blue','yellow']]
    if name=='WGD':
        return [get_color(x) for x in ['green','orange']]
    if name=='blues':
        return [get_color(x) for x in ['blue','sky-blue']]
    if name=='oranges':
        return [get_color(x) for x in ['dark-orange','orange']]
    if name=='oranges3':
        return ['#FF8423','#d55e00','#A24700']
    
def get_pal(name="okabe-ito"):
    return get_palette(name)
        
def get_color(name='light-grey', alpha=''):
    if name.startswith('#'): return name;
    return {
        'sky-blue':'#56b4e9',
        'orange':'#e69f00',
        'green':'#009e73',
        'dark-yellow':'#d3c511',
        'yellow':'#f0e442',
        'blue':'#0072b2',
        'dark-orange':'#d55e00',
        'do':'#d55e00',
        'pink':'#cc79a7',
        'light-grey':'#cccccc',
        'grey':'#666',
        'black':'#000'
    }[name]+alpha

def draw_legend(ax, colors, labels, lw=None, styles=None, marker=None, bbox_to_anchor=(1,1)):
    if lw==None:
        lw = [1 for n in range(0,len(labels))]
    if styles==None:
        styles = ['-' for n in range(0,len(labels))]
    if marker!=None:
        custom_lines = [Line2D([0],[0], color=colors[n], marker=marker, linestyle='None') for n in range(0,len(labels))]
    else:
        custom_lines = [Line2D([0],[0], color=colors[n], linestyle=styles[n], lw=lw[n]) for n in range(0,len(labels))]
    ax.legend(custom_lines, labels, bbox_to_anchor=bbox_to_anchor)


def set_axis_props(ax, **kwargs): 
    xlab = kwargs.get('xlabel', None)
    xfontsize = kwargs.get('xlabel_fontsize', mpl.rcParams['axes.labelsize'])
    if xlab != None:
        ax.set_xlabel(xlab, fontsize=xfontsize)
        
    ylab = kwargs.get('ylabel', None)
    yfontsize = kwargs.get('ylabel_fontsize', mpl.rcParams['axes.labelsize'])
    if ylab != None:
        ax.set_ylabel(ylab, fontsize=yfontsize)
    
    title = kwargs.get('title', None)
    titlefontsize = kwargs.get('titlefontsize', mpl.rcParams['axes.labelsize'])
    if title != None:
        ax.set_title(title, fontsize=titlefontsize)
    
    show_xticks = kwargs.get('show_xticks', True)
    if show_xticks==False:
        ax.tick_params(axis='x', which='both', length=0)
    
    show_yticks = kwargs.get('show_yticks', True)
    if show_yticks==False:
        ax.tick_params(axis='y', which='both', length=0)
        
    show_yticklabels = kwargs.get('show_yticklabels', True)
    if show_yticklabels==False:
        ax.get_yaxis().set_ticks([])
        
    show_xticklabels = kwargs.get('show_xticklabels', True)
    if show_xticklabels==False:
        ax.get_xaxis().set_ticks([])
        
    xtick_fontsize = kwargs.get('xtick_fontsize', mpl.rcParams['xtick.labelsize'])
    ax.tick_params(axis='x', which='both', labelsize=xtick_fontsize)
    
    ytick_fontsize = kwargs.get('ytick_fontsize', mpl.rcParams['ytick.labelsize'])
    ax.tick_params(axis='y', which='both', labelsize=ytick_fontsize)

    show_xaxis = kwargs.get('show_xaxis', True)
    if show_xaxis==False:
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', length=0)
    
    show_yaxis = kwargs.get('show_yaxis', True)
    if show_yaxis==False:
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='y', which='both', length=0)
        
    show_top_spine = kwargs.get('show_top_spine', False)
    if show_top_spine==True:
        ax.spines['top'].set_visible(True)

    show_right_spine = kwargs.get('show_right_spine', False)
    if show_right_spine==True:
        ax.spines['right'].set_visible(True)
        
    show_legend = kwargs.get('show_legend', True)
    if show_legend==False:
        ax.legend().remove()
      
    xticklabs = kwargs.get('xticklabels', None)
    if xticklabs != None:
        ax.set_xticklabels(xticklabs, fontsize=xfontsize) 
        
    yticklabs = kwargs.get('yticklabels', None)
    if yticklabs != None:
        ax.set_yticklabels(yticklabs, fontsize=yfontsize) 
        
        
def get_boxplot_props():
    return {'saturation':0.9, 'showcaps':False,
            'boxprops':dict(edgecolor='#333'), 'whiskerprops':dict(color='#333'), 
            'medianprops':dict(linewidth=1, color='#000'), 'capprops':dict(color='#333'),
            'flierprops':dict(marker='o', markerfacecolor='#aaa', markeredgecolor='#aaa', markersize=2, alpha=0.2),
            'meanprops':dict(marker='o', markersize=2, markeredgecolor='#444', markerfacecolor='#444')}

def label_bars(ax, labels, xoffset, color='k'):
    for rect, label in zip(ax.patches, labels):
        xoff = rect.get_width()-xoffset
        ax.text(rect.get_x()+xoff, rect.get_y()+rect.get_height()/2-0.05, label, ha='right', va='center', color=color)
        
def label_bars_vert(ax, labels, yoffset, color='k'):
    for rect, label in zip(ax.patches, labels):
        yoff = rect.get_height()+yoffset
        ax.text(rect.get_x()+rect.get_width()/2, rect.get_y()+yoff, label, ha='center', va='top', fontsize=8, color=color)
        
def draw_signif_FET(x1, x2, y1, y2, OR, pval, ax, yoffset=3, fraction=0.2, color='#666', alpha='80'):
    ax.text(x1+(x2-x1)*0.5, y1+yoffset, 'OR=%.2f%s'% (OR, ('*' if pval<0.05 else ' ')), fontsize=8, color=color, ha='center')
    ax.annotate("", xy=(x1, y1), xycoords='data', xytext=(x2, y2), 
                arrowprops=dict(lw=1, connectionstyle="bar,angle=180,fraction="+str(fraction/(x2-x1)), arrowstyle="-", color=color+alpha)) 
    
def draw_signif_MW(x1, x2, y1, pval, ax, yoffset=0, fraction=0.2, color='#666', star=False):
    if star:
        ax.text(x1+(x2-x1)*0.5, y1+yoffset, '%s' % ('*' if pval<0.05 else ' '), fontsize=8, color=color, ha='center')
        ax.annotate("", xy=(x1, y1), xycoords='data', xytext=(x2, y1), 
                    arrowprops=dict(lw=1, connectionstyle="bar,angle=180,fraction="+str(fraction/(x2-x1)), arrowstyle="-", color=color),
                    annotation_clip=False)
        return
    if pval>0.05:
        ax.text(x1+(x2-x1)*0.5, y1+yoffset, '$\it{p}$=%.2f'% (pval), fontsize=8, color=color, ha='center')
    elif pval<0.05 and pval>=0.001:
        ax.text(x1+(x2-x1)*0.5, y1+yoffset, '$\it{p}$=%.3f'% (pval), fontsize=8, color=color, ha='center')
    elif pval<1e-16:
        ax.text(x1+(x2-x1)*0.5, y1+yoffset, '$\it{p}$<1e-16', fontsize=8, color=color, ha='center')
    else:
        ax.text(x1+(x2-x1)*0.5, y1+yoffset, '$\it{p}$=%.e'% (pval), fontsize=8, color=color, ha='center')
        
    
def draw_signif_MW_w_CLES(x1, x2, y1, pval, cles, ax, yoffset=0, fraction=0.2, color='#666'):
    ax.text(x1+(x2-x1)*0.5, y1+yoffset, 'CLES=%.2f%s' % (cles, ('*' if pval<0.05 else ' ')), fontsize=8, color=color, ha='center')
    ax.annotate("", xy=(x1, y1), xycoords='data', xytext=(x2, y1), 
                arrowprops=dict(lw=1, connectionstyle="bar,angle=180,fraction="+str(fraction/(x2-x1)), arrowstyle="-", color=color),
                annotation_clip=False)
        