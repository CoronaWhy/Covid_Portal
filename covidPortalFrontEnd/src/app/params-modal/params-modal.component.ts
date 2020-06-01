import { Component, OnInit, Input, Output, EventEmitter, ViewChild} from '@angular/core';
// import { ParamsModalSubmitService } from '../services/params-modal-submit.service';

import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule, FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { FullScreenService } from '../services/full-screen.service';
import { Comment } from '../models/comment';
import * as math from 'mathjs'
import * as nifti from "nifti-reader-js"
import { HelpModalService } from '../services/help-modal.service';
import { HelpModalComponent } from '../help-modal/help-modal.component';
import { CommentModalService } from '../services/comment-modal.service';
import { ParamsModalService } from '../services/params-modal.service';
import { CommentModalComponent } from '../comment-modal/comment-modal.component';
import { Color, BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'ngbd-modal-content',
  providers: [],
  templateUrl: './params-modal.component.html',
  styleUrls: ['./params-modal.component.scss'],
})
// />

export class ParamsModalComponent implements OnInit {

  @Input() name;
  @Input() uploadFolderId;

  disableSubmit:boolean;
  commentForm: FormGroup;
  allowAddComment:boolean;
  showParamsFlag:boolean;

  message: string;


  @ViewChild(BaseChartDirective) // for the dynamic charts
  public chart: BaseChartDirective; // Now you can reference your chart via `this.chart`

  // handle region selection from drop down list
  ngOnInit() {



  }

  setSaliencyColor(){
  }

  setSaliencyData(selectedSaliencyDataIndex){
  }

  showHideCrossHairs(){

  }

  onRegionSelect(item: any) {
  }

  // handle region selection from drop down list
  onRegionDeSelect(item: any) {
  }

  // handler for select all regions
  onSelectAll(items: any) {
    console.log(items);
  }

  gotoCenter(){
  }

  setRoiSliderValue(){

  }

  resetBrightnessContrast(){
  }
  // switch between views: coronal, axial and sagittal
  changeView(selectedView){
  }// end method

  // switch between image classes : original brain, brain extraction, cortical thickness, warped image
  changeImageClass(imageClass){

  } // end method

  setSaliencyMapSliderValue(){

  }

  displaySaliencyMap(){

  }
  constructor(
   public activeModal: NgbActiveModal,

   private formBuilder: FormBuilder,
  ) {
    this.createForm();
    this.allowAddComment = false;
  }

    private checkInput(){
      if (this.commentForm.value != ''){
        this.disableSubmit = false;
      }
    }
    private createForm() {

    }

}
