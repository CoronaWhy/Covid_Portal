import { Component, OnInit, OnDestroy, Input, Output, EventEmitter, ElementRef, ViewChild, HostListener, ChangeDetectionStrategy} from '@angular/core';
import { ReportService } from './report-service';
import { Observable} from 'rxjs';
import { ReportData } from '../../models/overlayData';
import { UploadFolder} from '../../models/datafile';
import { FormBuilder, FormGroup, FormArray, FormControl, ReactiveFormsModule } from '@angular/forms';
import { trigger, transition, animate, style } from '@angular/animations'
import { ChartType, ChartDataSets, ChartOptions } from 'chart.js';
import * as Chart from 'chart.js';
import { Color, BaseChartDirective } from 'ng2-charts';
import { ActivatedRoute, Params } from '@angular/router';
import {AppSettings} from '../../app.settings';
import * as pluginAnnotations from 'chartjs-plugin-annotation';
import { DomSanitizer } from '@angular/platform-browser';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
// import { HelpModalService } from '../../services/help-modal.service';
// import { HelpModalComponent } from '../../help-modal/help-modal.component';
// import { CommentModalService } from '../../services/comment-modal.service';
// import { CommentModalComponent } from '../../comment-modal/comment-modal.component';
// import { FullScreenComponent } from '../../full-screen/full-screen.component';
import * as jsPDF from 'jspdf';

@Component({
    selector: 'app-report',
    providers: [ReportService],
    // providers: [reportService],

    templateUrl: './report.component.html',
    styleUrls: ['./report.component.scss'],
    animations: [
        trigger('slideInOut', [
          transition(':enter', [
            style({transform: 'translateX(20%)'}),
            animate('200ms ease-in', style({transform: 'translateX(0%)'}))
          ]),
          transition(':leave', [
            animate('200ms ease-in', style({transform: 'translateX(20%)'}))
          ])
        ])
      ]
})

export class ReportComponent implements OnInit{

  @ViewChild(BaseChartDirective) // for the dynamic charts
  public chart: BaseChartDirective; // Now you can reference your chart via `this.chart`

  // event emitter for changes in modal box
  // @Output() commentsListChange = new EventEmitter<Comment[]>();

  // listener for changes in coordinates on mouse move or click
  // coordinatesChangeListener = this.coordinatesChange.subscribe((coordinates) => {
  //     this.coordsArray = coordinates;
  // });

  // open modal
  // openModal(helpType: string) {
  //   const modalRef = this.modalService.open(HelpModalComponent);
  //   if (helpType == "helpImageClass"){
  //     modalRef.componentInstance.name = 'Clicking on the different buttons will load the corresponding images generated as a part of the MRI image processing.';
  //   }
  //   else if (helpType == "helpSearchType"){
  //     modalRef.componentInstance.name = 'Selecting a search type will show comments only for that  type - User, Algorithmically generated, or All.';
  //   }
  //   else if (helpType == "helpSaliencyMapSlider"){
  //     modalRef.componentInstance.name = 'Dynamically adjusts the opactiy of the saliency map.';
  //   }
  //   else if (helpType == "helpPDScore"){
  //     modalRef.componentInstance.name = 'Predicted PD Score.';
  //   }
  //   else if (helpType == "helpRoiGraphs"){
  //     modalRef.componentInstance.name = 'Shows the three graphs at the bottom of the image panels. The graphs will be dynamically generated based on saliency map slider value.';
  //   }
  //   else if (helpType == "helpRoiOverlaySlider"){
  //     modalRef.componentInstance.name = 'Dynamically adjusts opacity of the ROI overlays.';
  //   }
  //
  // }

  // download pdf
  downloadPDF(){
     // var doc = new jsPDF();
     //  doc.text(50,50,'Snapshot for brain' + this.uploadFolder.name);
  }

  // tasks: BackgroundTask[] = [];

  @Input()

  canvas:HTMLCanvasElement;

 public barChartOptions: ChartOptions = {
     responsive: true,
     // We use these empty structures as placeholders for dynamic theming.
     scales: { xAxes: [{}], yAxes: [{}] },
     plugins: {
       datalabels: {
         anchor: 'end',
         align: 'end',
       }
     }
   };
 public barPlotOptions: ChartOptions = {
     responsive: true,

     scales: { xAxes: [{
         ticks: {
           beginAtZero: true,
           min: 0,
           max: 100
       },
       gridLines: {
           offsetGridLines: false,
           display: false
        },
       // stacked: true

     }], yAxes: [{
         ticks: {
           beginAtZero: true,
           min: 0,
           max: 100
       },
       gridLines: {
           offsetGridLines: false,
           display: false
        },
       // stacked: true
     }] },
     plugins: {
        datalabels: {
           display: true,
           align: 'center',
           anchor: 'center'
        }
     }
   };


   public barPlotLabels: string[] = [];
   public barPlotType: ChartType = 'horizontalBar';
   public barPlotLegend = true;
   public barPlotData: ChartDataSets[];

   public barChartLabels: string[] = [];
   public barChartType: ChartType = 'bar';
   public barChartLegend = true;
   public barChartData: ChartDataSets[];

   barPlotRegions: string[] = [];
   barPlotValues: ChartDataSets[];

   // convert hex to RGB, as per discussion in https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
   hexToRgb(hex) {
     // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
     var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
     hex = hex.replace(shorthandRegex, function(m, r, g, b) {
       return r + r + g + g + b + b;
     });

     var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
     return result ? {
       r: parseInt(result[1], 16),
       g: parseInt(result[2], 16),
       b: parseInt(result[3], 16)
     } : null;
   }

  ngOnInit() {
  }

  constructor( private reportService: ReportService,
               private sanitizer: DomSanitizer,
               private route:ActivatedRoute,
               private modalService: NgbModal,
               private _elementRef: ElementRef,
               private formBuilder: FormBuilder,
             ) {
  };

}
