import { SequenceResultObj } from './sequence';
import { EpitopeExperimentResultObj } from './epitope';

export class ResidueObj {
  residueValue:number;
  residueColor:string;
  residuePosition:string;
}

export class AlignmentObj {
  label:number;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];

}

export class AlignmentResultObj {
  sequenceResultObj:SequenceResultObj;
  epitopeExperimentResultObj:EpitopeExperimentResultObj;

  alignmentObjList:AlignmentObj[];
  selectedAccessions:string[];
  nomenclaturePositionStrings:string[];
}
