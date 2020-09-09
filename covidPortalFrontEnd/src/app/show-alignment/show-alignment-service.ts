import { Observable } from "rxjs/Rx"
import { Injectable, OnInit }     from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Datafile, UploadFolder } from '../models/datafile';
import { AlignmentResultObj , AlignmentObj} from '../models/alignment';
import { EpitopeObj} from '../models/epitope';
import { StructureObj} from '../models/structure';

import {AppSettings} from '../app.settings';

@Injectable()
export class ShowAlignmentService {

    public showAlignmentUrl = AppSettings.BASE_URL + "/covidPortalApp/showAlignment/";

    public reloadAlignmentUrl = AppSettings.BASE_URL + "/covidPortalApp/reloadAlignment/";
    public reloadEpitopesUrl = AppSettings.BASE_URL + "/covidPortalApp/reloadEpitopes/";
    public reloadStructuresUrl = AppSettings.BASE_URL + "/covidPortalApp/reloadStructures/";

    constructor (private http: HttpClient) {}

    showAlignment(): Promise<AlignmentResultObj> {
       return this.http.post(this.showAlignmentUrl, {}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    reloadAlignment(selectedAccessions:string[]): Promise<AlignmentObj[]> {
       return this.http.post(this.reloadAlignmentUrl, {"selectedAccessions":selectedAccessions}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    reloadEpitopes(selectedEpitopeIds:string[], selectedEpitopeExperimentIds:string[]): Promise<EpitopeObj[]> {
       return this.http.post(this.reloadEpitopesUrl, {"selectedEpitopeIds":selectedEpitopeIds, "selectedEpitopeExperimentIds":selectedEpitopeExperimentIds}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    reloadStructures(selectedStructureIds:string[]): Promise<StructureObj[]> {
       return this.http.post(this.reloadStructuresUrl, {"selectedStructureIds":selectedStructureIds}).toPromise().then(res => res)
       .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
      console.error('An error occurred', error); // for demo purposes only
      return Promise.reject(error.message || error);
    }

}
