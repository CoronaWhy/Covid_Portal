import { ResidueObj } from './alignment';
import { TableColumnObj } from './tableColumn';
import { ColumnFilter } from './sequence';

export class EpitopeExperimentObj {
  id:number;
  iedb_id:string;
  host:string;
  assay_type:string;
  assay_result:string;
  mhc_allele:string;
  mhc_class:string;
  exp_method:string;
  measurement_type:string;
  isSelected:boolean;
}

export class EpitopeOffsetObj {
  iedb_id:string;
  offset:number;
}

export class EpitopeObj {
  iedb_id:string;
  epitopeExperimentObj:EpitopeExperimentObj;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
  sortColumnValue:string;
  percOffset:number;
  offset:number;
  internalSortColumnValue:string;
  externalSortColumnValue:string;
}

export class EpitopeExperimentResultObj {
  columnFilterList:ColumnFilter[];
  epitopeExperimentObjList:EpitopeExperimentObj[];
  epitopeExperimentTableColumnObjs :TableColumnObj[];
  epitopeSortColumn:string;
}
