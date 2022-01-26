import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile} from '../../models/datafile';
import 'rxjs/add/operator/toPromise';
import {AppSettings} from '../../app.settings';
@Injectable()
export class DatafileDetailService {

    public updateCellNameUrl = AppSettings.BASE_URL + "/striatumPortalApp/updateCellName/";
    public loadCellUrl = AppSettings.BASE_URL + "/striatumPortalApp/loadCell/";

    constructor (private http: HttpClient) {}

   //  updateCellName(cell:Cell): Promise<Cell> {
   //   return this.http.post(this.updateCellNameUrl, {"cell":cell}).toPromise().then(res => res)
   //     .catch(this.handleError);
   // }
   //
   //   loadCell(cellId:number): Promise<Cell> {
   //    return this.http.post(this.loadCellUrl, {"cellId":cellId}).toPromise().then(res => res)
   //      .catch(this.handleError);
   //  }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
