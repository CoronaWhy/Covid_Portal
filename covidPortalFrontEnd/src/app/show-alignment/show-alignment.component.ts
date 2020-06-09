import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ShowAlignmentService } from './show-alignment-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Datafile, UploadFolder } from '../models/datafile';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';
import { AlignmentObj, ResidueObj } from '../models/alignment';
import { ActivatedRoute, Params, Routes, Router } from '@angular/router';
import { Options } from 'ng5-slider';

@Component({
    selector: 'list-files',
    providers: [ShowAlignmentService],
    templateUrl: './show-alignment.component.html',
    styleUrls: ['./show-alignment.component.scss']
})

export class ShowAlignmentComponent implements OnInit, OnDestroy{

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
    selectedAccessions:string[];
    rangeSliderOptions: Options = {
    floor: 0,
    ceil: 10,
    vertical: true
    };
    rowNum:number;
    indexValue:number;
    maxVerticalSliderValue:number;
    verticalSliderValue:number;

    setVerticalSliderValue(event){
      let verticalSlider = document.getElementById('verticalSlider') as HTMLInputElement;
      this.verticalSliderValue = Number(verticalSlider.value);
      console.log(" index verticalSliderValue " + this.verticalSliderValue);
      let startIndex = 10-this.verticalSliderValue;
      this.displayAlignmentObjList = this.alignmentObjList.slice(startIndex,startIndex+3);

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
        // this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
        this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].residueObjList.slice(this.startPosition+this.positionSliderValue,this.startPosition+this.positionSliderValue+this.maxDisplayResidues);
      }
    }

    ngOnInit() {
      console.log( " on init ");

      this.route.paramMap.subscribe(params => {
        this.selectedAccessions = params["selectedAccessions"];
        console.log(this.selectedAccessions);
      })

      this.rowNum = 0;
      this.indexValue = 0;
      this.message = "";
      this.startPosition = 0;
      this.maxDisplayResidues = 60;
      this.endPosition = this.maxDisplayResidues;
      this.positionSliderValue = 0;

      this.maxVerticalSliderValue = 10;
      this.verticalSliderValue = 10;

      this.showAlignmentService.showAlignment().then(alignmentObjList => {
         // console.log(alignmentObjList);
         this.alignmentObjList = alignmentObjList;
         this.displayAlignmentObjList = this.alignmentObjList.slice(0,3);
         for (let i = 0; i < this.alignmentObjList.length; i++){
           if (i == 0){
             this.maxSliderValue = this.alignmentObjList[i].residueObjList.length - this.maxDisplayResidues;
           }
           // this.displayAignmentObjList[i].residueObjList = this.displayAignmentObjList[i].residueObjList.slice(this.startPosition,this.endPosition);
           this.alignmentObjList[i].displayResidueObjList = JSON.parse(JSON.stringify(this.alignmentObjList[i].residueObjList));
           this.alignmentObjList[i].displayResidueObjList = this.alignmentObjList[i].displayResidueObjList.slice(this.startPosition,this.endPosition);
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
