import { Component, OnInit, OnDestroy, Input, ViewChild, ElementRef} from '@angular/core';
import { DatafileDetailService } from './datafile-detail-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Datafile} from '../../models/datafile';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { Options } from 'ng5-slider';
import { ChartDataSets, ChartType, ChartOptions } from 'chart.js';
import { Color, BaseChartDirective, Label } from 'ng2-charts';
import * as pluginAnnotations from 'chartjs-plugin-annotation';

@Component({
    selector: 'list-files',
    providers: [DatafileDetailService],
    templateUrl: './datafile-detail.component.html',
    styleUrls: ['./datafile-detail.component.scss']
})

export class DatafileDetailComponent implements OnInit{
    @Input()
    datafile : UploadFolder;

    rangeSliderOptions: Options = {
      floor: 0,
      ceil: 100
    };

    epochRangeSliderOptions: Options = {
      floor: 0,
      ceil: 100
    };

    icaRangeSliderOptions: Options = {
      floor: 0,
      ceil: 100
    };

    lowPassSliderOptions: Options = {
      floor: 0,
      ceil: 100
    };

    highPassSliderOptions: Options = {
      floor: 0,
      ceil: 100
    };

    lowPassFilterFlag:boolean;
    highPassFilterFlag:boolean;

    filterOptions = [
      { 'id': 0, 'name': 'Uploaded', 'selected':false , 'color':'#EDF59A'},
      { 'id': 1, 'name': 'Analysis Submitted', 'selected':false , 'color':'#CBF022'},
      { 'id': 2, 'name': 'Score Calculated', 'selected':false , 'color':'#32FFC8'},
      { 'id': 3, 'name': 'Analysis Completed', 'selected':false , 'color':'#36CBEC'},
    ];

    ngOnInit() {

    }

    constructor( private datafileDetailService: DatafileDetailService,
                 private route: ActivatedRoute,
               ) {
    };
}
