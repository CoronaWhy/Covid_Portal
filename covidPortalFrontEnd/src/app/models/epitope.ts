import { ResidueObj } from './alignment';
import { TableColumnObj } from './tableColumn';

export class EpitopeExperimentObj {

  id:number;
  host:string;
  assay_type:string;
  assay_result:string;
  mhc_allele:string;
  mhc_class:string;
  exp_method:string;
  measurement_type:string;

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

  epitopeExperimentObjList:EpitopeExperimentObj[];
  epitopeExperimentTableColumnObjs :TableColumnObj[];
  epitopeSortColumn:string;

}
