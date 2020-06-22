import { SequenceResultObj } from './sequence';

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
  alignmentObjList:AlignmentObj[];
  selectedAccessions:string[];
  nomenclaturePositionStrings:string[];
}
