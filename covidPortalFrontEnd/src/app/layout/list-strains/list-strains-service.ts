import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { SequenceObj, SequenceResultObj } from '../../models/sequence';
import {AppSettings} from '../../app.settings';

@Injectable()
export class ListStrainsService {

    public getSequencesUrl = AppSettings.BASE_URL + "/covidPortalApp/listSequences/";

    constructor (private http: HttpClient) {}

    getSequences(): Promise<SequenceResultObj> {
       return this.http.post(this.getSequencesUrl, {responseType: 'text'}).toPromise().then(res => res as SequenceResultObj)
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
