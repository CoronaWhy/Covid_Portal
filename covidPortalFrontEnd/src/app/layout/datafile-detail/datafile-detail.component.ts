import { Component, OnInit, OnDestroy, Input, ViewChild, ElementRef} from '@angular/core';
import { DatafileDetailService } from './datafile-detail-service';
import { Observable} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Datafile} from '../../models/datafile';
import { Cell} from '../../models/cell';

import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { Options } from 'ng5-slider';
import * as pluginAnnotations from 'chartjs-plugin-annotation';

@Component({
    selector: 'list-files',
    providers: [DatafileDetailService],
    templateUrl: './datafile-detail.component.html',
    styleUrls: ['./datafile-detail.component.scss']
})

export class DatafileDetailComponent implements OnInit{
    @Input()
    cellId:number;
    cell:Cell;
    cellLoaded :boolean;
    activeTabTitleSections:string;
    loadCell(cellId:number){
      this.cellLoaded = false;
      this.datafileDetailService.loadCell(cellId)
      .then(cell => {
          this.cell = cell;
          console.log(this.cell);
          console.log(this.cell.secObjLists);

          this.cellLoaded = true;

      });
    }

  ngOnInit() {

      this.route.paramMap.subscribe(params => {
        this.cellId = +params.get("cellId");
      });
      this.cellLoaded = false;
      this.activeTabTitleSections = "Soma";
      this.loadCell(this.cellId);

    }

    constructor( private datafileDetailService: DatafileDetailService,
                 private route: ActivatedRoute,
               ) {
    };
}
