import { Component, ViewChild, OnInit, AfterViewInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ShowAlignmentService } from './show-alignment-service';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import { delay } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Datafile, UploadFolder } from '../models/datafile';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';
import { AlignmentObj, ResidueObj } from '../models/alignment';
import { SequenceResultObj, SequenceObj } from '../models/sequence';
import { PopupValueObj } from '../models/popupvalue';
import { EpitopeObj, EpitopeOffsetObj, EpitopeExperimentObj, EpitopeExperimentResultObj } from '../models/epitope';
import { StructureObj, StructureChainObj, StructureChainResultObj, DistanceObj } from '../models/structure';
import { ActivatedRoute, Params, Routes, Router } from '@angular/router';
import { Options } from 'ng5-slider';
import { Page } from '../models/page';
import { PagedData } from '../models/page-data';
import { of } from 'rxjs';
import { TableColumnObj } from '../models/tableColumn';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { PopupModalComponent } from '../popup-modal/popup-modal.component';

@Component({
    selector: 'list-files',
    providers: [ShowAlignmentService],
    templateUrl: './show-alignment.component.html',
    styleUrls: ['./show-alignment.component.scss']
})

export class ShowAlignmentComponent implements OnInit, OnDestroy, AfterViewInit{
    @Input()
    datafiles : UploadFolder[];
    allDatafiles : UploadFolder[];
    filterFilesOption:string;
    resultsAvailable:boolean;
    sub:Subscription;
    message:string;
    proteinResidueIndex:number;
    alignmentObjList:AlignmentObj[];
    displayAlignmentObjList:AlignmentObj[];
    maxDisplayResidues :number;
    startPosition:number;
    endPosition:number;
    maxSliderValue:number;
    searchDataFilesString:string;
    positionSliderValue:number;
    sequenceTableColumnObjs:TableColumnObj[];
    popupValueObjList:PopupValueObj[];
    epitopeOffsetObjs:EpitopeOffsetObj;
    selectedAccessions:string[];
    selectedEpitopeIds:string[];
    selectedResidueIndex:number;
    selectedStructureIds:string[];
    proteinDistanceObjList:DistanceObj[][];
    structureChainResultObj:StructureChainResultObj;
    rangeSliderOptions: Options = {
      floor: 0,
      ceil: 10,
      vertical: true
    };
    sortColumn:string;
    rowNum:number;
    indexValue:number;
    maxVerticalSliderValue:number;
    verticalSliderValue:number;
    showFiltersFlag:boolean;
    sequences:SequenceObj[];
    sequenceResultObj:SequenceResultObj;

    alignmentPrevButtonColor:string;
    alignmentNextButtonColor:string;

    epitopePrevButtonColor:string;
    epitopeNextButtonColor:string;
    structurePrevButtonColor:string;
    structureNextButtonColor:string;

    sequenceObjList:SequenceObj[];
    epitopeExperimentResultObj:EpitopeExperimentResultObj;
    structureChainObjList:StructureChainObj[];

    savedSequenceObjList:SequenceObj[];
    savedEpitopeExperimentObjList : EpitopeExperimentObj[];
    savedStructureChainObjList:StructureChainObj[];

    epitopeObjList:EpitopeObj[];
    displayEpitopeObjList:EpitopeObj[];
    epitopeExternalSortColumn:string;
    epitopeInternalSortColumn:string;
    structureObjList:StructureObj[];
    displayStructureObjList:StructureObj[];
    page : Page;
    rows : Array<SequenceObj>;
    cache: any;
    isLoading: boolean;
    displaySequenceObjList:SequenceObj[];

    epitopeExperimentObjList:EpitopeExperimentObj[];
    displayEpitopeExperimentObjList:EpitopeExperimentObj[];
    epitopeExperimentTableColumnObjs:TableColumnObj[];

    displayStructureChainObjList:StructureChainObj[];
    structureChainTableColumnObjs:TableColumnObj[];

    initialAlignment: boolean;

    searchString:string;
    searchEpitopeString:string;
    searchStructureString:string;

    savedSearchString:string;
    savedSearchEpitopeString:string;
    savedSearchStructureString:string;

    numRowsInPage:number;

    hideAlignmentPrevButton: boolean;
    hideAlignmentNextButton: boolean;

    hideEpitopePrevButton: boolean;
    hideEpitopeNextButton: boolean;

    hideStructurePrevButton: boolean;
    hideStructureNextButton: boolean;

    nomenclaturePositionStrings:string[];
    displayNomenclaturePositionStrings:string[];

    offset:number;
    epitopeOffset:number;
    structureOffset:number;

    numRowsInAlignment:number;

    sequenceSortColumn:string;
    epitopeSortColumn:string;
    structureSortColumn:string;

    sequenceTableSortColumn:string;
    epitopeTableSortColumn:string;
    structureTableSortColumn:string;

    epitopeVerticalSliderValue:number;
    structureVerticalSliderValue:number;

    sortStructureChainTableColumn = 'taxon';
    sortEpitopeExperimentTableColumn = 'host';

    @ViewChild('sequenceTable') sequenceTable;

    removeAlignmentObj(accession){

      this.alignmentObjList.forEach( (item, index) => {
        if(item.label === accession) this.alignmentObjList.splice(index,1);
      });

      this.sequenceObjList.forEach( (item, index) => {
        if(item.accession === accession) {
            item.isSelected = false;
          }
      });

      this.displayAlignmentObjList = this.alignmentObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
    }
    removeEpitopeObj(iedb_id){
      this.epitopeObjList.forEach( (item, index) => {
        if(item.iedb_id === iedb_id) this.epitopeObjList.splice(index,1);
      });

      this.epitopeExperimentObjList.forEach( (item, index) => {
        if(item.iedb_id === iedb_id) {
            item.isSelected = false;
          }
      });

      this.displayEpitopeObjList = this.epitopeObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
    }
    removeStructureObj(pdbchain){

      console.log (" in remove structure obj " + pdbchain);

      this.structureObjList.forEach( (item, index) => {
        if(item.pdbchain === pdbchain) this.structureObjList.splice(index,1);
      });

      if (this.structureObjList.length == 0){
          this.proteinDistanceObjList = [];
          this.proteinResidueIndex = -1;
      }

      this.selectedStructureIds.forEach( (item, index) => {
        if(item === pdbchain) this.selectedStructureIds.splice(index,1);
      });

      this.structureChainObjList.forEach( (item, index) => {
        if(item.pdbchain === pdbchain) {
            item.isSelected = false;
          }

      });

      this.displayStructureObjList = this.structureObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

      this.handleProteinResidueClick();
    }

