import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MonitorJobsRoutingModule } from './monitor-jobs-routing.module';
import { MonitorJobsComponent } from './monitor-jobs.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ListDatafilesModule } from '../list-datafiles/list-datafiles.module';

@NgModule({
    imports: [CommonModule,
              MonitorJobsRoutingModule,
              FormsModule,
              ReactiveFormsModule,
              ListDatafilesModule,
              NgbModule
            ],

    declarations: [MonitorJobsComponent]
})
export class MonitorJobsModule {}
