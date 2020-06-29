import { SequenceResultObj } from './sequence';
import { EpitopeExperimentResultObj, EpitopeObj } from './epitope';
import { StructureChainResultObj, StructureObj } from './structure';

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
  structureChainResultObj:StructureChainResultObj;

  alignmentObjList:AlignmentObj[];
  selectedAccessions:string[];

  epitopeObjList:EpitopeObj[];
  selectedEpitopeIds:string[];

  structureObjList:StructureObj[];
  selectedStructureIds:string[];

  nomenclaturePositionStrings:string[];
}
