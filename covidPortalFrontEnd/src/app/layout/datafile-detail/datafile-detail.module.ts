import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DatafileDetailRoutingModule } from './datafile-detail-routing.module';
import { DatafileDetailComponent } from './datafile-detail.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

@NgModule({
    imports: [CommonModule,
              DatafileDetailRoutingModule,
              FormsModule,
              ReactiveFormsModule,
              NgbModule
             ],

    declarations: [DatafileDetailComponent]
})
export class DatafileDetailModule {}
