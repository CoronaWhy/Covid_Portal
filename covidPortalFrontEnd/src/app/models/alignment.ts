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

export class NomenclaturePositionObj{


  nomenclaturePositionMajor0s:string[];
  nomenclaturePositionMajor1s:string[];
  nomenclaturePositionMajor2s:string[];
  nomenclaturePositionMinor0s:string[];

}

export class AlignmentResultObj {
  sequenceResultObj:SequenceResultObj;
  alignmentObjList:AlignmentObj[];
  selectedAccessions:string[];
  nomenclaturePositionObj:NomenclaturePositionObj;
}
