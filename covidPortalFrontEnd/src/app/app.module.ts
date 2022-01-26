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

import { ProjectService } from './services/project-service';
import { LoginService } from './services/login-service';
import { LogoutService } from './services/logout-service';

import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { SigninEmitterService} from './services/signin-emitter.service';
import { SignoutEmitterService} from './services/signout-emitter.service';
import { TokenInterceptor } from './shared/interceptor/token.interceptor';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HelpModalComponent } from './help-modal/help-modal.component';
import { PopupModalComponent } from './popup-modal/popup-modal.component';

import { NgxSortableModule } from 'ngx-sortable';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { LogoutComponent } from './logout/logout.component';
import { LoginComponent } from './login/login.component';

import { LoginModule } from './login/login.module';

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

  ],

  entryComponents: [
       HelpModalComponent,
       PopupModalComponent,
   ],

  declarations: [AppComponent, HelpModalComponent, PopupModalComponent],

  providers: [AuthGuard, ProjectService, LoginService, LogoutService, AuthService, LogoutComponent,
              SigninEmitterService, SignoutEmitterService, {

    provide: HTTP_INTERCEPTORS,
    useClass: TokenInterceptor,
    multi: true
  }],

  bootstrap: [AppComponent]
})
export class AppModule { }
