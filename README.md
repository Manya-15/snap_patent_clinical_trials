# Patent and Clinical Trial Data Analysis

This project includes tools for analyzing patent data and linking it to clinical trials. It is divided into two main sections:

1. **Patent Data Analysis**
2. **Clinical Trial Matching and Search**

- For all the patent related files and flow refer to [patents.md](patents.md)
- For all the clinica trial search related files or patent-clinical matching files and flow refer to [clinical.md](clinical.md)

----------

## TO DO LIST FOR MANYA
### for patents
1. connect all the patent codes into 1 pipeline, use the set union logic for merging them.
2. in lens code, try fixing the embeddings for better ranking
3. pubchem code not robust, works sometimes sometimes not
4. EPO not returning claims sometimes, add serper(google patents) as a back fall.

### for clinical trials search
1. scrape opentarget to get more data
2. find lnk b/w chembl ids and drugs

### in patent-clinical matching
1. remove the sponsor depencence. change the logic to matching found set of patents to found set of trials
2. make 1 more endpoint with entry with the help of publication no instead of lens id of patent.
3. work on the flow decided with mr. neeraj and mr. aayush to find the pattern file structure.

### plus point to research on
1. scrap the drugbank to add data in both patents and clinical trials
2. study papers for merging drugs and patents
3. make this entire system into pipeline or a set of endpoints all connected
