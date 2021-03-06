// Generated by https://quicktype.io

export interface Drug {
  mir_drug_list: DrugRecord[];
  records_num: number;
}

export interface DrugRecord {
  FDA: string;
  Method: string;
  Reference: string;
  CID: string;
  miRBase: string;
  Small_molecule: string;
  Support: string;
  Source: string;
  miRNA: string;
  Year: string;
  PMID: string;
  Pattern: string;
  Species: string;
  Condition: string;
}
