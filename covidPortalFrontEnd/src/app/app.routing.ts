import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { AuthGuard } from './shared';

const routes: Routes = [

    {
      path: '',
      redirectTo: 'show-alignment',
      pathMatch: 'full',
    },

    {
      path: 'show-alignment',
      redirectTo: 'show-alignment',
      pathMatch: 'full',
    },

    { path: '', loadChildren: () => import('./show-alignment/show-alignment.module').then(m => m.ShowAlignmentModule) },
    { path: 'dashboard', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule) },
    { path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginModule) },
    { path: 'logout', loadChildren: () => import('./logout/logout.module').then(m => m.LogoutModule) },
    { path: 'signup', loadChildren: () => import('./signup/signup.module').then(m => m.SignupModule) },
    { path: 'show-alignment', loadChildren: () => import('./show-alignment/show-alignment.module').then(m => m.ShowAlignmentModule) },

    { path: 'reset-password/:username', loadChildren: () => import('./reset-password/reset-password.module').then(m => m.ResetPasswordModule) },
    { path: 'email-resetpasswordlink', loadChildren: () => import('./email-resetpasswordlink/email-resetpasswordlink.module').then(m => m.EmailResetPasswordLinkModule) },
    { path: '**', redirectTo: 'not-found' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
