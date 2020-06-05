import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShowAlignmentRoutingModule } from './show-alignment-routing.module';
import { ShowAlignmentComponent } from './show-alignment.component';
import { FormsModule } from '@angular/forms';
// import { ListFilesFilterPipe} from '../../pipes/list-files-filter.pipe';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';
// import { BrowserModule } from '@angular/platform-browser';

@NgModule({
    imports: [CommonModule,
              ShowAlignmentRoutingModule,
              FormsModule,
              ReactiveFormsModule,
              NgbModule,
              // BrowserModule,
              // ReactiveFormsModule
            ],

    declarations: [ShowAlignmentComponent]
})
export class ShowAlignmentModule {}
