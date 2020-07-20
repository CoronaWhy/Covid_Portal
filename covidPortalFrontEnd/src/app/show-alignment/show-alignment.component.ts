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
import { EpitopeObj, EpitopeExperimentObj, EpitopeExperimentResultObj } from '../models/epitope';
import { StructureObj, StructureChainObj, StructureChainResultObj } from '../models/structure';
import { ActivatedRoute, Params, Routes, Router } from '@angular/router';
import { Options } from 'ng5-slider';
import { Page } from '../models/page';
import { PagedData } from '../models/page-data';
import { of } from 'rxjs';
import { TableColumnObj } from '../models/tableColumn';

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
    alignmentObjList:AlignmentObj[];
    displayAlignmentObjList:AlignmentObj[];
    maxDisplayResidues :number;
    startPosition:number;
    endPosition:number;
    maxSliderValue:number;
    searchDataFilesString:string;
    positionSliderValue:number;
    sequenceTableColumnObjs:TableColumnObj[];

    selectedAccessions:string[];
    selectedEpitopeIds:string[];
    selectedStructureIds:string[];

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
    sequenceObjList:SequenceObj[];

    epitopeObjList:EpitopeObj[];
    displayEpitopeObjList:EpitopeObj[];

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

    structureChainObjList:StructureChainObj[];
    displayStructureChainObjList:StructureChainObj[];
    structureChainTableColumnObjs:TableColumnObj[];

    initialAlignment: boolean;
    searchString:string;
    numRowsInPage:number;

    hidePrevButton: boolean;
    hideNextButton: boolean;

    epitopeHidePrevButton: boolean;
    epitopeHideNextButton: boolean;

    structureHidePrevButton: boolean;
    structureHideNextButton: boolean;

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

    @ViewChild('sequenceTable') sequenceTable;

    /**
     * A method that mocks a paged server response
     * @param page The selected page
     * @returns {any} An observable containing the employee data
     */
    public getResults(page: Page): Observable<PagedData<SequenceObj>> {
        return Observable.of(this.sequenceObjList).map(data => this.getPagedData(page));
    }

   sortSequenceTable (sortColumn)
   {
     if (this.sequenceSortColumn != sortColumn) {
         console.log(sortColumn);
         this.sequenceSortColumn = sortColumn;
         if (sortColumn == "organism") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.organism > b.sequenceObj.organism) ? 1 : -1);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.organism;
           }
         }
         else if (sortColumn == "host") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.host > b.sequenceObj.host) ? 1 : -1);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.host;
           }
         }
         else if (sortColumn == "taxon_name") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.taxon > b.sequenceObj.taxon) ? 1 : -1)
           for (let i = 0; i < this.alignmentObjList.length; i++){
             console.log(this.alignmentObjList[i].sequenceObj.taxon);
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.taxon;
           }
         }
         else if (sortColumn == "accession") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.organism > b.sequenceObj.organism) ? 1 : -1);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.accession;
           }
         }
         else if (sortColumn == "country") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.country > b.sequenceObj.country) ? 1 : -1);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.country;
           }
         }
         else if (sortColumn == "isolation_source") {
           this.alignmentObjList.sort((a, b) => (a.sequenceObj.isolate > b.sequenceObj.isolate) ? 1 : -1);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             this.alignmentObjList[i].sortColumnValue = this.alignmentObjList[i].sequenceObj.isolate;
           }
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

   sortEpitopeTable (sortColumn)
   {
       if (this.epitopeSortColumn != sortColumn) {
           console.log(sortColumn);
           this.epitopeSortColumn = sortColumn;
           if (sortColumn == "host") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.host > b.epitopeExperimentObj.host) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.host;
             }
           }
           else if (sortColumn == "assay_result") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.assay_result > b.epitopeExperimentObj.assay_result) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.assay_result;
             }
           }
           else if (sortColumn == "mhc_allele") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.mhc_allele > b.epitopeExperimentObj.mhc_allele) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.mhc_allele;
             }
           }
           else if (sortColumn == "mhc_class") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.mhc_class > b.epitopeExperimentObj.mhc_class) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.mhc_class;
             }
           }
           else if (sortColumn == "exp_method") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.exp_method > b.epitopeExperimentObj.exp_method) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.exp_method;
             }
           }
           else if (sortColumn == "measurement_type") {
             this.epitopeObjList.sort((a, b) => (a.epitopeExperimentObj.measurement_type > b.epitopeExperimentObj.measurement_type) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].epitopeExperimentObj.measurement_type;
             }
           }
           else if (sortColumn == "iedb_id") {
             this.epitopeObjList.sort((a, b) => (a.iedb_id > b.iedb_id) ? 1 : -1);
             for (let i = 0; i < this.epitopeObjList.length; i++){
               this.epitopeObjList[i].sortColumnValue = this.epitopeObjList[i].iedb_id;
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
         if (sortColumn == "taxon") {
           this.structureObjList.sort((a, b) => (a.structureChainObj.taxon > b.structureChainObj.taxon) ? 1 : -1);
           for (let i = 0; i < this.epitopeObjList.length; i++){
             this.structureObjList[i].sortColumnValue = this.structureObjList[i].structureChainObj.taxon;
           }
         }
         else if (sortColumn == "pdb_id") {
           this.structureObjList.sort((a, b) => (a.structureChainObj.pdb_id > b.structureChainObj.pdb_id) ? 1 : -1);
           for (let i = 0; i < this.structureObjList.length; i++){
             this.structureObjList[i].sortColumnValue = this.structureObjList[i].structureChainObj.pdb_id;
           }
         }
         else if (sortColumn == "chain") {
           this.structureObjList.sort((a, b) => (a.structureChainObj.chain > b.structureChainObj.chain) ? 1 : -1);
           for (let i = 0; i < this.structureObjList.length; i++){
             this.structureObjList[i].sortColumnValue = this.structureObjList[i].structureChainObj.chain;
           }
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

          if (sortColumn == "accession") {
            this.sequenceObjList.sort((a, b) => (a.accession > b.accession) ? 1 : -1);
          }
          else if (sortColumn == "organism") {
            this.sequenceObjList.sort((a, b) => (a.organism > b.organism) ? 1 : -1);
          }
          else if (sortColumn == "collection_date") {
            this.sequenceObjList.sort((a, b) => (a.collection_date > b.collection_date) ? 1 : -1);
          }
          else if (sortColumn == "country") {
            this.sequenceObjList.sort((a, b) => (a.country > b.country) ? 1 : -1);
          }
          else if (sortColumn == "host") {
            this.sequenceObjList.sort((a, b) => (a.host > b.host) ? 1 : -1);
          }
          else if (sortColumn == "isolation_source") {
            this.sequenceObjList.sort((a, b) => (a.isolation_source > b.isolation_source) ? 1 : -1);
          }
          else if (sortColumn == "coded_by") {
            this.sequenceObjList.sort((a, b) => (a.coded_by > b.coded_by) ? 1 : -1);
          }
          else if (sortColumn == "protein") {
            this.sequenceObjList.sort((a, b) => (a.protein > b.protein) ? 1 : -1);
          }
          else if (sortColumn == "taxon") {
            this.sequenceObjList.sort((a, b) => (a.taxon > b.taxon) ? 1 : -1);
          }
          else if (sortColumn == "isolate") {
            this.sequenceObjList.sort((a, b) => (a.isolate > b.isolate) ? 1 : -1);
          }

          this.displaySequenceObjList = this.sequenceObjList.slice(0,this.numRowsInAlignment);

       }
    }

    sortEpitopeExperimentTable (sortColumn)
    {
      // if (this.epitopeTableSortColumn != sortColumn) {
      //     console.log(sortColumn);
      //
      //     this.epitopeTableSortColumn = sortColumn;
      //
      //     if (sortColumn == "host") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.host > b.host) ? 1 : -1);
      //     }
      //     else if (sortColumn == "assay_type") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.assay_type > b.assay_type) ? 1 : -1);
      //     }
      //     else if (sortColumn == "assay_result") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.assay_result > b.assay_result) ? 1 : -1);
      //     }
      //     else if (sortColumn == "mhc_allele") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.mhc_allele > b.mhc_allele) ? 1 : -1);
      //     }
      //     else if (sortColumn == "mhc_class") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.mhc_class > b.mhc_class) ? 1 : -1);
      //     }
      //     else if (sortColumn == "exp_method") {
      //       this.epitopeExperimentObjList.sort((a, b) => (a.exp_method > b.exp_method) ? 1 : -1);
      //     }
      //
      //     this.displayEpitopeExperimentObjList = this.sequenceObjList.slice(0,this.numRowsInAlignment);
      //
      //  }
    }

    sortStructureChainTable (sortColumn)
    {
      // if (this.structureTableSortColumn != sortColumn) {
      //     console.log(sortColumn);
      //
      //     this.structureTableSortColumn = sortColumn;
      //
      //     if (sortColumn == "accessiohn") {
      //       this.structureChainjList.sort((a, b) => (a.accession > b.accession) ? 1 : -1);
      //     }
      //     else if (sortColumn == "organism") {
      //       this.structureChainjList.sort((a, b) => (a.accession > b.accession) ? 1 : -1);
      //     }
      //     else if (sortColumn == "collection_date") {
      //       this.structureChainjList.sort((a, b) => (a.accession > b.accession) ? 1 : -1);
      //     }
      //
      //     this.displayStructureChainjList = this.structureChainjList.slice(0,this.numRowsInAlignment);
      //
      //  }
    }

   showNext(){
     this.offset += 1;
     console.log(" this.offset " + this.offset);
     this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
     if (this.offset > 1){
       this.hidePrevButton = false;
     }

   }

   showPrev(){

      if (this.offset > 0){
        this.offset -= 1;
        this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
        if (this.offset == 0){
          this.hidePrevButton = true;
        }
      }

   }

   showEpitopeNext(){

     this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInPage);
     this.displayStructureChainObjList = this.structureChainObjList.slice(0,this.numRowsInPage);

     this.epitopeOffset += 1;
     console.log(" this.epitopeOffset " + this.epitopeOffset);
     this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.epitopeOffset*this.numRowsInPage, (this.epitopeOffset+1)*this.numRowsInPage );
     if (this.epitopeOffset > 1){
       this.epitopeHidePrevButton = false;
     }

    }

    showEpitopePrev(){

      if (this.epitopeOffset > 0){
        this.epitopeOffset -= 1;
        this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(this.epitopeOffset*this.numRowsInPage, (this.epitopeOffset+1)*this.numRowsInPage );
        if (this.epitopeOffset == 0){
          this.epitopeHidePrevButton = true;
        }
      }

    }

    showStructureNext(){

      this.structureOffset += 1;
      console.log(" this.structureOffset " + this.structureOffset);
      this.displayStructureChainObjList = this.structureChainObjList.slice(this.structureOffset*this.numRowsInPage, (this.structureOffset+1)*this.numRowsInPage );
      if (this.structureOffset > 1){
        this.structureHidePrevButton = false;
      }

     }

     showStructurePrev(){

       if (this.structureOffset > 0){
         this.structureOffset -= 1;
         this.displayStructureChainObjList = this.structureChainObjList.slice(this.structureOffset*this.numRowsInPage, (this.structureOffset+1)*this.numRowsInPage );
         if (this.epitopeOffset == 0){
           this.structureHidePrevButton = true;
         }
       }

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
             this.displayAlignmentObjList[i].displayResidueObjList = this.displayAlignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           }
        });
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
             this.displayEpitopeObjList[i].displayResidueObjList = this.displayEpitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           }
        });
      }
    }

    reloadStructures(value){
      console.log(value.currentTarget.defaultValue);
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
             this.displayStructureObjList[i].displayResidueObjList = this.displayStructureObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           }
        });
      }
    }

    filterDatatable(){

      this.sequenceObjList = this.sequenceObjList.filter(
        sequenceObj => sequenceObj.accession.includes(this.searchString));

      this.displaySequenceObjList = this.sequenceObjList.slice(0, this.numRowsInPage);
      console.log(this.displaySequenceObjList);

     }
    /**
     * Package companyData into a PagedData object based on the selected Page
     * @param page The page data used to get the selected data from companyData
     * @returns {PagedData<SequenceObj>} An array of the selected data and page
     */
    private getPagedData(page: Page): PagedData<SequenceObj> {
        let pagedData = new PagedData<SequenceObj>();
        console.log ( " in paged data " + this.sequenceObjList.length);
        // page.totalElements = this.sequenceObjList.length;
        page.totalElements = this.numRowsInPage;
        console.log(" page.totalElements " + page.totalElements );
        page.totalPages = page.totalElements / page.size;
        let start = page.pageNumber * page.size;
        let end = Math.min((start + page.size), page.totalElements);
        for (let i = start; i < end; i++){
            // let jsonObj = this.sequenceObjList[i];
            // let employee = new CorporateEmployee(jsonObj.name, jsonObj.gender, jsonObj.company, jsonObj.age);
            pagedData.data.push(this.sequenceObjList[i]);
        }
        console.log(" len pagedData.data " +   pagedData.data.length );

        pagedData.page = page;
        return pagedData;
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

      this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);

      // for (let i = 0; i < this.alignmentObjList.length; i++){
      //   this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      // }
      //
      // for (let i = 0; i < this.epitopeObjList.length; i++){
      //   this.epitopeObjList[i].displayResidueObjList = this.epitopeObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      // }
      //
      // for (let i = 0; i < this.structureObjList.length; i++){
      //   this.structureObjList[i].displayResidueObjList = this.structureObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      //   // console.log(this.structureObjList[i].residueObjList);
      // }
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

    ngOnInit() {
      console.log( " on init ");

      // this.route.paramMap.subscribe(params => {
      //   this.selectedAccessions = params["selectedAccessions"];
      //   console.log(this.selectedAccessions);
      // })

      this.isLoading = false;
      this.sequenceTableSortColumn = "accession";
      this.hidePrevButton = true;
      this.hideNextButton = false;

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

      this.selectedAccessions = [];

      this.selectedEpitopeIds = [];
      this.selectedStructureIds = [];

      this.initialAlignment = true;

      this.searchString = '';

      this.offset = 0;
      this.epitopeOffset = 0;
      this.structureOffset = 0;

      this.numRowsInPage = 3;
      this.numRowsInAlignment = 3;

      // this.sortSequenceTableColumn = '';
      // this.sortStructureChainTableColumn = '';
      // this.sortEpitopeExperimentTableColumn = '';

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

         console.log(this.sequenceTableColumnObjs);
         // console.log(this.structureChainTableColumns);
         this.sequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;
         this.displaySequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;

         this.structureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;
         this.displayStructureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;

         this.alignmentObjList = alignmentResult.alignmentObjList;
         this.epitopeObjList = alignmentResult.epitopeObjList;
         this.structureObjList = alignmentResult.structureObjList;

         console.log( " this.structureObjList " + this.structureObjList);

         this.epitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;
         this.displayEpitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;

         this.selectedAccessions = alignmentResult.selectedAccessions;
         this.selectedEpitopeIds = alignmentResult.selectedEpitopeIds;
         this.selectedStructureIds = alignmentResult.selectedStructureIds;

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
          console.log(this.displayStructureObjList[i].residueObjList);
        }


         // console.log(this.displayAignmentObjList);
      });
    }


    handleResidueClick(event:any){
      var target = event.target || event.srcElement || event.currentTarget;
      var idAttr = target.attributes.id.value;
      var data = idAttr.split("_");

      var listIndex = data[1];
      var resIndex = data[2];

      // console.log(" listIndex " + listIndex);
      // console.log(" resIndex " + resIndex);

      //   console.log( " position " + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.x + " " + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.y + " "
      // + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.z );
      //
      //   let selectedPosition = [this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.x , this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.y ,
      //   this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.z]

      console.log( " position " + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.x + " " + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.y + " "
    + this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.z );

      let selectedPosition = [this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.x , this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.y ,
      this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition.z]

      let distances:number[];
      let distance = 0;
      distances = [];
      for (let i = 0; i < this.displayStructureObjList[listIndex].residueObjList.length; i++){
        // console.log(this.displayStructureObjList[listIndex].displayResidueObjList[resIndex].residuePosition);
         distance = 0;
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

         // console.log(" i = " + i + " distance = " + distance);
      }

      console.log(" distances = " + distances.length);

      // normalise to 0 and 1
      let maxDistance = Math.max(...distances);
      let minDistance = Math.min(...distances);
      let rangeDistance = maxDistance - minDistance;

      let normalizedDistances = [];

      for (let i = 0; i < distances.length; i++){
        normalizedDistances.push (
          1- (distances[i] - minDistance)/rangeDistance
        );
      }

      console.log(" normalizedDistances length " + normalizedDistances.length);

      let baseColor = "#B95119";

      // let t = 'rgb(255,255,0)';
      // let f = 'rgb(0,0.100)';
      //
      // let tr = document.getElementById("tr_0");

      for (let i = 0; i< normalizedDistances.length; i++){

        // console.log( " i = " + i + " val " + normalizedDistances[i]*100);
        console.log( " i = " + i );

        let td = document.getElementById("td_0_"+ i);

        if(td){

          if (this.displayStructureObjList[listIndex].residueObjList[i].residueValue != '-'){

            td.style.backgroundColor = this.lightenDarkenColor(baseColor, normalizedDistances[i]*100);

            // console.log( " bkgcolor = " + td.style.backgroundColor );
          }

        }

      }

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
                 private route:ActivatedRoute,
                 private router: Router,
               ) {
    };

}
