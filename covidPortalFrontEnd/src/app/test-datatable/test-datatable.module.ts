import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TestDatatableRoutingModule } from './test-datatable-routing.module';
import { TestDatatableComponent } from './test-datatable.component';
import { FormsModule } from '@angular/forms';
// import { ListFilesFilterPipe} from '../../pipes/list-files-filter.pipe';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { ReactiveFormsModule } from '@angular/forms';
// import { BrowserModule } from '@angular/platform-browser';
import { Ng5SliderModule } from 'ng5-slider';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';

@NgModule({
    imports: [CommonModule,
              TestDatatableRoutingModule,
              FormsModule,
              ReactiveFormsModule,
              NgbModule,
              Ng5SliderModule,
              NgxDatatableModule
              // BrowserModule,
              // ReactiveFormsModule
            ],

    declarations: [TestDatatableComponent]
})
export class TestDatatableModule {}
