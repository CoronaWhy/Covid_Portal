import { ResidueObj } from './alignment';
import { TableColumnObj } from './tableColumn';

export class StructureChainObj {

  id:number;
  host:string;
  assay_type:string;
  assay_result:string;
  mhc_allele:string;
  mhc_class:string;
  exp_method:string;
  measurement_type:string;

}

export class StructureObj {
  pdbchain:string;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
}

export class StructureChainResultObj {

  structureChainObjList:StructureChainObj[];
  structureChainTableColumnObjs :TableColumnObj[];
  structureSortColumn:string;
}
