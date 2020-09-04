import { SequenceResultObj, SequenceObj } from './sequence';
import { EpitopeExperimentResultObj, EpitopeObj, EpitopeOffsetObj } from './epitope';
import { StructureChainResultObj, StructureObj } from './structure';

export class Coordinate {
  x:number;
  y:number;
  z:number;
}

export class ResidueObj {

  residueLabel:string;

  residueIndex:number;
  residueTableCellColor:string;
  residueValue:string;
  residueColor:string;
  residuePosition:Coordinate;
  residueDistance:number;
  isReferenceResidue:boolean;
  residueDistanceColor:string;
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

  selectedExpMethods:string[];

  structureObjList:StructureObj[];
  selectedStructureIds:string[];

  epitopeOffsetObjs:EpitopeOffsetObj;

  nomenclaturePositionStrings:string[];
}
