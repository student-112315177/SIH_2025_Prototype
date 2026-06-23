import pandas as pd
from Bio.Blast import NCBIXML
from Bio.Blast import NCBIWWW
from Bio import SeqIO
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")

print("Starting online BLAST search. This may take several minutes...")

# 1. Read your ASVs from the FASTA file
fasta_path = os.path.join(DATA_DIR, "fasta", "ASVs.fasta")
try:
    fasta_string = open(fasta_path).read()
    print("Successfully read ASVs.fasta. Submitting to NCBI BLAST...")
except FileNotFoundError:
    print(f"Error: {fasta_path} not found. Make sure the DADA2 step ran successfully.")
    exit()

# 2. Run the BLAST search online using NCBI's servers
# program="blastn", database="nt" (nucleotide), sequence=your_sequences
result_handle = NCBIWWW.qblast(program="blastn", database="nt", sequence=fasta_string)

print("BLAST search completed. Now parsing the results...")

# 3. Parse the results and flag any sequence with < 90% identity as novel
blast_results = []
# The results come back in a special format called XML, which we now read
blast_records = NCBIXML.parse(result_handle)

for record in blast_records:
    query_id = record.query.split(" ")[0] # Get the ASV_X ID
    
    # Check if there are any matches at all
    if not record.alignments:
        blast_results.append({
            "qseqid": query_id,
            "pident": 0,
            "sseqid": "No Match Found",
            "novelty_flag": True
        })
        continue

    # Get the best alignment and its top hit (HSP)
    top_alignment = record.alignments[0]
    top_hsp = top_alignment.hsps[0]
    
    # Calculate the percent identity for the best match
    percent_identity = (top_hsp.identities / top_hsp.align_length) * 100
    
    # Check if it meets our novelty threshold
    is_novel = percent_identity < 90.0
    
    blast_results.append({
        "qseqid": query_id,
        "pident": round(percent_identity, 2),
        "sseqid": top_alignment.title,
        "novelty_flag": is_novel
    })

# 4. Save the final report to a CSV file
output_df = pd.DataFrame(blast_results)
output_df.to_csv(os.path.join(DATA_DIR, "labels", "novelty_report.csv"), index=False)

print("Novelty flagging complete! Your report has been saved to data/labels/novelty_report.csv")