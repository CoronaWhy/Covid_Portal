import { ResidueObj } from './alignment';
import { TableColumnObj } from './tableColumn';
import { ColumnFilter } from './sequence';

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
  columnFilterList:ColumnFilter[];
  structureChainObjList:StructureChainObj[];
  structureChainTableColumnObjs :TableColumnObj[];
  structureSortColumn:string;
}

export class DistanceObj {
  pdbchain:string;
  offset:number;
  percOffset:number;
  backgroundColor:string;
}
