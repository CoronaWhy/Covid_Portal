import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { AuthGuard } from './shared';

const routes: Routes = [

    { path: '', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule)},
    { path: 'show-alignment', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule) },
    { path: 'dashboard', loadChildren: () => import('./layout/layout.module').then(m => m.LayoutModule) },

    { path: '**', redirectTo: 'not-found' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {}
