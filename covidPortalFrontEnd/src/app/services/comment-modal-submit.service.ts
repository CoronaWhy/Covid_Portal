import { Injectable } from '@angular/core';
import {AppSettings} from '../app.settings';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Comment } from '../models/comment';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class CommentModalSubmitService {
  BASE_URL=AppSettings.BASE_URL;

  public fetchAllCommentsUrl = AppSettings.BASE_URL + "/covidPortalApp/fetchAllComments/";

  constructor (private http: HttpClient) {}

  fetchAllComments(uploadFolderId:string): Promise<Comment[]> {
   return this.http.post(this.fetchAllCommentsUrl, { "uploadFolderId":uploadFolderId}).toPromise().then(res => res)
     .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }

}
