import { ResidueObj } from './alignment';

export class StructureObj {
  pdb_id:string;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
}

export class StructureChainObj {

  id:number;
  epitope:StructureObj;
  host:string;
  assay_type:string;
  assay_result:string;
  mhc_allele:string;
  mhc_class:string;
  exp_method:string;
  measurement_type:string;

}

export class StructureChainResultObj {

  structureChainObjList:StructureChainObj[];
  structureChainTableColumns :string[];
}
