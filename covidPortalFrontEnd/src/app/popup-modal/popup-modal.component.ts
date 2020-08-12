import { Component, OnInit, Input, Output, EventEmitter} from '@angular/core';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup, FormBuilder, FormControl, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { Comment } from '../models/comment';

@Component({
  selector: 'ngbd-modal-content',
  providers: [],
  templateUrl: './popup-modal.component.html',
  styleUrls: ['./popup-modal.component.scss'],
})
// />

export class PopupModalComponent implements OnInit {

  @Input() name;
  @Input() imageClass;
  @Input() uploadFolder;
  @Input() xPosition;
  @Input() yPosition;
  @Input() zPosition;
  @Input() uploadFolderId;
  @Input() popupValueObjList;

  commentForm: FormGroup;
  allowAddComment:boolean;
  // commentsList: Comment[];
  message: string;

  @Output() saveEvent = new EventEmitter<string>();

  ngOnInit() {
  }

  constructor(
   public activeModal: NgbActiveModal,
   private formBuilder: FormBuilder
  ) {
    this.createForm();
    this.allowAddComment = false;
  }

  checkInput(){
  }

  createForm() {
    this.commentForm = this.formBuilder.group({
      commentText: ''
    });
  }

  submitForm() {

  }

}
