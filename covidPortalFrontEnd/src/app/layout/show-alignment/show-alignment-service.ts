import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile, UploadFolder } from '../../models/datafile';
import { AlignmentObj, ResidueObj } from '../../models/alignment';

import {AppSettings} from '../../app.settings';

@Injectable()
export class ShowAlignmentService {

    public showAlignmentUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";
    public searchDatafilesUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";
    public getDatafilesUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";
    public deleteDatafileUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";

    public getSequenceUrl = AppSettings.BASE_URL + "/explorer/sequences";

    constructor (private http: HttpClient) {}

    // getSequence(): Promise<SequenceObj[]> {
    //     let headers = new HttpHeaders();
    //     headers.append('Content-Type', 'application/json');
    //     let params = new HttpParams().set("mesh_id",'D064370').set("alignment",'20200505').set("accession",'ACJ66971.1');
    //     return this.http.get(
    //         this.getSequenceUrl,
    //         { headers: headers, params: params}
    //     ).toPromise().then(res => res)
    //     .catch(this.handleError);
    // }

    showAlignment(): Promise<AlignmentObj[]> {
       return this.http.post(this.showAlignmentUrl, {}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    // the following are functions that we might not need
    getDatafiles(): Promise<UploadFolder[]> {
      return this.http.post(this.getDatafilesUrl, {}).toPromise().then(res => res as UploadFolder[]).catch(this.handleError);
    }

    deleteDatafile(datafileId:string): Promise<string> {
       return this.http.post(this.deleteDatafileUrl, {"datafileId":datafileId}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    searchDatafiles(searchString:string): Promise<UploadFolder[]> {
       return this.http.post(this.searchDatafilesUrl, {"searchString":searchString}).toPromise().then(res => res as UploadFolder[])
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
