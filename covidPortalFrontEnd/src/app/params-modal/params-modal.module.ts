import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ParamsModalRoutingModule } from './params-modal-routing.module';
import { ParamsModalComponent } from './params-modal.component';
import { ParamsModalService } from '../services/params-modal.service';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { ColorPickerModule } from 'ngx-color-picker';

@NgModule({
  imports: [
    CommonModule,
    ParamsModalRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    ColorPickerModule,
    NgMultiSelectDropDownModule
    //
    // NgMultiSelectDropDownModule.forRoot()
  ],
  declarations: [],
  providers:[ParamsModalService],
  // entryComponents: [
  //      ParamsModalComponent,
  //  ],
})
export class ParamsModalModule { }
