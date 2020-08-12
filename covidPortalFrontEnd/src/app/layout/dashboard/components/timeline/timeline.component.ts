import { Component, OnInit } from '@angular/core';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import {AppSettings} from '../../../../app.settings';

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss']
})
export class TimelineComponent implements OnInit {

  public getOverlayDataUrl = AppSettings.BASE_URL + "/covidPortalApp/getOverlayData";

  constructor(private  httpClient:HttpClient) { }

  ngOnInit() {
  }

}
