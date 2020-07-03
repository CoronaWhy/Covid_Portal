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
    sequenceTableColumns:string[];

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
    epitopeExperimentTableColumns:string[];

    structureChainObjList:StructureChainObj[];
    displayStructureChainObjList:StructureChainObj[];
    structureChainTableColumns:string[];

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
    sortSequenceTableColumn:string;
    sortStructureChainTableColumn:string;
    sortEpitopeExperimentTableColumn:string;
    epitopeVerticalSliderValue:number;

    @ViewChild('sequenceTable') sequenceTable;

    /**
     * A method that mocks a paged server response
     * @param page The selected page
     * @returns {any} An observable containing the employee data
     */
    public getResults(page: Page): Observable<PagedData<SequenceObj>> {
        return Observable.of(this.sequenceObjList).map(data => this.getPagedData(page));
    }

   sortSequenceTable ()
   {

   }
   sortEpitopeTable ()
   {

   }
   sortStructureChainTable(){}

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
        this.selectedAccessions.push(value.currentTarget.defaultValue);

        console.log(this.selectedAccessions);

        this.showAlignmentService.reloadAlignment(this.selectedAccessions).then(alignmentObjList => {
           for (let i = 0; i< alignmentObjList.length; i++){
             this.alignmentObjList.push(alignmentObjList[i]);
           }
           this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.alignmentObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.alignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
             this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
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
          for (let i = 0; i< epitopeObjList.length; i++){
            this.epitopeObjList.push(epitopeObjList[i]);
          }

           this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.epitopeObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.epitopeObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.epitopeObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.epitopeObjList[i].residueObjList));
             this.epitopeObjList[i].displayResidueObjList = this.epitopeObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
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
          for (let i = 0; i< structureObjList.length; i++){
            this.structureObjList.push(structureObjList[i]);
          }

           console.log(" structureObjList " + structureObjList);
           this.displayStructureObjList = this.structureObjList.slice(0,this.numRowsInAlignment);
           for (let i = 0; i < this.structureObjList.length; i++){
             if (i == 0){
               this.maxSliderValue = this.structureObjList[i].residueObjList.length - this.maxDisplayResidues;
             }
             this.structureObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.structureObjList[i].residueObjList));
             this.structureObjList[i].displayResidueObjList = this.structureObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
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
      console.log(" index verticalSliderValue " + this.verticalSliderValue);
      let startIndex = 10-this.verticalSliderValue;
      this.displayAlignmentObjList = this.alignmentObjList.slice(startIndex,startIndex+this.numRowsInPage);

    }

    setEpitopeVerticalSliderValue (event) {
      let verticalSlider = document.getElementById('epitopeVerticalSlider') as HTMLInputElement;
      this.verticalSliderValue = Number(verticalSlider.value);
      console.log(" index verticalSliderValue " + this.verticalSliderValue);
      let startIndex = 10-this.verticalSliderValue;
      this.displayEpitopeObjList = this.epitopeObjList.slice(startIndex,startIndex+this.numRowsInPage);

    }

    setStructureVerticalSliderValue (event) {
      let verticalSlider = document.getElementById('structureVerticalSlider') as HTMLInputElement;
      this.verticalSliderValue = Number(verticalSlider.value);
      console.log(" index verticalSliderValue " + this.verticalSliderValue);
      let startIndex = 10-this.verticalSliderValue;
      this.displayStructureObjList = this.structureObjList.slice(startIndex,startIndex+this.numRowsInPage);

    }

    sliderValueChange(event){
      console.log(" index value " + this.indexValue);
    }

    ngOnDestroy(){
    }

    setSliderValue(){
      let positionSlider = document.getElementById('positionSlider') as HTMLInputElement;
      this.positionSliderValue = Number(positionSlider.value);
      for (let i = 0; i < this.alignmentObjList.length; i++){
        this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
        this.epitopeObjList[i].displayResidueObjList = this.epitopeObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
        this.structureObjList[i].displayResidueObjList = this.structureObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);

        this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);

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

      this.sortSequenceTableColumn = '';
      this.sortStructureChainTableColumn = '';
      this.sortEpitopeExperimentTableColumn = '';

      this.showAlignmentService.showAlignment().then(alignmentResult => {
         // console.log(alignmentObjList);
         this.sequences = alignmentResult.sequenceResultObj.sequenceObjList;

         this.sequenceResultObj = alignmentResult.sequenceResultObj;
         this.sequenceTableColumns = this.sequenceResultObj.sequenceTableColumns;
         this.structureChainTableColumns = alignmentResult.structureChainResultObj.structureChainTableColumns;

         console.log(this.structureChainTableColumns);
         this.sequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;
         this.displaySequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;

         this.structureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;
         this.displayStructureChainObjList = alignmentResult.structureChainResultObj.structureChainObjList;

         this.alignmentObjList = alignmentResult.alignmentObjList;
         this.epitopeObjList = alignmentResult.epitopeObjList;
         this.structureObjList = alignmentResult.structureObjList;

         console.log( " this.structureObjList " + this.structureObjList);

         this.epitopeExperimentTableColumns = alignmentResult.epitopeExperimentResultObj.epitopeExperimentTableColumns;
         this.epitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;
         this.displayEpitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;

         this.selectedAccessions = alignmentResult.selectedAccessions;
         this.nomenclaturePositionStrings = alignmentResult.nomenclaturePositionStrings;

         this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition,this.endPosition);

         this.initialAlignment = false;

         this.displaySequenceObjList = this.sequenceObjList.slice(0, this.numRowsInPage);
         this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
         this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);
         this.displayStructureObjList = this.structureObjList.slice(0,this.numRowsInAlignment);

         this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInPage);
         this.displayStructureChainObjList = this.structureChainObjList.slice(0,this.numRowsInPage);

         for (let i = 0; i < this.alignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.alignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           // not needed to slice need to remove after testing
           this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
           this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
           // console.log(this.displayAignmentObjList[i].residueObjList);
         }

         for (let i = 0; i < this.epitopeObjList.length; i++){

           // not needed to slice need to remove after testing
           this.displayEpitopeObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.epitopeObjList[i].residueObjList));
           this.displayEpitopeObjList[i].displayResidueObjList = this.epitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           // console.log(this.displayAignmentObjList[i].residueObjList);
         }


        for (let i = 0; i < this.structureObjList.length; i++){

           // not needed to slice need to remove after testing
           this.displayStructureObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.structureObjList[i].residueObjList));
           this.displayStructureObjList[i].displayResidueObjList = this.structureObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
          // console.log(this.displayAignmentObjList[i].residueObjList);
        }


         // console.log(this.displayAignmentObjList);
      });
    }


    handleResidueClick(residueLabel, position){

    }

    constructor( private showAlignmentService: ShowAlignmentService,
                 private route:ActivatedRoute,
                 private router: Router,
               ) {
    };

}
