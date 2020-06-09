import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ListStrainsService } from './list-strains-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { SequenceObj, SequenceResultObj } from '../models/sequence';
import { ActivatedRoute, Params, Routes, Router } from '@angular/router';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';
// import {NgTableComponent, NgTableFilteringDirective, NgTablePagingDirective, NgTableSortingDirective} from '@swimlane/ngx-datatable';
import { ColumnMode } from '@swimlane/ngx-datatable';

@Component({
    selector: 'list-files',
    providers: [ListStrainsService],
    templateUrl: './list-strains.component.html',
    styleUrls: ['./list-strains.component.scss']
})

export class ListStrainsComponent implements OnInit, OnDestroy{

    @Input()
    filterFilesOption:string;
    resultsAvailable:boolean;
    sub:Subscription;
    message:string;
    sequenceObjList:SequenceObj[];
    sequenceResultObj:SequenceResultObj;
    selectedAccessions:string[];
    filterOptions = [
    ];

    searchDataFilesString:string;

    rowCount:number;
    pageSize:number;
    selectedCount:number;
    curPage:number;
    offset:number;
    isVisible:boolean;
    selectedMessage:string;
    sequenceTablecolumns:string[];

    pageLimit:number;

    ngOnDestroy(){
        // this.sub.unsubscribe();
    }


    ColumnMode = ColumnMode;

    ngOnInit() {
      console.log( " on init ");

      this.pageSize = 10;
      this.selectedCount = 0;
      this.curPage = 1;
      this.offset = 0;
      this.isVisible = true;
      this.selectedMessage = "";

      this.pageLimit = 10;

      this.message = "";
      this.selectedAccessions= [];
      this.listStrainsService.getSequences().then(sequenceResultObj => {
          this.sequenceResultObj = sequenceResultObj;
          this.rowCount = this.sequenceResultObj.sequenceObjList.length;
          this.sequenceTablecolumns = this.sequenceResultObj.sequenceTableColumns;
      });
    }

    submitSequences(){
      console.log(" in submit ");
      let selectedSequences :SequenceObj[];
      selectedSequences = this.sequenceResultObj.sequenceObjList.filter(
          sequenceObj => sequenceObj.isSelected === true);
        console.log(selectedSequences);
      for (let i = 0; i< selectedSequences.length; i++){
        this.selectedAccessions.push(selectedSequences[i].accession);
      }
      console.log(this.selectedAccessions);

      this.router.navigate(['show-alignment'], { queryParams: { 'selectedAccessions': this.selectedAccessions } })

      // this.listStrainsService.getSequences().then(sequenceObjList => {
      //     this.sequenceObjList = sequenceObjList;
      // });

    }

    deleteDatafile(event:any){

      // if (confirm("Are you sure you want to delete this file?")){
      //   var target = event.target || event.srcElement || event.currentTarget;
      //   var idAttr = target.attributes.id;
      //   var value = idAttr.nodeValue;
      //   var datafileId = value.split("_")[2]
      //   this.listStrainsService.deleteDatafile(datafileId).then((message) =>
      //   {
      //       this.message = message;
      //   }
      //   );
      //   this.listStrainsService.getDatafiles().then(datafiles => {
      //       this.datafiles = datafiles;
      //       this.allDatafiles = datafiles;
      //   });
      // }
    }

    filterDataFiles(){
      // console.log(" in filter 1 " + this.datafiles);
      // if (!this.filterFilesOption || this.filterFilesOption == "") {
      //   return;
      // }
      // this.datafiles = this.allDatafiles.filter(s => {
      //   if (this.filterFilesOption != ""){
      //     return s.status == this.filterFilesOption;
      // } else {
      //   return true;
      // }
      // });
      // console.log(" in filter 2 " + this.datafiles);
    }

    constructor( private listStrainsService: ListStrainsService,
                 private route:ActivatedRoute,
                 private router: Router,
               ) {
    };
}