    openAlignmentModal(value){
      // console.log(value);

      const alignmentModalRef = this.popupModalService.open(PopupModalComponent);

      this.popupValueObjList = [];

      let popupValueObj : PopupValueObj;
      let selectedAlignmentObj:AlignmentObj;
      let objKeys:any;
      for (let i = 0; i < this.displayAlignmentObjList.length; i++){
        if (this.displayAlignmentObjList[i].sequenceObj.accession == value){

          selectedAlignmentObj = this.displayAlignmentObjList[i];

          objKeys = Object.keys(selectedAlignmentObj.sequenceObj);

          for (let j = 0; j<objKeys.length; j++ ){
              popupValueObj = new PopupValueObj();
              popupValueObj.popupKey = objKeys[j];
              popupValueObj.popupValue = selectedAlignmentObj.sequenceObj[objKeys[j]];
              this.popupValueObjList.push(popupValueObj);

          }
          break;
        }
      }
      // console.log (" pushing 22 " + this.popupValueObjList);

      alignmentModalRef.componentInstance.popupValueObjList = this.popupValueObjList;

    }

    openEpitopeModal(value){
      console.log(value);

      const epitopeModalRef = this.popupModalService.open(PopupModalComponent);

      this.popupValueObjList = [];

      let popupValueObj : PopupValueObj;
      let selectedEpitopeObj:EpitopeObj;
      let objKeys:any;
      for (let i = 0; i < this.displayEpitopeObjList.length; i++){
        if (this.displayEpitopeObjList[i].iedb_id == value){

          selectedEpitopeObj = this.displayEpitopeObjList[i];

          objKeys = Object.keys(selectedEpitopeObj.epitopeExperimentObj);

          for (let j = 0; j<objKeys.length; j++ ){
              popupValueObj = new PopupValueObj();
              popupValueObj.popupKey = objKeys[j];
              popupValueObj.popupValue = selectedEpitopeObj.epitopeExperimentObj[objKeys[j]];
              this.popupValueObjList.push(popupValueObj);

          }
          break;
        }
      }

      epitopeModalRef.componentInstance.popupValueObjList = this.popupValueObjList;

    }

   openStructureModal(value){
     console.log(value);

     const structureModalRef = this.popupModalService.open(PopupModalComponent);

     this.popupValueObjList = [];

     let popupValueObj : PopupValueObj;
     let selectedStructureObj:StructureObj;
     let objKeys:any;
     for (let i = 0; i < this.displayStructureObjList.length; i++){
       if (this.displayStructureObjList[i].pdbchain == value){

         selectedStructureObj = this.displayStructureObjList[i];

         objKeys = Object.keys(selectedStructureObj.structureChainObj);

         for (let j = 0; j<objKeys.length; j++ ){
             popupValueObj = new PopupValueObj();
             popupValueObj.popupKey = objKeys[j];
             popupValueObj.popupValue = selectedStructureObj.structureChainObj[objKeys[j]];
             this.popupValueObjList.push(popupValueObj);

         }
         break;
       }
     }

     structureModalRef.componentInstance.popupValueObjList = this.popupValueObjList;

   }

   sortSequenceTable (sortColumn)
   {
     if (this.sequenceSortColumn != sortColumn) {
         console.log(sortColumn);
         this.sequenceSortColumn = sortColumn;

         this.alignmentObjList.sort((a, b) => (a.sequenceObj[sortColumn] > b.sequenceObj[sortColumn]) ? 1 : -1);
         for (let i = 0; i < this.alignmentObjList.length; i++){
           this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj[sortColumn];
         }

         this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
         for (let i = 0; i < this.displayAlignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.displayAlignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           this.displayAlignmentObjList[i].residueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
           this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
         }

          for (let i = 0; i< this.sequenceTableColumnObjs.length; i++) {
              if (this.sequenceTableColumnObjs[i].columnName == sortColumn) {
                this.sequenceTableColumnObjs[i].rowColor = "#A3E4EE";
              } else {
                this.sequenceTableColumnObjs[i].rowColor = "#FFFFFF";
              }
          }
      }
   }

