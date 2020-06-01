import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { AuthGuard } from './shared';

const routes: Routes = [

    {
      path: '',
      redirectTo: 'dashboard',
      pathMatch: 'full',
      canActivate: [AuthGuard]
    },

    {
      path: 'dashboard',
      redirectTo: 'dashboard',
      pathMatch: 'full',
      canActivate: [AuthGuard]
    },

    { path: '', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule), canActivate: [AuthGuard]},
    { path: 'dashboard', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule), canActivate: [AuthGuard] },
    { path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginModule) },
    { path: 'logout', loadChildren: () => import('./logout/logout.module').then(m => m.LogoutModule) },
    { path: 'signup', loadChildren: () => import('./signup/signup.module').then(m => m.SignupModule) },
    { path: 'reset-password/:username', loadChildren: () => import('./reset-password/reset-password.module').then(m => m.ResetPasswordModule) },
    { path: 'email-resetpasswordlink', loadChildren: () => import('./email-resetpasswordlink/email-resetpasswordlink.module').then(m => m.EmailResetPasswordLinkModule) },
    { path: '**', redirectTo: 'not-found' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
