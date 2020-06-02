import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { ListStrainsService } from './list-strains-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { SequenceObj } from '../../models/sequence';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';

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
    selectedAccessions:string[];
    filterOptions = [
    ];

    searchDataFilesString:string;

    ngOnDestroy(){
        // this.sub.unsubscribe();
    }

    ngOnInit() {
      console.log( " on init ");
      this.message = "";
      this.selectedAccessions= [];
      this.listStrainsService.getSequences().then(sequenceObjList => {
          this.sequenceObjList = sequenceObjList;
      });
    }

    submitSequences(){
      console.log(" in submit ");
      let selectedSequences :SequenceObj[];
      selectedSequences = this.sequenceObjList.filter(
          sequenceObj => sequenceObj.isSelected === true);
        console.log(selectedSequences);
      for (let i = 0; i< selectedSequences.length; i++){
        this.selectedAccessions.push(selectedSequences[i].accession);
      }
      console.log(this.selectedAccessions);
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
               ) {
    };
}
