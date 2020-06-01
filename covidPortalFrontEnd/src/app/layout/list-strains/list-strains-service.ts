import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { SequenceObj } from '../../models/sequence';
import {AppSettings} from '../../app.settings';

@Injectable()
export class ListStrainsService {

    public getSequencesUrl = AppSettings.BASE_URL + "/covidPortalApp/listSequences/";

    constructor (private http: HttpClient) {}

    getSequences(): Promise<SequenceObj[]> {
       return this.http.post(this.getSequencesUrl, {}).toPromise().then(res => res as SequenceObj[])
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
