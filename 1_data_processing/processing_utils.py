import pandas as pd
import itertools
import re
import scipy.stats as stats

# Load start and end of longest transcript for each gene
def load_ccds(file_ccds):
    ccds_full = pd.read_csv(file_ccds, sep='\t')
    # Only use entries with ccds_status == Public
    ccds_full = ccds_full[ccds_full.ccds_status == 'Public']
    assert(ccds_full[ccds_full.match_type!='Identical'].shape[0]==0)
    ccds_full = ccds_full.drop(columns=['ccds_status','match_type'])
    ccds_full = ccds_full.rename(columns={'#chromosome':'chr','gene_id':'entrez_id'}).astype({'cds_from':'int', 'cds_to':'int'})
    # Check that start is always lower value than end
    assert(ccds_full[ccds_full.cds_from > ccds_full.cds_to].shape[0]==0)
    # Look at full coding range for all transcripts, ignoring individual exons (in cds_locations columns)
    ccds = ccds_full[['chr','entrez_id','cds_from','cds_to','ccds_id']].drop_duplicates()
    # Keep longest transcript per gene only
    ccds = ccds.assign(cds_len = ccds.apply(lambda x: x.cds_to - x.cds_from, axis=1))
    ccds = ccds.sort_values(['entrez_id','cds_len'], ascending=True).drop_duplicates(subset=['entrez_id'], keep='last')
    ccds = ccds.sort_values(['chr','cds_from']).reset_index(drop=True).astype({'entrez_id':'int'})
    return ccds


# Four scenarios for partial/full overlap of segment and gene:
# 1 seg: ----##########-----
# 1 gene:      XXXX
# 2 seg: ----##########-----
# 2 gene:  XXXX
# 3 seg: ----##########-----
# 3 gene:           XXXX
# 4 seg: ----######-----
# 4 gene:  XXXXXXXXXX

def map_segment_partial(segment, df, percent):
    genes = df[((df.cds_from >= segment.startpos) & (df.cds_from <= segment.endpos)) | # gene start within segment
               ((df.cds_to   >= segment.startpos) & (df.cds_to   <= segment.endpos)) | # gene end within segment
               ((df.cds_from <= segment.startpos) & (df.cds_to   >= segment.endpos))]  # gene fully overlaps segment
    if genes.shape[0]==0: return []
    if percent==0: return list(genes.entrez_id)
    genes = genes.assign(overlap = genes.apply(
                          lambda x: len(range(max(x.cds_from, segment.startpos), min(x.cds_to, segment.endpos))), axis=1))
    return list(genes[genes.overlap >= percent*genes.cds_len].entrez_id)

def map_segment_full(segment, df, percent):
    genes = df[((df.cds_from >= segment.startpos) & (df.cds_from <= segment.endpos)) & # gene starts within segment AND
               ((df.cds_to   >= segment.startpos) & (df.cds_to   <= segment.endpos))]  # gene ends within segment
    return list(genes.entrez_id)

def get_overlap_length(x):
    return len(range(max(x.cds_from, x.startpos), min(x.cds_to, x.endpos)))

# segments df should have columns: chr, startpos, endpos
def map_segments_to_genes(segments, ccds, overlap_func, percent=0):
    segments = segments.assign(genes='')
    # Process one chromosome at a time
    for ch in [i for i in range(1, 25)]:
        df = ccds[ccds['chr']==ch]
        segments.loc[segments['chr']==ch, 'genes'] = segments.loc[segments['chr']==ch,:].apply(
            lambda x: overlap_func(x, df, percent), axis=1)
    return segments

# Each gene would only be deleted/amplified once per sample (no overlapping deletions b/c data is segments)
# so just count # of occurences in the list
def count_dels_per_gene(mapped_segments, bg_genes):
    glist = list(itertools.chain.from_iterable(mapped_segments.genes.values))
    df = pd.DataFrame(pd.Series(glist).value_counts(), columns=['n_sample']).reset_index()
    df =  df.rename(columns={'index':'entrez_id','n_sample':'n_del'})
    gene_dels = pd.merge(df, bg_genes, how='right').fillna({'n_del':0})
    return gene_dels

def count_dels_per_sample(mapped_segments, col):
    del_per_sample = mapped_segments.groupby([col]).apply(lambda x: len(list(itertools.chain.from_iterable(x.genes.values))))
    return del_per_sample.reset_index(name='n_genes').reset_index(drop=True)

def serialize_map(hd_map, fname):
    df = hd_map.assign(genes = hd_map.genes.apply(lambda x: ','.join(map(str, x)) if len(x)>0 else "-"))
    df = df.astype({'genes':str})
    df.to_csv(fname, index=0)

def deserialize_map(fname):
    hd_map = pd.read_csv(fname).astype({'genes':str})
    hd_map = hd_map.assign(genes = hd_map.genes.apply(lambda x: [int(n) for n in x.split(',')] if x!="-" else []))
    return hd_map


