import { Component, ViewChild, OnInit, AfterViewInit, OnDestroy, Input, ElementRef} from '@angular/core';
// import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ShowAlignmentService } from './show-alignment-service';
// import { Observable} from 'rxjs';
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

    selectedPDBChainIds:string[];

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
    nomenclaturePositionStrings:string[];
    displayNomenclaturePositionStrings:string[];
    offset:number;
    numRowsInAlignment:number;
    sortSequenceTableColumn:string;

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

   showNext(){
     this.offset += 1;
     console.log(" this.offset " + this.offset);
     // this.setPage({offset: this.offset, pageSize: 3});
     this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
     if (this.offset > 1){
       this.hidePrevButton = false;
     }
   }

   showPrev(){
      if (this.offset > 0){
        this.offset -= 1;
        this.displaySequenceObjList = this.sequenceObjList.slice(this.offset*this.numRowsInPage, (this.offset+1)*this.numRowsInPage );
        // this.setPage({offset: this.offset, pageSize: 3});
        if (this.offset == 0){
          this.hidePrevButton = true;
        }
      }

   }

   reloadSequences(value){
      console.log(value.currentTarget.defaultValue);
      if (value.currentTarget.checked){
        this.selectedAccessions.push(value.currentTarget.defaultValue);

        console.log(this.selectedAccessions);

        this.showAlignmentService.showAlignment(this.selectedAccessions,this.selectedEpitopeIds,this.selectedStructureIds,this.initialAlignment).then(alignmentResult => {
           this.alignmentObjList = alignmentResult.alignmentObjList;
           // this.sequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;
           // this.displaySequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;

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

    /**
     * Populate the table with new data based on the page number
     * @param page The page to select
     */
    setPage(pageInfo) {
      this.isLoading = true;
      this.page.pageNumber = pageInfo.offset;
      this.page.size = pageInfo.pageSize;

      this.getResults(this.page).subscribe(pagedData => {
        console.log (" *** in get results pagedData.data.length " + pagedData.data.length);
        this.page = pagedData.page;

        let rows = this.rows;

        console.log (" rows.length " + rows.length);
        console.log (" pagedData.page.totalElements " + pagedData.page.totalElements);

        if (rows.length !== pagedData.page.totalElements) {
          rows = Array.apply(null, Array(pagedData.page.totalElements));
          rows = rows.map((x, i) => this.rows[i]);
        }

        console.log (" this.page.size " + this.page.size);

        // calc start
        const start = this.page.pageNumber * this.page.size;

        // set rows to our new rows
        pagedData.data.map((x, i) => rows[i + start] = x);
        this.rows = rows;
        this.isLoading = false;
      });

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
      this.numRowsInPage = 3;
      this.numRowsInAlignment = 3;

      this.showAlignmentService.showAlignment(this.selectedAccessions, this.selectedEpitopeIds,this.selectedStructureIds,this.initialAlignment).then(alignmentResult => {
         // console.log(alignmentObjList);
         this.sequences = alignmentResult.sequenceResultObj.sequenceObjList;
         this.alignmentObjList = alignmentResult.alignmentObjList;
         this.sequenceResultObj = alignmentResult.sequenceResultObj;
         this.sequenceTableColumns = this.sequenceResultObj.sequenceTableColumns;
         this.epitopeExperimentTableColumns = alignmentResult.epitopeExperimentResultObj.epitopeExperimentTableColumns;

         this.sequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;
         this.displaySequenceObjList = alignmentResult.sequenceResultObj.sequenceObjList;

         this.epitopeObjList = alignmentResult.epitopeObjList;
         // debugger;
         console.log(" this.epitopeObjList " + this.epitopeObjList);
         // for (let i = 0; i< this.epitopeObjList.length; i++){
         //   console.log(" this.epitopeObjList " + this.epitopeObjList[i].iedb_id);
         // }
         this.displayEpitopeObjList = this.epitopeObjList.slice(0, this.numRowsInPage);

         this.epitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;
         this.displayEpitopeExperimentObjList = alignmentResult.epitopeExperimentResultObj.epitopeExperimentObjList;

         this.selectedAccessions = alignmentResult.selectedAccessions;
         this.nomenclaturePositionStrings = alignmentResult.nomenclaturePositionStrings;

         this.displayNomenclaturePositionStrings = this.nomenclaturePositionStrings.slice(this.startPosition,this.endPosition);

         this.initialAlignment = false;

         this.displaySequenceObjList = this.sequenceObjList.slice(0, this.numRowsInPage);

         this.displayAlignmentObjList = this.alignmentObjList.slice(0,this.numRowsInAlignment);
         this.displayEpitopeObjList = this.epitopeObjList.slice(0,this.numRowsInAlignment);

         this.displayEpitopeExperimentObjList = this.epitopeExperimentObjList.slice(0,this.numRowsInPage);
          // for (let i = 0; i < this.numRowsInPage; i++){
          //     this.rows.push(this.sequenceObjList[i]);
          // }
         // this.rows =
         // this.sequenceObjList.slice(0,9);

         // console.log( " init this.rows len " + this.rows.length);
         //
         // this.setPage({offset: this.offset, pageSize: 3});
         //
         for (let i = 0; i < this.alignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.alignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           // this.displayAignmentObjList[i].residueObjList = this.displayAignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);

           this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
           this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);

           this.displayEpitopeObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.epitopeObjList[i].residueObjList));
           this.displayEpitopeObjList[i].displayResidueObjList = this.epitopeObjList[i].residueObjList.slice(this.startPosition,this.endPosition);

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
