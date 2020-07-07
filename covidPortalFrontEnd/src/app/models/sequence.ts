import { TableColumnObj } from './tableColumn';

export class SequenceObj {

  id:number;
  isSelected:boolean;
  accession:string;
  organism:string;
  collection_date:string;
  country:string;
  host:string;
  isolation_source:string;
  coded_by:string;
  protein_id:string;
  taxon_id:string;
  isolate:string;

}

export class SequenceResultObj {

  sequenceObjList:SequenceObj[];
  sequenceTableColumnObjs :TableColumnObj[];
  sequenceSortColumn:string; 
}
