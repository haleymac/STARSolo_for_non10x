
import pandas as pd
import random 
import anndata as ad
from scipy.io import mmread
from scipy.sparse import csr_matrix




def add_barcode_quality_tag_to_sam(infile, outfile, barcode):
    """Add a CY:Z:]]]]]]]]] tag to sam file right after RG tag. Required for Starsolo use. F is best quality marker"""
    bamfile = infile
    outfile_path = outfile
    with open(bamfile, 'rt') as infile, open(outfile_path, 'wt') as outfile:
        lines = infile.readlines()
        for i, line in enumerate(lines):
            if line.startswith('@'):
                outfile.write(line)
            else:
                fields = line.split('\t')
                for i, field in enumerate(fields):
                    if field.startswith('RG:Z:'):
                        i = i

                # Find the index of the field containing 'RG:Z:'
                rg_index = next((i for i, field in enumerate(fields) if field.startswith('RG:Z:')), None)
                if rg_index is not None:
                    new_UMI = ''.join(random.choice("ATGC") for _ in range(10))
                    fields.insert(rg_index + 1, f'CR:Z:{barcode}')
                    fields.insert(rg_index + 2, 'CY:Z:FFFFFFFFFFFFFFFF')
                    fields.insert(rg_index + 3, f'CB:Z:{barcode}-1')
                    fields.insert(rg_index + 4, f'UR:Z:{new_UMI}')
                    fields.insert(rg_index + 5, 'UY:Z:FFFFFFFFFF')
                outfile.write('\t'.join(fields))


