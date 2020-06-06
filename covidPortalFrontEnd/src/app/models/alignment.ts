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

export class SequenceObj {
    accession:string;
    // residueObjList:ResidueObj[];
    sequence:string;
    displayResidueObjList:ResidueObj[];
}
