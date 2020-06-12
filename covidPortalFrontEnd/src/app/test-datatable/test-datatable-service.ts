import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile, UploadFolder } from '../models/datafile';
import { AlignmentResultObj } from '../models/alignment';
import {AppSettings} from '../app.settings';

@Injectable()
export class TestDatatableService {

    public testDatatableUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";

    constructor (private http: HttpClient) {}

    testDatatable(selectedAccessions:string[], initialAlignment:boolean): Promise<AlignmentResultObj> {
       return this.http.post(this.testDatatableUrl, {"selectedAccessions":selectedAccessions, "initialAlignment":initialAlignment}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
