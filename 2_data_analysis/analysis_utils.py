import pandas as pd
import scipy.stats as stats
import graphing_params as gp
import seaborn as sns

def draw_gene_pct_graph(df, ax, yoffset=8, clr='blue', alpha='E6'):
    clr = gp.get_color(clr)
    df['pct_of_all_genes'].plot.bar(stacked=True, ax=ax, width=0.9, color=clr, alpha=0.5, rot=0)
    gp.label_bars_vert(ax, [('%d%%' % round(n)) for n in df.pct_of_all_genes.values], yoffset, color=clr+alpha)
    gp.set_axis_props(ax, xlabel='', ylabel='% of passenger\ngenes', show_xticks=False)
    
def draw_paralog_pct_graph(df, ax, bg_genes, xlab='Samples with\ngene HD', clr='blue'):
    clr = gp.get_color(clr)
    for (tick, val) in zip(ax.get_xticks(), df['pct_paralog']):
        w=0.75; ax.plot([tick-w/2, tick+w/2], [val, val], lw=2, color=clr)
    gp.set_axis_props(ax, xlabel=xlab, ylabel='% paralogs')
    ax.axhline(sum(bg_genes.paralog)/bg_genes.shape[0]*100, linestyle='--', color='#000', lw=0.8)
    ax.set_ylim([50,90])

def draw_ess_paralog_pct_graph(df, ax, bg_genes, ess_col='depmap_ess', title=''):
    ax.set_xticks(ticks=[0,1,2]); ax.set_xticklabels(['0','1+','3+'])
    genes = bg_genes#.dropna(subset=[ess_col])
    for (tick, val) in zip(ax.get_xticks(), df['pct_ess_paralog']):
        w=0.75; ax.plot([tick-w/2, tick+w/2], [val, val], lw=2, color=gp.get_color('dark-orange'))
    ax.axhline(sum((genes[ess_col]==True)&(genes.paralog==True))/sum(genes.paralog)*100, 
               linestyle='--', color='#444')
    gp.set_axis_props(ax, ylabel='% paralogs that\nare essential', xlabel='Samples with\ngene HD', title=title)

    
def compute_bin(del_genes, b, n_del):
    if len(b)==1:
        df = del_genes[del_genes[n_del]==int(b)]
    elif b.endswith('+'):
        df = del_genes[del_genes[n_del]>=int(b[:-1])]
    else:
        df = del_genes[(del_genes[n_del]>=int(b.split('-')[0])) & (del_genes[n_del]<=int(b.split('-')[1]))]
    return df

def compute_del_proportions(del_genes, bins=['0','1+','3+'], ess_col='depmap_ess', n_del='n_del'):
    res = pd.DataFrame(columns=['pct_paralog','pct_ess_paralog','n_genes','pct_of_all_genes','n_paralogs','n_ess_paralogs'])
    for b in bins:
        df = compute_bin(del_genes, b, n_del)
        res.loc[b] = [sum(df.paralog)/df.shape[0]*100, 
                      sum(df.paralog & (df[ess_col]==True))/sum(df.paralog)*100,
                      df.shape[0], 
                      df.shape[0]/del_genes.shape[0]*100, 
                      sum(df.paralog),
                      sum(df.paralog & (df[ess_col]==True))]
    return res

def compute_del_FETs(df, bins=['0','1+','3+']):
    fet_res = pd.DataFrame(columns=['OR_par','pval_par','OR_ess','pval_ess'])
    # Comparing consecutive bins vs. comparing bin 0 vs. bin 1 and 2
    for i in range(1, len(bins)):
        b0 = bins[0]; b1 = bins[i]
        #             bin0   bin1
        # singleton |      |
        # paralog   |      |
        ctab = pd.DataFrame([[df.loc[b0].n_genes - df.loc[b0].n_paralogs, df.loc[b1].n_genes - df.loc[b1].n_paralogs],
                             [df.loc[b0].n_paralogs, df.loc[b1].n_paralogs]], index=['S','P'])
        #                   bin0   bin1
        # non-ess paralog |      |
        # ess paralog     |      |
        ctab2 = pd.DataFrame([[df.loc[b0].n_paralogs - df.loc[b0].n_ess_paralogs, df.loc[b1].n_paralogs - df.loc[b1].n_ess_paralogs],
                              [df.loc[b0].n_ess_paralogs, df.loc[b1].n_ess_paralogs]], index=['NEP','EP'])
        
        fet_res.loc[i] = stats.fisher_exact(ctab) + stats.fisher_exact(ctab2)
    
    return fet_res
