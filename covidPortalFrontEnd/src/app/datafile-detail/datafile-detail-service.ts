import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile} from '../../models/datafile';
import 'rxjs/add/operator/toPromise';
import {AppSettings} from '../../app.settings';
@Injectable()
export class DatafileDetailService {

    public getDatafilesUrl = AppSettings.BASE_URL + "/striatumPortalApp/getDatafile/";
    public submitAnalysisUrl = AppSettings.BASE_URL + "/striatumPortalApp/submitAnalysis/";
    public updateDatafileNameUrl = AppSettings.BASE_URL + "/striatumPortalApp/updateDatafileName/";
    public reloadDatafileUrl = AppSettings.BASE_URL + "/striatumPortalApp/reloadDatafile/";

    constructor (private http: HttpClient) {}

    getDatafile(datafileId:any): Promise<Datafile> {
     return this.http.post(this.getDatafilesUrl, {"datafileId":datafileId}).toPromise().then(res => res)
       .catch(this.handleError);
   }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
