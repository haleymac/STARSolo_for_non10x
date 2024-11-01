"""This script makes an H5ad anndata object from a STARSolo count matrix. Output from this function can be fed seamlessly into a Scanpy workflow"""

"""
Example useage:
python make_h5ad.py --solo_indir /path/to/STARSolo/output/directory --cell_barcodes_csv /path/to/barcodecsv/output/by/starsolo/snakefile --h5ad output/h5ad/file
"""



from scipy.io import mmread
from scipy.sparse import csr_matrix
import pandas as pd
import anndata as ad
import argparse


parser = argparse.ArgumentParser(description='Make h5ad from STARSolo count matrices')
parser.add_argument('--solo_indir', default=True, help='.Solo.out directory output by starsolo workflow')
parser.add_argument('--cell_barcodes_csv',type=str, required=True,help='Csv linking cell barcodes to cell identifiers (helpful if not 10x library)')
parser.add_argument('--h5ad',type=int, required=True,help='outpath for h5ad file')
args = parser.parse_args()


solo_indir = args.solo_indir
cell_barcodes_csv = args.cell_barcodes_csv
h5ad = args.h5ad


def make_h5ad_from_count_matrices(solo_indir, cell_barcodes_csv, h5ad):
    all_counts = f'{solo_indir}/Gene/filtered/matrix.mtx'
    spliced_counts = f'{solo_indir}/Velocyto/filtered/spliced.mtx'
    unspliced_counts = f'{solo_indir}/Velocyto/filtered/unspliced.mtx'
    solo_features_tsv = f'{solo_indir}/Velocyto/filtered/features.tsv'
    solo_barcodes_tsv = f'{solo_indir}/Velocyto/filtered/barcodes.tsv'
    
    barcodes =  pd.read_csv(solo_barcodes_tsv, sep = '\t', names=['barcode'])
    id_df = pd.read_csv(cell_barcodes_csv)
    barcodes = barcodes.merge(id_df, how = 'left', on = 'barcode')
    barcodes = list(barcodes.cell_id)
    
    features = pd.read_csv(solo_features_tsv, sep = '\t', names = ['ensembl_id', 'gene_name', 'expression'])
    gene_ids = list(features.gene_name)
    ensemble_ids = list(features.ensembl_id)
    
    all_matrix = mmread(all_counts)
    all_matrix = csr_matrix(all_matrix)
    adata = ad.AnnData(all_matrix.T)
    adata.obs_names = barcodes
    adata.var_names = gene_ids
    adata.var['ensemble_id'] = ensemble_ids

    spliced_matrix = mmread(spliced_counts).T
    spliced_matrix = csr_matrix(spliced_matrix)
    adata.layers["spliced"] = spliced_matrix

    unspliced_matrix = mmread(unspliced_counts).T
    unspliced_matrix = csr_matrix(unspliced_matrix)
    adata.layers["unspliced"] = unspliced_matrix

    adata.write_h5ad(filename=h5ad_path)
