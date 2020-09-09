import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule } from '@angular/router';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app.routing';

import { AppComponent } from './app.component';
import { AuthGuard , AuthService} from './shared';

import { TableListComponent } from './table-list/table-list.component';

import { NotificationsComponent } from './notifications/notifications.component';
import { UpgradeComponent } from './upgrade/upgrade.component';

import { ProjectService } from './services/project-service';
import { LoginService } from './services/login-service';
import { LogoutService } from './services/logout-service';

import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { SigninEmitterService} from './services/signin-emitter.service';
import { SignoutEmitterService} from './services/signout-emitter.service';

import { SignupService } from './services/signup-service';
import { ResetPasswordService } from './services/reset-password-service';
import { TokenInterceptor } from './shared/interceptor/token.interceptor';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HelpModalService } from './services/help-modal.service';
import { HelpModalComponent } from './help-modal/help-modal.component';
import { PopupModalComponent } from './popup-modal/popup-modal.component';

import { NgxSortableModule } from 'ngx-sortable';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { LogoutComponent } from './logout/logout.component';
import { LoginComponent } from './login/login.component';

import { LoginModule } from './login/login.module';

// import {
//   AgmCoreModule
// } from '@agm/core';

export function createTranslateLoader(http: HttpClient) {
    return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

@NgModule({
  imports: [

    CommonModule,
    BrowserModule,
    HttpClientModule,
    NgxSortableModule,
    NgbModule,
    TranslateModule.forRoot({
        loader: {
            provide: TranslateLoader,
            useFactory: createTranslateLoader,
            deps: [HttpClient]
        }
    }),
    NgMultiSelectDropDownModule.forRoot(),

    FormsModule,

    BrowserAnimationsModule,
    ReactiveFormsModule,
    RouterModule,
    AppRoutingModule,
    // AgmCoreModule.forRoot({
    //   apiKey: 'YOUR_GOOGLE_MAPS_API_KEY'
    // })
  ],
  entryComponents: [
       HelpModalComponent,
       PopupModalComponent,
   ],

  declarations: [AppComponent, HelpModalComponent, PopupModalComponent],

  providers: [AuthGuard, ProjectService, LoginService, SignupService, ResetPasswordService, LogoutService, AuthService, LogoutComponent,
              SigninEmitterService, SignoutEmitterService, HelpModalService,  {

    provide: HTTP_INTERCEPTORS,
    useClass: TokenInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
