import { SequenceResultObj, SequenceObj } from './sequence';
import { EpitopeExperimentResultObj, EpitopeObj } from './epitope';
import { StructureChainResultObj, StructureObj } from './structure';

export class Coordinate {
  x:number;
  y:number;
  z:number;
}

export class ResidueObj {
  residueValue:number;
  residueColor:string;
  residuePosition:Coordinate;
}

export class AlignmentObj {
  label:number;
  residueObjList:ResidueObj[];
  displayResidueObjList:ResidueObj[];
  sequenceObj:SequenceObj;
  sortColumnValue:string;
}

export class AlignmentResultObj {
  sequenceResultObj:SequenceResultObj;
  epitopeExperimentResultObj:EpitopeExperimentResultObj;
  structureChainResultObj:StructureChainResultObj;

  alignmentObjList:AlignmentObj[];
  selectedAccessions:string[];

  epitopeObjList:EpitopeObj[];
  selectedEpitopeIds:string[];

  structureObjList:StructureObj[];
  selectedStructureIds:string[];

  nomenclaturePositionStrings:string[];
}
