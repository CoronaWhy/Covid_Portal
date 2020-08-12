import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { DatafileDetailService } from './datafile-detail-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Datafile, UploadFolder, UploadFolderSubmitObj } from '../../models/datafile';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';

@Component({
    selector: 'list-files',
    providers: [DatafileDetailService],
    templateUrl: './datafile-detail.component.html',
    styleUrls: ['./datafile-detail.component.scss']
})

export class DatafileDetailComponent implements OnInit, OnDestroy{
    @Input()
    datafile : UploadFolder;
    uploadFolderSubmitObj: UploadFolderSubmitObj;
    fileId:any;
    message:string;
    activeTabTitle:string;
    statusColor:string;
    sub:Subscription;
    firstLoad:boolean;

    filterOptions = [
      { 'id': 0, 'name': 'Uploaded', 'selected':false , 'color':'#EDF59A'},
      { 'id': 1, 'name': 'Analysis Submitted', 'selected':false , 'color':'#CBF022'},
      { 'id': 2, 'name': 'Score Calculated', 'selected':false , 'color':'#32FFC8'},
      { 'id': 3, 'name': 'Analysis Completed', 'selected':false , 'color':'#36CBEC'},
    ];

    ngOnDestroy(){
        this.sub.unsubscribe();
    }

    ngOnInit() {
      this.route.paramMap.subscribe(params => {
        this.fileId = (params.get("fileId")).toString();
        this.message = "";

      });

      this.activeTabTitle = "Metadata";
      this.statusColor='#EDF59A';
      this.firstLoad = true;
      this.sub = Observable.interval(1000)
        .subscribe((val) => {
          this.datafileDetailService.getDatafile(this.fileId).then(datafile => {
              console.log("fetched data " + this.firstLoad);
              if (this.firstLoad){
                this.datafile = datafile;
                this.firstLoad = false;
              }
              else{
                this.datafile.logs = datafile.logs;
              }
              this.firstLoad = false;
              if ( this.datafile.status == "Uploaded" ) {
                this.activeTabTitle = "Analysis_Submit";
              }
              if ( this.datafile.status == "Analysis Submitted" ) {
                this.statusColor = this.datafile.rowColor;
              }
          });

      });

    }

    submitAnalysis(event:any){
      this.datafileDetailService.submitAnalysis(this.datafile.analysisProtocol, this.datafile.fileType, this.datafile.id).then((uploadFolderSubmitObj) =>
      {

          this.uploadFolderSubmitObj = uploadFolderSubmitObj;
          this.datafile = this.uploadFolderSubmitObj.uploadFolder;
          this.statusColor = this.datafile.rowColor;
          this.message = this.uploadFolderSubmitObj.message;

      }
      );
    }

    constructor( private datafileDetailService: DatafileDetailService,
                 private route: ActivatedRoute,
               ) {
    };
}
