import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PopupModalRoutingModule } from './popup-modal-routing.module';
import { PopupModalComponent } from './popup-modal.component';
import { PopupModalService } from '../services/popup-modal.service';

@NgModule({
  imports: [
    CommonModule,
    PopupModalRoutingModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  declarations: [],
  providers:[PopupModalService],
})
export class PopupModalModule { }
