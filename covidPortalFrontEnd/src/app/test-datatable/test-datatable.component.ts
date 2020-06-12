import { Component, ViewChild, OnInit, AfterViewInit, OnDestroy, Input, ElementRef} from '@angular/core';
// import { Component, OnInit, OnDestroy, Input, ElementRef} from '@angular/core';
import { TestDatatableService } from './test-datatable-service';
// import { Observable} from 'rxjs';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import { delay } from 'rxjs/operators';

import { HttpClient } from '@angular/common/http';
import { Datafile, UploadFolder } from '../models/datafile';
import 'rxjs/add/observable/interval';
import { Subscription } from 'rxjs/Subscription';
import { AlignmentObj, ResidueObj, NomenclaturePositionObj } from '../models/alignment';
import { SequenceResultObj, SequenceObj } from '../models/sequence';
import { ActivatedRoute, Params, Routes, Router } from '@angular/router';
import { Options } from 'ng5-slider';
import { Page } from '../models/page';
import { PagedData } from '../models/page-data';
import { of } from 'rxjs';

@Component({
    selector: 'list-files',
    providers: [TestDatatableService],
    templateUrl: './test-datatable.component.html',
    styleUrls: ['./test-datatable.component.scss']
})

export class TestDatatableComponent implements OnInit{


  title = 'angular-datatables';


   rows = [];

   ngOnInit() {
     this.fetch((data) => {
       this.rows = data;
     });
   }

   fetch(cb) {
     const req = new XMLHttpRequest();
     req.open('GET', `http://swimlane.github.io/ngx-datatable/assets/data/company.json`);

     req.onload = () => {
       const data = JSON.parse(req.response);
       cb(data);
     };

     req.send();
   }

}
