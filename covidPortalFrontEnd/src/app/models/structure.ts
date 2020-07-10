import { ResidueObj } from './alignment';
import { TableColumnObj } from './tableColumn';

export class StructureChainObj {
  taxon:string;
  pdb_id:string;
  chain:string;

}

export class StructureObj {
  pdbchain:string;
  structureChainObj:StructureChainObj;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
  sortColumnValue:string;
}

export class StructureChainResultObj {
  structureChainObjList:StructureChainObj[];
  structureChainTableColumnObjs :TableColumnObj[];
  structureSortColumn:string;
}
