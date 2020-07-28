import { TableColumnObj } from './tableColumn';

export class ColumnFilter {
  columnName:string;
  columnFilterValues:string[];
  selectedValue:string;
}

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
  protein:string;
  taxon:string;
  isolate:string;
}

export class SequenceResultObj {
  columnFilterList:ColumnFilter[];
  sequenceObjList:SequenceObj[];
  sequenceTableColumnObjs :TableColumnObj[];
  sequenceSortColumn:string;
}
