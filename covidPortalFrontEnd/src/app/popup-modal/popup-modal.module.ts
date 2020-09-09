import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PopupModalRoutingModule } from './popup-modal-routing.module';
import { PopupModalComponent } from './popup-modal.component';
import { PopupModalService } from '../services/popup-modal.service';
import { BrowserModule } from '@angular/platform-browser'

@NgModule({
  imports: [
    CommonModule,
    PopupModalRoutingModule,
    FormsModule,
    BrowserModule,
    ReactiveFormsModule,
  ],
  declarations: [],
  providers:[PopupModalService],
})
export class PopupModalModule { }