   sortEpitopeTable (sortColumn, columnNumber)
   {
      console.log(this.epitopeObjList[0].epitopeExperimentObj[sortColumn] + " : " + columnNumber);
       if ( (this.epitopeExternalSortColumn != sortColumn && columnNumber == 0) || (this.epitopeInternalSortColumn != sortColumn && columnNumber == 1) ) {
           console.log(sortColumn);
           if (columnNumber == 0){
             this.epitopeExternalSortColumn = sortColumn;
           } else if (columnNumber == 1){
             this.epitopeInternalSortColumn = sortColumn;
           }

           if (sortColumn == "iedb_id") {
             this.epitopeObjList.sort((a, b) => (a.iedb_id > b.iedb_id) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].iedb_id;
             }
           } else {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj[this.epitopeExternalSortColumn] > b.epitopeExperimentObj[this.epitopeExternalSortColumn]) ? 1 : ( a.epitopeExperimentObj[this.epitopeInternalSortColumn] > b.epitopeExperimentObj[this.epitopeInternalSortColumn] ? 1 :-1) );
             for (let i = 0; i < this.epitopeObjList.length; i++){
               if (columnNumber == 0){
                 // console.log(" setting ")
                 this.epitopeObjList[i].externalSortColumnValue = this.epitopeObjList[i].epitopeExperimentObj[sortColumn];
               }
               else if (columnNumber == 1){
                 this.epitopeObjList[i].internalSortColumnValue = this.epitopeObjList[i].epitopeExperimentObj[sortColumn];
               }
             }
           }

           this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.displayEpitopeObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.displayEpitopeObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.displayEpitopeObjList[i].residueObjList = JSON.parse(JSON.stringify(this.epitopeObjList[i].residueObjList));
             this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           }

            for (let i = 0; i< this.epitopeExperimentTableColumnObjs.length; i++) {
                if (this.epitopeExperimentTableColumnObjs[i].columnName == sortColumn) {
                  this.epitopeExperimentTableColumnObjs[i].rowColor = "#A3E4EE";
                } else {
                  this.epitopeExperimentTableColumnObjs[i].rowColor = "#FFFFFF";
                }
            }
        }
   }

   sortStructureTable(sortColumn){
     if (this.structureSortColumn != sortColumn) {
         console.log(sortColumn);
         this.structureSortColumn = sortColumn;
         this.structureObjList.sort((a, b) => (a.structureChainObj[sortColumn] > b.structureChainObj[sortColumn]) ? 1 : -1);
         for (let i = 0; i < this.structureObjList.length; i++){
           this.structureObjList[i].sortColumnValue = this.structureObjList[i].structureChainObj.taxon;
         }

         this.displayStructureObjList = this.structureObjList.slice(0,this.numRowsInAlignment);
         for (let i = 0; i < this.displayStructureObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.displayStructureObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           this.displayStructureObjList[i].residueObjList = JSON.parse(JSON.stringify(this.structureObjList[i].residueObjList));
           this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
         }

          for (let i = 0; i< this.structureChainTableColumnObjs.length; i++) {
              if (this.structureChainTableColumnObjs[i].columnName == sortColumn) {
                this.structureChainTableColumnObjs[i].rowColor = "#A3E4EE";
              } else {
                this.structureChainTableColumnObjs[i].rowColor = "#FFFFFF";
              }
          }
      }
   }

    sortSequenceMainTable (sortColumn)
    {
      if (this.sequenceTableSortColumn != sortColumn) {
          console.log(sortColumn);

          this.sequenceTableSortColumn = sortColumn;

          this.sequenceObjList.sort((a, b) => (a[sortColumn]  > b[sortColumn]) ? 1 : -1);

          this.displaySequenceObjList = this.sequenceObjList.slice(0,this.numRowsInAlignment);

       }
    }

    sortEpitopeExperimentTable (sortColumn)
    {
      if (this.epitopeTableSortColumn != sortColumn) {
          console.log(sortColumn);

          this.epitopeTableSortColumn = sortColumn;

          this.epitopeExperimentObjList.sort((a, b) => (a[sortColumn] > b[sortColumn]) ? 1 : -1);

          this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInAlignment);

       }
    }

    sortStructureChainTable (sortColumn)
    {
      if (this.structureTableSortColumn != sortColumn) {
          console.log(sortColumn);

          this.structureTableSortColumn = sortColumn;

          this.structureChainObjList.sort((a, b) => (a[sortColumn] > b[sortColumn]) ? 1 : -1);

          this.displayStructureChainObjList = this.structureChainObjList.slice(0,this.numRowsInAlignment);

       }
    }

   filterSequenceTable(columnName, columnFilterValue){

     console.log(" columnName " + columnName + " columnFilterValue " + columnFilterValue);

     this.sequenceObjList = JSON.parse(JSON.stringify(this.savedSequenceObjList));

     let tempList = [];
     let okFlag : boolean;

     for (let i = 0; i < this.sequenceObjList.length; i++){
       // console.log(" i = " + i);
        for (let j = 0; j < this.sequenceResultObj.columnFilterList.length; j++){
          // console.log(" j = " + j);
          // console.log(" this.sequenceResultObj.columnFilterList[j].columnName = " + this.sequenceResultObj.columnFilterList[j].columnName + " columnName " + this.sequenceObjList[i][columnName] + " filter " + columnFilterValue);

          // for column the user wants to filter
          if (columnFilterValue != '' ){

            if (this.sequenceResultObj.columnFilterList[j].columnName == columnName  && this.sequenceObjList[i][columnName] == columnFilterValue) {
               // console.log (" ************* in loop " + this.sequenceResultObj.columnFilterList[j].columnName + " - " + columnName && this.sequenceObjList[i][columnName]);
               okFlag = true;
               for (let k = 0; k < this.sequenceResultObj.columnFilterList.length; k++){
                 // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                   if (j!=k
                      && this.sequenceResultObj.columnFilterList[k].selectedValue
                      && this.sequenceResultObj.columnFilterList[k].selectedValue != ''
                      &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue
                      ) {
                    console.log (this.sequenceResultObj.columnFilterList[k].selectedValue);
                      okFlag = false;
                      break;
                 }
               }
               if (okFlag){
                 tempList.push(this.sequenceObjList[i]);
               }
               this.sequenceResultObj.columnFilterList[j].selectedValue = columnFilterValue;
             }
          }
          else {
            okFlag = true;
            for (let k = 0; k < this.sequenceResultObj.columnFilterList.length; k++){

                if (this.sequenceResultObj.columnFilterList[k].columnName == columnName){
                  this.sequenceResultObj.columnFilterList[k].selectedValue = '';
                }

              // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                if (j!=k
                   && this.sequenceResultObj.columnFilterList[k].selectedValue
                   && this.sequenceResultObj.columnFilterList[k].selectedValue != ''
                   &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue
                   ) {
                 console.log (this.sequenceResultObj.columnFilterList[k].selectedValue);
                   okFlag = false;
                   break;
              }
            }
            if (okFlag){
              tempList.push(this.sequenceObjList[i]);
            }

          }

        }
     }
      // console.log(tempList);

      this.displaySequenceObjList = tempList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

   }

   filterEpitopeTable(columnName, columnFilterValue){

     // console.log(" columnName " + columnName + " columnFilterValue " + columnFilterValue);
     //
     // this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));
     //
     // this.epitopeExperimentObjList = this.epitopeExperimentObjList.filter(item => {
     //      return item[columnName].includes(columnFilterValue);
     //  });
     //
     //  this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

     console.log(" columnName " + columnName + " columnFilterValue " + columnFilterValue);

     this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));

     let tempList = [];
     let okFlag : boolean;

     for (let i = 0; i < this.epitopeExperimentObjList.length; i++){
       // console.log(" i = " + i);
        for (let j = 0; j < this.epitopeExperimentResultObj.columnFilterList.length; j++){
          // console.log(" j = " + j);
          // console.log(" this.sequenceResultObj.columnFilterList[j].columnName = " + this.sequenceResultObj.columnFilterList[j].columnName + " columnName " + this.sequenceObjList[i][columnName] + " filter " + columnFilterValue);

          // for column the user wants to filter
          if (columnFilterValue != '' ){

            if (this.epitopeExperimentResultObj.columnFilterList[j].columnName == columnName  && this.epitopeExperimentObjList[i][columnName] == columnFilterValue) {
               // console.log (" ************* in loop " + this.sequenceResultObj.columnFilterList[j].columnName + " - " + columnName && this.sequenceObjList[i][columnName]);
               okFlag = true;
               for (let k = 0; k < this.epitopeExperimentResultObj.columnFilterList.length; k++){
                 // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                   if (j!=k
                      && this.epitopeExperimentResultObj.columnFilterList[k].selectedValue != ''
                      && this.epitopeExperimentResultObj.columnFilterList[k].selectedValue
                      &&  this.epitopeExperimentObjList[i][this.epitopeExperimentResultObj.columnFilterList[k].columnName] != this.epitopeExperimentResultObj.columnFilterList[k].selectedValue
                      ) {
                    console.log (this.epitopeExperimentResultObj.columnFilterList[k].selectedValue);
                      okFlag = false;
                      break;
                 }
               }
               if (okFlag){
                 tempList.push(this.epitopeExperimentObjList[i]);
               }
               this.epitopeExperimentResultObj.columnFilterList[j].selectedValue = columnFilterValue;
             }
          }
          else {
            okFlag = true;
            for (let k = 0; k < this.epitopeExperimentResultObj.columnFilterList.length; k++){

                if (this.epitopeExperimentResultObj.columnFilterList[k].columnName == columnName){
                  this.epitopeExperimentResultObj.columnFilterList[k].selectedValue = '';
                }

              // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                if (j!=k
                   && this.epitopeExperimentResultObj.columnFilterList[k].selectedValue
                   && this.epitopeExperimentResultObj.columnFilterList[k].selectedValue != ''
                   &&  this.epitopeExperimentObjList[i][this.epitopeExperimentResultObj.columnFilterList[k].columnName] != this.epitopeExperimentResultObj.columnFilterList[k].selectedValue
                   ) {
                 console.log (this.epitopeExperimentResultObj.columnFilterList[k].selectedValue);
                   okFlag = false;
                   break;
              }
            }
            if (okFlag){
              tempList.push(this.epitopeExperimentObjList[i]);
            }

          }

        }
     }
      // console.log(tempList);

      this.displayEpitopeExperimentObjList = tempList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

   }

   filterStructureTable(columnName, columnFilterValue){

     console.log(" columnName " + columnName + " columnFilterValue " + columnFilterValue);

     if (this.searchString.length > this.savedSearchString.length){

       this.structureChainObjList = JSON.parse(JSON.stringify(this.savedStructureChainObjList));

     }

     this.savedSearchString = this.searchString;

     // this.structureChainObjList.filter(item => {
     //      return item[columnName].includes(columnFilterValue);
     //  });
     //
     //  this.displayStructureChainObjList = this.structureChainObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
     //
     //  console.log(" columnName " + columnName + " columnFilterValue " + columnFilterValue);
     //
     //  this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));

      let tempList = [];
      let okFlag : boolean;

      for (let i = 0; i < this.structureChainObjList.length; i++){
        // console.log(" i = " + i);
         for (let j = 0; j < this.structureChainResultObj.columnFilterList.length; j++){
           // console.log(" j = " + j);
           // console.log(" this.sequenceResultObj.columnFilterList[j].columnName = " + this.sequenceResultObj.columnFilterList[j].columnName + " columnName " + this.sequenceObjList[i][columnName] + " filter " + columnFilterValue);

           // for column the user wants to filter
           if (columnFilterValue != '' ){

             if (this.structureChainResultObj.columnFilterList[j].columnName == columnName  && this.structureChainObjList[i][columnName] == columnFilterValue) {
                // console.log (" ************* in loop " + this.sequenceResultObj.columnFilterList[j].columnName + " - " + columnName && this.sequenceObjList[i][columnName]);
                okFlag = true;
                for (let k = 0; k < this.structureChainResultObj.columnFilterList.length; k++){
                  // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                    if (j!=k
                       && this.structureChainResultObj.columnFilterList[k].selectedValue != ''
                       && this.structureChainResultObj.columnFilterList[k].selectedValue
                       &&  this.structureChainObjList[i][this.structureChainResultObj.columnFilterList[k].columnName] != this.structureChainResultObj.columnFilterList[k].selectedValue
                       ) {
                     console.log (this.structureChainResultObj.columnFilterList[k].selectedValue);
                       okFlag = false;
                       break;
                  }
                }
                if (okFlag){
                  tempList.push(this.structureChainObjList[i]);
                }
                this.structureChainResultObj.columnFilterList[j].selectedValue = columnFilterValue;
              }
           }
           else {
             okFlag = true;
             for (let k = 0; k < this.structureChainResultObj.columnFilterList.length; k++){

                 if (this.structureChainResultObj.columnFilterList[k].columnName == columnName){
                   this.structureChainResultObj.columnFilterList[k].selectedValue = '';
                 }

               // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
                 if (j!=k
                    && this.structureChainResultObj.columnFilterList[k].selectedValue
                    && this.structureChainResultObj.columnFilterList[k].selectedValue != ''
                    &&  this.structureChainObjList[i][this.structureChainResultObj.columnFilterList[k].columnName] != this.structureChainResultObj.columnFilterList[k].selectedValue
                    ) {
                  console.log (this.structureChainResultObj.columnFilterList[k].selectedValue);
                    okFlag = false;
                    break;
               }
             }
             if (okFlag){
               tempList.push(this.structureChainObjList[i]);
             }

           }

         }
      }
       // console.log(tempList);

       this.displayStructureChainObjList = tempList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );


   }

    resetSequenceTable () {

      this.sequenceObjList = JSON.parse(JSON.stringify(this.savedSequenceObjList));
      this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

      for (let k = 0; k < this.sequenceResultObj.columnFilterList.length; k++){
           this.sequenceResultObj.columnFilterList[k].selectedValue = '';
      }

    }

    resetEpitopeExperimentTable () {

       this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));
       this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

       for (let k = 0; k < this.epitopeExperimentResultObj.columnFilterList.length; k++){
            this.epitopeExperimentResultObj.columnFilterList[k].selectedValue = '';
       }


    }

   resetStructureChainTable () {

     this.structureChainObjList = JSON.parse(JSON.stringify(this.savedStructureChainObjList));
     this.displayStructureChainObjList = this.structureChainObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );

     for (let k = 0; k < this.structureChainResultObj.columnFilterList.length; k++){
       // if (j!=k && this.sequenceResultObj.columnFilterList[k].selectedValue!= '' &&  this.sequenceObjList[i][this.sequenceResultObj.columnFilterList[k].columnName] != this.sequenceResultObj.columnFilterList[k].selectedValue ) {
          this.structureChainResultObj.columnFilterList[k].selectedValue = '';
     }


   }

   showAlignmentPrev(){

      if (this.offset > 0){
        this.offset -= 1;
        this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
        if (this.offset == 0){
          this.hideAlignmentPrevButton = true;
          this.alignmentPrevButtonColor = "#93477C";
        }
        if (this.displaySequenceObjList.length < this.numRowsInPage){
          this.hideAlignmentNextButton = true;
          this.alignmentNextButtonColor = "#93477C";
        }
      }
   }

   showAlignmentNext(){
      this.offset += 1;
      console.log(" this.offset " + this.offset);
      this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
      if (this.offset > 1){
        this.hideAlignmentPrevButton = false;
        this.alignmentPrevButtonColor = "#834793";
      }
      if (this.displaySequenceObjList.length < this.numRowsInPage){
        this.hideAlignmentNextButton = true;
        this.alignmentNextButtonColor = "#93477C";
      }
   }

   showEpitopeNext(){

     this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInPage);

     this.epitopeOffset += 1;
     console.log(" this.epitopeOffset " + this.epitopeOffset);
     this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.epitopeOffset*this.numRowsInPage, (this.epitopeOffset+1)*this.numRowsInPage );
     // if (this.epitopeOffset > 1){
     //   this.epitopeHidePrevButton = false;
     //   this.epitopePrevButtonColor = "#93477C";
     // }
     if (this.epitopeOffset == 0){
       this.hideEpitopePrevButton = true;
       this.epitopePrevButtonColor = "#93477C";
     }
     if (this.displayEpitopeExperimentObjList.length < this.numRowsInPage){
       this.hideEpitopeNextButton = true;
       this.epitopeNextButtonColor = "#93477C";
     }
  }

  showEpitopePrev(){

    if (this.epitopeOffset > 0){
      this.epitopeOffset -= 1;
      this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.epitopeOffset*this.numRowsInPage, (this.epitopeOffset+1)*this.numRowsInPage );
      // if (this.epitopeOffset == 0){
      //   this.epitopeHidePrevButton = true;
      // }
    }
    if (this.epitopeOffset > 1){
      this.hideEpitopePrevButton = false;
      this.epitopePrevButtonColor = "#834793";
    }
    if (this.displayEpitopeExperimentObjList.length < this.numRowsInPage){
      this.hideEpitopeNextButton = true;
      this.epitopeNextButtonColor = "#93477C";
    }

  }

    showStructureNext(){

      this.structureOffset += 1;
      console.log(" this.structureOffset " + this.structureOffset);
      this.displayStructureChainObjList = this.structureChainObjList.slice(this.structureOffset*this.numRowsInPage, (this.structureOffset+1)*this.numRowsInPage );
      // if (this.structureOffset > 1){
      //   this.structureHidePrevButton = false;
      // }

      if (this.structureOffset == 0){
        this.hideStructurePrevButton = true;
        this.structurePrevButtonColor = "#93477C";
      }
      if (this.displayStructureChainObjList.length < this.numRowsInPage){
        this.hideStructureNextButton = true;
        this.structureNextButtonColor = "#93477C";
      }

     }

     showStructurePrev(){

       if (this.structureOffset > 0){
         this.structureOffset -= 1;
         this.displayStructureChainObjList = this.structureChainObjList.slice(this.structureOffset*this.numRowsInPage, (this.structureOffset+1)*this.numRowsInPage );
         // if (this.epitopeOffset == 0){
         //   this.structureHidePrevButton = true;
         // }
       }
       if (this.structureOffset > 1){
         this.hideStructurePrevButton = false;
         this.structurePrevButtonColor = "#834793";
       }
       if (this.displayStructureChainObjList.length < this.numRowsInPage){
         this.hideStructureNextButton = true;
         this.structureNextButtonColor = "#93477C";
       }

    }

    positionToEpitope(offset){
      console.log(" offset "  + offset);

      this.positionSliderValue = offset;
      this.slideSequences();
    }

    positionStructure(offset){
      console.log(" offset "  + offset);

      this.positionSliderValue = offset;
      this.slideSequences();
    }

    reloadAlignment(value){
      console.log(value.currentTarget.defaultValue);
      if (value.currentTarget.checked){
        console.log(typeof(this.selectedAccessions) + " :: " + value.currentTarget.defaultValue);
        this.selectedAccessions.push(value.currentTarget.defaultValue);

        console.log(this.selectedAccessions);

        this.showAlignmentService.reloadAlignment(this.selectedAccessions).then(alignmentObjList => {
           // for (let i = 0; i< alignmentObjList.length; i++){
           //   this.alignmentObjList.push(alignmentObjList[i]);
           // }
           this.alignmentObjList = alignmentObjList;
           console.log( " alignmentObjList " + alignmentObjList);
           this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.displayAlignmentObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.displayAlignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.displayAlignmentObjList[i].residueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
             this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].residueObjList.slice(this.startPosition+ this.positionSliderValue,this.endPosition+ this.positionSliderValue);
           }
        });
      } else { // if unchecked
          this.removeAlignmentObj(value.currentTarget.defaultValue);
      }
    }

    reloadEpitopes(value){
      console.log(value.currentTarget.defaultValue);
      if (value.currentTarget.checked){
        this.selectedEpitopeIds.push(value.currentTarget.defaultValue);

        console.log(this.selectedEpitopeIds);

        this.showAlignmentService.reloadEpitopes(this.selectedEpitopeIds).then(epitopeObjList => {
          // for (let i = 0; i< epitopeObjList.length; i++){
          //   this.epitopeObjList.push(epitopeObjList[i]);
          // }
           console.log(epitopeObjList);
           this.epitopeObjList = epitopeObjList;
           this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.displayEpitopeObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.displayEpitopeObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.displayEpitopeObjList[i].residueObjList = JSON.parse(JSON.stringify(this.epitopeObjList[i].residueObjList));
             this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition+ this.positionSliderValue,this.endPosition+ this.positionSliderValue);
           }
        });
      } else { // if unchecked
          this.removeEpitopeObj(value.currentTarget.defaultValue);
      }
    }

    reloadStructures(value){

      console.log(value.currentTarget.defaultValue);
      console.log(" this.displayStructureObjList " + this.displayStructureObjList);

      if (value.currentTarget.checked){
        this.selectedStructureIds.push(value.currentTarget.defaultValue);

        console.log(this.selectedStructureIds);

        this.showAlignmentService.reloadStructures(this.selectedStructureIds).then(structureObjList => {
          // for (let i = 0; i< structureObjList.length; i++){
          //   this.structureObjList.push(structureObjList[i]);
          // }
           this.structureObjList = structureObjList;
           console.log(" structureObjList " + structureObjList);
           this.displayStructureObjList = this.structureObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.displayStructureObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.displayStructureObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.displayStructureObjList[i].residueObjList = JSON.parse(JSON.stringify(this.structureObjList[i].residueObjList));
             this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition+ this.positionSliderValue,this.endPosition+ this.positionSliderValue);
           }
        });

        this.handleProteinResidueClick();

      } else { // if unchecked
          this.removeStructureObj(value.currentTarget.defaultValue);
      }
    }

    filterSequenceDatatable(){

      // this.sequenceObjList = JSON.parse(JSON.stringify(this.savedSequenceObjList));

      console.log(" this.sequenceObjList length " + this.sequenceObjList.length);

      this.sequenceObjList = JSON.parse(JSON.stringify(this.savedSequenceObjList));

      let tempList = [];
      let selectFlag:boolean;
      if (this.sequenceObjList.length > 0){
        let objKeys = Object.keys(this.sequenceObjList[0]);

        for (let i = 0; i < this.sequenceObjList.length; i++){
          selectFlag = false;
          for (let j = 0; j < objKeys.length; j++){
              console.log(" obj " + this.sequenceObjList[i] + " key " + objKeys[j]);
              if (this.sequenceObjList[i][objKeys[j]] &&  this.sequenceObjList[i][objKeys[j]].includes (this.searchString) ) {
                selectFlag = true;
              }
          }
          if (selectFlag) {
            tempList.push(this.sequenceObjList[i]);
          }
        }
        this.displaySequenceObjList = tempList.slice(0, this.numRowsInPage);
        this.sequenceObjList = tempList;
        console.log(this.displaySequenceObjList);
      }

     }

     filterEpitopeDataTable(){

       console.log(" this.epitopeExperimentObjList length " + this.epitopeExperimentObjList.length);

       // this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));

       // if (this.searchEpitopeString.length > this.savedSearchEpitopeString.length){

       this.epitopeExperimentObjList = JSON.parse(JSON.stringify(this.savedEpitopeExperimentObjList));

       // }
       //
       // this.savedSearchEpitopeString = this.searchEpitopeString;

       let tempList = [];
       let selectFlag:boolean;
       if (this.epitopeExperimentObjList.length > 0){
         let objKeys = Object.keys(this.epitopeExperimentObjList[0]);

         for (let i = 0; i < this.epitopeExperimentObjList.length; i++){
           selectFlag = false;
           for (let j = 0; j < objKeys.length; j++){
               console.log(" obj " + this.epitopeExperimentObjList[i] + " key " + objKeys[j]);
               if (this.epitopeExperimentObjList[i][objKeys[j]] &&  this.epitopeExperimentObjList[i][objKeys[j]].includes (this.searchEpitopeString) ) {
                 selectFlag = true;
               }
           }
           if (selectFlag) {
             tempList.push(this.epitopeExperimentObjList[i]);
           }
         }
         this.displayEpitopeExperimentObjList = tempList.slice(0, this.numRowsInPage);
         this.epitopeExperimentObjList = tempList;

         console.log(this.displayEpitopeExperimentObjList);
       }

    }

    filterStructureDataTable(){

      console.log(" this.structureChainObjList length " + this.structureChainObjList.length);

      // this.structureChainObjList = JSON.parse(JSON.stringify(this.savedStructureChainObjList));

      // if (this.searchStructureString.length > this.savedSearchStructureString.length){

      this.structureChainObjList = JSON.parse(JSON.stringify(this.savedStructureChainObjList));

      // }
      //
      // this.savedSearchStructureString = this.searchStructureString;

      let tempList = [];
      let selectFlag:boolean;
      if (this.structureChainObjList.length > 0){
        let objKeys = Object.keys(this.structureChainObjList[0]);

        for (let i = 0; i < this.structureChainObjList.length; i++){
          selectFlag = false;
          for (let j = 0; j < objKeys.length; j++){
              console.log(" obj " + this.structureChainObjList[i] + " key " + objKeys[j]);
              if (this.structureChainObjList[i][objKeys[j]] &&  this.structureChainObjList[i][objKeys[j]].includes (this.searchStructureString) ) {
                selectFlag = true;
              }
          }
          if (selectFlag) {
            tempList.push(this.structureChainObjList[i]);
          }
        }
        this.displayStructureChainObjList = tempList.slice(0, this.numRowsInPage);
        this.structureChainObjList = tempList;

        console.log(this.displayStructureChainObjList);
      }

     }

    showHideFilters(){
      if(this.showFiltersFlag ){
        this.showFiltersFlag  = false;
      }
      else{
        this.showFiltersFlag  = true;
      }// if flag
    }

    setVerticalSliderValue(event){
      let verticalSlider = document.getElementById('verticalSlider') as HTMLInputElement;
      this.verticalSliderValue = Number(verticalSlider.value);
      let startIndex = 10-this.verticalSliderValue;
      if (this.alignmentObjList.length >= startIndex+this.numRowsInPage ) {
        this.displayAlignmentObjList = this.alignmentObjList.slice(startIndex,startIndex+this.numRowsInPage);
      }

      for (let i = 0; i < this.displayAlignmentObjList.length; i++){
        this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
      }

    }

    setEpitopeVerticalSliderValue (event) {
      let verticalSlider = document.getElementById('epitopeVerticalSlider') as HTMLInputElement;
      this.epitopeVerticalSliderValue = Number(verticalSlider.value);
      console.log(" index epitopeVerticalSliderValue " + this.epitopeVerticalSliderValue);
      let startIndex = 10-this.epitopeVerticalSliderValue;
      if (this.epitopeObjList.length >= startIndex+this.numRowsInPage ) {
        this.displayEpitopeObjList = this.epitopeObjList.slice(startIndex,startIndex+this.numRowsInPage);
      }

      for (let i = 0; i < this.displayEpitopeObjList.length; i++){
        this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
      }

    }

    setStructureVerticalSliderValue (event) {
      let verticalSlider = document.getElementById('structureVerticalSlider') as HTMLInputElement;
      this.structureVerticalSliderValue = Number(verticalSlider.value);
      console.log(" index structureVerticalSliderValue " + this.structureVerticalSliderValue);
      let startIndex = 10-this.verticalSliderValue;
      if (this.structureObjList.length > startIndex+this.numRowsInPage){
        this.displayStructureObjList = this.structureObjList.slice(startIndex,startIndex+this.numRowsInPage);
      }

      for (let i = 0; i < this.displayStructureObjList.length; i++){
        this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
      }

    }

    sliderValueChange(event){
      console.log(" index value " + this.indexValue);
    }

    ngOnDestroy(){
    }

    setSliderValue(){
      let positionSlider = document.getElementById('positionSlider') as HTMLInputElement;
      this.positionSliderValue = Number(positionSlider.value);
      this.slideSequences();
    }

    slideSequences(){

      this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);

      for (let i = 0; i < this.displayAlignmentObjList.length; i++){
        this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      }

      for (let i = 0; i < this.displayEpitopeObjList.length; i++){
        this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      }

      for (let i = 0; i < this.displayStructureObjList.length; i++){
        this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
        // console.log(this.structureObjList[i].residueObjList);
      }

    }

    ngAfterViewInit() {

      // this.sequenceTable = document.getElementById("sequenceTable")
      //
      // this.sequenceTable.bodyComponent.updatePage = function(direction: string): void {
      //   let offset = this.indexes.first / this.pageSize;
      //
      //   if (direction === 'up') {
      //     offset = Math.ceil(offset);
      //   } else if (direction === 'down') {
      //     offset = Math.floor(offset);
      //   }
      //
      //   if (direction !== undefined && !isNaN(offset)) {
      //     this.page.emit({ offset });
      //   }
      // }

    }

    showHideEpitopePanel(value){
      console.log(value);
      let panel = document.getElementById('epitopepanel');

      if (value == '0'){
          panel.style.display='table-row-group';
      } else if (value == '1'){
        panel.style.display='none';
      }
    }
    showHideStructurePanel(value){
      let panel = document.getElementById('structurepanel');

      if (value == '0'){
          panel.style.display='table-row-group';
      } else if (value == '1'){
        panel.style.display='none';
      }
    }

    ngOnInit() {
      console.log( " on init ");

      // this.route.paramMap.subscribe(params => {
      //   this.selectedAccessions = params["selectedAccessions"];
      //   console.log(this.selectedAccessions);
      // })
      this.savedSearchString = '';
      this.savedSearchEpitopeString = '';
      this.savedSearchStructureString = '';

      this.proteinResidueIndex = -1;

      this.isLoading = false;
      this.sequenceTableSortColumn = "accession";
      this.hideAlignmentPrevButton = true;
      this.hideAlignmentNextButton = false;

      this.showFiltersFlag = false;
      this.rowNum = 0;
      this.indexValue = 0;
      this.message = "";
      this.startPosition = 0;
      this.maxDisplayResidues = 16;
      this.endPosition = this.maxDisplayResidues;
      this.positionSliderValue = 0;

      this.page = new Page();

      this.cache = {};
      this.rows = [];

      this.maxVerticalSliderValue = 10;
      this.verticalSliderValue = 10;
      this.epitopeVerticalSliderValue = 10;
      this.structureVerticalSliderValue = 10;

      this.epitopeExternalSortColumn = 'exp_method';
      this.epitopeInternalSortColumn = 'assay_result';

      this.selectedAccessions = [];

      this.selectedEpitopeIds = [];
      this.selectedStructureIds = [];

      this.initialAlignment = true;

      this.searchString = '';

      this.offset = 0;
      this.epitopeOffset = 0;
      this.structureOffset = 0;


            this.alignmentPrevButtonColor = "#93477C";
            this.alignmentNextButtonColor = "#834793";

            this.epitopePrevButtonColor = "#93477C";
            this.epitopeNextButtonColor = "#834793";

            this.structurePrevButtonColor = "#93477C";
            this.structureNextButtonColor = "#834793";
      this.numRowsInPage = 3;
      this.numRowsInAlignment = 3;

      this.alignmentPrevButtonColor = "#93477C";
      this.alignmentNextButtonColor = "#834793";

      this.epitopePrevButtonColor = "#93477C";
      this.epitopeNextButtonColor = "#834793";

      this.structurePrevButtonColor = "#93477C";
      this.structureNextButtonColor = "#834793";

      // this.sortSequenceTableColumn = '';
      this.sortStructureChainTableColumn = 'taxon';
      this.sortEpitopeExperimentTableColumn = 'host';

      this.showAlignmentService.showAlignment().then(alignmentResult => {
         // console.log(alignmentObjList);
         this.sequences = alignmentResult.sequenceResultObj.sequenceObjList;

         this.sequenceResultObj = alignmentResult.sequenceResultObj;

         this.sequenceTableColumnObjs = this.sequenceResultObj.sequenceTableColumnObjs;
         this.sequenceSortColumn = this.sequenceResultObj.sequenceSortColumn;

         this.epitopeExperimentTableColumnObjs = alignmentResult.epitopeExperimentResultObj.epitopeExperimentTableColumnObjs;
         console.log (" epitopeExperimentTableColumnObjs = " + this.epitopeExperimentTableColumnObjs);
         this.epitopeSortColumn = alignmentResult.epitopeExperimentResultObj.epitopeSortColumn;

         this.structureChainTableColumnObjs = alignmentResult.structureChainResultObj.structureChainTableColumnObjs;
         this.structureSortColumn = alignmentResult.structureChainResultObj.structureSortColumn;
         this.structureChainResultObj = alignmentResult.structureChainResultObj;
         console.log(this.sequenceTableColumnObjs);
         // console.log(this.structureChainTableColumns);

         // sequence obj list
         this.sequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;
         this.savedSequenceObjList = JSON.parse(JSON.stringify(alignmentResult.sequenceResultObj.sequenceObjList));
         this.displaySequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;

         // structures
         this.structureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;
         this.savedStructureChainObjList = JSON.parse(JSON.stringify(this.structureChainObjList));
         this.displayStructureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;

         this.alignmentObjList = alignmentResult.alignmentObjList;
         this.epitopeObjList = alignmentResult.epitopeObjList;
         this.structureObjList = alignmentResult.structureObjList;

         console.log( " this.structureObjList " + this.structureObjList);

         // epitopes
         this.epitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;
         this.savedEpitopeExperimentObjList = JSON.parse(JSON.stringify(this.epitopeExperimentObjList));
         this.displayEpitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;

         this.epitopeExperimentResultObj = alignmentResult.epitopeExperimentResultObj;

         this.selectedAccessions = alignmentResult.selectedAccessions;
         this.selectedEpitopeIds = alignmentResult.selectedEpitopeIds;
         this.selectedStructureIds = alignmentResult.selectedStructureIds;

         this.epitopeOffsetObjs = alignmentResult.epitopeOffsetObjs;

         this.nomenclaturePositionStrings = alignmentResult.nomenclaturePositionStrings;

         this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition,this.endPosition);

         this.initialAlignment = false;

         this.displaySequenceObjList = this.sequenceObjList.slice(0, this.numRowsInPage);
         this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInPage);
         this.displayStructureChainObjList = this.structureChainObjList.slice(0,this.numRowsInPage);

         this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
         this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);
         this.displayStructureObjList = this.structureObjList.slice(0,this.numRowsInAlignment);

         for (let i = 0; i < this.alignmentObjList.length; i++){
           this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.host;
         }

         for (let i = 0; i < this.epitopeObjList.length; i++){
           this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.host;
             this.epitopeObjList[i].externalSortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.exp_method;
             this.epitopeObjList[i].internalSortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.assay_result;
         }

         for (let i = 0; i < this.structureObjList.length; i++){
           this.structureObjList[i].sortColumnValue = this.structureObjList[i].structureChainObj.taxon;
         }

         for (let i = 0; i < this.displayAlignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.displayAlignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           // not needed to slice need to remove after testing
           this.displayAlignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.displayAlignmentObjList[i].residueObjList));
           this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
           // console.log(this.displayAignmentObjList[i].residueObjList);
         }

         for (let i = 0; i < this.displayEpitopeObjList.length; i++){

           // not needed to slice need to remove after testing
           this.displayEpitopeObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.displayEpitopeObjList[i].residueObjList));
           this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           // console.log(this.displayAignmentObjList[i].residueObjList);
         }


        for (let i = 0; i < this.displayStructureObjList.length; i++){
           // console.log(" in structure i = " + i);
           // not needed to slice need to remove after testing
           this.displayStructureObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.displayStructureObjList[i].residueObjList));
           this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
        }
         // console.log(this.displayAignmentObjList);
      });
    }

    handleProteinResidueClick(){

      if (this.proteinResidueIndex == -1){
        return;
      }

      console.log(" ^^^ in handle protein residue click ");

      this.proteinDistanceObjList = [];

      for (let listIndex = 0; listIndex < this.displayStructureObjList.length; listIndex++){

        let distances:number[];
        let distance = 0;
        distances = [];

        let distanceObjList = [];

        let normalizedDistances = [];

        let selectedPosition = [this.displayStructureObjList[listIndex].displayResidueObjList[this.proteinResidueIndex].residuePosition.x , this.displayStructureObjList[listIndex].displayResidueObjList[this.proteinResidueIndex].residuePosition.y ,
        this.displayStructureObjList[listIndex].displayResidueObjList[this.proteinResidueIndex].residuePosition.z]

        console.log(" listIndex " + listIndex);
        console.log(" len  this.displayStructureObjList " + this.displayStructureObjList.length);

        for (let i = 0; i < this.displayStructureObjList[listIndex].residueObjList.length; i++){
          // console.log(this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition);
           distance = 0;
           // if (listIndex == 0){
           //   console.log(" len  this.displayStructureObjList[listIndex].residueObjList " + this.displayStructureObjList[listIndex].residueObjList.length + " i = " + i);
           // }
           if (this.displayStructureObjList[listIndex].residueObjList[i].residueValue != '-'){
              distance =

              Math.sqrt
              (

                (
                  (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.x - selectedPosition[0])
                    *
                  (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.x - selectedPosition[0])
                )

                +

                (
                   (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.y - selectedPosition[1])
                     *
                   (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.y - selectedPosition[1])

                )

                +

                (
                   (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.y - selectedPosition[2])
                     *
                   (this.displayStructureObjList[listIndex].residueObjList[i].residuePosition.y - selectedPosition[2])

                )

             );
           }
           distances.push(distance);
           if (i > 168 && i < 188){
             console.log(" listIndex = " + listIndex + " i = " + i + " distance = " + distance);
          }
        }
      // console.log(" distances = " + distances.length);

      // normalise to 0 and 1
      let maxDistance = Math.max(...distances);
      let minDistance = Math.min(...distances);
      let rangeDistance = maxDistance - minDistance;

      for (let j = 0; j < distances.length; j++){
        normalizedDistances.push (
          1- (distances[j] - minDistance)/rangeDistance
        );
      }

      // console.log(" normalizedDistances length " + normalizedDistances.length);

      let baseColor = "#ADB236";

      // let t = 'rgb(255,255,0)';
      // let f = 'rgb(0,0.100)';
      //
      // let tr = document.getElementById("tr_0");
      let distanceObj : DistanceObj;
      let distanceColor : string;
      for (let i = 0; i< normalizedDistances.length; i++){

         if (i >= this.displayStructureObjList[listIndex].residueObjList.length){
           break;
         }

          // if (normalizedDistances[i] == 0){
          //   console.log( " normalizedDistances = " + i + " -- " + normalizedDistances[i]);
          // }
          distanceObj = new DistanceObj();

          distanceObj.percOffset = 0;
          distanceObj.backgroundColor = "#D9D9E1";
          distanceObj.offset = i;

          if (this.displayStructureObjList[listIndex].residueObjList[i].residueValue != '-'){

            distanceColor = this.lightenDarkenColor(baseColor, normalizedDistances[i]*100);

            this.displayStructureObjList[listIndex].residueObjList[i].residueTableCellColor = distanceColor;

            distanceObj.percOffset = normalizedDistances[i]*100;
            // if (i > 168 && i < 188){
            //   console.log(" list index = " + listIndex + " i = " + i + " offset = " + normalizedDistances[i]*100);
            // }
            if ( normalizedDistances[i] != 0 ) {
              distanceObj.backgroundColor = distanceColor;
            }
            else {
              distanceObj.backgroundColor = "#8B0000";
            }

          }
          distanceObjList.push(distanceObj);
      }
      this.proteinDistanceObjList.push(distanceObjList);
    }
    // console.log(this.proteinDistanceObjList);
    }

    handleResidueClick(event:any){
      var target = event.target || event.srcElement || event.currentTarget;
      var idAttr = target.attributes.id.value;
      var data = idAttr.split("_");

      var listIndex = data[1];
      var resIndex = data[2];
      this.proteinResidueIndex = resIndex;

      this.handleProteinResidueClick();
    }
    // color range generator
    // https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors    //Version 4.0
    lightenDarkenColor(col, amt) {

        var usePound = true;

        if (col[0] == "#") {
            col = col.slice(1);
            usePound = true;
        }

        var num = parseInt(col,16);

        var r = (num >> 16) + amt;

        if (r > 255) r = 255;
        else if  (r < 0) r = 0;

        var b = ((num >> 8) & 0x00FF) + amt;

        if (b > 255) b = 255;
        else if  (b < 0) b = 0;

        var g = (num & 0x0000FF) + amt;

        if (g > 255) g = 255;
        else if (g < 0) g = 0;

        return (usePound?"#":"") + (g | (b << 8) | (r << 16)).toString(16);

    }

    constructor( private showAlignmentService: ShowAlignmentService,
                 private popupModalService: NgbModal,
                 private route:ActivatedRoute,
                 private router: Router,
               ) {
    };

}
