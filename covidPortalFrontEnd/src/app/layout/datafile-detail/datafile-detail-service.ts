import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile, UploadFolder, UploadFolderSubmitObj } from '../../models/datafile';
import 'rxjs/add/operator/toPromise';
import {AppSettings} from '../../app.settings';

@Injectable()
export class DatafileDetailService {

    public getDatafilesUrl = AppSettings.BASE_URL + "/covidPortalApp/getDatafile/";
    public submitAnalysisUrl = AppSettings.BASE_URL + "/covidPortalApp/submitAnalysis/";
    public updateDatafileNameUrl = AppSettings.BASE_URL + "/covidPortalApp/updateDatafileName/";

    // private message:string;
    constructor (private http: HttpClient) {}

    getDatafile(datafileId:any): Promise<UploadFolder> {
     return this.http.post(this.getDatafilesUrl, {"datafileId":datafileId}).toPromise().then(res => res)
       .catch(this.handleError);
   }

   submitAnalysis(analysisProtocol:string, fileType:string, datafileId:string): Promise<UploadFolderSubmitObj> {
     return this.http.post(this.submitAnalysisUrl, {"datafileId":datafileId,"analysisProtocol":analysisProtocol, "fileType":fileType}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    updateDatafileName(datafileName:string, uploadFolderId:string): Promise<string> {
     return this.http.post(this.updateDatafileNameUrl, {"datafileName":datafileName, "uploadFolderId":uploadFolderId}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
