in_vcf_path = "/home/iHiO10009/yuching/data/dbSNP"

import vcf

# list of chrom_pos  ex. NC_000001_pos
def dbSNPAnno(inFile, inVcfPath, outFile, inChrCol, inPosCol):
    print(inFile)
    f = open(inFile)
    fout = open(outFile, "w")
    lines = f.readlines()
    chrPosDict = {}
    chromList = []
    for line in lines:
        cols = line.strip("\n").split("\t")
        chrom = cols[inChrCol] #cols[0]
        if len(chrom) == 1:
            chrom = "NC_00000" + chrom
        elif len(chrom) == 2:
            chrom = "NC_0000" + chrom
        else:
            print(chrom)
            print("Please check if the chrom is right.")
        chromList.append(chrom)
        pos = cols[inPosCol] #cols[2]
        temp = chrom + "_" + pos
        chrPosDict[temp] = line.strip("\n")
    chromList = list(set(chromList))
    # chrom = NC_0000xx or NC_00000x
    for chrom in chromList:
        print(chrom)
        vcf_reader = vcf.Reader(open(inVcfPath + "/" + chrom + ".vcf"))
        count = 0
        for record in vcf_reader:
            count += 1
            if count % 5000000 ==0:
                print(count)
            chrom = record.CHROM.split(".")[0]
            pos = str(record.POS)
            vcf_temp = chrom + "_" + pos
            if vcf_temp in chrPosDict.keys():
                old_line = chrPosDict[vcf_temp]
                alt_str_list = []
                for alt_temp in record.ALT:
                    alt_str_list.append(str(alt_temp))
                fout.write(old_line + "\t" + chrom + "\t" + pos + "\t" + str(record.ID) + "\t" + str(record.REF) + "\t" + ",".join(alt_str_list) + "\t")
                if "GENEINFO" in record.INFO.keys():
                    fout.write(record.INFO["GENEINFO"] + "\t")
                else:
                    fout.write("\t")
                if "PSEUDOGENEINFO" in record.INFO.keys():
                    fout.write(record.INFO["PSEUDOGENEINFO"] + "\t")
                else:
                    fout.write("\t")
                if "CLNSIG" in record.INFO.keys():
                    cln_str_list = []
                    for cln_temp in record.INFO["CLNSIG"]:
                        cln_str_list.append(str(cln_temp))
                    fout.write(",".join(cln_str_list) + "\n")
                else:
                    fout.write("\n")
    fout.close()
    f.close()

in_file = "/home/iHiO10009/yuching/data/1.QC_GWAS_v3/impute2_keepFinalBCControls_updateSex_logistic_sigPvalues.txt"
out_file = "/home/iHiO10009/yuching/data/1.QC_GWAS_v3/impute2_keepFinalBCControls_updateSex_logistic_sigPvalues_annotated.txt"
dbSNPAnno(in_file, in_vcf_path , out_file, 0, 2)