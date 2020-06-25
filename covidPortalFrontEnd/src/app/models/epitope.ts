import { ResidueObj } from './alignment';

export class EpitopeObj {
  iedb_id:string;
  // protein:string;
  // alignment:string;
  // sequence:string;
  // offset:number;
  // measurement_type:string;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
}

export class EpitopeExperimentObj {

  id:number;
  epitope:EpitopeObj;
  host:string;
  assay_type:string;
  assay_result:string;
  mhc_allele:string;
  mhc_class:string;
  exp_method:string;
  measurement_type:string;

}

export class EpitopeExperimentResultObj {

  epitopeExperimentObjList:EpitopeExperimentObj[];
  epitopeExperimentTableColumns :string[];
}
